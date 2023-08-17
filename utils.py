from datetime import datetime
import tiktoken
from config import CHATGPT_MODEL

def format_date_timestamp(date: str) -> float:
    date_object = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    return date_object.timestamp() 

def split_list(list: list, size = 7):
	sublist_size = size
	sublists = [list[i:i+sublist_size] for i in range(0, len(list), sublist_size)]
	return sublists

def count_tokens(messages: list[str]) -> int:
	total = 0
	enc = tiktoken.encoding_for_model(CHATGPT_MODEL)
	for message in messages:
		total += len(enc.encode(message))
	return total