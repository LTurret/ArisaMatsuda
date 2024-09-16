import logging
import re


def html_parser(html: str, selector: str = "twitter") -> list:
    pattern: str = r'<a[^>]*class="tweet-link"[^>]*href="(.+).."'
    tweet_url: list[str] = re.findall(pattern, html)
    tweet_url = list(map(lambda string: url_split(string, selector), tweet_url))
    return tweet_url


def url_split(raw_string: str, selector: str = "twitter") -> str:
    domain_manifest: dict = {"twitter": "https://twitter.com", "x": "https://x.com", "nitter": "https://nitter.net"}
    curl_compose: str = f"{domain_manifest[selector]}{raw_string}"
    return curl_compose


def debug() -> None:
    from requests import get, Response
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    response: Response = get(getenv("cdn_url"))
    html_content: str = response.text
    queue: list[str] = html_parser(html_content)
    logging.debug(queue)


if __name__ == "__main__":
    logger = logging.getLogger("urllib3")
    logger.setLevel(logging.CRITICAL)
    logging.basicConfig(level=logging.DEBUG, format="%(message)s ", datefmt="%Y-%m-%d %H:%M:%S")
    try:
        debug()
    except Exception as exception:
        logging.debug(exception)
