# Playwright E2E Test Automation Framework

**Playwright · pytest · POM 4-Layer · Allure · GitHub Actions** 기반 웹 E2E 자동화 프레임워크.

> 실서비스(OTT) 규모에서 운영하던 E2E 프레임워크의 **공개 데모**  포트폴리오 프로젝트입니다. 로그인 → 상품 → 장바구니 → 체크아웃 핵심 플로우를 다룹니다.

<br>

## 아키텍처 (4-Layer)

```
locators → pages → flows → tests
 (요소 위치)  (페이지 동작)  (비즈니스 로직)  (테스트 케이스)
```

| Layer | 책임 | 금지 |
|-------|------|------|
| `locators/` | CSS/data-test 셀렉터 정의만 | Playwright 호출 금지 |
| `pages/` | 페이지 단위 동작 (`BasePage` 상속) | 비즈니스 로직 금지 |
| `flows/` | 여러 Page 조합 (로그인·체크아웃) | assertion 금지 |
| `tests/` | AAA 패턴 · assertion | selector 직접 작성 금지 |

<br>

## 설치 & 실행

```bash
uv sync
uv run playwright install chromium

uv run pytest tests/ -v                 # 전체
uv run pytest tests/ -m p0 -v           # 핵심 경로만
uv run pytest tests/ -n 3 -v            # xdist 병렬
uv run pytest tests/ --headed-mode -v   # 브라우저 표시(디버깅)
```

<br>

## 리포트 (Allure)

```bash
uv run pytest tests/ --alluredir=allure-results
allure serve allure-results            # 로컬 확인
```

CI(`.github/workflows/e2e.yml`)가 매 실행마다 Allure 리포트를 생성해 **GitHub Pages(`gh-pages`)에 자동 배포**합니다. → 라이브 대시보드로 결과·트렌드를 확인.

<br>

## 설계 원칙

- **테스트 독립성** — 매 테스트마다 새 browser context 로 상태 격리
- **Locator는 `data-test` 우선** — UI 변경에 강하게
- **AAA(Arrange-Act-Assert)** 구조 일관 적용
- **실패 시 전체 화면 스크린샷 → Allure 첨부** (진단 보조)
- **마커 기반 우선순위** (`p0`/`p1`), flaky 격리(`quarantine`)

<br>

## 라이브 리포트

> CI 1회 실행 후 활성화: `https://<github-id>.github.io/playwright-e2e-framework/`
