# serambi_scraper.py
from bs4 import BeautifulSoup as soup
import pandas as pd
from tqdm import tqdm
from datetime import datetime as dt, timedelta
import requests
import math
import os

class SerambiScraper:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.fake_user_agent = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
        }

    def scrape(self):
        titles = []
        links = []
        label_berita = []
        dates = []
        contents = []

        current_date = self.start_date
        total_days = (self.end_date - self.start_date).days + 1

        with tqdm(total=total_days, desc="Processing", unit="day") as pbar:
            while current_date <= self.end_date:
                tgl_awal = current_date.day
                bln = current_date.month
                thn = current_date.year
                halaman = 1
                ttl_hal = 1

                while halaman <= ttl_hal:
                    url = f'https://aceh.tribunnews.com/index-news/nanggroe?date={thn}-{bln:02d}-{tgl_awal:02d}&page={halaman}'
                    html = requests.get(url, headers=self.fake_user_agent).text
                    bsobj = soup(html, 'lxml')
                    data = bsobj.select('ul.lsi li.ptb15')
                    jmlh_hal = bsobj.find('div', {'class': 'pt10 pb10'})
                    ttl_hal = math.ceil(int(jmlh_hal.find('b').text) / 20) if jmlh_hal and jmlh_hal.find('b') else 1

                    for i in range(len(data)):
                        try:
                            html_cntn = requests.get(data[i].find('h3').find('a').get('href'), headers=self.fake_user_agent).text
                            bsobj_cntn = soup(html_cntn, 'lxml')
                            isi = bsobj_cntn.find('div', class_='side-article txt-article multi-fontsize editcontent')
                            contents.append(isi.text.strip() if isi else 'null')
                            
                            link = data[i].find('h3').find('a').get('href')
                            label = 'tribunnews' if 'tribunnews' in link else 'other'
                            label_berita.append(label)
                            titles.append(data[i].find('h3').find('a').get('title').strip())
                            links.append(data[i].find('h3').find('a').get('href'))
                            dates.append(f'{thn}-{bln:02d}-{tgl_awal:02d}')
                        except AttributeError:
                            pass
                        if i == 19:
                            break
                    halaman += 1
                pbar.update(1)
                current_date += timedelta(days=1)

        df = pd.DataFrame({
            'periode': dates,
            'label': label_berita,
            'headline': titles,
            'content': contents,
            'link': links,
        })

        output_file = f'./hasil_scrapping_serambi/Serambi_{self.start_date.strftime("%Y%m%d")}_to_{self.end_date.strftime("%Y%m%d")}.csv'
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8')

        return df
