import openai, collect, json
from config import OPENAI_API_KEY, CHATGPT_MODEL, SYSTEM_MESSAGE
from utils import split_list
from news_filters import is_in_last_24_hours, is_not_empty

openai.api_key = OPENAI_API_KEY

output_file = open('./assets/output.txt', 'w', encoding='utf-8')
input_file = open('./assets/input.txt', 'w', encoding='utf-8')

def start() -> None:
	clean_news = []
	with open('./src/channel_messages.json', encoding="utf-8") as dirt_file:
		dirt_news = json.load(dirt_file)
		for news in dirt_news:
			news_message: str = news["message"]
			news_message.replace('\n', '').replace('t.me/orda_kz', '')
			if is_in_last_24_hours(news) and is_not_empty(news_message):
				clean_news.append(news["message"])

	subnews = split_list(clean_news, 10)
	
	for news in subnews:
		print(f'List of news: {subnews.index(news)+1}/{len(subnews)}')
		chatgpt_news_chat(news)
	
	dirt_file.close()
	output_file.close()
	input_file.close()

def chatgpt_news_chat(clean_news: list[str]) -> None:
	print(clean_news, file=input_file)
	messages = [ { "role": "system", "content": SYSTEM_MESSAGE } ]
	for news in clean_news:
		print(f'{round(((clean_news.index(news)+1)/len(clean_news))*100, 2)}% - {(clean_news.index(news)+1)}/{len(clean_news)}')
		messages.append({ "role": "user", "content": news })
		chat = openai.ChatCompletion.create( model=CHATGPT_MODEL, messages=messages )
		print(chat.choices[0].message.content + '\n', file=output_file)
		# messages.append({ "role": "assistant", "content": chat.choices[0].message.content })
	
if __name__ == "__main__":
    start()
