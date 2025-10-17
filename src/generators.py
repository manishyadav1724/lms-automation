import time, random

def unique_email(domain: str = "cpraedcourse.com", prefix: str = "testuser"):
    return f"{prefix}{int(time.time())}{random.randint(1000,9999)}@{domain}"

