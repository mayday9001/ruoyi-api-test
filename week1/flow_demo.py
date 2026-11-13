# -*- coding: utf-8 -*-
"""
week1/flow_demo.py
第一个完整的接口测试脚本：创建 → 查询 → 更新 → 删除 → 验证删除

特点：
  1. 数据唯一（时间戳命名）→ 可以重复运行
  2. try/finally 清理 → 不留垃圾数据
  3. 每步三层断言 → 失败时能定位
  4. 支持跑多遍，验证可重复性

运行：python flow_demo.py
"""
import time

import requests

# 本地 mock 服务（mock_api.py，启动后监听 8000）
# 换回公网时改成 "https://api.restful-api.dev" 即可
BASE = "http://127.0.0.1:8000"
TIMEOUT = (5, 30)


def unique_name(prefix="flow"):
    """用毫秒时间戳造唯一名字，保证脚本可重复运行"""
    return f"{prefix}-{int(time.time() * 1000)}"


# ==========================================================
# 用例 1：创建
# ==========================================================
def test_create(name, data):
    print(f"\n[1] 创建：{name}")
    payload = {"name": name, "data": data}
    resp = requests.post(f"{BASE}/objects", json=payload, timeout=TIMEOUT)

    # ① HTTP 层
    assert resp.status_code in (200, 201), \
        f"创建失败: {resp.status_code} {resp.text[:200]}"

    body = resp.json()

    # ② 结构层
    assert "id" in body, f"响应缺少 id: {body}"
    assert isinstance(body["id"], str), f"id 类型错误: {type(body['id'])}"
    assert body["id"] != "", "id 为空"

    # ③ 数据层（自己造的数据，可以断等于）
    assert body["name"] == name, f"name 不符: 期望 {name}，实际 {body.get('name')}"
    assert body["data"]["price"] == data["price"], \
        f"price 不符: 期望 {data['price']}，实际 {body.get('data', {}).get('price')}"

    print(f"    ✓ 创建成功 id={body['id']}")
    return body["id"]


# ==========================================================
# 用例 2：查询
# ==========================================================
def test_get(object_id, expect_name):
    print(f"[2] 查询：{object_id}")
    resp = requests.get(f"{BASE}/objects/{object_id}", timeout=TIMEOUT)

    assert resp.status_code == 200, \
        f"查询失败: {resp.status_code} {resp.text[:200]}"

    body = resp.json()
    assert str(body["id"]) == str(object_id), \
        f"id 不一致: 请求 {object_id}，返回 {body.get('id')}"
    assert body["name"] == expect_name, \
        f"name 不一致: 期望 {expect_name}，实际 {body.get('name')}"

    print(f"    ✓ 查询成功 name={body['name']}")
    return body


# ==========================================================
# 用例 3：更新（PUT 全量）
# ==========================================================
def test_update(object_id, new_name, new_price):
    print(f"[3] 更新：{object_id}")
    payload = {
        "name": new_name,
        "data": {
            "price": new_price,
            "color": "蓝色",
            "owner": "mayday9001",
        },
    }
    resp = requests.put(f"{BASE}/objects/{object_id}", json=payload, timeout=TIMEOUT)

    assert resp.status_code == 200, \
        f"更新失败: {resp.status_code} {resp.text[:200]}"

    body = resp.json()
    assert body["name"] == new_name, f"更新未生效: {body.get('name')}"
    assert body["data"]["price"] == new_price, \
        f"price 未生效: {body.get('data', {}).get('price')}"

    print(f"    ✓ 更新成功 name={body['name']} price={body['data']['price']}")
    return body


# ==========================================================
# 用例 4：删除 + 验证删除
# ==========================================================
def test_delete(object_id):
    print(f"[4] 删除：{object_id}")
    resp = requests.delete(f"{BASE}/objects/{object_id}", timeout=TIMEOUT)

    # 200 和 204 都算成功（具体哪个取决于实现，已记入接口清单）
    assert resp.status_code in (200, 204), \
        f"删除失败: {resp.status_code} {resp.text[:200]}"

    # ★ 关键：删完必须再查一次，证明真的删了
    check = requests.get(f"{BASE}/objects/{object_id}", timeout=TIMEOUT)
    assert check.status_code == 404, \
        f"删除后仍能查到 id={object_id}，实际状态码 {check.status_code}"

    print(f"    ✓ 删除成功，验证查询返回 404")


# ==========================================================
# 一条完整链路
# ==========================================================
def run_flow(round_no):
    """跑一遍完整流程，返回是否成功"""
    name = unique_name(f"flow-r{round_no}")
    new_name = name + "-已更新"

    object_id = None
    try:
        object_id = test_create(name, {"price": 88, "color": "黑色", "owner": "mayday9001"})
        test_get(object_id, name)
        test_update(object_id, new_name, 199)
        test_get(object_id, new_name)          # 更新后再查一次，确认落库
        test_delete(object_id)
        object_id = None                        # 已删，finally 不用再删
        return True
    except AssertionError as e:
        print(f"    ✗ 失败: {e}")
        return False
    finally:
        if object_id:
            print(f"    🧹 清理残留 id={object_id}")
            try:
                requests.delete(f"{BASE}/objects/{object_id}", timeout=TIMEOUT)
            except Exception:
                pass


# ==========================================================
# 幂等性探针：同一请求连发 3 次
# ==========================================================
def idempotency_probe():
    print("\n" + "=" * 60)
    print("幂等性探针：同一个创建请求连发 3 次")
    print("=" * 60)

    payload = {"name": unique_name("idem"), "data": {"price": 1, "owner": "mayday9001"}}
    ids = []
    try:
        for i in range(1, 4):
            resp = requests.post(f"{BASE}/objects", json=payload, timeout=TIMEOUT)
            assert resp.status_code in (200, 201), f"第 {i} 次创建失败: {resp.status_code}"
            oid = resp.json()["id"]
            ids.append(oid)
            print(f"  第 {i} 次 → id={oid}")

        print(f"\n  3 次返回的 id: {ids}")
        if len(set(ids)) == 3:
            print("  ✅ 3 个不同 id → POST 不幂等（符合 HTTP 规范，每次都是新资源）")
        else:
            print("  ⚠️ 出现重复 id → 后端做了去重，POST 表现为幂等（加分设计）")

    finally:
        for oid in ids:
            try:
                requests.delete(f"{BASE}/objects/{oid}", timeout=TIMEOUT)
            except Exception:
                pass
        if ids:
            print(f"  🧹 已清理 {len(ids)} 条探针数据")


# ==========================================================
# 入口
# ==========================================================
if __name__ == "__main__":
    rounds = 3
    results = []

    print("=" * 60)
    print(f"开始执行：连续跑 {rounds} 遍完整流程（验证可重复性）")
    print("=" * 60)

    for i in range(1, rounds + 1):
        print(f"\n{'=' * 60}\n第 {i} / {rounds} 遍\n{'=' * 60}")
        ok = run_flow(i)
        results.append(ok)

    print("\n" + "=" * 60)
    print("执行结果汇总")
    print("=" * 60)
    for i, ok in enumerate(results, start=1):
        print(f"  第 {i} 遍：{'PASS ✅' if ok else 'FAIL ❌'}")
    print(f"\n  通过率：{sum(results)}/{rounds}")

    # 全部通过才做幂等性探针（否则先修问题）
    if all(results):
        idempotency_probe()

    print("\n全部结束。")