import requests

url = "https://api.restful-api.dev/objects"
resp = requests.get(url, timeout=30)

print("状态码:", resp.status_code)
print("耗时:", resp.elapsed.total_seconds(), "秒")
print("响应体前 200 字符:")
print(resp.text[:200])