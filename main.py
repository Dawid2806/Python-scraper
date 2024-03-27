import requests
from bs4 import BeautifulSoup
from db import  execute_query


def main():
    url = 'https://ekino-tv.pl/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    list_ul = soup.find_all('ul', class_='list')[:-1]

    for ul in list_ul:
        list_items = ul.find_all('li')

        for li in list_items:
            image = li.find('img')
            image_url = f"https:{image['src']}" if image else 'No image found'
            title_div = li.find('div', class_='title')
            title = title_div.text.strip() if title_div else 'No title found'
            categories = ', '.join([a.text for a in li.find('div', class_='info-categories').find_all('a')]) if li.find(
                'div', class_='info-categories') else 'No categories found'
            description_div = li.find('div', class_='movieDesc')
            description = description_div.text.strip() if description_div else 'No description found'

            print(f"Image URL: {image_url}")
            print(f"Title: {title}")
            print(f"Categories: {categories}")
            print(f"Description: {description}")

            query = 'INSERT INTO movies (image_url, title, categories, description) VALUES (%s, %s, %s, %s)'
            params = (image_url, title, categories, description)
            execute_query(query, params)

            print('--------------------------------')


if __name__ == '__main__':
    main()
