# -*- coding: utf-8 -*-
"""
mock_api.py —— 本地被测系统（零依赖，只用 Python 标准库）

作用：
  1. 解决公网 API 的问题（每日 50 次限额、响应 7~8 秒、网络抖动）
  2. 提供与 api.restful-api.dev 一致的 CRUD 接口
  3. 响应时间 < 10ms，可以放心跑 3 遍、30 遍

启动：
  python mock_api.py
  （默认监听 http://127.0.0.1:8000）

接口：
  GET    /ping                健康检查（返回 200 + {"status":"ok"}）
  GET    /objects             查询全部
  GET    /objects/{id}        按 id 查询（不存在返回 404）
  POST   /objects             创建（返回 200 + 新对象）
  PUT    /objects/{id}        全量更新（未传字段置 null ← 与线上一致）
  PATCH  /objects/{id}        局部更新（只改传入字段）
  DELETE /objects/{id}        删除（返回 200）

说明：
  - 数据存在内存里，重启服务即清空
  - 故意保留了一些"线上系统的不完美"：PUT 全量替换、限流用 429 才是对的
"""
import json
import sys
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 8000

# 内存数据库：id -> 对象
DB = {}


def _new_id():
    """32 位十六进制 id（模仿雪花/UUID 风格）"""
    return uuid.uuid4().hex


def _now_ms():
    return int(time.time() * 1000)


def _seed():
    """预置 3 条数据，方便一启动就有东西可查"""
    presets = [
        ("Google Pixel 6 Pro", {"color": "Cloudy White", "capacity": "128 GB"}),
        ("Apple iPhone 12 Mini", None),          # 故意留一条 data 为 null
        ("Samsung Galaxy Z Fold2", {"price": 689.99}),
    ]
    for name, data in presets:
        oid = _new_id()
        DB[oid] = {"id": oid, "name": name, "data": data, "createdAt": _now_ms()}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # ---------- 工具方法 ----------
    def _send(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def _path_parts(self):
        """把 /objects/abc 拆成 ['objects', 'abc']"""
        path = self.path.split("?")[0].strip("/")
        return path.split("/") if path else []

    def log_message(self, fmt, *args):
        # 只打印简短日志，避免刷屏
        print(f"  {self.command:<6} {self.path:<40} → {args[1] if len(args) > 1 else ''}")

    # ---------- GET ----------
    def do_GET(self):
        parts = self._path_parts()

        if parts == ["ping"]:
            return self._send(200, {"status": "ok"})

        if parts == ["objects"]:
            return self._send(200, list(DB.values()))

        if len(parts) == 2 and parts[0] == "objects":
            oid = parts[1]
            if oid in DB:
                return self._send(200, DB[oid])
            return self._send(404, {"error": f"Object with id = {oid} not found"})

        return self._send(404, {"error": "Not Found"})

    # ---------- POST ----------
    def do_POST(self):
        parts = self._path_parts()
        if parts != ["objects"]:
            return self._send(404, {"error": "Not Found"})

        body = self._read_body()
        if not isinstance(body, dict) or "name" not in body:
            return self._send(400, {"error": "name is required"})

        oid = _new_id()
        DB[oid] = {
            "id": oid,
            "name": body.get("name"),
            "data": body.get("data"),
            "createdAt": _now_ms(),
        }
        # 与线上一致：创建成功返回 200（不是 201）
        return self._send(200, DB[oid])

    # ---------- PUT（全量替换）----------
    def do_PUT(self):
        parts = self._path_parts()
        if len(parts) != 2 or parts[0] != "objects":
            return self._send(404, {"error": "Not Found"})

        oid = parts[1]
        if oid not in DB:
            return self._send(404, {"error": f"Object with id = {oid} not found"})

        body = self._read_body()
        # ★ 全量替换语义：没传的字段直接置 None（与线上实测行为一致）
        DB[oid] = {
            "id": oid,
            "name": body.get("name"),
            "data": body.get("data"),
            "updatedAt": _now_ms(),
        }
        return self._send(200, DB[oid])

    # ---------- PATCH（局部更新）----------
    def do_PATCH(self):
        parts = self._path_parts()
        if len(parts) != 2 or parts[0] != "objects":
            return self._send(404, {"error": "Not Found"})

        oid = parts[1]
        if oid not in DB:
            return self._send(404, {"error": f"Object with id = {oid} not found"})

        body = self._read_body()
        # ★ 局部更新语义：只覆盖传入的字段
        for k, v in body.items():
            if k != "id":
                DB[oid][k] = v
        DB[oid]["updatedAt"] = _now_ms()
        return self._send(200, DB[oid])

    # ---------- DELETE ----------
    def do_DELETE(self):
        parts = self._path_parts()
        if len(parts) != 2 or parts[0] != "objects":
            return self._send(404, {"error": "Not Found"})

        oid = parts[1]
        if oid not in DB:
            return self._send(404, {"error": f"Object with id = {oid} not found"})

        del DB[oid]
        # 与线上一致：删除成功返回 200
        return self._send(200, {"message": f"Object with id = {oid} has been deleted."})

    # ---------- 不支持的方法 ----------
    def _not_allowed(self):
        self._send(405, {"error": f"Method {self.command} not allowed"})

    do_HEAD = _not_allowed


def main():
    port = PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    _seed()
    server = ThreadingHTTPServer((HOST, port), Handler)
    print("=" * 58)
    print(f"  Mock API 已启动：http://{HOST}:{port}")
    print("=" * 58)
    print(f"  预置数据：{len(DB)} 条")
    print("  可用接口：")
    for line in [
        "GET    /ping",
        "GET    /objects",
        "GET    /objects/{id}",
        "POST   /objects",
        "PUT    /objects/{id}",
        "PATCH  /objects/{id}",
        "DELETE /objects/{id}",
    ]:
        print("    " + line)
    print()
    print("  按 Ctrl+C 停止")
    print("=" * 58)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止。")
        server.shutdown()


if __name__ == "__main__":
    main()
