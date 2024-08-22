# app/config.py

class Config:
    API_URLS = [
        "https://api1.com?member_id=",
        "https://api2.com?member_id=",
        "https://api3.com?member_id="
    ]
    COALESCE_STRATEGY = "average"  # default strategy, Also "min", "max", "median"

config = Config()

