import requests

BASE = "https://api.restful-api.dev/objects"

# ---------- 方式 A：手动拼 URL（不推荐）----------
r1 = requests.get(f"{BASE}?id=1", timeout=30)
print("A 的 URL:", r1.url)

# ---------- 方式 B：params 参数（推荐）----------
r2 = requests.get(BASE, params={"id": "1"}, timeout=30)
print("B 的 URL:", r2.url)

# 两个 URL 应该完全一样

# ---------- 多个同名的 key（列表形式传参）----------
r3 = requests.get(BASE, params=[("id", "1"), ("id", "2")], timeout=(30))
print("C 的 URL:", r3.url)
print("C 返回条数:", len(r3.json()))

# ---------- headers ----------
r4 = requests.get(
    BASE,
    headers={
        "User-Agent": "mayday-test/1.0",
        "Accept": "application/json",
    },
    timeout=(60),
)
print("\n实际发出的请求头（部分）:", r4.request.headers.get("User-Agent"))