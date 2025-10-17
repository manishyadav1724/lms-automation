import os

BASE_URL = os.getenv("BASE_URL", "https://staging-lms.gitview.net")
LOGIN_EMAIL = os.getenv("LOGIN_EMAIL", "manishnewdasboard_014@gmail.com")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "Test1@1234")
REG_EMAIL = os.getenv("REG_EMAIL", "manishnewdasboard9@gmail.com")

HEADLESS = os.getenv("HEADLESS", "1") != "1"   # default headless
PAGELOAD_TIMEOUT = int(os.getenv("PAGELOAD_TIMEOUT", "60"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
