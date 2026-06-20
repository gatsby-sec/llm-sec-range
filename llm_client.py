"""多提供商 LLM 调用封装。OpenAI 兼容 /chat/completions。
provider: 'deepseek'(直连) | 'openrouter'(聚合众多国产/国外小模型)。"""
import requests
import config

_SESSION = requests.Session()


class LLMError(Exception):
    pass


def _provider_conf(provider):
    if provider == "openrouter":
        return (config.OPENROUTER_BASE_URL + "/chat/completions",
                config.OPENROUTER_API_KEY,
                {"HTTP-Referer": "http://localhost", "X-Title": "LLM SecRange"})
    # 默认 deepseek 直连
    return (config.DEEPSEEK_BASE_URL + "/chat/completions",
            config.DEEPSEEK_API_KEY, {})


def chat(messages, temperature=0.7, max_tokens=1024, model=None,
         provider="deepseek", timeout=90):
    """messages: [{"role","content"}]。返回字符串内容。"""
    url, key, extra = _provider_conf(provider)
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", **extra}
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
        raise LLMError(f"请求 {provider} 失败：{e}")
    if r.status_code != 200:
        raise LLMError(f"{provider} 返回 {r.status_code}: {r.text[:300]}")
    try:
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError) as e:
        raise LLMError(f"解析 {provider} 响应失败：{e}; body={r.text[:300]}")


def ask(system, user, **kw):
    """便捷：单轮 system + user。"""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    return chat(msgs, **kw)
