"""
cloudscraper.py — пример использования cloudscraper для обхода классической Cloudflare IUAM ("checking your browser").

Установка:
    pip install cloudscraper

Примечания:
- cloudscraper может помочь с классической Cloudflare JS-защитой (IUAM), но не решает CAPTCHA.
- Всегда соблюдайте правила сайта и не нарушайте ToS.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

import cloudscraper


def fetch(url: str, timeout: int = 15) -> "requests.Response":
    """Скачивает страницу с помощью cloudscraper и возвращает объект Response.

    Аргументы:
        url: целевой URL
        timeout: таймаут в секундах

    Возвращает:
        requests.Response
    """
    scraper = cloudscraper.create_scraper()
    # можно настроить заголовки по необходимости
    scraper.headers.update({"Accept": "text/html,application/xhtml+xml"})
    resp = scraper.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="cloudscraper — пример запроса через Cloudflare IUAM")
    parser.add_argument("url", help="URL для загрузки")
    parser.add_argument("--timeout", type=int, default=15, help="таймаут в секундах")
    args = parser.parse_args(argv)

    try:
        resp = fetch(args.url, timeout=args.timeout)
    except Exception as e:
        print(f"Ошибка запроса: {e}", file=sys.stderr)
        return 2

    print(resp.status_code)
    # печатаем первые 500 символов, чтобы не засорять консоль
    print(resp.text[:500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
