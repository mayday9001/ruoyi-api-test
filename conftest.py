# -*- coding: utf-8 -*-
"""全局 fixture：所有测试目录共用"""
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def base_url():
    """服务地址：改环境只改这一行"""
    return BASE_URL


@pytest.fixture(scope="session")
def token(base_url):
    """登录一次，整个测试会话共用这个 token"""
    resp = requests.post(
        f"{base_url}/auth",
        json={"username": "admin", "password": "admin123"},
        timeout=5,
    )
    assert resp.status_code == 200, f"登录失败: {resp.status_code} {resp.text}"
    return resp.json()["token"]