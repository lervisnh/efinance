
import re
from typing import Dict
import rich

from ..shared import session, request_proxies


def set_request_proxies(proxies: Dict[str, str]) -> None:
    def proxies_valid(proxies: Dict[str, str]):
        if not isinstance(proxies, dict):
            raise ValueError("Proxies must be a dict.")
        if not proxies:
            rich.print("Clearing all request proxies.")

        # 定义有效的代理协议
        valid_protocols = {'http', 'https', 'socks', 'socks5', 'socks4'}
        # 代理URL的简单正则表达式模式
        proxy_pattern = re.compile(r'^(http|https|socks[45]?)://.*$')

        # 检查每个代理配置
        for protocol, proxy_url in proxies.items():
            if not isinstance(protocol, str) or not isinstance(proxy_url, str):
                raise TypeError(f"Proxy protocol and URL must be strings, got {type(protocol).__name__}:{type(proxy_url).__name__}")
            # 检查协议是否有效
            if protocol not in valid_protocols:
                raise ValueError(f"Invalid proxy protocol: {protocol}. Supported protocols: {', '.join(valid_protocols)}")
            # 检查代理URL格式是否符合基本要求
            if not proxy_pattern.match(proxy_url):
                raise ValueError(f"Invalid proxy URL format: {proxy_url}. Should be in format 'protocol://host:port'")

    global request_proxies
    proxies_valid(proxies)

    if request_proxies:
        # 如果 request_proxies 不为空，先把旧的打印出来
        rich.print(f"Old request proxies: {request_proxies}")

    if proxies:
        request_proxies.clear()
        request_proxies.update(proxies)
        # 再把新的打印出来
        rich.print(f"New request proxies: {request_proxies}")
        session.proxies = request_proxies