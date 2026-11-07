# names = ["admin","test01","张三"]
#
# # 1.取值
# print(names[0])
# print(names[1])
#
# # 2.增
# names.append("test02")
# print(names)
# names.insert(0,"李四")
# print(names)
# names.extend(["a","b"])
# print(names)
#
# # 3.删
# names.remove("张三")
# print(names)
# names.pop() # 删除末尾
# del names[0]
# print(names)
#
#
# # 4.改
# names[0] = "root"
# print(names)
#
# # 5.查
# res1 = "admin" in names
# print(res1)
# res2 = names.index("a")
# print(res2)
# names.append("a")
# res3 = names.count("a")
# print(res3)
#
# # 6.排序
# names1 = ["b", "a"]
#
# result = names1.sort()     # ❌ result 是 None！sort 不返回值
# print("6:",result)             # None
#
# # 7.切片
# print(names)
# names[0:2]

# 练习
names = ["admin","test01","张三"]
# 加一个 "test02" 到末尾
names.append("test02")
# 删掉 "张三"
names.remove("张三")
# 打印第 2 个元素
print(names[1])
# 用负索引打印最后一个
print(names[-1])
# 反转后打印
names.reverse()
print(names)
# 排序后打印
sorted(names)
print(names)




