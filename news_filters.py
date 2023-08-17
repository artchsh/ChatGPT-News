from utils import format_date_timestamp
from datetime import datetime

def is_in_last_24_hours(news):
    news_timestamp = format_date_timestamp(news["date"])
    return datetime.now().timestamp() - news_timestamp < 1000 * 60 * 60 * 24

def is_not_empty(news):
    return news != ""