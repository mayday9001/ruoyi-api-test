# -*- coding: utf-8 -*-
"""
scope 实验：观察每个 fixture 被执行几次
必须用 -s 才能看到 print
"""
import pytest


@pytest.fixture(scope="function")
def f_func():
    print("\n    【function 创建】")
    yield "function值"
    print("    【function 销毁】")


@pytest.fixture(scope="module")
def f_module():
    print("\n    【module 创建】")
    yield "module值"
    print("    【module 销毁】")


@pytest.fixture(scope="session")
def f_session():
    print("\n    【session 创建】")
    yield "session值"
    print("    【session 销毁】")


def test_a(f_func, f_module, f_session):
    print("  → 用例 test_a 执行")


def test_b(f_func, f_module, f_session):
    print("  → 用例 test_b 执行")


class TestGroup:
    def test_c(self, f_func, f_module, f_session):
        print("  → 用例 test_c 执行")

    def test_d(self, f_func, f_module, f_session):
        print("  → 用例 test_d 执行")