# -*- coding: utf-8 -*-
"""被攻击目标模型的选择层。用户可在右上角切换，选择存入会话。
列表按『小/低版本优先』排序，默认取第一个。"""
from flask import session

# 顺序即展示顺序：小模型在前，默认用第一个
MODELS = [
    {"id": "deepseek-v4-flash", "label": "DeepSeek V4 Flash", "note": "小·快·默认"},
    {"id": "deepseek-v4-pro", "label": "DeepSeek V4 Pro", "note": "大·强"},
]
DEFAULT = MODELS[0]["id"]
_IDS = {m["id"] for m in MODELS}


def current():
    m = session.get("target_model")
    return m if m in _IDS else DEFAULT


def set_model(m):
    if m in _IDS:
        session["target_model"] = m
        return True
    return False
