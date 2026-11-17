# -*- coding: utf-8 -*-
"""skip / skipif / xfail / 自定义 mark 的四种用法"""
import sys

import pytest


# ① skip：无条件跳过，用例永远不跑
@pytest.mark.skip(reason="接口还没开发完，等 V2")
def test_not_implemented():
    assert False


# ② skipif：条件跳过，条件为 True 才跳过
@pytest.mark.skipif(sys.version_info < (3, 10), reason="需要 Python 3.10+")
def test_need_new_python():
    assert True


# ③ xfail：预期失败
@pytest.mark.xfail(reason="已知 bug：空 name 应该 400，实际 200")
def test_known_bug():
    assert 1 == 2        # 故意失败 → 结果 XFAIL（预期内，不算红）


# ④ xfail 但实际通过了 → XPASS
@pytest.mark.xfail(reason="预期失败，但它其实过了")
def test_unexpected_pass():
    assert 1 == 1


# ⑤ 自定义 mark：给用例打标签
@pytest.mark.smoke
def test_health_check(session, base_url):
    resp = session.get(f"{base_url}/ping", timeout=(5, 30))
    assert resp.status_code == 200


@pytest.mark.slow
def test_list_all(session, base_url):
    resp = session.get(f"{base_url}/objects", timeout=(5, 30))
    assert resp.status_code == 200