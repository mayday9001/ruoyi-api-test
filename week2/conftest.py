# -*- coding: utf-8 -*-
"""
conftest.py —— pytest 自动加载的共享配置文件

放在这个目录下，本目录及子目录的所有测试文件都能直接用里面的 fixture，
不需要 import。
"""
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def base_url():
    """被测系统地址"""
    return BASE_URL


@pytest.fixture(scope="session")
def session():
    """整个 pytest 会话复用一个 requests.Session"""
    s = requests.Session()
    s.headers.update({"User-Agent": "mayday-api-test/1.0"})
    print("\n  [session] 创建 Session")
    yield s
    s.close()
    print("  [session] 关闭 Session")


@pytest.fixture(scope="module")
def objects(session, base_url):
    """整个文件只请求一次列表，多个用例共用这份数据"""
    print("\n  [objects] 发起请求 GET /objects")
    resp = session.get(f"{base_url}/objects", timeout=(5, 30))
    assert resp.status_code == 200, f"列表查询失败: {resp.status_code}"
    return resp.json()