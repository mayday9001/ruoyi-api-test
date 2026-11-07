import json
# with open("user.json",encoding = 'utf-8') as f:
#     data = json.load(f)
# print(f"读到了",data["code"])
#
# user = data["data"]
# print("有多少人:",len(user))
#
# names = []
# for i in user:
#     names.append(i.get("name","未知"))
# print(names)
#
# names.sort()
# print(names)


# ---------------包装成函数-------------------
def load_names(file_path):
    """读 json 文件，返回排序后的 name 列表"""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    users = data.get("data") or []
    names = []
    for u in users:
        names.append(u.get("name", "未知"))

    names.sort()
    return names

print(load_names("user.json"))
