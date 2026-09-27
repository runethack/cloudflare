"""
cloudscraper.py
Пример использования cloudscraper для обхода классической Cloudflare IUAM ("checking your browser").

Улучшённый README и дополнительные файлы в репозитории помогают индексироваться поисковикам; этот файл — удобный исполняемый пример.

Установка:
    pip install cloudscraper

Использование:
    python cloudscraper.py https://example.com

Примечания:
- cloudscraper может помочь с классической Cloudflare JS-защитой (IUAM), но не решает CAPTCHA.
- Всегда соблюдайте правила сайта и не нарушайте ToS.
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

import cloudscraper


def create_scraper() -> "cloudscraper.CloudScraper":
    """Создаёт и настраивает cloudscraper CloudScraper.

    Можно дополнительно настраивать заголовки, прокси и retry-логику по необходимости.
    """
    scraper = cloudscraper.create_scraper()  # использует requests-подобный интерфейс
    # рекомендуемые заголовки для имитации реального браузера
    scraper.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    return scraper


def fetch(url: str, timeout: int = 15) -> "requests.Response":
    """Скачивает страницу с помощью cloudscraper и возвращает объект Response.

    Аргументы:
        url: целевой URL
        timeout: таймаут в секундах

    Возвращает:
        requests.Response
    """
    scraper = create_scraper()
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
