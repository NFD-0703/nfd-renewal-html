from pathlib import Path
import html
import json
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "src" / "pages"
OUTPUT_DIR = ROOT / "docs"
PUBLIC_DIR = ROOT / "public"


def discover_page_names() -> list[str]:
    if SOURCE_DIR.exists():
        names = sorted(path.name for path in SOURCE_DIR.glob("*.html") if path.name != "index_en.html")
        if names:
            return names
    return sorted(
        name
        for name in subprocess.run(
            ["git", "ls-files", "*.html"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()
        if "/" not in name and name != "index_en.html"
    )


PAGE_NAMES = discover_page_names()


def default_base_path() -> str:
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    ).stdout.strip()
    match = re.search(r"/([^/]+?)(?:\.git)?$", remote)
    if not match:
        return ""
    repo = match.group(1)
    if repo.endswith(".github.io"):
        return ""
    return f"/{repo}"


def default_site_origin() -> str:
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    ).stdout.strip()
    match = re.search(r"github\.com[:/]([^/]+)/", remote)
    if not match:
        return ""
    return f"https://{match.group(1).lower()}.github.io"


SITE_BASE_PATH = os.environ.get("SITE_BASE_PATH", "").rstrip("/")
SITE_ORIGIN = os.environ.get("SITE_ORIGIN", "https://www.nfd.kr").rstrip("/")
SITE_URL = os.environ.get("SITE_URL", f"{SITE_ORIGIN}{SITE_BASE_PATH}").rstrip("/")
PARTIALS = ROOT / "partials"

LABELS = {
    "en": {
        "partner_label": "Data Center Partner",
        "consulting_partner_label": "Data Center Consulting Partner",
        "about": "About",
        "about_us": "About Us",
        "mission_vision": "Mission & Vision",
        "history": "History",
        "organization": "Organization",
        "services": "Services",
        "projects": "Projects",
        "careers": "Careers",
        "our_values": "Our Values",
        "open_roles": "Open Roles",
        "news": "News",
        "contact_us": "Contact Us",
        "company": "Company",
        "more": "More",
        "development_consulting": "Development Consulting",
        "design_engineering": "Design Engineering",
        "pm_services": "PM Services",
        "operations_management": "Operations Management",
        "tagline": "We build the future of sustainable<br>digital infrastructure through expertise and trust.",
    },
    "ko": {
        "partner_label": "데이터센터 파트너",
        "consulting_partner_label": "데이터센터 컨설팅 파트너",
        "about": "회사소개",
        "about_us": "회사소개",
        "mission_vision": "미션 & 비전",
        "history": "연혁",
        "organization": "조직도",
        "services": "서비스",
        "projects": "프로젝트",
        "careers": "채용",
        "our_values": "인재상",
        "open_roles": "채용공고",
        "news": "뉴스",
        "contact_us": "문의하기",
        "company": "회사",
        "more": "더보기",
        "development_consulting": "개발 컨설팅",
        "design_engineering": "설계 엔지니어링",
        "pm_services": "PM 서비스",
        "operations_management": "운영 관리",
        "tagline": "전문성과 신뢰를 바탕으로<br>지속 가능한 디지털 인프라의 미래를 만듭니다.",
    },
}

ABOUT_PAGES = {"about-us.html", "mission-vision.html", "history.html", "org.html"}
SERVICE_PAGES = {
    "services.html",
    "service-development.html",
    "service-engineering.html",
    "service-pm.html",
    "service-operations.html",
}
CAREERS_PAGES = {
    "careers-values.html",
    "careers.html",
    "careers-architect-engineer.html",
    "careers-csa-engineer.html",
    "careers-estate-development.html",
    "careers-mechanical-electrical.html",
}

SEO_DESCRIPTION = {
    "en": {
        "index.html": "NFD Korea, also known as nfdkorea, provides data center development, design engineering, project management, and operations consulting in Korea.",
        "about-us.html": "Learn about NFD Korea, nfdkorea, a data center consulting and development partner based in Seoul, Korea.",
        "services.html": "Explore NFD Korea services for data center development consulting, design engineering, project management, and operations.",
        "projects.html": "View data center projects developed, managed, or advised by NFD Korea, nfdkorea.",
        "contact.html": "Contact NFD Korea for data center development, engineering, project management, and operations consulting.",
    },
    "ko": {
        "index.html": "NFD Korea, nfdkorea는 데이터센터 개발, 설계 엔지니어링, 프로젝트 관리, 운영 컨설팅을 제공하는 데이터센터 전문 기업입니다.",
        "about-us.html": "NFD Korea, nfdkorea는 서울을 기반으로 데이터센터 개발 및 운영 컨설팅을 제공하는 전문 파트너입니다.",
        "services.html": "NFD Korea의 데이터센터 개발 컨설팅, 설계 엔지니어링, 프로젝트 관리, 운영 관리 서비스를 확인하세요.",
        "projects.html": "NFD Korea, nfdkorea가 개발, 관리, 자문한 데이터센터 프로젝트를 확인하세요.",
        "contact.html": "데이터센터 개발, 엔지니어링, PM, 운영 컨설팅 문의는 NFD Korea에 연락하세요.",
    },
}

DEFAULT_DESCRIPTION = {
    "en": "NFD Korea, also known as nfdkorea, is a data center consulting and development company supporting digital infrastructure projects in Korea.",
    "ko": "NFD Korea, nfdkorea는 국내 데이터센터 개발과 디지털 인프라 프로젝트를 지원하는 데이터센터 컨설팅 전문 기업입니다.",
}

SEO_KEYWORDS = {
    "en": "NFD Korea, NFDKorea, nfdkorea, NFD, data center Korea, data center consulting, data center development, IDC Korea",
    "ko": "NFD Korea, NFDKorea, nfdkorea, 엔에프디코리아, NFD, 데이터센터, 데이터센터 컨설팅, 데이터센터 개발, IDC",
}

KO_TEXT = {
    "Home – NFD Korea": "홈 – NFD Korea",
    "NFD Korea | Data Center Consulting & Development": "NFD Korea | 데이터센터 컨설팅 및 개발",
    "About Us": "회사소개",
    "About": "회사소개",
    "Home": "홈",
    "Mission & Vision": "미션 & 비전",
    "History": "연혁",
    "Organization": "조직도",
    "Services": "서비스",
    "Projects": "프로젝트",
    "Careers": "채용",
    "Our Values": "인재상",
    "Open Roles": "채용공고",
    "News": "뉴스",
    "Contact Us": "문의하기",
    "Company": "회사",
    "More": "더보기",
    "Data Center Partner": "데이터센터 파트너",
    "Data Center Consulting Partner": "데이터센터 컨설팅 파트너",
    "We build the future of sustainable<br>digital infrastructure through expertise and trust.": "전문성과 신뢰를 바탕으로<br>지속 가능한 디지털 인프라의 미래를 만듭니다.",
    "All rights reserved.": "All rights reserved.",
    "Drive Your Future<br><em>with Next Frontier Drive</em>": "Next Frontier Drive와 함께<br><em>미래를 이끌어갑니다</em>",
    "NFD Korea brings development, design engineering, project management, and operations together to build resilient, scalable data center platforms.": "NFD Korea는 개발, 설계 엔지니어링, 프로젝트 관리, 운영 역량을 결합해 안정적이고 확장 가능한 데이터센터 플랫폼을 구축합니다.",
    "Explore Services": "서비스 보기",
    "Why NFD Korea": "왜 NFD Korea인가",
    "Why choose<br>NFD Korea": "NFD Korea를<br>선택해야 하는 이유",
    "We provide practical answers to investor and client challenges with strong technical judgment and extensive delivery experience.": "탄탄한 기술 판단력과 풍부한 수행 경험으로 투자자와 고객의 과제에 실질적인 해답을 제공합니다.",
    "What We Offer": "제공 서비스",
    "Differentiated services<br>for each project stage": "프로젝트 단계별<br>차별화된 서비스",
    "View All Services": "전체 서비스 보기",
    "Start your data center project<br>with the right team.": "올바른 팀과 함께<br>데이터센터 프로젝트를 시작하세요.",
    "View Projects": "프로젝트 보기",
    "Data Center Development": "데이터센터 개발",
    "Design Engineering": "설계 엔지니어링",
    "Project Management": "프로젝트 관리",
    "Operations Management": "운영 관리",
    "Development Consulting": "개발 컨설팅",
    "PM Services": "PM 서비스",
    "Operations Leasing": "운영 및 임대",
    "Learn more": "자세히 보기",
    "One-stop total solution": "원스톱 토털 솔루션",
    "Average 22 years of field experience": "평균 22년의 현장 경험",
    "Global network": "글로벌 네트워크",
    "Proprietary liquid cooling design": "자체 액체냉각 설계",
    "High-efficiency PUE 1.33": "고효율 PUE 1.33",
    "We are building a team that<br>can lead <em>complex data center</em><br>development.": "복잡한 <em>데이터센터</em><br>개발을 이끌 수 있는<br>팀을 만들고 있습니다.",
    "With clarity, discipline, and strong execution — we're looking for professionals who are shaping the future of digital infrastructure.": "명확함, 원칙, 강한 실행력을 바탕으로 디지털 인프라의 미래를 만들어갈 전문가를 찾습니다.",
    "Who we look for": "우리가 찾는 인재",
    "Professionals shaping the future of the data center industry.": "데이터센터 산업의 미래를 함께 만들어갈 전문가.",
    "Ownership": "주인의식",
    "Continuous Growth": "지속 성장",
    "Execution": "실행력",
    "Collaboration": "협업",
    "We are looking for people<br>who want to grow with us.": "NFD Korea와 함께<br>성장할 인재를 찾습니다.",
    "View Open Roles": "채용공고 보기",
    "Apply Now": "지원하기",
    "<h3>Apply</h3>": "<h3>지원하기</h3>",
    "Submit Your Application": "지원서 제출",
    "Use the button below to submit your application, or send your resume to enquiry@nfd.kr.": "아래 버튼으로 지원서를 제출하거나 enquiry@nfd.kr로 이력서를 보내주세요.",
    "Back to News": "뉴스 목록으로",
    "Contact": "문의",
    "Submit": "제출",
    "Send Message": "메시지 보내기",
}

LANG_CSS = """
<style>
.n-lang{display:flex;align-items:center;gap:3px;margin-left:10px;border:1px solid var(--border,#DDE3EF);border-radius:7px;padding:3px;background:rgba(255,255,255,.72);flex-shrink:0}
.n-lang a{font-family:var(--ff-en,'DM Sans',sans-serif);font-size:12px;font-weight:700;line-height:1;color:var(--gray-t,#4A5568);padding:7px 9px;border-radius:5px;text-decoration:none}
.n-lang a.active{background:var(--navy,#1A2B52);color:#fff}
.n-menu>li .sub-menu{top:100%}
.n-menu>li.open .sub-menu{display:block}
@media(max-width:1024px){.n-lang{margin-left:auto}.n-cta{display:none}}
</style>
"""

LANG_SCRIPT = """
<script>
document.querySelectorAll('[data-lang-choice]').forEach((link)=>{
  link.addEventListener('click',()=>localStorage.setItem('nfd_lang',link.dataset.langChoice));
});
let navCloseTimer;
const closeOpenNavItems = (exceptItem) => {
  document.querySelectorAll('.n-menu>li.open').forEach((openItem)=>{
    if(openItem !== exceptItem) openItem.classList.remove('open');
  });
};
document.querySelectorAll('.n-menu>li').forEach((item)=>{
  if(!item.querySelector('.sub-menu')) return;
  item.addEventListener('mouseenter',()=>{
    clearTimeout(navCloseTimer);
    closeOpenNavItems(item);
    item.classList.add('open');
  });
  item.addEventListener('mouseleave',()=>{
    clearTimeout(navCloseTimer);
    navCloseTimer = setTimeout(()=>item.classList.remove('open'),180);
  });
});
document.querySelectorAll('.n-menu>li>a.has-sub').forEach((trigger)=>{
  trigger.addEventListener('click',(event)=>{
    event.preventDefault();
    const item = trigger.closest('li');
    const isOpen = item.classList.contains('open');
    clearTimeout(navCloseTimer);
    closeOpenNavItems(item);
    item.classList.toggle('open',!isOpen);
  });
});
document.addEventListener('click',(event)=>{
  if(!event.target.closest('.n-menu')) {
    closeOpenNavItems();
  }
});
</script>
"""


def render_template(template_name: str, values: dict[str, str]) -> str:
    text = (PARTIALS / template_name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    missing = re.findall(r"{{[^}]+}}", text)
    if missing:
        raise ValueError(f"Unresolved placeholders in {template_name}: {', '.join(sorted(set(missing)))}")
    return text


def active(value: bool) -> str:
    return "active" if value else ""


def partial_values(lang: str, filename: str) -> dict[str, str]:
    values = dict(LABELS[lang])
    values.update(
        {
            "filename": filename,
            "about_active": active(filename in ABOUT_PAGES),
            "services_active": active(filename in SERVICE_PAGES),
            "projects_active": active(filename == "projects.html"),
            "careers_active": active(filename in CAREERS_PAGES),
            "news_active": active(filename in {"news.html", "news-detail.html"}),
            "en_active": active(lang == "en"),
            "ko_active": active(lang == "ko"),
        }
    )
    return values


def replace_layout_partials(text: str, lang: str, filename: str) -> str:
    values = partial_values(lang, filename)
    header = render_template("header.html", values)
    footer = render_template("footer.html", values)
    text, header_count = re.subn(r'<nav\s+id="nav"[\s\S]*?</nav>', header, text, count=1)
    text, footer_count = re.subn(r'<footer[\s\S]*?</footer>', footer, text, count=1)
    if header_count != 1:
        raise ValueError(f"{filename}: expected one <nav id=\"nav\"> block, replaced {header_count}")
    if footer_count != 1:
        raise ValueError(f"{filename}: expected one <footer> block, replaced {footer_count}")
    return text


def rewrite_assets(text: str) -> str:
    text = re.sub(r'((?:src|poster)=["\'])images/', r'\1../images/', text)
    text = re.sub(r'(url\(["\']?)images/', r'\1../images/', text)
    return text


def rewrite_html_links(text: str) -> str:
    def repl(match):
        quote, href = match.group(1), match.group(2)
        if re.match(r'^(?:https?:|mailto:|tel:|#|/|\.\./)', href):
            return match.group(0)
        if ".html" not in href:
            return match.group(0)
        base, frag = (href.split("#", 1) + [""])[:2]
        filename = Path(base).name
        suffix = f"#{frag}" if frag else ""
        return f'href={quote}{filename}{suffix}{quote}'

    return re.sub(r'href=(["\'])([^"\']+)\1', repl, text)


def translate_ko(text: str) -> str:
    for en, ko in sorted(KO_TEXT.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(en, ko)
        text = text.replace(html.escape(en), html.escape(ko))
    return text


def page_title(text: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, re.I | re.S)
    if not match:
        return "NFD Korea"
    return re.sub(r"\s+", " ", match.group(1)).strip()


def seo_description(lang: str, filename: str) -> str:
    return SEO_DESCRIPTION.get(lang, {}).get(filename, DEFAULT_DESCRIPTION[lang])


def seo_json_ld(lang: str, filename: str, title: str, description: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{SITE_URL}/#organization",
                "name": "NFD Korea",
                "alternateName": ["NFDKorea", "nfdkorea", "NFD Korea Co., Ltd.", "엔에프디코리아"],
                "url": SITE_URL,
                "email": "enquiry@nfd.kr",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "199-2 Nonhyun-dong",
                    "addressLocality": "Gangnam-gu",
                    "addressRegion": "Seoul",
                    "addressCountry": "KR",
                },
                "sameAs": ["https://www.linkedin.com/company/nfd-home"],
            },
            {
                "@type": "WebSite",
                "@id": f"{SITE_URL}/#website",
                "name": "NFD Korea",
                "alternateName": ["nfdkorea", "NFDKorea"],
                "url": SITE_URL,
                "publisher": {"@id": f"{SITE_URL}/#organization"},
                "inLanguage": "ko-KR" if lang == "ko" else "en",
            },
            {
                "@type": "WebPage",
                "@id": page_url(lang, filename),
                "url": page_url(lang, filename),
                "name": title,
                "description": description,
                "isPartOf": {"@id": f"{SITE_URL}/#website"},
                "about": {"@id": f"{SITE_URL}/#organization"},
                "inLanguage": "ko-KR" if lang == "ko" else "en",
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def inject_head(text: str, lang: str, filename: str) -> str:
    text = re.sub(r'<html\b[^>]*>', f'<html lang="{lang}">', text, count=1)
    title = page_title(text)
    description = seo_description(lang, filename)
    meta = (
        f'\n<link rel="canonical" href="{page_url(lang, filename)}">\n'
        f'<link rel="alternate" hreflang="en" href="{page_url("en", filename)}">\n'
        f'<link rel="alternate" hreflang="ko" href="{page_url("ko", filename)}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{page_url("en", filename)}">\n'
        f'<meta name="description" content="{html.escape(description, quote=True)}">\n'
        f'<meta name="keywords" content="{html.escape(SEO_KEYWORDS[lang], quote=True)}">\n'
        f'<meta property="og:type" content="website">\n'
        f'<meta property="og:site_name" content="NFD Korea">\n'
        f'<meta property="og:title" content="{html.escape(title, quote=True)}">\n'
        f'<meta property="og:description" content="{html.escape(description, quote=True)}">\n'
        f'<meta property="og:url" content="{page_url(lang, filename)}">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<script type="application/ld+json">{seo_json_ld(lang, filename, title, description)}</script>\n'
    )
    text = re.sub(r'(<meta name="viewport"[^>]*>)', r'\1' + meta, text, count=1)
    text = text.replace("</head>", LANG_CSS + "\n</head>", 1)
    return text


def inject_language_script(text: str) -> str:
    text = text.replace("</body>", LANG_SCRIPT + "\n</body>", 1)
    return text


def read_source(filename: str) -> str:
    source_path = SOURCE_DIR / filename
    if source_path.exists():
        return source_path.read_text(encoding="utf-8")
    return subprocess.run(
        ["git", "show", f"HEAD:{filename}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout


def ensure_source_pages():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for filename in PAGE_NAMES:
        source_path = SOURCE_DIR / filename
        if source_path.exists():
            continue
        source_path.write_text(
            subprocess.run(
                ["git", "show", f"HEAD:{filename}"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            ).stdout,
            encoding="utf-8",
        )


def build_page(filename: str, lang: str) -> str:
    text = read_source(filename)
    if lang == "ko":
        text = translate_ko(text)
    text = replace_layout_partials(text, lang, filename)
    text = rewrite_assets(text)
    text = rewrite_html_links(text)
    text = inject_head(text, lang, filename)
    text = inject_language_script(text)
    return text


def root_stub(filename: str, title: str) -> str:
    safe_title = html.escape(title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,follow">
<link rel="alternate" hreflang="en" href="{page_url("en", filename)}">
<link rel="alternate" hreflang="ko" href="{page_url("ko", filename)}">
<link rel="alternate" hreflang="x-default" href="{page_url("en", filename)}">
<title>{safe_title}</title>
<script>
(function(){{
  var page = "{filename}";
  var saved = localStorage.getItem("nfd_lang");
  var browser = (navigator.languages && navigator.languages[0]) || navigator.language || "";
  var tz = "";
  try {{ tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; }} catch(e) {{}}
  var lang = saved || (/^ko\\b/i.test(browser) || tz === "Asia/Seoul" ? "ko" : "en");
  if (lang !== "ko" && lang !== "en") lang = "en";
  location.replace("./" + lang + "/" + page + location.search + location.hash);
}}());
</script>
</head>
<body>
<p>Redirecting to <a href="./en/{filename}">English</a> / <a href="./ko/{filename}">Korean</a>.</p>
</body>
</html>
"""


def page_url(lang: str, filename: str) -> str:
    if SITE_URL:
        return f"{SITE_URL}/{lang}/{filename}"
    return f"{SITE_BASE_PATH}/{lang}/{filename}"


def generate_sitemap() -> str:
    urls = []
    for filename in PAGE_NAMES:
        for lang in ("en", "ko"):
            urls.append(
                f"""  <url>
    <loc>{html.escape(page_url(lang, filename))}</loc>
    <xhtml:link rel="alternate" hreflang="en" href="{html.escape(page_url("en", filename))}" />
    <xhtml:link rel="alternate" hreflang="ko" href="{html.escape(page_url("ko", filename))}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{html.escape(page_url("en", filename))}" />
  </url>"""
            )
    body = "\n".join(urls)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{body}
</urlset>
"""


def generate_robots() -> str:
    sitemap_url = f"{SITE_URL}/sitemap.xml" if SITE_URL else f"{SITE_BASE_PATH}/sitemap.xml"
    return f"""User-agent: *
Allow: /

User-agent: Yeti
Allow: /

Sitemap: {sitemap_url}
"""


def copy_public_files():
    if not PUBLIC_DIR.exists():
        return
    for source in PUBLIC_DIR.rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(PUBLIC_DIR)
        target = OUTPUT_DIR / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main():
    ensure_source_pages()
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    for lang in ("en", "ko"):
        (OUTPUT_DIR / lang).mkdir(parents=True, exist_ok=True)
    for filename in PAGE_NAMES:
        for lang in ("en", "ko"):
            (OUTPUT_DIR / lang / filename).write_text(build_page(filename, lang), encoding="utf-8")

    for filename in PAGE_NAMES:
        source = read_source(filename)
        m = re.search(r"<title>(.*?)</title>", source, re.I | re.S)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else f"NFD Korea - {filename}"
        (OUTPUT_DIR / filename).write_text(root_stub(filename, title), encoding="utf-8")

    if (ROOT / "images").exists():
        shutil.copytree(ROOT / "images", OUTPUT_DIR / "images")
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    (OUTPUT_DIR / "CNAME").write_text("www.nfd.kr\n", encoding="utf-8")
    (OUTPUT_DIR / "sitemap.xml").write_text(generate_sitemap(), encoding="utf-8")
    (OUTPUT_DIR / "robots.txt").write_text(generate_robots(), encoding="utf-8")
    copy_public_files()


if __name__ == "__main__":
    main()
