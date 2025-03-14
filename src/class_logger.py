import logging


def initialization(func: callable) -> callable:
    logging.debug(f"↳ Extension {__name__} loaded.")
    return func

def deletion(func: callable) -> callable:
    logging.debug(f"↳ Extension {__name__} removed.")
    return func