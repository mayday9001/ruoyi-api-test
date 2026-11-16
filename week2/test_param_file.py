# -*- coding: utf-8 -*-
"""
数据外置：把用例数据放到 json 文件里，代码只写一遍

为什么外置？
    · 加用例 = 改 json，不用碰代码（测试和开发分离，别人也能加）
    · 一份数据可以给"接口测试"和"性能测试"同时用
    · 代码 diff 干净，评审时只看数据变化

跑法：
    pytest test_param_file.py -v
"""
import json
import os

import pytest

# __file__ = 本文件路径；dirname 拿到 week2 目录；再拼 data/xxx.json
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load_cases(filename):
    """读 json，返回 list"""
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:      # 中文必须写 encoding
        return json.load(f)


# 模块级变量：pytest 收集用例时会读它
GET_CASES = load_cases("get_cases.json")


@pytest.mark.parametrize(
    "case",
    GET_CASES,
    ids=[c["desc"] for c in GET_CASES],   # 用 desc 当用例名，报告可读
)
def test_get_not_exist_from_file(case, session, base_url):
    resp = session.get(f"{base_url}/objects/{case['oid']}", timeout=(5, 30))
    assert resp.status_code == case["expect_status"], (
        f"[{case['desc']}] 期望 {case['expect_status']}，实际 {resp.status_code}"
    )
    assert "error" in resp.json()


# ---------------------------------------------------------------- 加一个"元测试"
# 测数据本身：防止有人往 json 里塞了缺字段的用例，导致后面报 KeyError 而不是断言失败
def test_case_file_schema():
    """校验数据文件格式：每条都必须有 desc / oid / expect_status"""
    assert GET_CASES, "用例文件不能为空"
    for i, case in enumerate(GET_CASES):
        for key in ("desc", "oid", "expect_status"):
            assert key in case, f"第 {i} 条数据缺字段 {key}: {case}"
