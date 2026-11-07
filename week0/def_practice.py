# def greet(name):          # name 是参数，调用时要给
#     print(f"你好，{name}")
#
# greet("lyy")           # 传值
#
#
# def login(user, pwd="123456"):
#     print(user, pwd)
#
# login("admin")                      # admin 123456（用默认值）
#
# login("admin", "abc")     # admin abc（传了就覆盖）
#
# def create_user(name, age, city):
#     ...
#                                                                 # 传参顺序
# create_user("张三", 20, "北京")                    # 按位置
# create_user(age=20, name="张三", city="北京")                    # 按名字（顺序随意）

# def count_status(rows):
#     """统计每个 status 各有多少个"""
#     result = {}
#     for u in rows:
#         s = u["status"]
#         result[s] = result.get(s, 0) + 1
#     return result
#
#
# resp = {"rows": [
#     {"userName": "admin",  "status": "0"},
#     {"userName": "test01", "status": "1"},
#     {"userName": "test02", "status": "0"},
# ]}
#
# print(count_status(resp["rows"]))     # {'0': 2, '1': 1}

def get_username(rows):
    names = []
    for u in rows:
        names.append(u["userName"])
    return names
resp = {"rows": [
     {"userName": "admin",  "status": "0"},
     {"userName": "test01", "status": "1"},
     {"userName": "test02", "status": "0"},
 ]}
print(get_username(resp["rows"]))
