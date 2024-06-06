from datetime import datetime


def today():
    today = datetime.today()
    return today.strftime("%Y-%m-%d")
