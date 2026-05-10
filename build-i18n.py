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
    "Start your data center project<br>with the right team.": "최적의 팀과 함께<br>데이터센터 프로젝트를 시작하세요.",
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
    "Inquiry Type": "문의 유형",
    "Name": "이름",
    "Message": "문의 내용",
    "Email": "이메일",
    "A trusted partner for data center development and operations consulting, built on expertise and execution.": "전문성과 실행력을 바탕으로 데이터센터 개발과 운영 컨설팅을 제공하는 신뢰할 수 있는 파트너입니다.",
    "Drive Your Future": "미래를 이끄는 힘",
    "with Next Frontier Drive": "Next Frontier Drive와 함께",
    "expertise and innovation": "전문성과 혁신",
    "We place our clients' value and business success first, delivering optimal strategies and solutions tailored to the data center industry. In a rapidly evolving digital infrastructure environment, we offer expertise that keeps projects moving with clarity and confidence.": "고객의 가치와 사업 성공을 최우선으로 생각하며, 데이터센터 산업에 특화된 최적의 전략과 솔루션을 제공합니다. 빠르게 변화하는 디지털 인프라 환경에서 프로젝트가 명확하고 안정적으로 나아가도록 전문성을 제공합니다.",
    "From site selection and development strategy to customer acquisition, design management, construction management, and operational efficiency, we provide": "부지 선정과 개발 전략부터 고객 유치, 설계 관리, 시공 관리, 운영 효율화까지",
    "expert services across the full lifecycle": "데이터센터 전 생애주기에 걸친 전문 서비스를 제공합니다",
    "of the data center.": " ",
    "Our Clients": "주요 고객",
    "Our Partners": "주요 파트너",
    "We work alongside global investors and data center operators on high-value infrastructure projects.": "글로벌 투자자 및 데이터센터 운영사와 함께 고부가가치 인프라 프로젝트를 수행합니다.",
    "Global Private Equity · Investor": "글로벌 사모펀드 · 투자자",
    "Data Center Operator · Partner": "데이터센터 운영사 · 파트너",
    "Start your next project": "다음 프로젝트를 시작하세요",
    "View 서비스": "서비스 보기",
    "View 인재상": "인재상 보기",
    "Next Frontier Drive Korea": "Next Frontier Drive Korea",
    "Next Frontier Drive와 함께": "Next Frontier Drive와 함께",
    "Scroll": "스크롤",
    "From site selection to capital strategy, we support the full development cycle through one integrated team.": "부지 선정부터 자본 전략까지 하나의 통합 팀으로 전체 개발 사이클을 지원합니다.",
    "Architecture, electrical, mechanical, and control systems are aligned through coordinated engineering analysis.": "건축, 전기, 기계, 제어 시스템을 통합 엔지니어링 분석으로 정렬합니다.",
    "Senior specialists with deep field experience manage schedule, cost, quality, and delivery risk together.": "풍부한 현장 경험을 갖춘 시니어 전문가들이 일정, 비용, 품질, 수행 리스크를 함께 관리합니다.",
    "Reliable and efficient facility operations protect uptime, tenant requirements, and long-term business continuity.": "안정적이고 효율적인 시설 운영으로 가동률, 임차사 요구사항, 장기적인 사업 연속성을 보호합니다.",
    "We cover the full data center lifecycle, from land sourcing and investment strategy to operations, within one organization.": "부지 발굴과 투자 전략부터 운영까지 데이터센터 전 생애주기를 하나의 조직 안에서 지원합니다.",
    "Specialists across architecture, civil, electrical, mechanical, and controls lead execution directly.": "건축, 토목, 전기, 기계, 제어 분야 전문가들이 직접 실행을 이끕니다.",
    "We help attract customers through strong relationships with global CSPs, domestic and overseas developers, and institutional investors.": "글로벌 CSP, 국내외 개발사, 기관투자자와의 강한 네트워크를 바탕으로 고객 유치를 지원합니다.",
    "Validated cost efficiency from the Yongin Deokseong-ri project and recent CAPEX benchmarking improves planning accuracy.": "용인 덕성리 프로젝트와 최신 CAPEX 벤치마킹에서 검증된 비용 효율성으로 계획 정확도를 높입니다.",
    "Optimized energy design lowers operating cost while helping clients meet uptime and ESG targets together.": "최적화된 에너지 설계로 운영비를 낮추고 가동률 및 ESG 목표 달성을 함께 지원합니다.",
    "Data center development and advisory": "데이터센터 개발 및 자문",
    "We support site selection, investment structuring, and feasibility planning with disciplined project strategy.": "체계적인 프로젝트 전략을 바탕으로 부지 선정, 투자 구조화, 사업성 검토를 지원합니다.",
    "Design and engineering consulting": "설계 및 엔지니어링 컨설팅",
    "Coordinated multidisciplinary analysis improves resiliency, constructability, and cost performance.": "통합 다분야 분석으로 복원력, 시공성, 비용 성능을 높입니다.",
    "Experienced leaders manage cost, quality, schedule, and delivery risk through every project milestone.": "경험 많은 리더들이 프로젝트의 주요 마일스톤마다 비용, 품질, 일정, 수행 리스크를 관리합니다.",
    "Colocation leasing and operations": "코로케이션 임대 및 운영",
    "Tenant-ready space and stable operations help protect service continuity and long-term performance.": "입주 준비가 완료된 공간과 안정적인 운영으로 서비스 연속성과 장기 성과를 보호합니다.",
    "Backed by accumulated experience and a global network, we help clients build successful digital infrastructure.": "축적된 경험과 글로벌 네트워크를 바탕으로 고객의 성공적인 디지털 인프라 구축을 지원합니다.",
    "Our": "우리의",
    "Mission": "미션",
    "Vision": "비전",
    "Supporting the successful delivery of digital infrastructure.": "디지털 인프라의 성공적인 구축을 지원합니다.",
    "We analyze client needs with precision and provide the most effective solutions. Our mission is to empower every client to build resilient, high-performance digital infrastructure — on time, on budget, and built to last.": "고객의 요구를 정밀하게 분석하고 가장 효과적인 솔루션을 제공합니다. 우리의 미션은 모든 고객이 정해진 일정과 예산 안에서 오래 지속되는 고성능 디지털 인프라를 구축하도록 돕는 것입니다.",
    "Building scalable and sustainable data center platforms.": "확장 가능하고 지속 가능한 데이터센터 플랫폼을 구축합니다.",
    "With expertise and execution capability, we lead the next wave of digital infrastructure. We envision a future where every data center we touch sets a new benchmark for efficiency, scalability, and sustainability.": "전문성과 실행력을 바탕으로 디지털 인프라의 다음 흐름을 이끕니다. 우리가 참여하는 모든 데이터센터가 효율성, 확장성, 지속가능성의 새로운 기준이 되는 미래를 지향합니다.",
    "Value 01": "가치 01",
    "Value 02": "가치 02",
    "Value 03": "가치 03",
    "Value 04": "가치 04",
    "Expertise": "전문성",
    "Partnership": "파트너십",
    "Innovation": "혁신",
    "Sustainability": "지속가능성",
    "Disciplined engineering and informed decision-making.": "체계적인 엔지니어링과 근거 있는 의사결정.",
    "Close collaboration with clients, investors, and operators.": "고객, 투자자, 운영사와의 긴밀한 협업.",
    "Forward-looking solutions for evolving digital infrastructure.": "진화하는 디지털 인프라를 위한 선제적 솔루션.",
    "Long-term performance shaped by efficiency and resilience.": "효율성과 복원력으로 만드는 장기 성과.",
    "Expertise · Partnership · Innovation · Sustainability": "전문성 · 파트너십 · 혁신 · 지속가능성",
    "Through advanced knowledge and close collaboration, we create innovative and sustainable value. These four pillars guide every decision, every project, and every relationship we build.": "고도화된 지식과 긴밀한 협업을 통해 혁신적이고 지속 가능한 가치를 만듭니다. 네 가지 가치는 모든 의사결정, 프로젝트, 관계의 기준입니다.",
    "we support our clients in building successful digital infrastructure.": "고객의 성공적인 디지털 인프라 구축을 지원합니다.",
    "A structured specialist organization supporting client projects from strategy through delivery.": "전략부터 실행까지 고객 프로젝트를 지원하는 전문 조직 체계입니다.",
    "Chief Executive Officer": "대표이사",
    "Finance & Management": "재무 및 경영관리",
    "HR and recruitment management": "인사 및 채용 관리",
    "Finance and accounting operations": "재무 및 회계 운영",
    "General affairs and administration support": "총무 및 행정 지원",
    "Technical Division": "기술 부문",
    "Technical DD·TestFit": "기술 DD · Test Fit",
    "Design, engineering, and VE": "설계, 엔지니어링 및 VE",
    "CAPEX development and schedule review": "CAPEX 산정 및 일정 검토",
    "Phase-by-phase PM and LLE management": "단계별 PM 및 LLE 관리",
    "Commissioning and operations management": "커미셔닝 및 운영 관리",
    "Development & Sales": "개발 및 영업",
    "New site development": "신규 부지 개발",
    "Business structure, budget, and underwriting models": "사업 구조, 예산 및 언더라이팅 모델",
    "Client management and contract execution": "고객 관리 및 계약 실행",
    "Teams Within the Technical Division": "기술 부문 산하 팀",
    "Architectural Team": "건축팀",
    "Electrical Team": "전기팀",
    "Mechanical Team": "기계팀",
    "Controls Team": "제어팀",
    "From founding to today, a fast-moving track record of growth.": "창립 이후 빠르게 성장해 온 주요 이력입니다.",
    "Acceleration of flagship developments": "핵심 개발 프로젝트 가속화",
    "Expanded execution capability and brand integration": "수행 역량 확대 및 브랜드 통합",
    "Partnership formation and pre-construction progress": "파트너십 구축 및 착공 전 단계 진전",
    "회사 launch and first major platform": "회사 출범 및 첫 주요 플랫폼 구축",
    "Service Portfolio": "서비스 포트폴리오",
    "We provide differentiated services across development, engineering, construction, and operations for data center projects.": "데이터센터 프로젝트의 개발, 엔지니어링, 시공, 운영 전반에 걸쳐 차별화된 서비스를 제공합니다.",
    "We guide site diligence, feasibility, and investment planning with practical strategies that shape project success from the earliest stage.": "초기 단계부터 프로젝트 성공을 설계하는 실질적 전략으로 부지 검토, 사업성 분석, 투자 계획을 지원합니다.",
    "Pre, technical, legal, tax DD, and test-fit execution": "Pre, 기술, 법무, 세무 DD 및 Test Fit 수행",
    "Investment structure and business model planning": "투자 구조 및 사업 모델 수립",
    "High-accuracy planning backed by current CAPEX data": "최신 CAPEX 데이터를 바탕으로 한 고정밀 계획",
    "Learn 더보기 →": "자세히 보기 →",
    "We deliver tailored design and engineering support aligned with tenant requirements, reliability targets, and operating efficiency.": "임차사 요구사항, 신뢰성 목표, 운영 효율에 맞춘 설계 및 엔지니어링 지원을 제공합니다.",
    "Integrated architectural, electrical, mechanical, and controls analysis": "건축, 전기, 기계, 제어 통합 분석",
    "Engineering tailored to target customer specifications": "목표 고객 요구사항에 맞춘 엔지니어링",
    "Design optimization with quality and cost in balance": "품질과 비용의 균형을 고려한 설계 최적화",
    "Reviews focused on operating efficiency and future expansion": "운영 효율과 향후 확장성을 고려한 검토",
    "In-house liquid cooling design capability": "자체 액체냉각 설계 역량",
    "Senior discipline experts across architecture, civil, electrical, mechanical, and controls": "건축, 토목, 전기, 기계, 제어 분야별 시니어 전문가",
    "Integrated management from development through operations": "개발부터 운영까지 통합 관리",
    "Owner-minded control of cost, quality, and schedule": "발주자 관점의 비용, 품질, 일정 관리",
    "Early risk management to protect planned milestones": "계획된 마일스톤을 지키기 위한 선제 리스크 관리",
    "Colocation leasing and operations management": "코로케이션 임대 및 운영 관리",
    "We help maintain uptime, operational efficiency, and tenant satisfaction through disciplined facilities and service management.": "체계적인 시설 및 서비스 관리를 통해 가동률, 운영 효율, 임차사 만족도를 유지합니다.",
    "Tenant-ready colocation environments for different customer profiles": "고객 유형별 입주 준비형 코로케이션 환경",
    "Support for SLA and lease requirements by tenant type": "임차사 유형별 SLA 및 임대 조건 지원",
    "Efficient facilities management and operations optimization": "효율적인 시설 관리 및 운영 최적화",
    "Ongoing infrastructure capacity management": "지속적인 인프라 용량 관리",
    "Operations structured around service stability and continuity": "서비스 안정성과 연속성을 중심으로 한 운영 체계",
    "Step-by-step service process": "단계별 서비스 프로세스",
    "From land strategy to live operations, our four-stage process keeps delivery structured and accountable.": "부지 전략부터 운영 개시까지 4단계 프로세스로 체계적이고 책임감 있게 수행합니다.",
    "Site development": "부지 개발",
    "Site Selection": "부지 선정",
    "Design and permits": "설계 및 인허가",
    "Pre-Construction": "착공 전 단계",
    "Construction": "시공",
    "Operation": "운영",
    "Site selection and test-fit review": "부지 선정 및 Test Fit 검토",
    "Preliminary due diligence": "예비 실사",
    "Technical DD for target tenants": "목표 임차사 대상 기술 DD",
    "Optimized business structure planning": "최적 사업 구조 수립",
    "Budget and investment model setup": "예산 및 투자 모델 수립",
    "Project planning and requirements definition": "프로젝트 계획 및 요구사항 정의",
    "Cost estimate and budget planning": "공사비 산정 및 예산 계획",
    "Design and permitting optimization": "설계 및 인허가 최적화",
    "Contractor and major equipment procurement support": "시공사 및 주요 장비 조달 지원",
    "LLE item selection and contracting": "LLE 품목 선정 및 계약",
    "Schedule and construction cost management": "일정 및 공사비 관리",
    "Design change and VE or VO control": "설계 변경 및 VE/VO 관리",
    "Permitting revision coordination": "인허가 변경 조율",
    "Major equipment delivery and commissioning": "주요 장비 납품 및 커미셔닝",
    "Operations readiness planning": "운영 준비 계획",
    "Data center operations management": "데이터센터 운영 관리",
    "Facilities, security, and telecom coordination": "시설, 보안, 통신 통합 관리",
    "Operating cost and efficiency oversight": "운영비 및 효율 관리",
    "Tenant interface management": "임차사 인터페이스 관리",
    "Want to discuss your service needs?": "필요한 서비스를 논의하고 싶으신가요?",
    "Speak directly with our specialists.": "전문가와 직접 상담하세요.",
    "& Consulting": "및 컨설팅",
    "From site due diligence to feasibility analysis, we deliver trusted strategies for your data center investment decisions.": "부지 실사부터 사업성 분석까지 데이터센터 투자 의사결정을 위한 신뢰도 높은 전략을 제공합니다.",
    "Overview": "개요",
    "The success of a data center project": "데이터센터 프로젝트의 성공은",
    "is decided in the early development stage.": "초기 개발 단계에서 결정됩니다.",
    "Core DD Service Areas": "핵심 DD 서비스 영역",
    "Avg. Expert Experience": "전문가 평균 경력",
    "Core Capabilities": "핵심 역량",
    "3 Core Development 서비스": "3대 핵심 개발 서비스",
    "We provide phased expertise from early-stage development through investment structure design.": "초기 개발부터 투자 구조 설계까지 단계별 전문성을 제공합니다.",
    "Site Selection & Assessment": "부지 선정 및 평가",
    "Proprietary site selection and client land assessment": "자체 부지 선정 및 고객 보유 부지 평가",
    "Risk and opportunity analysis by site condition": "부지 조건별 리스크 및 기회 분석",
    "Comprehensive review of infrastructure, power, and regulatory environment": "인프라, 전력, 인허가 환경 종합 검토",
    "Project Due Diligence (DD)": "프로젝트 실사(DD)",
    "We systematically execute Pre, Technical, Legal, and Tax DD to sharpen the accuracy of investment decision-making.": "Pre, 기술, 법무, 세무 DD를 체계적으로 수행해 투자 의사결정의 정확도를 높입니다.",
    "Pre DD · Technical DD · Legal DD · Tax DD execution": "Pre DD · 기술 DD · 법무 DD · 세무 DD 수행",
    "Application and review of proprietary Test Fit designs": "자체 Test Fit 설계 적용 및 검토",
    "Technical review reflecting target tenant requirements": "목표 임차사 요구사항을 반영한 기술 검토",
    "Risk assessment reports to support investment decisions": "투자 의사결정을 지원하는 리스크 평가 보고서",
    "Investment Structure & Business Model": "투자 구조 및 사업 모델",
    "Investment structure and business model design": "투자 구조 및 사업 모델 설계",
    "High-precision feasibility analysis and financial modeling": "고정밀 사업성 분석 및 재무 모델링",
    "Investor and financial institution presentation support": "투자자 및 금융기관 프레젠테이션 지원",
    "The success of a data center project is determined in the early development stage.": "데이터센터 프로젝트의 성공은 초기 개발 단계에서 결정됩니다.",
    "Service Process": "서비스 프로세스",
    "개발 컨설팅 Process": "개발 컨설팅 프로세스",
    "From initial site review to investment decision — we provide close support at every stage.": "초기 부지 검토부터 투자 의사결정까지 모든 단계에서 긴밀하게 지원합니다.",
    "Step 01": "1단계",
    "Step 02": "2단계",
    "Step 03": "3단계",
    "Step 04": "4단계",
    "Site Review & Selection": "부지 검토 및 선정",
    "Due Diligence (DD) 실행력": "실사(DD) 수행",
    "Starting with Pre DD, we conduct Technical, Legal, and Tax DD in sequence. Through proprietary Test Fit designs, we precisely calculate capacity and CAPEX to support confident decision-making.": "Pre DD를 시작으로 기술, 법무, 세무 DD를 순차적으로 수행합니다. 자체 Test Fit 설계를 통해 수용 용량과 CAPEX를 정밀하게 산정하여 확신 있는 의사결정을 지원합니다.",
    "Investment Structure & Business Model Planning": "투자 구조 및 사업 모델 수립",
    "Want to learn more about 개발 컨설팅?": "개발 컨설팅이 더 궁금하신가요?",
    "Speak directly with our experts.": "전문가와 직접 상담하세요.",
    "Design & Engineering": "설계 및 엔지니어링",
    "Consulting": "컨설팅",
    "We deliver customized data center design and engineering solutions tailored to each client's unique requirements.": "고객별 요구사항에 맞춘 데이터센터 설계 및 엔지니어링 솔루션을 제공합니다.",
    "Integrated Design Solutions": "통합 설계 솔루션",
    "Optimized for Tenant Requirements": "임차사 요구사항에 최적화",
    "4 Core Design & Engineering Capabilities": "4대 핵심 설계 및 엔지니어링 역량",
    "From in-house specialist engineers to client-tailored optimization — we take full responsibility for every stage of design.": "내부 전문 엔지니어부터 고객 맞춤 최적화까지 설계의 모든 단계를 책임집니다.",
    "In-House Specialist Engineers": "내부 전문 엔지니어",
    "Integrated Multi-Discipline Design": "다분야 통합 설계",
    "Through integrated analysis across architecture, electrical, mechanical, and controls, we deliver robust, coherent designs. We minimize inter-discipline interfaces to ensure design quality throughout.": "건축, 전기, 기계, 제어 분야의 통합 분석을 통해 견고하고 일관된 설계를 제공합니다. 분야 간 인터페이스를 최소화해 설계 품질을 확보합니다.",
    "Tenant-Tailored 서비스": "임차사 맞춤 서비스",
    "We provide design and engineering services that meet the specific requirements of target tenants — from hyperscalers to enterprise clients — addressing a diverse range of demand profiles.": "하이퍼스케일러부터 엔터프라이즈 고객까지 다양한 수요 특성에 맞춰 목표 임차사의 요구사항을 충족하는 설계 및 엔지니어링 서비스를 제공합니다.",
    "Client-Centered Optimization": "고객 중심 최적화",
    "We deliver design optimization consulting that balances quality and economic performance. Through detailed design reviews that consider operational efficiency and scalability, we create lasting long-term value.": "품질과 경제성을 균형 있게 고려한 설계 최적화 컨설팅을 제공합니다. 운영 효율과 확장성을 고려한 상세 설계 검토를 통해 장기적인 가치를 만듭니다.",
    "Optimal design enables optimal operations,": "최적의 설계가 최적의 운영을 가능하게 하고,",
    "and optimal operations become your competitive advantage.": "최적의 운영은 고객의 경쟁력이 됩니다.",
    "Engineering Disciplines": "엔지니어링 분야",
    "Design & Engineering Disciplines": "설계 및 엔지니어링 분야",
    "Architectural Design": "건축 설계",
    "Data center-specific architectural planning and structural review. We provide comprehensive support including space planning that reflects operational efficiency and scalability, as well as fire safety and code review.": "데이터센터에 특화된 건축 계획과 구조 검토를 수행합니다. 운영 효율과 확장성을 반영한 공간 계획, 소방 안전 및 법규 검토까지 종합적으로 지원합니다.",
    "Electrical Design": "전기 설계",
    "Mechanical Design (Cooling)": "기계 설계(냉각)",
    "Controls (BMS / DCIM)": "제어(BMS / DCIM)",
    "BMS and DCIM control system design and integration review. We architect control systems that maximize operational stability and efficiency through real-time monitoring and intelligent automation.": "BMS 및 DCIM 제어 시스템 설계와 통합 검토를 수행합니다. 실시간 모니터링과 지능형 자동화를 통해 운영 안정성과 효율을 극대화하는 제어 시스템을 설계합니다.",
    "Need Design & Engineering": "설계 및 엔지니어링",
    "Operations & Leasing": "운영 및 임대",
    "04 — Operations & Leasing": "04 — 운영 및 임대",
    "Colocation & Data Center": "코로케이션 및 데이터센터",
    "We ensure service reliability and business continuity for our clients through stable and efficient operations management.": "안정적이고 효율적인 운영 관리를 통해 고객의 서비스 신뢰성과 사업 연속성을 보장합니다.",
    "Stable Operations Are": "안정적인 운영은",
    "Your Competitive Advantage": "고객의 경쟁력입니다",
    "Core 서비스": "핵심 서비스",
    "3 Core Operations 서비스": "3대 핵심 운영 서비스",
    "Tenant-tailored leasing, operational efficiency, and service reliability — three pillars that define how we run your data center.": "임차사 맞춤 임대, 운영 효율, 서비스 신뢰성은 데이터센터 운영의 세 가지 핵심 축입니다.",
    "Tenant-Tailored Colocation": "임차사 맞춤 코로케이션",
    "We provide colocation environments customized to diverse tenant profiles, with flexible SLA and contractual terms adapted to each tenant type.": "다양한 임차사 유형에 맞춘 코로케이션 환경을 제공하고, 임차사별 특성에 맞는 유연한 SLA와 계약 조건을 지원합니다.",
    "Customized SLA and contract management by tenant type": "임차사 유형별 맞춤 SLA 및 계약 관리",
    "Appropriate CAPEX alignment with development conditions": "개발 조건에 맞춘 적정 CAPEX 정렬",
    "Tailored space configurations for hyperscalers, enterprise, and SME tenants": "하이퍼스케일러, 엔터프라이즈, 중소형 임차사를 위한 맞춤 공간 구성",
    "Tenant move-in readiness and onboarding support": "임차사 입주 준비 및 온보딩 지원",
    "High Operational Efficiency": "높은 운영 효율",
    "We maximize facility management and operational efficiency to deliver cost-effective data center operations.": "시설 관리와 운영 효율을 극대화해 비용 효율적인 데이터센터 운영을 제공합니다.",
    "Maximized facility management and operational efficiency": "시설 관리 및 운영 효율 극대화",
    "Continuous infrastructure capacity management to sustain efficiency": "효율 유지를 위한 지속적인 인프라 용량 관리",
    "Service Reliability": "서비스 신뢰성",
    "We deliver operations management that places client service reliability and business continuity at the forefront of everything we do.": "고객의 서비스 신뢰성과 사업 연속성을 최우선으로 하는 운영 관리를 제공합니다.",
    "Guaranteed client service reliability and business continuity": "고객 서비스 신뢰성 및 사업 연속성 보장",
    "24/7 monitoring and incident response framework": "24/7 모니터링 및 장애 대응 체계",
    "Business Continuity Plan (BCP)-based operations management": "BCP 기반 운영 관리",
    "Regular audits and compliance support": "정기 감사 및 컴플라이언스 지원",
    "Reliable and efficient operations management is your competitive advantage.": "안정적이고 효율적인 운영 관리는 고객의 경쟁력입니다.",
    "Operational Management Capabilities": "운영 관리 역량",
    "Facility Management": "시설 관리",
    "Integrated Facility Management": "통합 시설 관리",
    "We operate an integrated management system covering electrical, mechanical, fire safety, security, and communications infrastructure. Dedicated specialists monitor facility status in real time and carry out preventive maintenance to protect uptime.": "전기, 기계, 소방, 보안, 통신 인프라를 포괄하는 통합 관리 체계를 운영합니다. 전담 전문가가 시설 상태를 실시간으로 모니터링하고 예방 정비를 수행해 가동률을 보호합니다.",
    "Capacity Management": "용량 관리",
    "Infrastructure Capacity Management": "인프라 용량 관리",
    "We continuously analyze power, cooling, and space capacity to proactively respond to shifts in tenant demand. Through disciplined capacity planning and optimization, we sustain operational efficiency over time.": "전력, 냉각, 공간 용량을 지속적으로 분석해 임차사 수요 변화에 선제적으로 대응합니다. 체계적인 용량 계획과 최적화를 통해 운영 효율을 지속적으로 유지합니다.",
    "Tenant Interface": "임차사 인터페이스",
    "Tenant Interface Management": "임차사 인터페이스 관리",
    "Through dedicated points of contact for each tenant, we handle SLA compliance reporting, infrastructure change requests, and issue resolution with speed and accountability. Tenant satisfaction is managed as a core operating metric.": "임차사별 전담 창구를 통해 SLA 준수 보고, 인프라 변경 요청, 이슈 해결을 신속하고 책임감 있게 처리합니다. 임차사 만족도를 핵심 운영 지표로 관리합니다.",
    "Speak with our experts about": "전문가와 상담하세요",
    "Phase-by-Phase Project": "단계별 프로젝트",
    "Delivered by One Unified Team": "하나의 통합 팀이 수행합니다",
    "Our specialists in architecture, civil, electrical, mechanical, and controls engineering — with an average of 22 years' experience — take full accountability for meeting cost, quality, and schedule targets.": "평균 22년 경력의 건축, 토목, 전기, 기계, 제어 엔지니어링 전문가들이 비용, 품질, 일정 목표 달성을 책임집니다.",
    "Core Strengths": "핵심 강점",
    "Discipline-specific expertise, integrated management systems, and proactive risk control — together, they deliver your project.": "분야별 전문성, 통합 관리 체계, 선제적 리스크 관리를 결합해 프로젝트를 수행합니다.",
    "Discipline-Specific Expert Team": "분야별 전문 팀",
    "In-house experts across architecture, civil, electrical, mechanical, and controls": "건축, 토목, 전기, 기계, 제어 분야 내부 전문가",
    "Average 22+ years of experience per discipline": "분야별 평균 22년 이상 경력",
    "Efficient management of all project stakeholders": "프로젝트 이해관계자 효율적 관리",
    "Cost, Quality & Schedule Control": "비용, 품질 및 일정 관리",
    "We operate an integrated management system to achieve our clients' cost, quality, and schedule targets without compromise.": "고객의 비용, 품질, 일정 목표를 타협 없이 달성하기 위해 통합 관리 체계를 운영합니다.",
    "Consistent goals and strategy maintained by a single unified organization": "단일 통합 조직을 통한 일관된 목표와 전략 유지",
    "Proactive review of design changes (VE/VO) and cost impact analysis": "설계 변경(VE/VO) 선제 검토 및 비용 영향 분석",
    "Progress vs. plan monitoring with early corrective action": "계획 대비 진행률 모니터링 및 조기 시정 조치",
    "Owner-side quality inspection and acceptance framework": "발주자 관점의 품질 검사 및 인수 체계",
    "Proactive Risk Management": "선제적 리스크 관리",
    "We identify and manage phase-specific risks in advance to keep the project on schedule and on target.": "단계별 리스크를 사전에 식별하고 관리해 프로젝트가 일정과 목표를 지키도록 합니다.",
    "Phase-by-phase risk identification and mitigation planning": "단계별 리스크 식별 및 완화 계획",
    "Integrated management of permitting, procurement, and construction risks": "인허가, 조달, 시공 리스크 통합 관리",
    "Structured stakeholder communication framework": "체계적인 이해관계자 커뮤니케이션 체계",
    "Early operational readiness (OR) review and transition support": "초기 운영 준비(OR) 검토 및 전환 지원",
    "Our Experts": "전문가",
    "An Industry-Leading": "업계를 선도하는",
    "Avg. experience": "평균 경력",
    "per discipline": "분야별",
    "Engineering disciplines": "엔지니어링 분야",
    "(Arch · Civil · Elec · Mech · Controls)": "(건축 · 토목 · 전기 · 기계 · 제어)",
    "Project phases": "프로젝트 단계",
    "managed end-to-end": "전 과정 관리",
    "Single unified team": "단일 통합 팀",
    "integrated management": "통합 관리",
    "Service Phases": "서비스 단계",
    "We systematically manage all four phases — from development through operations.": "개발부터 운영까지 네 단계를 체계적으로 관리합니다.",
    "Development Phase": "개발 단계",
    "Site selection and Test-Fit review": "부지 선정 및 Test Fit 검토",
    "Preliminary Due Diligence (Pre DD)": "예비 실사(Pre DD)",
    "Target tenant Technical DD support": "목표 임차사 기술 DD 지원",
    "Business structure optimization planning": "사업 구조 최적화 계획",
    "Budget and investment model development": "예산 및 투자 모델 개발",
    "Design & Permitting Phase": "설계 및 인허가 단계",
    "Design and permitting optimization management": "설계 및 인허가 최적화 관리",
    "Contractor and key equipment procurement support": "시공사 및 핵심 장비 조달 지원",
    "Long-Lead Equipment (LLE) selection and contract management": "장납기 장비(LLE) 선정 및 계약 관리",
    "Construction Phase": "시공 단계",
    "Design change and VE/VO management": "설계 변경 및 VE/VO 관리",
    "Permitting change coordination": "인허가 변경 조율",
    "Key equipment delivery and commissioning management": "핵심 장비 납품 및 커미셔닝 관리",
    "Operational Readiness (OR) planning": "운영 준비(OR) 계획",
    "Operations Phase": "운영 단계",
    "Integrated facility, security, and communications management": "시설, 보안, 통신 통합 관리",
    "Operations cost and efficiency management": "운영비 및 효율 관리",
    "Consistent goals and strategy across every phase, supporting the successful delivery of your project.": "모든 단계에서 일관된 목표와 전략을 유지해 프로젝트의 성공적인 수행을 지원합니다.",
    "Speak with our experts": "전문가와 상담하기",
    "Total Pipeline": "전체 파이프라인",
    "Energy Efficiency Achieved": "달성 에너지 효율",
    "Owner Development": "자체 개발",
    "Owner-developed projects": "자체 개발 프로젝트",
    "Owner Development · In Progress": "자체 개발 · 진행 중",
    "Owner Development · Hyperscale Program": "자체 개발 · 하이퍼스케일 프로그램",
    "Owner Development · In Development": "자체 개발 · 개발 중",
    "Power Capacity": "수전 용량",
    "IT Load": "IT 부하",
    "Data Hall": "데이터홀",
    "Site Area": "대지 면적",
    "Gross Floor Area": "연면적",
    "SCOPE OF WORK": "업무 범위",
    "Land development and investor attraction with Warburg Pincus": "Warburg Pincus와 토지 개발 및 투자자 유치",
    "Tenant attraction with global CSP LOI and carrier LOC secured": "글로벌 CSP LOI 및 통신사 LOC 확보를 통한 임차사 유치",
    "Groundbreaking Sep 2025 · Completion Q2 2028": "2025년 9월 착공 · 2028년 2분기 준공",
    "Groundbreaking Q3 2026 · Completion Q4 2028": "2026년 3분기 착공 · 2028년 4분기 준공",
    "Permitting Jul 2026 · Groundbreaking Q1 2027": "2026년 7월 인허가 · 2027년 1분기 착공",
    "Advisory 프로젝트": "자문 프로젝트",
    "Consulting engagements": "컨설팅 수행 프로젝트",
    "Consulting · Pre-Construction": "컨설팅 · 착공 전 단계",
    "Consulting · In Operation": "컨설팅 · 운영 중",
    "Scope": "범위",
    "Tenant sourcing, design, engineering": "임차사 소싱, 설계, 엔지니어링",
    "Engineering consulting": "엔지니어링 컨설팅",
    "Permitting Sep 2025 · Groundbreaking Q1 2026": "2025년 9월 인허가 · 2026년 1분기 착공",
    "Completion Jul 2025 · Operations from Oct 2025": "2025년 7월 준공 · 2025년 10월 운영 개시",
    "Case Study": "사례 연구",
    "CAPEX efficiency": "CAPEX 효율",
    "tenant secured": "임차사 확보",
    "expansion flexibility": "확장 유연성",
    "Discuss This Project →": "프로젝트 상담하기 →",
    "Let's start your next": "다음 프로젝트를",
    "project together.": "함께 시작하세요.",
    "Career opportunities": "채용 기회",
    "Driven by necessity, we provide solutions that help clients navigate challenges with integrity and foresight.": "필요에서 출발한 솔루션으로 고객이 정직함과 선견지명을 바탕으로 과제를 해결하도록 돕습니다.",
    "Development Sales": "개발 영업",
    "Full-time": "정규직",
    "Senior": "시니어",
    "Real-estate Manager": "부동산 개발 매니저",
    "Real-estate development manager": "부동산 개발 매니저",
    "Senior Project Manager": "시니어 프로젝트 매니저",
    "Senior project manager": "시니어 프로젝트 매니저",
    "Mechanical & Electrical Engineer": "기계·전기 엔지니어",
    "Mechanical and electrical engineer": "기계·전기 엔지니어",
    "Senior CSA Engineer": "시니어 CSA 엔지니어",
    "Senior CSA engineer": "시니어 CSA 엔지니어",
    "Mechanical Engineer": "기계 엔지니어",
    "Electrical Engineer": "전기 엔지니어",
    "Land deal sourcing, structuring, due diligence, and negotiation of key terms and transaction documents": "토지 거래 발굴, 구조화, 실사 및 주요 조건·거래 문서 협상",
    "Manage data center projects from due diligence through design development, permitting, construction and turnover.": "실사부터 설계 개발, 인허가, 시공, 인계까지 데이터센터 프로젝트를 관리합니다.",
    "Create and review Civil, Structural, and Architectural design for data center facilities": "데이터센터 시설의 토목, 구조, 건축 설계를 작성하고 검토합니다.",
    "Manage project schedules, budgets, and risks from a mechanical and electrical engineering perspective": "기계·전기 엔지니어링 관점에서 프로젝트 일정, 예산, 리스크를 관리합니다.",
    "Reach out even if there is no open role.": "현재 열린 포지션이 없어도 문의해 주세요.",
    "We always welcome exceptional talent.": "NFD Korea는 뛰어난 인재를 항상 환영합니다.",
    "Position Overview": "포지션 개요",
    "Key Responsibilities": "주요 업무",
    "Required Experience and Qualifications": "필수 경험 및 자격",
    "Location": "근무지",
    "Seoul headquarters or project sites in the Seoul metro area": "서울 본사 또는 수도권 프로젝트 현장",
    "Occasional overseas travel may be required.": "필요 시 해외 출장이 있을 수 있습니다.",
    "Manage data center projects from due diligence through design development, permitting, construction and turnover": "실사부터 설계 개발, 인허가, 시공, 인계까지 데이터센터 프로젝트를 관리",
    "Manage overall project design, schedules, budgets, and risks": "프로젝트 설계, 일정, 예산, 리스크 전반 관리",
    "Oversee overall permitting processes, collaborating closely with local authorities and regulatory bodies": "지자체 및 관계 기관과 긴밀히 협업해 인허가 전 과정 관리",
    "Provide oversight of vendor selection, tender reviews, and contractor performance": "벤더 선정, 입찰 검토, 시공사 성과 관리",
    "Manage teams of engineering and technical staff, mentoring individuals and driving high performance": "엔지니어링 및 기술 인력 팀을 관리하고 멘토링하며 높은 성과를 이끌어냄",
    "Bachelor's degree in Architecture or Engineering": "건축 또는 엔지니어링 분야 학사 학위",
    "A minimum of 10 years of experience on large-scale infrastructure, commercial, industrial, or mission-critical projects such as data centers": "데이터센터 등 대규모 인프라, 상업, 산업 또는 미션 크리티컬 프로젝트 10년 이상 경험",
    "Solid project management experience and skills for handling multiple projects and stakeholder interfaces": "복수 프로젝트와 이해관계자 인터페이스를 관리할 수 있는 탄탄한 프로젝트 관리 경험과 역량",
    "Proficiency in English communication for technical discussions, documentation, and client interaction": "기술 논의, 문서 작성, 고객 커뮤니케이션을 위한 영어 소통 능력",
    "We are seeking a Senior CSA Engineer with direct experience in Civil, Structural, and Architectural design for large-scale data center facilities. This role requires a strong background in design documentation, permitting, and coordination with MEP disciplines.": "대규모 데이터센터 시설의 토목, 구조, 건축 설계 경험을 보유한 시니어 CSA 엔지니어를 찾습니다. 설계 문서화, 인허가, MEP 분야와의 조율 경험이 중요합니다.",
    "Create and manage CSA design documentation": "CSA 설계 문서 작성 및 관리",
    "Coordinate with MEP engineering disciplines for integrated design solutions": "통합 설계 솔루션을 위해 MEP 엔지니어링 분야와 조율",
    "Manage technical reviews and documentation to ensure permitting compliance": "인허가 적합성을 확보하기 위한 기술 검토 및 문서 관리",
    "Optimize designs for constructability, sustainability, and structural resilience": "시공성, 지속가능성, 구조적 복원력을 고려한 설계 최적화",
    "Conduct technical meetings and communicate effectively with international clients and partners in English": "기술 회의를 진행하고 해외 고객 및 파트너와 영어로 효과적으로 소통",
    "Bachelor's degree in Architecture, Civil, or Structural Engineering": "건축, 토목 또는 구조공학 학사 학위",
    "A minimum of 10 years of experience on large-scale infrastructure or mission-critical projects such as data centers": "데이터센터 등 대규모 인프라 또는 미션 크리티컬 프로젝트 10년 이상 경험",
    "Proven experience in CSA design and documentation for industrial or commercial facilities": "산업 또는 상업 시설의 CSA 설계 및 문서화 경험",
    "Proficiency with engineering tools (e.g., AutoCAD, Revit, Navisworks)": "엔지니어링 도구 활용 능력(AutoCAD, Revit, Navisworks 등)",
    "Strong English communication skills for technical discussions and client interaction": "기술 논의 및 고객 커뮤니케이션을 위한 영어 소통 능력",
    "Candidates must have no restrictions on international business travel": "해외 출장에 결격 사유가 없어야 합니다.",
    "We are a leading data center development company seeking a Real-estate Manager with direct experience in land acquisition and deal execution. This role requires a deep understanding of feasibility studies, development processes, and the data center industry, along with the ability to collaborate across disciplines and communicate effectively in English with global stakeholders.": "NFD Korea는 토지 매입과 거래 실행 경험을 보유한 부동산 개발 매니저를 찾고 있습니다. 사업성 검토, 개발 프로세스, 데이터센터 산업에 대한 깊은 이해와 함께 다양한 분야와 협업하고 글로벌 이해관계자와 영어로 효과적으로 소통할 수 있어야 합니다.",
    "Originate and evaluate investment opportunities in data center projects": "데이터센터 프로젝트 투자 기회 발굴 및 평가",
    "Participate in development processes including land acquisition, permitting, and setting a construction schedule from an investor's perspective": "투자자 관점에서 토지 매입, 인허가, 시공 일정 수립 등 개발 프로세스 참여",
    "Collaborate across technical, commercial, and legal teams to ensure project alignment and investment protection": "기술, 사업, 법무 팀과 협업해 프로젝트 정합성과 투자 보호 확보",
    "Prepare investment memorandum, IC presentation and on-going reports for stakeholders and debtors": "이해관계자 및 대주단을 위한 투자 메모, 투자심의 자료, 진행 보고서 작성",
    "10–15 years of experience in real estate development, with direct involvement in land acquisition and deal execution": "부동산 개발 10~15년 경력 및 토지 매입·거래 실행 직접 경험",
    "Proven track record in sourcing, structuring, and closing land or infrastructure transactions, preferably including data center or industrial projects": "토지 또는 인프라 거래 발굴, 구조화, 종결 실적. 데이터센터 또는 산업 프로젝트 경험 우대",
    "Solid understanding of feasibility analysis, permitting, zoning, and development processes": "사업성 분석, 인허가, 용도지역, 개발 프로세스에 대한 탄탄한 이해",
    "Familiarity with project financing, capital structuring, and risk management for real-estate assets": "부동산 자산의 프로젝트 파이낸싱, 자본 구조화, 리스크 관리 이해",
    "Fluent written and verbal communication skills in both Korean and English": "한국어와 영어 모두 능숙한 서면 및 구두 커뮤니케이션 능력",
    "We are seeking a Senior Mechanical & Electrical Engineer with direct experience in designing and delivering large-scale infrastructure projects. This role requires a strong background in mechanical and electrical system design, construction execution, and commissioning (Cx), along with the ability to collaborate across disciplines and communicate effectively in English with global stakeholders.": "대규모 인프라 프로젝트의 설계와 수행 경험을 보유한 시니어 기계·전기 엔지니어를 찾습니다. 기계·전기 시스템 설계, 시공 수행, 커미셔닝(Cx)에 대한 탄탄한 경험과 함께 다양한 분야와 협업하고 글로벌 이해관계자와 영어로 효과적으로 소통할 수 있어야 합니다.",
    "Design and review mechanical systems including HVAC, piping, cooling, and fire protection for data center facilities": "데이터센터 시설의 HVAC, 배관, 냉각, 소방 등 기계 시스템 설계 및 검토",
    "Design and review electrical single line drawings including GENSET, Loadbank, UPS/BATT, MV/LV ATS, containments, power supply and fire-alarm protection": "GENSET, Loadbank, UPS/BATT, MV/LV ATS, containment, 전원 공급, 화재 경보를 포함한 전기 단선도 설계 및 검토",
    "Apply BIM tools (e.g., Revit, AutoCAD) to produce and manage design documentation": "BIM 도구(Revit, AutoCAD 등)를 활용한 설계 문서 작성 및 관리",
    "Provide technical support during construction and commissioning phases": "시공 및 커미셔닝 단계의 기술 지원",
    "Lead vendor and consultant coordination to ensure design compliance and project alignment": "설계 적합성과 프로젝트 정합성 확보를 위한 벤더 및 컨설턴트 조율",
    "Understand and apply Computational Fluid Dynamics (CFD) principles to airflow, heat distribution and cooling efficiency": "공기 흐름, 열 분포, 냉각 효율에 CFD 원리를 이해하고 적용",
    "Bachelor's degree or higher in Mechanical or Electrical Engineering": "기계 또는 전기공학 학사 이상",
    "Minimum 7 years of experience in large-scale infrastructure projects such as data centers, semiconductor facilities, or clean rooms": "데이터센터, 반도체 시설, 클린룸 등 대규모 인프라 프로젝트 7년 이상 경험",
    "Direct involvement in mechanical and electrical system design and execution": "기계 및 전기 시스템 설계와 수행 직접 경험",
    "Practical experience using BIM tools such as Revit, AutoCAD, or Navisworks": "Revit, AutoCAD, Navisworks 등 BIM 도구 실무 경험",
    "Experience in project management roles (PM or CM), including scheduling, budgeting, and vendor coordination": "일정, 예산, 벤더 조율을 포함한 PM 또는 CM 역할 경험",
    "Hands-on experience in data center construction and commissioning (Cx)": "데이터센터 시공 및 커미셔닝(Cx) 실무 경험",
    "Strong English communication skills for technical discussions, documentation, and client interaction": "기술 논의, 문서 작성, 고객 커뮤니케이션을 위한 영어 소통 능력",
    "01 — Value": "01 — 가치",
    "02 — Value": "02 — 가치",
    "03 — Value": "03 — 가치",
    "04 — Value": "04 — 가치",
    "Professionals who take ownership and responsibility to achieve company goals. We seek individuals who treat every project as their own.": "회사 목표 달성을 위해 주인의식과 책임감을 갖는 전문가. 모든 프로젝트를 자신의 일처럼 대하는 인재를 찾습니다.",
    "Professionals who continuously develop their expertise through learning and experience. Growth is not optional — it's part of the job.": "학습과 경험을 통해 전문성을 지속적으로 키우는 전문가. 성장은 선택이 아니라 업무의 일부입니다.",
    "Professionals who focus on both process and results to deliver the best outcomes. We value action, discipline, and follow-through.": "과정과 결과 모두에 집중해 최상의 성과를 만드는 전문가. 실행, 원칙, 완결성을 중요하게 생각합니다.",
    "Professionals who build strong teamwork through open communication and collaboration. Together, we build more than we could alone.": "열린 소통과 협업으로 강한 팀워크를 만드는 전문가. 함께할 때 더 큰 성과를 만듭니다.",
    "Have a project in mind or facing a critical challenge? Let's connect — we bring purpose-driven solutions, guided by expertise and integrity.": "구상 중인 프로젝트가 있거나 중요한 과제를 마주하고 계신가요? 전문성과 신뢰를 바탕으로 목적에 맞는 솔루션을 함께 찾겠습니다.",
    "Address": "주소",
    "199-2 Nonhyun-dong, Gangnam-gu, Seoul": "서울특별시 강남구 논현동 199-2",
    "Connect with us →": "LinkedIn에서 연결하기 →",
    "Business Hours": "운영 시간",
    "Weekdays 09:00 - 18:00 (KST)": "평일 09:00 - 18:00 (KST)",
    "For project inquiries, investment partnerships, hiring, or general questions, our team will respond within 1-2 business days.": "프로젝트 문의, 투자 파트너십, 채용, 일반 문의에 대해 영업일 기준 1~2일 이내에 답변드리겠습니다.",
    "Full Name *": "이름 *",
    "Your name": "이름",
    "회사 name (optional)": "회사명(선택)",
    "Email *": "이메일 *",
    "Phone": "연락처",
    "Inquiry Type *": "문의 유형 *",
    "Please select": "선택해 주세요",
    "데이터센터 개발 Consulting": "데이터센터 개발 컨설팅",
    "설계 엔지니어링 Consulting": "설계 엔지니어링 컨설팅",
    "Colocation and 운영 관리": "코로케이션 및 운영 관리",
    "Investment Partnership": "투자 파트너십",
    "채용 Inquiry": "채용 문의",
    "Other": "기타",
    "Project Scale / Scope": "프로젝트 규모 / 범위",
    "Example: 40MW IDC development (optional)": "예: 40MW IDC 개발(선택)",
    "Message *": "문의 내용 *",
    "Please share your inquiry in detail.": "문의 내용을 자세히 작성해 주세요.",
    "Send Inquiry →": "문의 보내기 →",
    "Thank you. Our team will contact you shortly.": "감사합니다. 담당자가 곧 연락드리겠습니다.",
    "We could not send your inquiry. Please try again or email enquiry@nfd.kr.": "문의 전송에 실패했습니다. 다시 시도하시거나 enquiry@nfd.kr로 이메일을 보내주세요.",
    "Submission failed: ": "전송 실패: ",
    "General Inquiry": "일반 문의",
    "* Required fields": "* 필수 입력 항목",
    "뉴스 & Insights": "뉴스 & 인사이트",
    "Latest 뉴스": "최신 뉴스",
    "Recent updates": "최근 소식",
    "Jul 25, 2025": "2025년 7월 25일",
    "Sep 24, 2025": "2025년 9월 24일",
    "An update on new strategic partnerships and the kickoff of additional large-scale data center developments.": "새로운 전략적 파트너십과 추가 대규모 데이터센터 개발 착수 소식입니다.",
    "NFD Korea continues to grow as a trusted business partner in data center development and operations consulting, backed by technical expertise and practical execution.": "NFD Korea는 기술 전문성과 실질적인 실행력을 바탕으로 데이터센터 개발 및 운영 컨설팅 분야의 신뢰받는 비즈니스 파트너로 성장하고 있습니다.",
    "Large-scale hyperscale programs including Yongin Deokseong-ri IDC, Ansan IDC, and Dangjin IDC are progressing steadily. In particular, Yongin Deokseong-ri IDC is setting a new benchmark in the domestic market with 80MW of incoming power capacity and a high-efficiency PUE of 1.33.": "용인 덕성리 IDC, 안산 IDC, 당진 IDC 등 대규모 하이퍼스케일 프로그램이 안정적으로 진행되고 있습니다. 특히 용인 덕성리 IDC는 80MW 수전 용량과 PUE 1.33의 고효율 성능으로 국내 시장의 새로운 기준을 제시하고 있습니다.",
    "Interest from global CSPs remains strong, and collaboration with major domestic and international telecom operators continues to expand. NFD Korea will keep creating stronger outcomes and new opportunities through close partnership with clients and stakeholders.": "글로벌 CSP의 관심은 계속 높게 유지되고 있으며, 국내외 주요 통신사와의 협력도 확대되고 있습니다. NFD Korea는 고객 및 이해관계자와의 긴밀한 파트너십을 통해 더 강한 성과와 새로운 기회를 만들어가겠습니다.",
    "NFD Korea has strengthened its global network through a new partnership with a Taiwan-based IDC developer. This collaboration is expected to expand the company's presence across the Asia-Pacific data center development market.": "NFD Korea는 대만 기반 IDC 개발사와의 새로운 파트너십을 통해 글로벌 네트워크를 강화했습니다. 이번 협력은 아시아태평양 데이터센터 개발 시장에서 회사의 입지를 확대하는 계기가 될 것으로 기대됩니다.",
    "The first 200MW phase and second 100MW phase of Dangjin Songsan IDC have also officially moved forward. With a combined scale of 300MW, the program is planned as one of Korea's largest hyperscale data center campuses, designed to meet growing demand from global cloud service providers.": "당진 송산 IDC의 1단계 200MW와 2단계 100MW도 공식적으로 추진되고 있습니다. 총 300MW 규모의 이 프로그램은 글로벌 클라우드 서비스 제공자의 증가하는 수요에 대응하기 위한 국내 최대급 하이퍼스케일 데이터센터 캠퍼스로 계획되고 있습니다.",
    "Supported by its proprietary liquid cooling design capability, NFD Korea will continue delivering data center solutions optimized for high-density AI computing environments and help clients build resilient digital infrastructure through ongoing technical innovation.": "자체 액체냉각 설계 역량을 기반으로 NFD Korea는 고밀도 AI 컴퓨팅 환경에 최적화된 데이터센터 솔루션을 지속적으로 제공하고, 꾸준한 기술 혁신을 통해 고객의 견고한 디지털 인프라 구축을 지원하겠습니다.",
    "The latest updates from NFD Korea, along with perspective on the evolving data center industry.": "NFD Korea의 최신 소식과 변화하는 데이터센터 산업에 대한 인사이트를 전합니다.",
    "NFD Korea project development update": "NFD Korea 프로젝트 개발 현황 업데이트",
    "Read the latest progress across NFD Korea's data center development programs and current project milestones.": "NFD Korea의 데이터센터 개발 프로그램과 주요 프로젝트 마일스톤의 최신 진행 상황을 확인하세요.",
    "NFD Korea expands partnerships and launches new projects": "NFD Korea, 파트너십 확대 및 신규 프로젝트 착수",
    "A major update on active data center developments and current project milestones at NFD Korea.": "NFD Korea가 진행 중인 데이터센터 개발과 현재 프로젝트 마일스톤에 대한 주요 업데이트입니다.",
    "An update on broader global partnerships and the start of additional strategic data center developments.": "글로벌 파트너십 확대와 추가 전략적 데이터센터 개발 착수에 대한 소식입니다.",
    "We place our clients' value and business success first, delivering optimal strategies and solutions tailored to the data center industry. In a rapidly evolving digital infrastructure environment, we offer practical answers to the complex challenges faced by investors and clients.": "고객의 가치와 사업 성공을 최우선으로 생각하며 데이터센터 산업에 특화된 최적의 전략과 솔루션을 제공합니다. 빠르게 변화하는 디지털 인프라 환경에서 투자자와 고객이 마주한 복잡한 과제에 실질적인 해답을 제시합니다.",
    "Company launch and first major platform": "회사 출범 및 첫 주요 플랫폼 구축",
    "Company name (optional)": "회사명(선택)",
    "Backed by accumulated experience and a global network,": "축적된 경험과 글로벌 네트워크를 바탕으로",
    "Value": "가치",
    "Insights": "인사이트",
    "Learn More →": "자세히 보기 →",
    "STEP 01": "1단계",
    "STEP 02": "2단계",
    "STEP 03": "3단계",
    "STEP 04": "4단계",
    "Operations": "운영",
    "3 Core Development Services": "3대 핵심 개발 서비스",
    "Want to learn more about Development Consulting?": "개발 컨설팅이 더 궁금하신가요?",
    "Tenant-Tailored Services": "임차사 맞춤 서비스",
    "3 Core Operations Services": "3대 핵심 운영 서비스",
    "Data center-specific architectural planning and structural review. We provide comprehensive support including space planning that reflects operational efficiency and scalability, as well as fire safety and security circulation design.": "데이터센터에 특화된 건축 계획과 구조 검토를 수행합니다. 운영 효율과 확장성을 반영한 공간 계획은 물론 소방 안전과 보안 동선 설계까지 종합적으로 지원합니다.",
    "We operate an integrated management system covering electrical, mechanical, fire safety, security, and communications infrastructure. Dedicated specialists monitor facility status in real time and carry out maintenance across all disciplines.": "전기, 기계, 소방, 보안, 통신 인프라를 포괄하는 통합 관리 체계를 운영합니다. 전담 전문가가 시설 상태를 실시간으로 모니터링하고 분야별 유지보수를 수행합니다.",
    "We continuously analyze power, cooling, and space capacity to proactively respond to shifts in tenant demand. Through disciplined capacity planning and optimization, we sustain operational efficiency at all times.": "전력, 냉각, 공간 용량을 지속적으로 분석해 임차사 수요 변화에 선제적으로 대응합니다. 체계적인 용량 계획과 최적화를 통해 항상 운영 효율을 유지합니다.",
    "3 Core PM Strengths": "3대 핵심 PM 강점",
    "Cost estimation and budget planning": "공사비 산정 및 예산 계획",
    "Recruitment Inquiry": "채용 문의",
    "Careers Inquiry": "채용 문의",
    "News &amp; Insights": "뉴스 &amp; 인사이트",
    "News & Insights": "뉴스 & 인사이트",
    "Latest News": "최신 뉴스",
    "Advisory Projects": "자문 프로젝트",
    "04 — Operations Leasing": "04 — 운영 및 임대",
    "Operations Management Services.": "운영 관리 서비스.",
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
    text = re.sub(r"((?:img|image|src)\s*:\s*['\"])images/", r"\1../images/", text)
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
