from imports import *


with open(get_relative_path("config.json")) as f:
    config = load(f, object_hook=lambda x: SimpleNamespace(**x))


if config.eye_candy.suppress_logger:
    logger.remove()
