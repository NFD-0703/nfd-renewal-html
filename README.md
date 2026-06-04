# NFD Renewal Static Site

This repository keeps editable source files separate from GitHub Pages output.

## Site structure

The published site is generated into `docs/`.

- Korean is the default public site:
  - `https://www.nfd.kr/`
  - `https://www.nfd.kr/services.html`
  - `https://www.nfd.kr/news.html`
- English pages live under `/en/`:
  - `https://www.nfd.kr/en/index.html`
  - `https://www.nfd.kr/en/services.html`
  - `https://www.nfd.kr/en/news.html`
- `docs/ko/*.html` is still generated as compatibility output, but Korean canonical URLs point to the root Korean pages.
- `news-detail.html` is a legacy page that redirects to `news.html`; news articles now use generated static URLs.

Do not edit files in `docs/` directly. They are generated.

## Edit source files

- Page content: `src/pages/*.html`
- News data: `src/news.json`
- Shared header: `partials/header.html`
- Shared footer: `partials/footer.html`
- Images: `images/`
- Static root files, such as verification HTML: `public/`

## Add news

Add news items to `src/news.json`, then run the build. Do not create or edit generated news pages in `docs/` directly.

Each news item needs:

- `slug`: URL-safe id used for the generated filename.
- `category`: English and Korean labels.
- `date`: `iso`, English display date, and Korean display date.
- `image.card`: image used on the news list.
- `image.detail`: image used on the news detail page.
- `title`, `summary`, `subtitle`, `body`: English and Korean content.

Example:

```json
{
  "slug": "new-data-center-announcement",
  "category": {
    "en": "News",
    "ko": "뉴스"
  },
  "date": {
    "iso": "2026-01-15",
    "en": "Jan 15, 2026",
    "ko": "2026. 1. 15"
  },
  "image": {
    "card": "images/remote/example-w800.webp",
    "detail": "images/remote/example-w1200.webp"
  },
  "title": {
    "en": "New data center announcement",
    "ko": "신규 데이터센터 발표"
  },
  "summary": {
    "en": "Short summary for the news list and SEO description.",
    "ko": "뉴스 목록과 SEO 설명에 사용되는 짧은 요약입니다."
  },
  "subtitle": {
    "en": "Longer subtitle shown at the top of the detail page.",
    "ko": "상세 페이지 상단에 표시되는 보조 설명입니다."
  },
  "body": {
    "en": [
      "First paragraph.",
      "Second paragraph."
    ],
    "ko": [
      "첫 번째 문단입니다.",
      "두 번째 문단입니다."
    ]
  }
}
```

The build generates Korean root pages, English pages, and compatibility Korean pages:

```text
docs/news-new-data-center-announcement.html
docs/en/news-new-data-center-announcement.html
docs/ko/news-new-data-center-announcement.html
```

## Build

Run this before publishing changes:

```bash
python3 build-i18n.py
```

The build creates:

- Korean root HTML pages in `docs/*.html`
- English pages in `docs/en/*.html`
- compatibility Korean pages in `docs/ko/*.html`
- news list and detail pages generated from `src/news.json`
- `docs/news-detail.html` legacy redirect to `news.html`
- `docs/sitemap.xml`
- `docs/robots.txt`
- `docs/images/*`
- files copied from `public/`

For a custom domain, the default build already uses `https://www.nfd.kr`. To override it:

```bash
SITE_BASE_PATH="" SITE_ORIGIN="https://www.nfd.kr" python3 build-i18n.py
```

## SEO notes

- The canonical Korean URLs are root URLs, such as `https://www.nfd.kr/services.html`.
- The English canonical URLs are under `/en/`, such as `https://www.nfd.kr/en/services.html`.
- `hreflang` links connect Korean and English versions.
- `x-default` points to the Korean root URL.
- Generated news detail pages include `NewsArticle` structured data.
- `news-detail.html` is not included in the sitemap; it exists only for old links and redirects to `news.html`.

## GitHub Pages

Set GitHub Pages to:

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/docs`
