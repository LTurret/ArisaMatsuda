from re import findall


def segment(urls: dict, upper_snowflake: int) -> list:
    regex: str = r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)"
    segmented: list[int] = []

    for url in urls:
        if int(findall(regex, url)[0]) > upper_snowflake:
            segmented.append(url)

    segmented = [int(findall(r"https\:\/\/[x|twitter]+\.com\/.+\/status\/(\d+)", url)[0]) for url in segmented]

    return segmented


def debug():
    dummy: list[str] = [
        "https://twitter.com/imasml_theater/status/1780114650526605616",
        "https://twitter.com/imasml_theater/status/1780476295002104198",
        "https://twitter.com/imasml_theater/status/1780521587881746915",
        "https://twitter.com/imasml_theater/status/1780529132419563615",
        "https://twitter.com/imasml_theater/status/1780544230815133784",
        "https://twitter.com/imasml_theater/status/1780551785683542395",
        "https://twitter.com/imasml_theater/status/1780763174767390756",
        "https://twitter.com/imasml_theater/status/1780793382438134206",
        "https://twitter.com/imasml_theater/status/1780838672289436132",
        "https://twitter.com/imasml_theater/status/1780838923209785686",
        "https://twitter.com/imasml_theater/status/1780839175052525718",
        "https://twitter.com/imasml_theater/status/1780839426467258456",
        "https://twitter.com/imasml_theater/status/1780839678175797395",
        "https://twitter.com/imasml_theater/status/1780839930073170027",
        "https://twitter.com/imasml_theater/status/1780840181135724701",
        "https://twitter.com/imasml_theater/status/1780840432663978312",
        "https://twitter.com/imasml_theater/status/1780883979526340940",
        "https://twitter.com/imasml_theater/status/1780884221512253618",
        "https://twitter.com/imasml_theater/status/1780899079012413613",
        "https://twitter.com/imasml_theater/status/1781155769544802435",
        "https://twitter.com/imasml_theater/status/1771488315335667761",
    ]
    print(f'Count: {len(segment(dummy, int(input("Enter snowflake: "))))}')


if __name__ == "__main__":
    try:
        debug()
        print("\033[93m")  # Format warning
    except Exception as exception:
        print(exception)
    raise Warning(f"{__file__} Running with debug mode, Please note that this script is not tend to run independently.")
