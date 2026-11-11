import requests

URL = "https://httpbin.org/bearer"

# ---------- 1. 不带 token ----------
r1 = requests.get(URL, timeout=(5, 30))
print("不带 token:", r1.status_code)
print(r1.text[:100])

# ---------- 2. 带正确 token ----------
headers = {"Authorization": "Bearer my-secret-token-123"}
r2 = requests.get(URL, headers=headers, timeout=(5, 30))
print("\n带 token:", r2.status_code)
print(r2.text[:200])

# # ① 登录拿 token
# login_resp = requests.post(
#     "https://restful-booker.herokuapp.com/auth",
#     json={"username": "admin", "password": "password123"},
#     timeout=(5, 30),
# )
#
# body = login_resp.json()
# print(body)
# token = login_resp.json()["token"]
# print("拿到 token:", token)
#
# # ② 后续请求带上
# headers = {"Cookie": f"token={token}"}       # 老式：放 Cookie
# # 或者
# headers = {"Authorization": f"Bearer {token}"}  # 现代：放 Header