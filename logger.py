import logging

logging.basicConfig(
    level=logging.INFO,  # INFO / DEBUG / WARNING / ERROR
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)



# log inside file
# import logging
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#
# file_handler = logging.FileHandler("app.log")
# file_handler.setFormatter(formatter)
#
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)
# logger.addHandler(console_handler)
