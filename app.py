# -*- coding: utf-8 -*-
"""LLM 攻防靶场 · 本地 Web 系统入口。
模块：Dashboard / CTF 提示注入 / OWASP LLM Top10 / Agent 靶场 / 聚合清单。
被渗透的目标模型：DeepSeek。
"""
import socket
from flask import Flask, render_template

import config
from modules.ctf import bp as ctf_bp
from modules.owasp import bp as owasp_bp
from modules.agent_range import bp as agent_bp
from modules.catalog import bp as catalog_bp

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

app.register_blueprint(ctf_bp)
app.register_blueprint(owasp_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(catalog_bp)


@app.route("/")
def index():
    return render_template("index.html")


def _pick_port():
    if config.PORT:
        return config.PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))  # 让内核分配随机空闲端口
    port = s.getsockname()[1]
    s.close()
    return port


if __name__ == "__main__":
    port = _pick_port()
    print("=" * 60)
    print("  🛡️  LLM 攻防靶场 · LLM Security Range")
    print(f"  ➜  http://127.0.0.1:{port}")
    print(f"  目标模型: {config.DEEPSEEK_MODEL} @ {config.DEEPSEEK_BASE_URL}")
    print(f"  Agent Docker 隔离: {'开' if config.AGENT_USE_DOCKER else '关(本地模拟)'}")
    print("=" * 60)
    app.run(host="127.0.0.1", port=port, debug=False)
