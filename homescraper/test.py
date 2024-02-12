from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

driver = webdriver.Chrome()

driver.get("https://www.zillow.com/rental-manager/price-my-rental/results/12929-plover-st-lakewood-oh-44107/")

time.sleep(10)

driver.quit()