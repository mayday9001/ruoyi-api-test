# -*- coding: utf-8 -*-
"""验证 Session 的三个能力（独立脚本，不是 pytest 用例）"""
import requests

BASE = "http://127.0.0.1:8000"


def main():
    # ---------- A：requests.get（一次性） ----------
    print("=== A: requests.get ===")
    r = requests.get(f"{BASE}/ping", headers={"User-Agent": "single-request/1.0"})
    print("实际发出的 User-Agent:", r.request.headers.get("User-Agent"))

    # ---------- B：Session（可复用） ----------
    print("\n=== B: requests.Session ===")
    s = requests.Session()
    s.headers.update({"User-Agent": "mayday-test/1.0"})   # 设一次
    s.cookies.set("token", "my-cookie-123")               # 塞个 cookie

    r1 = s.get(f"{BASE}/ping", timeout=(5, 30))
    r2 = s.get(f"{BASE}/objects", timeout=(5, 30))

    print("第 1 次 UA     :", r1.request.headers.get("User-Agent"))
    print("第 2 次 UA     :", r2.request.headers.get("User-Agent"))
    print("第 1 次 Cookie :", r1.request.headers.get("Cookie"))
    print("第 2 次 Cookie :", r2.request.headers.get("Cookie"))

    s.close()


if __name__ == "__main__":
    main()