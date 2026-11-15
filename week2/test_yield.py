# -*- coding: utf-8 -*-
"""
yield fixture：前置造数据，后置清数据
"""
import pytest


@pytest.fixture
def created_object(session, base_url):
    """创建一条数据，用例跑完自动删掉"""
    resp = session.post(
        f"{base_url}/objects",
        json={"name": "fixture-test", "data": {"price": 1, "owner": "mayday9001"}},
        timeout=(5, 30),
    )
    assert resp.status_code == 200, f"创建失败: {resp.status_code}"
    oid = resp.json()["id"]
    print(f"\n    [前置] 创建了 {oid}")

    yield oid

    resp = session.delete(f"{base_url}/objects/{oid}", timeout=(5, 30))
    print(f"    [后置] 清理 {oid}，状态码 {resp.status_code}")


def test_created_can_query(created_object, session, base_url):
    """用例1：创建出来的对象能查到"""
    resp = session.get(f"{base_url}/objects/{created_object}", timeout=(5, 30))
    assert resp.status_code == 200
    assert resp.json()["name"] == "fixture-test"
    print("    → 查询通过")


def test_created_can_update(created_object, session, base_url):
    """用例2：能被更新"""
    resp = session.put(
        f"{base_url}/objects/{created_object}",
        json={"name": "反正改一下", "data": {"price": 2, "owner": "mayday9001"}},
        timeout=(5, 30),
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "反正改一下"
    print("    → 更新通过")