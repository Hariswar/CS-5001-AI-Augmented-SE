Here's the well-documented Python module for a web scraper:

```python
"""
Web Scraper Module

A modular web scraper that fetches, parses, and extracts data from web pages.
Supports configurable settings, error handling, and multiple output formats.

Classes:
    ScraperConfig: Configuration for the web scraper.
    HTTPClient: Handles HTTP requests with retry logic.
    HTMLParser: Parses HTML content and extracts data.
    DataExtractor: Extracts structured data from parsed HTML.
    ResultHandler: Manages output of scraping results.
    Logger: Handles logging for the scraper.

Functions:
    scrape_url: Main function to scrape a single URL.
    extract_data: Extracts data from HTML using rules.
    save_results: Saves results to file in specified format.
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import csv
import time
import logging
from typing import Dict, List, Optional, TypedDict, Any
from html.parser import HTMLParser
from collections import deque

class ScraperConfig:
    """Configuration for the web scraper.

    Attributes:
        user_agent: User agent string for HTTP requests.
        delay: Delay between requests in seconds.
        max_retries: Maximum number of retries for failed requests.
        timeout: Timeout for HTTP requests in seconds.
        output_format: Format for output ('json' or 'csv').
        output_path: Path to save output file.
    """

    def __init__(
        self,
        user_agent: str = "MyScraper/1.0",
        delay: float = 1.0,
        max_retries: int = 3,
        timeout: int = 10,
        output_format: str = "json",
        output_path: str = "results.json"
    ):
        self.user_agent = user_agent
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.output_format = output_format
        self.output_path = output_path

class ScrapingResult(TypedDict):
    """Result of a single scraping operation.

    Attributes:
        url: The URL that was scraped.
        status: HTTP status code (if successful).
        data: Extracted data (if successful).
        error: Error message (if failed).
    """
    url: str
    status: Optional[int]
    data: Optional[Dict[str, Any]]
    error: Optional[str]

class ExtractedData(TypedDict):
    """Structured data extracted from a web page.

    Attributes:
        title: Page title.
        links: List of links found on the page.
        meta: Dictionary of meta tags.
    """
    title: str
    links: List[str]
    meta: Dict[str, str]

class HTTPClient:
    """Handles HTTP requests with retry logic and delay management."""

    def __init__(self, config: ScraperConfig):
        self.config = config
        self.last_request_time = 0

    def _enforce_delay(self) -> None:
        """Enforce delay between requests to avoid rate limiting."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.config.delay:
            time.sleep(self.config.delay - elapsed)
        self.last_request_time = time.time()

    def fetch(self, url: str) -> bytes:
        """Fetch content from a URL with retry logic.

        Args:
            url: URL to fetch.

        Returns:
            Raw content bytes.

        Raises:
            Exception: If all retries fail.
        """
        headers = {"User-Agent": self.config.user_agent}
        req = urllib.request.Request(url, headers=headers)

        for attempt in range(self.config.max_retries):
            self._enforce_delay()
            try:
                with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                    return response.read()
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                if attempt == self.config.max_retries - 1:
                    raise Exception(f"Failed after {self.config.max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff

        raise Exception("Unexpected error in fetch")

class HTMLParser(HTMLParser):
    """Parses HTML content and extracts structured data."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.meta = {}

    def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
        """Handle start tags in HTML."""
        if tag == "a":
            for attr, value in attrs:
                if attr == "href":
                    self.links.append(value)
        elif tag == "meta":
            meta_data = dict(attrs)
            if "name" in meta_data and "content" in meta_data:
                self.meta[meta_data["name"]] = meta_data["content"]

    def handle_data(self, data: str) -> None:
        """Handle data in HTML."""
        if self.get_starttag_text() == "<title>":
            self.title = data.strip()

    def get_extracted_data(self) -> ExtractedData:
        """Return extracted data as a dictionary."""
        return {
            "title": self.title,
            "links": self.links,
            "meta": self.meta
        }

class DataExtractor:
    """Extracts structured data from parsed HTML."""

    @staticmethod
    def extract(html: str, rules: Dict[str, str]) -> ExtractedData:
        """Extract data from HTML using rules.

        Args:
            html: HTML content to parse.
            rules: Dictionary of extraction rules (e.g., {"title": "h1"})

        Returns:
            Extracted data as a dictionary.
        """
        parser = HTMLParser()
        parser.feed(html)
        return parser.get_extracted_data()

class ResultHandler:
    """Manages output of scraping results."""

    @staticmethod
    def save_results(results: List[ScrapingResult], config: ScraperConfig) -> None:
        """Save results to file in specified format.

        Args:
            results: List of scraping results.
            config: Scraper configuration.
        """
        if config.output_format == "json":
            with open(config.output_path, "w") as f:
                json.dump(results, f, indent=2)
        elif config.output_format == "csv":
            with open(config.output_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["URL", "Status", "Title", "Links", "Error"])
                for result in results:
                    row = [
                        result["url"],
                        result["status"],
                        result["data"]["title"] if result["data"] else "",
                        ", ".join(result["data"]["links"]) if result["data"] else "",
                        result["error"] if result["error"] else ""
                    ]
                    writer.writerow(row)
        else:
            raise ValueError(f"Unsupported output format: {config.output_format}")

class Logger:
    """Handles logging for the scraper."""

    @staticmethod
    def setup_logging(level: int = logging.INFO) -> None:
        """Setup basic logging configuration.

        Args:
            level: Logging level (default: logging.INFO).
        """
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    @staticmethod
    def log_error(message: str) -> None:
        """Log an error message.

        Args:
            message: Error message to log.
        """
        logging.error(message)

    @staticmethod
    def log_info(message: str) -> None:
        """Log an informational message.

        Args:
            message: Informational message to log.
        """
        logging.info(message)

def scrape_url(url: str, config: ScraperConfig) -> ScrapingResult:
    """Fetch and parse a single URL.

    Args:
        url: URL to scrape.
        config: Scraper configuration.

    Returns:
        ScrapingResult containing the result of the operation.
    """
    result: ScrapingResult = {
        "url": url,
        "status": None,
        "data": None,
        "error": None
    }

    try:
        client = HTTPClient(config)
        html = client.fetch(url)
        result["status"] = 200
        result["data"] = DataExtractor.extract(html, {})
    except Exception as e:
        result["error"] = str(e)
        Logger.log_error(f"Failed to scrape {url}: {str(e)}")

    return result

def extract_data(html: str, rules: Dict[str, str]) -> ExtractedData:
    """Extract data from HTML using rules.

    Args:
        html: HTML content to parse.
        rules: Dictionary of extraction rules.

    Returns:
        Extracted data as a dictionary.
    """
    return DataExtractor.extract(html, rules)

def save_results(results: List[ScrapingResult], config: ScraperConfig) -> None:
    """Save results to file in specified format.

    Args:
        results: List of scraping results.
        config: Scraper configuration.
    """
    ResultHandler.save_results(results, config)

def main():
    """Example usage of the web scraper."""
    Logger.setup_logging()

    config = ScraperConfig(
        user_agent="MyScraper/1.0",
        delay=1.0,
        max_retries=3,
        timeout=10,
        output_format="json",
        output_path="results.json"
    )

    urls = [
        "https://example.com",
        "https://example.org"
    ]

    results = []
    for url in urls:
        result = scrape_url(url, config)
        results.append(result)
        Logger.log_info(f"Scraped {url}: {'Success' if not result['error'] else 'Failed'}")

    save_results(results, config)
    Logger.log_info(f"Saved results to {config.output_path}")

if __name__ == "__main__":
    main()
