# -*- coding: utf-8 -*-
"""
参数化入门（@pytest.mark.parametrize）—— 一个函数，多组数据，各自独立出报告

为什么不用 for 循环？
    for 循环里第一条数据断言失败，后面全不跑，报告里只有 1 条红。
    参数化会把每组数据变成"独立的用例"，互不影响 —— 这叫做**失败隔离**。

跑法：
    pytest test_param_intro.py -v
    pytest test_param_intro.py -v -k "ids"     # 只看某一节
"""
import pytest

BASE = "http://127.0.0.1:8000"


# ---------------------------------------------------------------- 1. 单参数
@pytest.mark.parametrize("name", ["abc", "中文名称", "x" * 100, "带空格 的名字"])
def test_single_param(name):
    """参数只有一个：装饰器第一个参数是参数名，第二个是"值的列表" """
    assert isinstance(name, str)
    assert name.strip() == name, f"首尾不应有空格: {name!r}"


# ---------------------------------------------------------------- 2. 多参数
# 参数名写成 "a, b, expected"（逗号分隔的字符串）
# 每个值是一个元组/列表，个数必须和参数名个数一致，否则收集阶段就报错
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, -100, 0),
    ],
)
def test_multi_param(a, b, expected):
    assert a + b == expected


# ---------------------------------------------------------------- 3. ids
# 不加 ids 时，报告里显示的是 [abc]、[中文名称]，复杂数据会显示成一坨
# 加 ids 后显示 [200-正常]、[404-不存在]，一眼知道哪条挂了
@pytest.mark.parametrize(
    "status, ok",
    [(200, True), (404, False)],
    ids=["200-正常", "404-不存在"],
)
def test_ids(status, ok):
    assert (status == 200) is ok


# ---------------------------------------------------------------- 4. 与 fixture 组合
# 参数化管"数据"，fixture 管"环境"（session / base_url），两者互不干扰
@pytest.mark.parametrize(
    "oid",
    ["not-exist-1", "not-exist-2", "0"],
    ids=["字母id", "字母id2", "纯数字id"],
)
def test_get_not_exist(oid, session, base_url):
    """查不存在的 id，三条数据分别独立断言 404"""
    resp = session.get(f"{base_url}/objects/{oid}", timeout=(5, 30))
    assert resp.status_code == 404, f"应为 404，实际 {resp.status_code}"
    assert "not found" in resp.json()["error"].lower()


# ---------------------------------------------------------------- 5. 叠加 = 笛卡尔积
# 两个 parametrize 叠加，不是 2+2=4 而是 2x2=4 个用例
# 想只取"配对"的数据，就不要叠加，用第 2 节那种多参数写法
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", ["a", "b"])
def test_cartesian(x, y):
    assert f"{x}{y}" in {"1a", "1b", "2a", "2b"}


# ---------------------------------------------------------------- 6. pytest.param
# 想在"某一条数据"上单独挂 mark（skip / xfail），用 pytest.param 包一层
@pytest.mark.parametrize(
    "code",
    [
        pytest.param(200, id="正常"),
        pytest.param(500, id="服务端错误-示例跳过", marks=pytest.mark.skip(reason="演示：单条数据跳过")),
    ],
)
def test_single_case_mark(code):
    assert code < 400


# ---------------------------------------------------------------- 7. 反例：for 循环的问题
# 下面这种写法看起来"省事"，但它只有 1 个用例：
#   第一条失败 → 后面全部不跑 → 报告里看不出是哪几条数据有问题
# 参数化才是对的写法，这里只做对比，不参与收集
def _bad_example_not_collected():
    for payload in [{"name": ""}, {"name": "x" * 200}]:
        assert payload["name"], f"name 不能为空: {payload}"
