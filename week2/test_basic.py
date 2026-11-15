# -*- coding: utf-8 -*-
"""
week2/test_basic.py —— 第一个 pytest 用例集

运行方式：
    pytest                              # 跑全部
    pytest -v                           # 显示每个用例名
    pytest -s                           # 显示 print 输出
    pytest -k "ping"                    # 只跑名字含 ping 的
    pytest test_basic.py::test_ping     # 只跑这一个函数
"""
import requests

BASE = "http://127.0.0.1:8000"


def test_ping():
    """用例1：健康检查"""
    resp = requests.get(f"{BASE}/ping", timeout=(5, 30))
    assert resp.status_code == 200, f"状态码异常: {resp.status_code}"
    assert resp.json()["status"] == "ok"


def test_get_objects():
    """用例2：查询列表"""
    resp = requests.get(f"{BASE}/objects", timeout=(5, 30))
    assert resp.status_code == 200

    body = resp.json()
    assert isinstance(body, list), f"返回应为列表，实际 {type(body)}"
    assert len(body) >= 3, f"预置数据不足，实际 {len(body)} 条"


def test_assert_rewrite():
    """用例3：演示 pytest 的 assert 重写"""
    user = {"name": "mayday", "age": 20, "roles": ["admin"]}

    assert user["age"] == 20
    assert "name" in user
    assert len(user["roles"]) == 1
    body = {"rows": [{"id": 1}, {"id": 2}]}
    assert len(body["rows"]) == 2

