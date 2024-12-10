from bs4 import BeautifulSoup
import requests
import re

def sanitize_filename(file_name):
    # Replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)

def parse_chapter(chapter_location, chapter_name, url):
    chapter = requests.get(url)

    soup = BeautifulSoup(chapter.text, "html.parser")

    article = soup.find('div', {'class': 'article-inner'})

    for obj in article.find_all('div', {'class': 'code-block'}):
        obj.decompose()
        
    for obj in article.find_all('div', {'class': 'prevnext'}):
        obj.decompose()

    for obj in article.find_all('span'):
        obj.decompose()

    for obj in article.find_all('footer'):
        obj.decompose()

    for obj in article.find_all('img'):
        # obj['src'] = obj['data-ezsrc']
        if obj.get('data-ezsrc'):
            image_url = obj['data-ezsrc']
        else:
            image_url = obj['src']

        response = requests.get(image_url)
        if response.status_code == 200:
        # Open a file in binary write mode and save the image
            if obj.get('alt'):
                image_name = obj.get('alt')
            else:
                image_name = obj.get('src').split('.')[-2].split('/')[-1]

            image_name = sanitize_filename(image_name)   
            
            with open(f'./images/{image_name}.png', 'wb') as file:
                file.write(response.content)  # Write the image content to the file
            print("Image downloaded successfully.")
        obj['src'] = f'../../images/{image_name}.png'
        del obj['data-ezsrc']
        del obj['ezimgfmt']
        del obj['class']

    with open(f"{chapter_location}/{chapter_name}.html", 'w', encoding='utf-8') as f:
        f.write(article.prettify())