# NFD Renewal Static Site

This repository keeps editable source files separate from GitHub Pages output.

## Edit source files

- Page content: `src/pages/*.html`
- Shared header: `partials/header.html`
- Shared footer: `partials/footer.html`
- Images: `images/`
- Static root files, such as verification HTML: `public/`

Do not edit files in `docs/` directly. They are generated.

## Build

Run this before publishing changes:

```bash
python3 build-i18n.py
```

The build creates:

- `docs/index.html` and root redirect stubs
- `docs/en/*.html`
- `docs/ko/*.html`
- `docs/sitemap.xml`
- `docs/robots.txt`
- `docs/images/*`
- files copied from `public/`

## GitHub Pages

Set GitHub Pages to:

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/docs`

For a custom domain, rebuild with:

```bash
SITE_BASE_PATH="" SITE_ORIGIN="https://www.nfd.kr" python3 build-i18n.py
```

The default build already uses `https://www.nfd.kr`.
