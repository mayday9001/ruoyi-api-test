import requests

BASE = "https://api.restful-api.dev"
new_id = None      # 先定义，finally 里才能用

try:
    # 造数据 + 测试
    resp = requests.post(f"{BASE}/objects",
                         json={"name": "临时测试数据", "data": {"owner": "mayday9001"}},
                         timeout=(5, 30))
    new_id = resp.json()["id"]
    print("创建了:", new_id)

    # 各种测试...
    assert resp.status_code in (200, 201)



    updated = {
        "name": "自动化测试商品-mayday-已更新",
        "data": {"price": 1234, "color": "蓝色", "owner": "mayday9001"},
    }

    resp = requests.put(f"{BASE}/objects/{new_id}", json=updated, timeout=(5, 30))
    assert resp.status_code == 200
    print("PUT 后:", resp.json())




finally:
    # 不管上面成功还是报错，都要清理
    if new_id:
        r = requests.delete(f"{BASE}/objects/{new_id}", timeout=(5, 30))
        print(f"清理 {new_id}，状态码: {r.status_code}")


