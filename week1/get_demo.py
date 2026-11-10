"""
week1/get_demo.py
requests 发 GET 请求 + 三层断言

运行：python get_demo.py
"""
import requests

BASE_URL = "https://api.restful-api.dev"

response = requests.get(f"{BASE_URL}/objects",timeout=(10,30))
print(response.text)


def test_get_list():
    """用例 1：查列表 —— 验状态码、类型、数量、字段"""
    resp = requests.get(f"{BASE_URL}/objects", timeout=(10,30))

    # 第 1 层：HTTP
    assert resp.status_code == 200, f"状态码应为 200，实际 {resp.status_code}"

    # 第 2 层：结构
    body = resp.json()
    assert isinstance(body, list), f"返回应为列表，实际 {type(body)}"
    assert len(body) >= 13, f"数量应 >=13，实际 {len(body)}"

    # 第 3 层：字段
    first = body[0]
    assert "id" in first, f"第一条缺少 id 字段: {first}"
    assert isinstance(first["id"], str), f"id 应为字符串，实际 {type(first['id'])}"
    assert "name" in first

    print(f"✓ 用例1 通过 | {len(body)} 条 | 耗时 {resp.elapsed.total_seconds():.2f}s")
    return body


def test_get_one(object_id):
    """用例 2：按 id 查单条 —— 验 id 一致"""
    resp = requests.get(f"{BASE_URL}/objects/{object_id}", timeout=(10,30))

    assert resp.status_code == 200, f"状态码应为 200，实际 {resp.status_code}"

    body = resp.json()
    assert str(body["id"]) == str(object_id), \
        f"返回 id 与请求不一致: 请求 {object_id}，返回 {body['id']}"
    assert "name" in body
    assert body["name"] != "", "name 不应该为空"

    print(f"✓ 用例2 通过 | id={object_id} | name={body['name']}")
    return body


def test_not_found():
    """用例 3：查不存在的 id —— 期望 404"""
    resp = requests.get(f"{BASE_URL}/objects/99999999", timeout=(10,30))

    assert resp.status_code == 404, \
        f"不存在的 id 应返回 404，实际 {resp.status_code}，响应: {resp.text[:200]}"

    print(f"✓ 用例3 通过 | 不存在的 id 返回 404")


if __name__ == "__main__":
    data = test_get_list()
    test_get_one(data[0]["id"])      # 用列表里第一条的 id 查单条 ← 接口关联
    test_not_found()
    print("\n全部用例通过 ✅")