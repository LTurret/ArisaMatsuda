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


def debug():
    # Control factor
    selector: str | None = None

    with open("./response.html") as file:
        queue: list = html_parser(file, selector)
        print(queue)


if __name__ == "__main__":
    try:
        debug()
        print("\033[93m")  # Format warning
    except Exception as exception:
        print(exception)
    raise Warning(f"{__file__} Running with debug mode, Please note that this script is not tend to run independently.")
