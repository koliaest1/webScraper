import string
import requests
import os

from bs4 import BeautifulSoup


def main():
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"
    page_count = int(input())
    article_type = input()
    for i in range(0, page_count):
        try:
            os.mkdir(f'Page_{i+1}')
            os.chdir(f'Page_{i+1}')
        except FileExistsError:
            os.chdir(f'Page_{i + 1}')
        print(os.getcwd().split("/")[-1])
        r = requests.get(f'{url}&page={i+1}')
        soup = BeautifulSoup(r.content, 'html.parser', from_encoding='UTF-8')
        soup.prettify()
        articles = soup.find_all('article')
        files = []
        for article in articles:
            article_text = article.find('span', {'data-test': 'article.type'}).text
            if article_text == article_type:
                article_title = article.find('a').text
                print(article_title)
                new_title = ""
                for char in article_title:
                    if char not in string.punctuation and char != " ":
                        new_title += char
                    else:
                        new_title += "_"
                article_url = 'https://www.nature.com/nature' + article.find('a')['href']
                r1 = requests.get(article_url)
                soup = BeautifulSoup(r1.content, 'html.parser')
                new_title = new_title.rstrip("_")
                article_body = soup.find('p', {"class": "article__teaser"})
                file = open(f'{new_title}.txt', 'w', encoding='utf-8')
                article_to_write = article_body.text
                file.write(article_to_write)
                files.append(f'{new_title}.txt')
                file.close()
            print(files)
        current_dir = os.getcwd().split("/")
        del current_dir[-1]
        new_dir = "/".join(current_dir)
        os.chdir(new_dir)


if __name__ == "__main__":
    main()
