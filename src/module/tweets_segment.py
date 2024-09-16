import logging

from re import findall


def segment(urls: dict, upper_snowflake: int) -> list:
    regex: str = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"
    segmented: list[int] = []

    for url in urls:
        tweet_id: int = int(findall(regex, url)[0])
        logging.debug(f"{tweet_id} {tweet_id - upper_snowflake}")
        if tweet_id > upper_snowflake:
            segmented.append(url)

    segmented = [int(findall(r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)", url)[0]) for url in segmented]
    return segmented


def debug() -> None:
    manifest: list[str] = [
        "https://twitter.com/imasml_theater/status/1833339865162768888",
        "https://twitter.com/imasml_theater/status/1835332755544056023",
        "https://twitter.com/imasml_theater/status/1834651886487531848",
        "https://twitter.com/imasml_theater/status/1834608474866811266",
        "https://twitter.com/imasml_theater/status/1834608223997104459",
        "https://twitter.com/imasml_theater/status/1834607984225443903",
        "https://twitter.com/imasml_theater/status/1834502526705823838",
        "https://twitter.com/imasml_theater/status/1834502277157322822",
        "https://twitter.com/imasml_theater/status/1834396578792308773",
        "https://twitter.com/imasml_theater/status/1834207837343383963",
        "https://twitter.com/imasml_theater/status/1834206809785307630",
        "https://twitter.com/imasml_theater/status/1834206000456630375",
        "https://twitter.com/imasml_theater/status/1834080495354687699",
        "https://twitter.com/imasml_theater/status/1834080243684180399",
        "https://twitter.com/imasml_theater/status/1834079992180867578",
        "https://twitter.com/imasml_theater/status/1834079740715786539",
        "https://twitter.com/imasml_theater/status/1834079491116658783",
        "https://twitter.com/imasml_theater/status/1834064391870054608",
        "https://twitter.com/imasml_theater/status/1834034195288691043",
        "https://twitter.com/imasml_theater/status/1833831119537741890",
        "https://twitter.com/imasml_theater/status/1833792850490007757",
    ]
    logging.debug(f'Count: {len(segment(manifest, int(input("Enter upper snowflake: "))))}')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s ", datefmt="%Y-%m-%d %H:%M:%S")
    try:
        debug()
    except Exception as exception:
        logging.debug(exception)
