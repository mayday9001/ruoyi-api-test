import requests

resp = requests.get("https://api.restful-api.dev/objects", timeout=(5,30))

# ---------- 1. status_code ----------
print("=== status_code ===")
print("值:", resp.status_code)
print("类型:", type(resp.status_code))

# ---------- 2. text（字符串）----------
print("\n=== text ===")
print("类型:", type(resp.text))
print("前 80 字符:", resp.text[:80])

# ---------- 3. json()（转成 Python 对象）----------
print("\n=== json() ===")
data = resp.json()
print("类型:", type(data))
print("长度:", len(data))
print("第一条:", data[0])

# ---------- 4. elapsed（耗时）----------
print("\n=== elapsed ===")
print("类型:", type(resp.elapsed))
print("秒数:", resp.elapsed.total_seconds())