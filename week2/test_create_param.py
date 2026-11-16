# -*- coding: utf-8 -*-
"""
参数化实战：POST /objects 多组数据，1 个函数覆盖 5 条用例

对照 W1 的 flow_demo.py：那边是"脚本跑一遍"，这边是"5 条独立用例 + 报告"。
跑法：
    pytest test_create_param.py -v
"""
import json
import os

import pytest

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

with open(os.path.join(DATA_DIR, "create_cases.json"), encoding="utf-8") as f:
    CREATE_CASES = json.load(f)


@pytest.fixture
def cleanup_created(session, base_url):
    """记录本用例创建出来的 id，用例结束统一删掉，避免污染数据"""
    created = []
    yield created
    for oid in created:
        session.delete(f"{base_url}/objects/{oid}", timeout=(5, 30))


@pytest.mark.parametrize(
    "case",
    CREATE_CASES,
    ids=[c["desc"] for c in CREATE_CASES],
)
def test_create_object(case, session, base_url, cleanup_created):
    resp = session.post(f"{base_url}/objects", json=case["payload"], timeout=(5, 30))

    # 1) 状态码
    assert resp.status_code == case["expect_status"], (
        f"[{case['desc']}] 期望 {case['expect_status']}，实际 {resp.status_code}，响应 {resp.text}"
    )

    body = resp.json()

    # 2) 负例：只校验错误信息，不往下走了
    if case["expect_status"] != 200:
        assert "error" in body
        return

    # 3) 正例：字段值 + 字段类型 + 服务端补充字段
    assert body["name"] == case["expect_name"]
    assert isinstance(body["id"], str) and len(body["id"]) == 32
    assert isinstance(body["createdAt"], int) and body["createdAt"] > 0
    # data 传什么回来什么（传 null 回来也是 null）
    assert body["data"] == case["payload"].get("data")

    # 4) 创建后能查到 —— 这才是"真的创建成功了"
    created_id = body["id"]
    cleanup_created.append(created_id)
    got = session.get(f"{base_url}/objects/{created_id}", timeout=(5, 30))
    assert got.status_code == 200
    assert got.json()["name"] == case["expect_name"]
