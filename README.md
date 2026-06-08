# Playwright E2E Test Automation Framework

**Playwright · pytest · POM 4-Layer · Allure · GitHub Actions** 기반 웹 E2E 자동화 프레임워크 + **커스텀 리포트 대시보드**.

> OTT 규모 서비스에서 운영하던 E2E 자동화의 **공개 데모** 포트폴리오 프로젝트입니다. (회사 코드·데이터 미포함 — 전부 새로 작성)

🔗 **Live demo**: `https://duo2208.github.io/playwright-e2e-framework/` *(CI + Pages 활성화 후)*

<br>

## ✨ 핵심 특징

- **4-Layer POM** — `locators → pages → flows → tests` 계층 분리로 UI 변경에 강한 구조
- **커스텀 리포트 대시보드** — 기본 Allure 위에 직접 만든 5개 페이지(요약·실패 로그·추이·타임라인·테스트 케이스)
- **AI 진단 정확도 추적** — 실패 자동 분류(Locator drift / Timing / API contract / Environment)와 예측 적중률 시각화
- **CI/CD 자동 배포** — GitHub Actions → Allure 생성 → GitHub Pages 자동 게시 (일 1회 cron)
- **운영 관점** — 5-state(PASS/FAIL/BROKEN/SKIP) · flaky 격리(quarantine) · xdist 병렬 · 워커별 타임라인

> ⚠️ 리포트 대시보드의 실패/추이/정확도는 **프레임워크 시연용 Sample 데이터**입니다(각 페이지에 표기). 실제 E2E 테스트는 saucedemo 대상으로 CI에서 검증됩니다.

<br>

## 🗂️ 커스텀 리포트 (5개 페이지)

| 페이지 | 내용 |
|--------|------|
| **요약** | 통과율 도넛 · 5-state 카드 · 런/CPU/병렬도 메트릭 · 우선순위 점검 · 가장 느린 테스트 · 점검 영역(그룹별 통과율) |
| **실패 로그** | master-detail 2-pane (좌 목록 / 우 상세) · 스텝 표 · AI 진단 노트 · 에러 트레이스 |
| **추이** | 🧠 AI 진단 정확도(대분류/세부/권장조치 적중률 + sparkline + 혼동 Top3) · fail 추세 · 격리 후보 · Fail 빈도 Top10 |
| **타임라인** | 워커별(gw0~N) 실행 Gantt 차트 |
| **테스트 케이스** | 상태·그룹별 필터 + 전체 목록 |

<br>

## 🏗️ 아키텍처 (4-Layer)

```
locators → pages → flows → tests
 (요소 위치)  (페이지 동작)  (비즈니스 로직)  (테스트 케이스)
```

| Layer | 책임 | 금지 |
|-------|------|------|
| `locators/` | CSS/`data-test` 셀렉터 정의만 | Playwright 호출 금지 |
| `pages/` | 페이지 단위 동작 (`BasePage` 상속) | 비즈니스 로직 금지 |
| `flows/` | 여러 Page 조합 (로그인·체크아웃) | assertion 금지 |
| `tests/` | AAA 패턴 · assertion | selector 직접 작성 금지 |

<br>

## 🚀 설치 & 실행

```bash
uv sync
uv run playwright install chromium

uv run pytest tests/ -v                 # 전체
uv run pytest tests/ -m p0 -v           # 핵심 경로만 (P0)
uv run pytest tests/ -n 3 -v            # xdist 병렬
uv run pytest tests/ --headed-mode -v   # 브라우저 표시(디버깅)
```

<br>

## 📊 리포트 생성

```bash
# 실제 테스트 결과로
uv run pytest tests/ --alluredir=allure-results
allure serve allure-results

# 시연용 대시보드 (Sample 데이터 — 커스텀 5개 페이지 전체)
python scripts/seed_mock_data.py mock-results
allure generate mock-results --clean -o allure-report
python scripts/apply_branding.py allure-report mock-results   # 브랜딩 + 커스텀 페이지 주입
allure open allure-report
```

CI(`.github/workflows/e2e.yml`)가 매 실행마다 리포트를 생성해 **GitHub Pages(`gh-pages`)에 자동 배포**합니다.

<br>

## 📁 디렉토리

```
config/         환경 설정 (base.yml) + Allure 브랜딩 (custom-logo/)
locators/ pages/ flows/   4-Layer (요소·동작·비즈니스 로직)
tests/          test_*.py + conftest.py (브라우저 fixture·실패 스크린샷·Allure 메타)
scripts/
  ├─ generate_report.py   커스텀 멀티 페이지 리포트 생성기
  ├─ apply_branding.py     Allure 브랜딩 + 사이드바·리다이렉트 주입
  └─ seed_mock_data.py     시연용 Sample 데이터 생성
.github/workflows/e2e.yml  CI: pytest → Allure → GitHub Pages 배포
```

<br>

## 🧭 설계 원칙

- **테스트 독립성** — 매 테스트마다 새 browser context 로 상태 격리
- **Locator는 `data-test` 우선** — UI 변경에 강하게
- **AAA(Arrange-Act-Assert)** 구조 일관 적용
- **실패 시 전체 화면 스크린샷 → Allure 첨부** (진단 보조)
- **5-state 분류 + 마커 기반 우선순위**(`p0`/`p1`) · flaky 격리(`quarantine`)
- **무엇을 자동화하지 *않을지*** 판단 — 유지보수 가능한 범위 우선
