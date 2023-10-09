import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

url = 'https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1'

data = requests.get(url=url ,headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

meta_image = soup.select_one('meta[property="og:image"]')
meta_title = soup.select_one('meta[property="og:title"]')
meta_description = soup.select_one('meta[property="og:description"]')

image = meta_image['content']
title = meta_title['content']
desc = meta_description['content']

print(image)
print(title)
print(desc)
