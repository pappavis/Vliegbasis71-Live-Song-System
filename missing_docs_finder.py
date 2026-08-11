#!/usr/bin/env python3

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from urllib.parse import (
    urljoin,
    urlparse,
    urldefrag,
    unquote,
)

import requests
from bs4 import BeautifulSoup


START_URL = (
    "https://pappavis.github.io/"
    "Vliegbasis71-Live-Song-System/"
)

SITE_PREFIX = "/Vliegbasis71-Live-Song-System/"

TIMEOUT = 15

IGNORED_SCHEMES = (
    "mailto:",
    "tel:",
    "javascript:",
    "data:",
)


@dataclass(frozen=True)
class QueueItem:
    url: str
    source: str


@dataclass(frozen=True)
class BrokenLink:
    status: str
    url: str
    source: str


class MkDocsLinkCrawler:

    def __init__(self, start_url: str):
        self.start_url = self.normalize(start_url)

        parsed = urlparse(self.start_url)

        self.hostname = parsed.hostname
        self.visited: set[str] = set()
        self.queued: set[str] = set()

        self.broken: list[BrokenLink] = []
        self.redirects: list[tuple[str, str]] = []

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent":
                    "Vliegbasis71-MkDocs-LinkChecker/1.0"
            }
        )

    # --------------------------------------------------------
    # URL helpers
    # --------------------------------------------------------

    @staticmethod
    def normalize(url: str) -> str:
        url, _fragment = urldefrag(url)

        parsed = urlparse(url)

        return parsed._replace(
            fragment=""
        ).geturl()

    def is_internal(self, url: str) -> bool:
        parsed = urlparse(url)

        return (
            parsed.hostname == self.hostname
            and parsed.path.startswith(SITE_PREFIX)
        )

    @staticmethod
    def is_ignored(href: str) -> bool:

        value = href.strip().lower()

        if not value:
            return True

        if value.startswith("#"):
            return True

        return value.startswith(IGNORED_SCHEMES)

    @staticmethod
    def looks_like_html(url: str) -> bool:

        path = urlparse(url).path.lower()

        ignored_extensions = (
            ".css",
            ".js",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".svg",
            ".ico",
            ".webp",
            ".pdf",
            ".zip",
            ".json",
            ".xml",
            ".txt",
            ".woff",
            ".woff2",
            ".ttf",
            ".mp3",
            ".wav",
            ".opus",
            ".mp4",
        )

        return not path.endswith(ignored_extensions)

    # --------------------------------------------------------
    # HTML parsing
    # --------------------------------------------------------

    def extract_links(
        self,
        page_url: str,
        html: str,
    ) -> set[str]:

        soup = BeautifulSoup(html, "html.parser")

        links: set[str] = set()

        for tag in soup.find_all("a", href=True):

            href = tag["href"].strip()

            if self.is_ignored(href):
                continue

            absolute = urljoin(page_url, href)

            absolute = self.normalize(absolute)

            links.add(absolute)

        return links

    # --------------------------------------------------------
    # Queue
    # --------------------------------------------------------

    def enqueue(
        self,
        queue: deque[QueueItem],
        url: str,
        source: str,
    ) -> None:

        url = self.normalize(url)

        if url in self.visited:
            return

        if url in self.queued:
            return

        self.queued.add(url)

        queue.append(
            QueueItem(
                url=url,
                source=source,
            )
        )

    # --------------------------------------------------------
    # Request
    # --------------------------------------------------------

    def request(
        self,
        item: QueueItem,
    ) -> requests.Response | None:

        try:

            response = self.session.get(
                item.url,
                timeout=TIMEOUT,
                allow_redirects=True,
            )

            return response

        except requests.RequestException as exc:

            self.broken.append(
                BrokenLink(
                    status="ERROR",
                    url=item.url,
                    source=item.source,
                )
            )

            print(
                f"ERR  {item.url}\n"
                f"     FROM: {item.source}\n"
                f"     {exc}"
            )

            return None

    # --------------------------------------------------------
    # Crawl
    # --------------------------------------------------------

    def crawl(self) -> None:

        queue: deque[QueueItem] = deque()

        self.enqueue(
            queue,
            self.start_url,
            "<START>",
        )

        while queue:

            item = queue.popleft()

            self.queued.discard(item.url)

            if item.url in self.visited:
                continue

            self.visited.add(item.url)

            response = self.request(item)

            if response is None:
                continue

            status = response.status_code

            print(
                f"{status:3}  {item.url}"
            )

            if response.url != item.url:

                self.redirects.append(
                    (
                        item.url,
                        response.url,
                    )
                )

            if status >= 400:

                self.broken.append(
                    BrokenLink(
                        status=str(status),
                        url=item.url,
                        source=item.source,
                    )
                )

                print(
                    f"     ^^^ BROKEN\n"
                    f"     FROM: {item.source}"
                )

                continue

            content_type = response.headers.get(
                "Content-Type",
                "",
            ).lower()

            if "text/html" not in content_type:
                continue

            links = self.extract_links(
                response.url,
                response.text,
            )

            for link in sorted(links):

                # --------------------------------------------
                # External links are deliberately ignored.
                #
                # We're checking the complete internal
                # GitHub Pages site.
                # --------------------------------------------

                if not self.is_internal(link):
                    continue

                self.enqueue(
                    queue,
                    link,
                    response.url,
                )

    # --------------------------------------------------------
    # Report
    # --------------------------------------------------------

    def report(self) -> None:

        print()
        print("=" * 78)
        print("CRAWL SUMMARY")
        print("=" * 78)

        print(
            f"Pages / resources checked : "
            f"{len(self.visited)}"
        )

        print(
            f"Broken links found        : "
            f"{len(self.broken)}"
        )

        print(
            f"Redirects found           : "
            f"{len(self.redirects)}"
        )

        print()
        print("=" * 78)
        print("404 / BROKEN")
        print("=" * 78)

        if not self.broken:

            print(
                "✅ Geen interne broken links gevonden."
            )

        else:

            for broken in sorted(
                self.broken,
                key=lambda x: (
                    x.url,
                    x.source,
                ),
            ):

                print()
                print(
                    f"[{broken.status}] "
                    f"{unquote(broken.url)}"
                )

                print(
                    f"    linked from:"
                )

                print(
                    f"    {unquote(broken.source)}"
                )

        if self.redirects:

            print()
            print("=" * 78)
            print("REDIRECTS")
            print("=" * 78)

            for source, target in self.redirects:

                print()
                print(
                    f"{source}"
                )

                print(
                    f"    -> {target}"
                )


def main() -> None:

    crawler = MkDocsLinkCrawler(
        START_URL
    )

    crawler.crawl()

    crawler.report()


if __name__ == "__main__":
    main()
   
