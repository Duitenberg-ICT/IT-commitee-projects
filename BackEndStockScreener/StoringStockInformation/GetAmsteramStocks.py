import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
def get_amsterdam_stocks(url):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    stock_names = []

    try:
        while True:
            # Wait for the stock symbols to load on the page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div/div/div[1]/div[2]/div/main/section/div[3]/div/div/div[1]/div[2]/div[4]/div/a[2]'))
            )

            # Fetch page source and parse with BeautifulSoup
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            stock_entries = soup.find_all('td', class_='stocks-symbol')

            for entry in stock_entries:
                stock_symbol = entry.text.strip()
                stock_names.append(stock_symbol)

            # Check if the "Next" button is present
            try:
                next_button = driver.find_element(By.ID,'#stocks-data-table-es_next')
                if "disabled" not in next_button.get_attribute("class"):
                    print("Clicking 'Next' button")
                    next_button.click()
                    # Wait a moment for the page to load. Adjust the wait time as necessary.
                    WebDriverWait(driver, 10).until(
                        EC.staleness_of(next_button)
                    )
                    # Optionally, wait for the next set of stocks to appear by checking for a known element to reappear
                else:
                    # If the "Next" button is disabled, break the loop
                    print("No more pages")
                    break
                # Wait for the stock symbols to load on the page
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'stocks-symbol'))
                )   
            
            except Exception as e:
                print(f"Failed to click 'Next' button or 'Next' button not found: {e}")
                break
    finally:
        driver.quit()

        # Folder path where the file will be saved
    folder_path = 'StoringStockInformation'
    file_name = 'amsterdam_stocks.txt'
    full_path = os.path.join(folder_path, file_name)

    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Write the list of stock names to the file within the folder
    with open(full_path, 'w') as file:
        for stock in stock_names:
            file.write(stock + '\n')
            
    print(stock_names)
    return stock_names

# Example URL - Replace with the actual URL if it's different
get_amsterdam_stocks('https://live.euronext.com/en/markets/amsterdam/equities/list')
