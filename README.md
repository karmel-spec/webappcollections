# The Larson Gallery

Showcase site for all of Karmel Larson's webapps — gallery-wall design, real screenshots, per-app detail pages with feedback forms, phases, and a build queue.

## Editing
- Edit `template.html` (never `index.html` directly)
- Screenshots live in `assets/screens/` as `<id>-main/-d1..d4/-m1..m2.jpg`
- Home-screen icons in `assets/icons/`
- Rebuild: `python3 build.py` (regenerates `index.html` with everything embedded)

## Deploy
Connected to Netlify — every push to `main` auto-deploys. Forms (app requests + per-app feedback) are Netlify Forms; submissions appear in the Netlify dashboard.
