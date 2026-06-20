"""DeepSeek 调用封装。OpenAI 兼容 /chat/completions。"""
import requests
import config

_SESSION = requests.Session()


class LLMError(Exception):
    pass


def chat(messages, temperature=0.7, max_tokens=1024, model=None, timeout=60):
    """messages: [{"role": "system"/"user"/"assistant", "content": "..."}]
    返回字符串内容。"""
    url = f"{config.DEEPSEEK_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model or config.DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }
    try:
        r = _SESSION.post(url, json=payload, headers=headers, timeout=timeout)
    except requests.RequestException as e:
        raise LLMError(f"请求 DeepSeek 失败：{e}")
    if r.status_code != 200:
        raise LLMError(f"DeepSeek 返回 {r.status_code}: {r.text[:300]}")
    try:
        return r.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        raise LLMError(f"解析 DeepSeek 响应失败：{e}; body={r.text[:300]}")


def ask(system, user, **kw):
    """便捷：单轮 system + user。"""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    return chat(msgs, **kw)
