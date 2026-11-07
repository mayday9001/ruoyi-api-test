import json
# # 1.创建字典
# user = {"uesrId" : 1, "userName" : "mayday" ,"status" : "0"}
# print("1:" , user)
#
# # 2.取值
# print("2-a:" , user.get("userName"))
# print("2-b:" , user.get("age"))
# print("2-c:" , user.get("age",18))
#
# # 3.增/改
# user["emal"] = "291260..."
# user["status"] = "1"
# print("3:" , user)
#
# # 4.删除
# del user["emal"]
# print("4:" , user)
#
# # 5.keys / values / items
# print("5-a:" , list(user.keys()))
# print("5-b:" , list(user.values()))
# print("5-c:" , list(user.items()))
#
# # 6.遍历
# for k in user:
#     print("6-a:" , k , "->" , user[k])
# for k , v in user.items():
#     print("6-b:" , k , "->" , v)
#
# # 7. 判断
# print("7:", "userName" in user, "age" in user)
#
# # 8. 嵌套字典
# resp = {
#     "code": 200,
#     "msg": "查询成功",
#     "rows": [
#         {"userId": 1, "userName": "admin", "status": "0",
#          "roles": [{"roleName": "超级管理员"}]},
#         {"userId": 2, "userName": "test01", "status": "1",
#          "roles": [{"roleName": "普通角色"}]},
#     ],
#     "total": 2,
# }
# print("8-a:", resp["rows"][0]["userName"])
# print("8-b:", resp["rows"][0]["roles"][0]["roleName"])
#
# # 9. json 序列化 / 反序列化
# s = json.dumps(resp,ensure_ascii=False, )
# print("9-a:", s[:80].replace("\n" ," "), "...")
# back = json.loads(s)
# print("9-b:",back["code"])
#
# # 10. 推导式➕合并
# names = [u["userName"] for u in resp["rows"]]
# print("10-a:",names)
#
# user.update({"pageNum":1}) # 合并另一个字典
# print("10-b:",user)
#
# # 练习一:
# # 用 resp，输出 ['admin', 'test01']
# for k in resp["rows"]:
#    print("10-c",k["userId"],k["userName"])
#
# # 练习二:
# # 期望输出：{"0": 1, "1": 1}
# # 提示：新建一个空字典 result = {}，遍历 resp["rows"]，
# # 用 result[status] = result.get(status, 0) + 1
# result = {}
# for k in resp["rows"]:
#     status = k["status"]
#     result[status] = result.get(status,0) + 1
#
# print(result)

# 练习三:
# 写个函数取所有用户名；如果 resp 里没有 rows，返回空列表，别报错。



resp = {
     "code": 200,
     "msg": "查询成功",
     "rows": [
         {"userId": 1, "userName": "admin", "status": "0",
          "roles": [{"roleName": "超级管理员"}]},
         {"userId": 2, "userName": "test01", "status": "1",
          "roles": [{"roleName": "普通角色"}]},
     ],
     "total": 2,
 }
# 写个函数取所有用户名；如果 resp 里没有 rows，返回空列表，别报错。




