# DESIGN — Forum DevOps Fil Rouge

> Front **volontairement minimal** : « le cœur du module est DevOps, pas le framework front ». Ce doc reste léger ; ne pas sur-investir l'UI.

## Périmètre UI

Interface minimale suffisant à démontrer le forum. Pas de design system élaboré, pas d'animations, pas de SPA lourde. Server-side rendering ou petit front statique consommant l'API REST.

## Écrans minimaux

| Écran | Contenu | Action |
|-------|---------|--------|
| Liste des catégories | catégories du forum | → ouvrir une catégorie |
| Liste des sujets | topics d'une catégorie | → ouvrir un sujet · créer un sujet |
| Détail d'un sujet | messages (posts) du topic | → poster un message |
| Auth | inscription / connexion | session ou JWT basique |

## Tokens UI (minimaux)

- **Couleurs :** palette neutre par défaut (ne pas hardcoder de hex épars — centraliser si un front est ajouté).
- **Typographie :** police système (`system-ui`), une seule famille.
- **Espacement :** échelle simple (4 / 8 / 16 px).

## Hors scope (rappel)

- Thèmes, dark mode, design responsive avancé
- Composants riches (éditeur WYSIWYG, modales complexes)
- Temps réel / notifications

> Si le groupe ajoute un vrai front, lister ici les composants réutilisables avant d'en créer de nouveaux (Reuse > Invent).

---
*Last updated: 2026-06-03*
