"""
week1/crud_demo.py
写操作完整链路：创建 → 查询 → 更新 → 删除 → 验证删除 → 清理

运行：python crud_demo.py
"""
import requests

BASE = "https://api.restful-api.dev"
TIMEOUT = (5, 30)


def create_object(name, data):
    """用例 1：创建 —— 断言自己造的数据"""
    payload = {"name": name, "data": data}
    resp = requests.post(f"{BASE}/objects", json=payload, timeout=TIMEOUT)

    assert resp.status_code in (200, 201), \
        f"创建失败: {resp.status_code} {resp.text[:200]}"

    body = resp.json()
    assert "id" in body, f"响应缺少 id: {body}"
    # 自己造的数据，可以断言具体值
    assert body["name"] == name, f"name 不符: {body.get('name')}"

    print(f"  ✓ 创建成功 id={body['id']} name={body['name']}")
    return body["id"]


def get_object(object_id):
    """查询单条"""
    resp = requests.get(f"{BASE}/objects/{object_id}", timeout=TIMEOUT)
    assert resp.status_code == 200, f"查询失败: {resp.status_code}"
    return resp.json()


def update_object(object_id, payload):
    """用例 2：更新 —— 断言更新生效"""
    resp = requests.put(f"{BASE}/objects/{object_id}", json=payload, timeout=TIMEOUT)
    assert resp.status_code == 200, f"更新失败: {resp.status_code}"

    body = resp.json()
    assert body["name"] == payload["name"], f"更新未生效: {body.get('name')}"
    print(f"  ✓ 更新成功 name={body['name']}")
    return body


def delete_object(object_id):
    """用例 3：删除并验证真的删了"""
    resp = requests.delete(f"{BASE}/objects/{object_id}", timeout=TIMEOUT)
    assert resp.status_code in (200, 204), f"删除失败: {resp.status_code}"

    # 关键：删完必须验证
    after = requests.get(f"{BASE}/objects/{object_id}", timeout=TIMEOUT)
    assert after.status_code == 404, \
        f"删除后仍能查到 id={object_id}，实际状态码 {after.status_code}"
    print(f"  ✓ 删除成功，且验证查询返回 404")


def main():
    new_id = None
    try:
        print("① 创建")
        new_id = create_object(
            "crud-demo-mayday",
            {"price": 100, "color": "红色", "owner": "mayday9001"},
        )

        print("② 更新")
        update_object(new_id, {
            "name": "crud-demo-mayday-已更新",
            "data": {"price": 200, "color": "蓝色", "owner": "mayday9001"},
        })

        print("③ 删除并验证")
        delete_object(new_id)
        new_id = None      # 已删掉，finally 不用再删

    except AssertionError as e:
        print(f"\n❌ 用例失败: {e}")
        raise
    finally:
        if new_id:
            print(f"\n🧹 清理残留数据 id={new_id}")
            try:
                requests.delete(f"{BASE}/objects/{new_id}", timeout=TIMEOUT)
            except Exception:
                pass


if __name__ == "__main__":
    main()
    print("\n全部通过 ✅")