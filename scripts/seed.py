#!/usr/bin/env python3
"""Remplit le forum avec des données de démonstration.

Usage :
    docker compose up -d            # l'API doit tourner sur localhost:8000
    python3 scripts/seed.py

Le script crée quelques utilisateurs, catégories, sujets et messages, via
l'API REST publique. Il n'utilise que la bibliothèque standard (aucune
dépendance à installer) et attend que l'API soit prête avant de commencer.
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://localhost:8000"


def api(method, path, data=None, token=None, form=False):
    """Appel HTTP minimal. Retourne (status_code, corps_json)."""
    headers = {}
    body = None
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode() or "null"
            return resp.status, json.loads(raw)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode() or "null"
        try:
            return exc.code, json.loads(raw)
        except json.JSONDecodeError:
            return exc.code, raw


def wait_for_api(timeout=60):
    """Attend que /health réponde, jusqu'à `timeout` secondes."""
    print("⏳ Attente de l'API sur", BASE, "...")
    for _ in range(timeout):
        try:
            status, _ = api("GET", "/health")
            if status == 200:
                print("✅ API prête.")
                return True
        except Exception:
            pass
        time.sleep(1)
    print("❌ L'API ne répond pas. Lance d'abord : docker compose up -d")
    return False


def register_and_login(user):
    """Crée le compte (ou l'ignore s'il existe) puis se connecte."""
    api("POST", "/auth/register", data=user)  # 400 si déjà créé : on continue
    # /login attend l'email dans le champ « username », en form-urlencoded
    status, body = api(
        "POST",
        "/auth/login",
        data={"username": user["email"], "password": user["password"]},
        form=True,
    )
    if status != 200:
        print(f"❌ Connexion échouée pour {user['username']} : {body}")
        sys.exit(1)
    return body["access_token"]


def created(what, status, body):
    """Vérifie qu'une création a réussi (201 + id) avant d'utiliser le résultat."""
    if status != 201 or not isinstance(body, dict) or "id" not in body:
        print(f"❌ Échec création {what} (HTTP {status}) : {body}")
        sys.exit(1)
    return body


# --- Données de démonstration -------------------------------------------------

USERS = [
    {"username": "Alvin", "email": "alvin@forum.dev", "password": "demo1234"},
    {"username": "Camille", "email": "camille@forum.dev", "password": "demo1234"},
    {"username": "Théo", "email": "theo@forum.dev", "password": "demo1234"},
    {"username": "Baptiste", "email": "baptiste@forum.dev", "password": "demo1234"},
]

# Chaque sujet : (catégorie, titre, auteur, [(auteur, message), ...])
CONTENT = [
    {
        "category": ("Annonces", "Informations importantes de l'équipe"),
        "topics": [
            (
                "Soutenance le 24/06",
                "Alvin",
                [
                    ("Alvin", "Rendez-vous mercredi 24/06 après-midi, salle 306. Pensez à tester la démo avant !"),
                    ("Camille", "C'est noté. Le pipeline est au vert de mon côté."),
                    ("Baptiste", "Et le déploiement Compose démarre en une commande, on est prêts."),
                ],
            ),
        ],
    },
    {
        "category": ("Entraide DevOps", "Questions Docker, CI/CD et déploiement"),
        "topics": [
            (
                "Mon conteneur ne démarre pas",
                "Camille",
                [
                    ("Camille", "Mon API plante au démarrage, une idée de ce qui cloche ?"),
                    ("Théo", "Tu as un healthcheck sur la base ? L'API démarre peut-être avant que Postgres soit prêt."),
                    ("Camille", "Ah oui, j'avais oublié le depends_on. Je l'ajoute, merci !"),
                    ("Théo", "Avec plaisir 🙂"),
                ],
            ),
            (
                "slim ou alpine pour l'image Python ?",
                "Baptiste",
                [
                    ("Baptiste", "On part sur python:slim ou python:alpine pour notre image ?"),
                    ("Alvin", "slim. Alpine complique l'installation des libs C et fait perdre du temps."),
                    ("Baptiste", "Ok, slim c'est validé."),
                ],
            ),
        ],
    },
    {
        "category": ("Hors-sujet", "Discussions libres"),
        "topics": [
            (
                "Pause café avant la répét' ?",
                "Théo",
                [
                    ("Théo", "Qui est chaud pour un café avant de répéter la soutenance ?"),
                    ("Camille", "Moi !"),
                    ("Alvin", "J'arrive."),
                ],
            ),
        ],
    },
    {
        "category": ("Galerie", "Partage de photos de l'équipe"),
        "topics": [
            (
                "Photos pour le trombinoscope",
                "Alvin",
                [
                    ("Alvin", "Voici ma photo pour le trombinoscope 📸"),
                    ("Alvin", "/alvin.png"),
                    ("Camille", "Parfait ! Et voilà la mienne :"),
                    ("Camille", "/camille.png"),
                    ("Théo", "Au top, je rajoute la mienne ce soir."),
                ],
            ),
        ],
    },
]


def main():
    if not wait_for_api():
        sys.exit(1)

    # Idempotence simple : si des catégories existent déjà, on ne re-remplit pas.
    status, cats = api("GET", "/categories/")
    if status == 200 and cats:
        print(f"ℹ️  Le forum contient déjà {len(cats)} catégorie(s) — rien à faire.")
        print("   (Pour repartir de zéro : docker compose down -v puis up -d)")
        return

    print("🔑 Création des comptes de démonstration...")
    tokens = {u["username"]: register_and_login(u) for u in USERS}

    for block in CONTENT:
        cat_name, cat_desc = block["category"]
        # Une catégorie est créée par Alvin (n'importe quel compte authentifié convient)
        cat = created(
            f"catégorie « {cat_name} »",
            *api("POST", "/categories/", data={"name": cat_name, "description": cat_desc}, token=tokens["Alvin"]),
        )
        print(f"📂 Catégorie : {cat_name}")

        for title, author, messages in block["topics"]:
            topic = created(
                f"sujet « {title} »",
                *api("POST", f"/categories/{cat['id']}/topics", data={"title": title}, token=tokens[author]),
            )
            print(f"   💬 Sujet : {title}")

            for msg_author, content in messages:
                created(
                    f"message dans « {title} »",
                    *api("POST", f"/topics/{topic['id']}/posts", data={"content": content}, token=tokens[msg_author]),
                )
            print(f"      → {len(messages)} messages")

    print("\n✅ Forum rempli ! Rafraîchis le front : http://localhost:8080")
    print("   Comptes de démo (mot de passe : demo1234) :")
    for u in USERS:
        print(f"   - {u['email']}")


if __name__ == "__main__":
    main()
