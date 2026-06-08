"""pytest 전역 설정 — 브라우저 fixture · 실패 시 스크린샷 → Allure 첨부.

테스트 독립성: 매 테스트마다 새 browser context 로 상태를 격리한다.
"""
from __future__ import annotations

import allure
import pytest
from playwright.sync_api import Page, sync_playwright

from utils.config import load_config


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headed-mode", action="store_true", default=False, help="브라우저 화면 표시(디버깅용)"
    )


@pytest.fixture(scope="session")
def config() -> dict:
    return load_config()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    """각 단계 결과를 item 에 저장 — fixture teardown 에서 실패 여부 판단용."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def page(request: pytest.FixtureRequest, config: dict) -> Page:
    headed = request.config.getoption("--headed-mode")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not headed)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(config["default_wait_timeout"])
        try:
            yield page
        finally:
            report = getattr(request.node, "rep_call", None)
            if report is not None and report.failed:
                _attach_failure_screenshot(page, request.node.name)
            context.close()
            browser.close()


def _attach_failure_screenshot(page: Page, test_name: str) -> None:
    """실패 시 전체 화면 스크린샷을 Allure 에 첨부. (진단 보조라 실패해도 무시)"""
    try:
        screenshot = page.screenshot(full_page=True)
        allure.attach(
            screenshot, name=f"failure-{test_name}", attachment_type=allure.attachment_type.PNG
        )
    except Exception as error:
        print(f"[screenshot skip] {type(error).__name__}: {error}")
