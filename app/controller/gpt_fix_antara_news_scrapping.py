import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime, timedelta
import logging

class AntaraScraper:
    def __init__(self, pages=6, csv_file='./hasil_scrapping_antara/automasi_antara.csv'):
        self.pages = pages
        self.csv_file = csv_file
        self.csv_columns = ['periode', 'label', 'headline', 'content', 'link']
        self.processed_links = set()
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self._load_processed_links()

    def _load_processed_links(self):
        if os.path.exists(self.csv_file):
            with open(self.csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.processed_links.add(row['link'])

    def get_page_content(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            return None

    def get_judul_berita(self, page_number):
        url = f"https://www.antaranews.com/tag/indeks/{page_number}"
        content = self.get_page_content(url)
        judul_berita = []
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            articles = soup.find_all('h2', class_='h5')
            for link in articles:
                links = link.find('a')
                if links:
                    judul_berita.append(links.text)
        return judul_berita

    def get_link_berita(self, page_number):
        link_data = []
        url = f"https://www.antaranews.com/tag/indeks/{page_number}"
        content = self.get_page_content(url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            articles = soup.find_all('h2', class_='h5')
            for link in articles:
                links = link.find('a')
                if links:
                    link_data.append(links['href'])
        return link_data

    def convert_publish_date(self, publish_date_str):
        # Mapping Indonesian month names to numbers
        months = {
            "Januari": "01",
            "Februari": "02",
            "Maret": "03",
            "April": "04",
            "Mei": "05",
            "Juni": "06",
            "Juli": "07",
            "Agustus": "08",
            "September": "09",
            "Oktober": "10",
            "November": "11",
            "Desember": "12"
        }

        # Extract the date part from the string
        try:
            date_part = publish_date_str.split(', ')[1]
            day, month_str, year = date_part.split(' ')[0:3]
            month = months[month_str]
            formatted_date = f"{year}-{month}-{day}"
            return formatted_date
        except Exception as e:
            return 'null'

    def get_content_berita(self, link_berita, judul_berita):
        for idx, link in enumerate(link_berita):
            if link in self.processed_links:
                continue

            content = self.get_page_content(link)
            if content:
                article_soup = BeautifulSoup(content, "html.parser")
                article_content = article_soup.find('div', class_='post-content')
                article_content = article_content.get_text(strip=True) if article_content else 'null'
                article_detail_div = article_soup.find('div', class_='wrap__article-detail-info')
                if article_detail_div:
                    publish_date_element = article_soup.find('div', class_='wrap__article-detail-info').find('span', class_='text-secondary font-weight-normal')
                    publish_date = publish_date_element.get_text(strip=True) if publish_date_element else 'null'
                    publish_date = self.convert_publish_date(publish_date)
                    if publish_date == self.yesterday:
                        label = 'antaranews' if 'antaranews' in link else 'other'
                        self.save_to_csv(judul_berita[idx], link, article_content, publish_date, label)
                        self.processed_links.add(link)
                else:
                    logging.error(f"Could not find div with class 'wrap__article-detail-info' in article: {link}")
            else:
                logging.error(f"Failed to fetch article: {link}")

    def save_to_csv(self, headline, link, content, publish_date, label):
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.csv_columns)
            if file.tell() == 0:  # Menulis header jika file kosong
                writer.writeheader()
            data_row = {
                'periode': publish_date,
                'label': label,
                'headline': headline,
                'content': content,
                'link': link,
            }
            writer.writerow(data_row)
            file.flush()  # Flush file buffer to ensure data is written

    def scrape(self):
        if not os.path.exists(os.path.dirname(self.csv_file)):
            os.makedirs(os.path.dirname(self.csv_file))
        for page in range(1, self.pages + 1):
            judul_berita = self.get_judul_berita(page)
            link_berita = self.get_link_berita(page)
            self.get_content_berita(link_berita, judul_berita)


