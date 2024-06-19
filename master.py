import subprocess
import schedule
import time
from os import listdir

def run_scraper(script):
    result = subprocess.run(['python', script], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{script} success")
    else:
        print(f"{script} error: {result.stderr}")

def job():
    scrapers = listdir("Scrapers")
    
    for scraper in scrapers:
        run_scraper(scraper)

schedule.every().day.at("09:00").do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)