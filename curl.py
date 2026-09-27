"""
curl.py — пример использования curl_cffi для эмуляции браузерного TLS/UA fingerprinting.

Установка:
    pip install curl-cffi

Запуск:
    python curl.py https://example.com
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from curl_cffi import requests
from curl_cffi.requests import CurlResponse


def create_session(impersonate: str = "chrome124") -> requests.Session:
    """Создаёт и настраивает сессию curl_cffi с указанием профиля браузера."""
    session = requests.Session(impersonate=impersonate)
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    return session


def fetch(url: str, timeout: int = 15, impersonate: str = "chrome124") -> CurlResponse:
    session = create_session(impersonate=impersonate)
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="curl_cffi example — эмуляция браузера")
    parser.add_argument("url", help="URL для загрузки")
    parser.add_argument("--impersonate", default="chrome124", help="профиль для impersonate (например chrome124)")
    parser.add_argument("--timeout", type=int, default=15, help="таймаут в секундах")
    args = parser.parse_args(argv)

    try:
        resp = fetch(args.url, timeout=args.timeout, impersonate=args.impersonate)
    except Exception as e:
        print(f"Ошибка запроса: {e}", file=sys.stderr)
        return 2

    print(resp.status_code)
    print(resp.text[:500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
