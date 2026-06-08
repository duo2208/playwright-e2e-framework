"""장바구니 — 상품 담기/배지 수량(P0)."""
from __future__ import annotations

import allure
import pytest

from flows.auth_flow import login_as


@allure.feature("장바구니")
class TestCart:
    @pytest.mark.p0
    @allure.title("상품 담기 → 장바구니 배지 수량 1 증가")
    def test_add_to_cart_updates_badge(self, page, config):
        # Arrange
        user = config["users"]["standard"]
        inventory = login_as(
            page,
            base_url=config["base_url"],
            timeout=config["default_wait_timeout"],
            username=user["username"],
            password=user["password"],
        )
        assert inventory.cart_count() == 0
        # Act
        inventory.add_backpack_to_cart()
        # Assert
        assert inventory.cart_count() == 1
