# -*- coding: utf-8 -*-
"""booking 接口用例：查询 / 单个查询 / 创建 / 更新 / 删除"""
import requests


def test_list_objects(base_url):
    """① 查询全部"""
    resp = requests.get(f"{base_url}/objects", timeout=5)

    # 断言 1：状态码
    assert resp.status_code == 200

    # 断言 2：关键字段（结构）
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 3
    item = body[0]
    assert set(item) >= {"id", "name", "data", "createdAt"}

    # 断言 3：字段类型
    assert isinstance(item["id"], str)
    assert isinstance(item["name"], str)
    assert isinstance(item["createdAt"], int)


def test_get_one_object(base_url):
    """② 单个查询"""
    # ① 准备：从列表里挑一个真实存在的 id（不自己造，因为预置的 3 条一定在）
    listing = requests.get(f"{base_url}/objects", timeout=5).json()
    oid = listing[0]["id"]

    # ② 发请求
    resp = requests.get(f"{base_url}/objects/{oid}", timeout=5)

    # ③ 断言
    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == oid
    assert set(body) >= {"id", "name", "data", "createdAt"}

    assert isinstance(body["name"], str)
    assert isinstance(body["createdAt"], int)

def test_create_object(base_url):
    """③ 创建"""
    # ① 准备：请求体写成变量，后面断言要拿它比对
    payload = {"name": "测试机", "data": {"price": 1}}

    # ② 发请求
    resp = requests.post(f"{base_url}/objects", json=payload, timeout=5)

    # ③ 断言
    assert resp.status_code == 200          # 注意：mock_api 创建成功返回 200，不是 201

    body = resp.json()
    assert body["name"] == payload["name"]  # 回显一致
    assert body["data"] == payload["data"]
    assert "id" in body                     # 服务端生成了 id

    assert isinstance(body["id"], str)
    assert len(body["id"]) == 32            # mock_api 用 uuid4().hex，固定 32 位
    assert isinstance(body["createdAt"], int)

    # ④ 清理
    requests.delete(f"{base_url}/objects/{body['id']}", timeout=5)

def test_update_object(base_url):
    """④ 更新（PUT 全量替换）"""
    # ① 准备：先造一个带 data 的对象
    created = requests.post(
        f"{base_url}/objects",
        json={"name": "旧名字", "data": {"price": 1}},
        timeout=5,
    ).json()
    oid = created["id"]

    # ② 发请求：只传 name，故意不传 data
    resp = requests.put(f"{base_url}/objects/{oid}", json={"name": "新名字"}, timeout=5)

    # ③ 断言
    assert resp.status_code == 200

    body = resp.json()
    assert body["id"] == oid
    assert body["name"] == "新名字"
    assert body["data"] is None             # ★ 关键：PUT 把没传的 data 抹成 null
    assert isinstance(body["name"], str)

    # ④ 清理
    requests.delete(f"{base_url}/objects/{oid}", timeout=5)

def test_delete_object(base_url):
    """⑤ 删除"""
    # ① 准备
    created = requests.post(
        f"{base_url}/objects",
        json={"name": "待删除", "data": None},
        timeout=5,
    ).json()
    oid = created["id"]

    # ② 发请求
    resp = requests.delete(f"{base_url}/objects/{oid}", timeout=5)

    # ③ 断言（前半：删除本身的响应）
    assert resp.status_code == 200

    body = resp.json()
    assert oid in body["message"]           # 提示信息里带 id
    assert isinstance(body["message"], str)

    # ③ 断言（后半：★ 二次验证，删完必须查不到）
    after = requests.get(f"{base_url}/objects/{oid}", timeout=5)
    assert after.status_code == 404