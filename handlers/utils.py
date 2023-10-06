import requests
import bs4
import json
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
      

      
def get_news():
  ''' 
  Get news from https://kun.uz/ and save it in data/news.json
  :return: list of news
  '''
  
  try: os.mkdir('data')
  except: pass
  
  list_news = []
  
  soup = bs4.BeautifulSoup(requests.get('https://kun.uz').text, 'lxml')
  
  row = soup.select('body > div.outer-wrapper > div > main > div.container.mb-50 > div.row > div.col-md-9 > div.top-news > div.top-news__small-items > div')
  
  for news in row[0].find_all(class_='col-md-6'):
    img =news.find('img').attrs['src']
    title = news.find('a', class_='small-news__title').text
    link = news.find('a', class_='small-news__title').attrs['href']
    
    list_news.append({'img': img, 'title': title, 'link': f"https://kun.uz{link}"})
  
  with open(os.path.join('data', 'news.json'), 'w') as f:
    json.dump(list_news, f)
  
  return list_news


def news_keyboard(mes_id, link):
  return InlineKeyboardMarkup([[
              InlineKeyboardButton("Zo'r", callback_data=f's*{mes_id}*{link[-30:]}'),
              InlineKeyboardButton("Yaxshi", callback_data=f'g*{mes_id}*{link[-30:]}'),
              InlineKeyboardButton("Yomon", callback_data=f'b*{mes_id}*{link[-30:]}')
        ]])