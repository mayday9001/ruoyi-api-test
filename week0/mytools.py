"""我自己的工具库"""


def add(a, b):
    """两数相加"""
    return a + b


def get_names(rows):
    """从 rows 里取出所有 name"""
    names = []
    for u in rows:
        names.append(u.get("name", "未知"))
    return names


if __name__ == "__main__":
    # 只有在命令行直接 python mytools.py 时才执行
    print("自测：add(1,2) =", add(1, 2))

PI = 3.14