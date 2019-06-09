import schedule
import time
import scraper



schedule.every().day.at("05:43").do(scraper.scrape())

while True:
    schedule.run_pending()
    time.sleep(60)