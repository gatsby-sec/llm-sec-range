<div align="center">

# 🛡️ LLM SecRange · 大模型攻防渗透测试靶场

**一个从零打造的本地化大模型攻防练习平台**

提示注入闯关 · OWASP LLM Top 10 · 脆弱 Agent 靶场 · 靶场资料聚合

被攻击的目标模型接入 **DeepSeek**，真实可被绕过；Agent 危险操作隔离在沙箱 / Docker 容器内。

![home](docs/screenshots/01-home.png)

</div>

---

## ✨ 这是什么

`LLM SecRange` 是一个**单体 Flask Web 系统**，把社区里优秀的大模型攻防靶场（AIGoat、damn-vulnerable-llm-agent、ai-prompt-ctf 等）的核心玩法，重新整合成一个开箱即用、全中文、接真实大模型的本地训练场。适合：

- 🧑‍💻 安全工程师 / 红队 / 渗透测试学习 LLM 攻击面
- 🎓 AI 安全教学与 CTF 出题
- 🏢 团队内做 LLM 应用安全意识培训

> ⚠️ **仅供授权的安全教育 / 渗透测试训练**。所有漏洞与危险操作均隔离在本地沙箱内，请勿用于真实攻击。

---

## ⚔️ 开箱即用的渗透语句

每个关卡都内置了**完整、可直接复制的渗透测试语句**（不只是模糊提示）——点一下即自动填入输入框开打。覆盖：提示注入越权、字母拆分/北约音标/首字母藏字绕过输出过滤、跨轮分段泄露绕过审查、SQL 注入、路径穿越、伪造 `Observation:` 欺骗 ReAct 循环等真实手法。新手照着打能通关，进阶者可在此基础上自行变形。

---

## 🧠 会话管理

所有与模型的对话均为**多轮有记忆**：模型记住此前的交流，支持「分多步社会工程 / 跨轮拼接 payload」等高级攻击。每个对话窗口顶部显示当前**记忆轮数**，并提供 **🗑️ 清空记忆 / 新会话** 按钮一键重置上下文，互不干扰地反复试验不同攻击路径。CTF、OWASP labs、Agent 三处独立维护各自会话。

---

## 🧩 四大模块

### 1. CTF · 提示注入闯关（Gandalf 式 8 关）
防御逐级加固：从「毫无防备」到「输入/输出双过滤 + 模糊匹配 + LLM 看门人 + 输入意图审查」。目标是诱导模型吐出每关的暗号。

| 关卡 | 防御强度 |
|---|---|
| L1 毫无防备 | 无 |
| L2 口头约束 → L3 拒绝谈论 | 系统提示约束 |
| L4 输出过滤 → L5 输入过滤 | 关键词/明文拦截 |
| L6 LLM 看门人 → L7 全家桶 → L8 偏执狂 | 多重守卫叠加 |

<img src="docs/screenshots/02-ctf-list.png" width="49%"> <img src="docs/screenshots/03-ctf-attack.png" width="49%">

### 2. OWASP LLM Top 10 靶场（2025 版）
覆盖十大风险，每类一个可上手的 lab，含可攻击关与缓解讲解关：

`LLM01 提示注入` · `LLM02 敏感信息泄露` · `LLM03 供应链` · `LLM04 数据与模型投毒` · `LLM05 不当输出处理(XSS)` · `LLM06 过度代理` · `LLM07 系统提示泄露` · `LLM08 向量与嵌入弱点` · `LLM09 错误信息` · `LLM10 无限制消耗`

<img src="docs/screenshots/04-owasp-list.png" width="49%"> <img src="docs/screenshots/05-owasp-attack.png" width="49%">

### 3. Agent 靶场 · 脆弱 ReAct 银行客服
一个接 DeepSeek 的 ReAct Agent，工具实现存在真实漏洞，4 个夺旗目标：

- 💉 **SQL 注入** — `get_transactions` 字符串拼接，dump 他人交易
- 📂 **路径穿越** — `read_doc` 未规范化路径，读取沙箱机密文件
- 💸 **越权转账** — `transfer` 不校验账户归属（过度代理）
- 🖥️ **命令执行** — `run_command` 被诱导执行任意命令（经 Docker 隔离）

通过**提示注入**（伪造系统消息、注入假 Observation、社工身份）让 Agent 滥用工具权限。攻破后实时展示 ReAct 推理轨迹与夺取的 flag。

![agent](docs/screenshots/07-agent-attack.png)

### 4. 聚合清单
精选 GitHub 大模型攻防靶场仓库，标注 Star 与**活跃状态**（近半年是否更新）。

![catalog](docs/screenshots/06-catalog.png)

---

## 🚀 一键部署

### 方式一：脚本启动（推荐本地）
```bash
git clone https://github.com/<你的用户名>/llm-sec-range.git
cd llm-sec-range
cp .env.example .env        # 编辑 .env 填入你的 DEEPSEEK_API_KEY
bash run.sh                 # 自动建 venv、装依赖、起服务（随机端口）
```
启动后终端会打印访问地址，如 `http://127.0.0.1:<随机端口>`。

### 方式二：Docker Compose（推荐隔离部署）
```bash
cp .env.example .env        # 填入 DEEPSEEK_API_KEY
docker compose up -d        # 浏览器打开 http://localhost:8000
```

### 方式三：手动
```bash
pip install -r requirements.txt
cp .env.example .env        # 填 key
python app.py
```

### （可选）开启 Agent 的 Docker 隔离执行
让 `run_command` 在一次性容器内真实执行（而非本地模拟）：
```bash
bash agent_sandbox/build.sh         # 构建沙箱镜像
# 在 .env 里设 AGENT_USE_DOCKER=1，重启服务
```

---

## ⚙️ 配置（`.env`）

| 变量 | 说明 | 默认 |
|---|---|---|
| `DEEPSEEK_API_KEY` | DeepSeek API Key（**必填**） | — |
| `DEEPSEEK_BASE_URL` | API 地址 | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | 模型 | `deepseek-chat` |
| `PORT` | Web 端口（0/留空=随机） | 随机 |
| `AGENT_USE_DOCKER` | Agent 命令执行是否走 Docker | `0` |

> 🔑 Key 只存在本地 `.env`（已 `.gitignore`），不会进入仓库。

---

## 🏗️ 架构

```
llm-sec-range/
├── app.py                 # Flask 入口（随机端口）
├── config.py              # 配置 + .env 加载
├── llm_client.py          # DeepSeek 调用封装
├── modules/               # 四大模块蓝图
│   ├── ctf.py             #   提示注入闯关 + 守卫链
│   ├── owasp.py           #   OWASP Top10 labs
│   ├── agent_range.py     #   ReAct Agent 循环
│   └── catalog.py         #   聚合清单
├── data/                  # 关卡 / 清单数据
├── agent_sandbox/         # Agent 工具沙箱 + Docker 隔离
├── templates/ static/     # 前端（暗色 hacker 风）
└── docker-compose.yml     # 一键容器部署
```

---

## 🙏 致谢 / 灵感来源

本项目玩法参考了以下优秀开源靶场（详见站内「聚合清单」）：
[AISecurityConsortium/AIGoat](https://github.com/AISecurityConsortium/AIGoat) ·
[opena2a-org/damn-vulnerable-ai-agent](https://github.com/opena2a-org/damn-vulnerable-ai-agent) ·
[c-goosen/ai-prompt-ctf](https://github.com/c-goosen/ai-prompt-ctf) ·
[ReversecLabs/damn-vulnerable-llm-agent](https://github.com/ReversecLabs/damn-vulnerable-llm-agent) ·
[ottosulin/awesome-ai-security](https://github.com/ottosulin/awesome-ai-security)

## 📜 License

MIT — 仅限合法、授权的安全研究与教育用途。
