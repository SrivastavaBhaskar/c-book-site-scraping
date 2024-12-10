import os
import re
import requests
from bs4 import BeautifulSoup

import parse_chapter

index = requests.get("https://www.learncpp.com/")

soup = BeautifulSoup(index.text, "html.parser")

def sanitize_filename(file_name):
    # Replace invalid characters with an underscore
    return re.sub(r'[<>:"/\\|?*]', '_', file_name)

def generate_index():
    lessontables = soup.find_all('div', {'class': 'lessontable'})

    for lessontable in lessontables:
        lesson_number = lessontable.find('div', {'class': 'lessontable-header-chapter'}).text
        lesson_name = lessontable.find('div', {'class': 'lessontable-header-title'}).text

        file_name = lesson_number + " - " + lesson_name
        
        file_name = file_name.replace('\xa0', ' ').strip()
        file_name = sanitize_filename(file_name)

        with open("index.html", 'a') as f:
            f.write(file_name)
            f.write('\n')
            f.write('\n')

        sections = lessontable.find_all('div', {'class': 'lessontable-row'})

        for section in sections:
            section_number = section.find('div', {'class': 'lessontable-row-number'}).text
            section_name = section.find('div', {'class': 'lessontable-row-title'}).text
            section_url = section.find('a')['href']

            section_details = section_number + " " + section_name + " - " + f'./chapters/{file_name}/{section_number}.html'

            with open("index.html", 'a') as f:
                f.write(section_details)
                f.write('\n')

            if not os.path.exists(f'./chapters/{file_name}'):
                os.makedirs(f'./chapters/{file_name}')

            parse_chapter.parse_chapter(f'./chapters/{file_name}', section_number, section_url)

        with open("index.html", 'a') as f:
            f.write('\n')



generate_index()
