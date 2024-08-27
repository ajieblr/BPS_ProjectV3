from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from app.controller.gpt_fix_antara_news_scrapping import AntaraScraper
from app.controller.serambi_scrapping import SerambiScraper
from app.model_handler.refactor_indobert_model import SentimentAnalysis
import time
from datetime import datetime as dt, timedelta

def cetak_kata():
    print("Cetak kata")
    time.sleep(3000)

# Muat variabel dari .env
load_dotenv()

from app import app

yesterday = dt.now() - timedelta(days=1)
start_date = yesterday
end_date = yesterday

# app\data\Merged_20240720_to_20240720.csv
model_path = 'app/model_handler/model_save/sentiment_models/indobert_model_tf_category.h5'
csv_file_path = f'app/data/Merged_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv'
output_file_path = f'app/model_handler/hasil_predik/Predict_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv'



def predict():
    sentiment_analysis = SentimentAnalysis(model_path, csv_file_path)
    sentiment_analysis.save_predictions(output_file_path)

def run_serambiScraper():
    yesterday = dt.now() - timedelta(days=1)
    start_date = yesterday
    end_date = yesterday

    scraper = SerambiScraper(start_date, end_date)
    df = scraper.scrape()
    print("Scraping completed. Data saved to CSV.")

def run_scrapper():
    scraper = AntaraScraper(pages=6, csv_file=f'./hasil_scrapping_antara/Antara_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv')
    scraper.scrape()

    time.sleep(15)

    scraper = SerambiScraper(start_date, end_date)
    df = scraper.scrape()
    print("Scraping completed. Data saved to CSV.")

def run_antarascrapper():
    scraper = AntaraScraper(pages=6, csv_file=f'./hasil_scrapping_antara/Antara_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv')
    scraper.scrape()

if __name__ == '__main__':
    try:
        scheduler = BackgroundScheduler()

        # Tambahkan job pertama

        scheduler.add_job(predict, 'cron', hour=21, minute=7) 
        scheduler.start()

        app.run(debug=True) # use_reloader=False
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()  
