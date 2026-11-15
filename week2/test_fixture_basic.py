# -*- coding: utf-8 -*-
"""
fixture 入门：用参数名"注入"依赖
"""


def test_objects_count(objects):
    """objects 是 fixture 名，pytest 自动把它的返回值传进来"""
    print(f"  拿到了 {len(objects)} 条数据")
    assert len(objects) >= 3


def test_objects_id_type(objects):
    print("  再验一次字段类型")
    for o in objects:
        assert isinstance(o["id"], str)


def test_ping(session, base_url):
    resp = session.get(f"{base_url}/ping", timeout=(5, 30))
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"