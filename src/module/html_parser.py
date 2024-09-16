from re import search

from bs4 import BeautifulSoup


def html_parser(html: str, selector: str = "twitter") -> list:
    soup: BeautifulSoup | list[str] = BeautifulSoup(html, "html.parser")
    soup = soup.find_all("a", class_="tweet-link")
    soup = list(map(str, soup))
    soup = list(map(lambda string: url_slice(string, selector), soup))
    return soup


def url_slice(raw_string: str, selector: str = "twitter") -> str:
    domain_manifest: dict = {"twitter": "https://twitter.com", "x": "https://x.com", "nitter": "https://nitter.net"}
    expression: str = r"href=\"(.+)\""
    api_slice: str = search(expression, raw_string).group(1)[:-2]
    text: str = f"{domain_manifest[selector]}{api_slice}"
    return text


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
        print("\033[93m")  # Format warning
    except Exception as exception:
        logging.debug(exception)
