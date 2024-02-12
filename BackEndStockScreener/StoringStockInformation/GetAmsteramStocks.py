import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_amsterdam_stocks(url):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    # Initialize an empty list to hold stock names
    stock_names = []

    # Wait for JavaScript to load content
    # You might need to add explicit waits here

    # Use WebDriverWait to wait for a specific element to be loaded
    try:
        # Wait for up to 10 seconds until an element with class 'stocks-name' is present
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'stocks-name'))
        WebDriverWait(driver, 10).until(element_present)

        # Now that the page is loaded, you can fetch the page source
        html = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        
        # Find all the <td> tags with the class 'stocks-name'
        stock_entries = soup.find_all('td', class_='stocks-name')

        for entry in stock_entries:
            # Each stock name is within an <a> tag inside the <td class="stocks-name">
            a_tag = entry.find('a')
            if a_tag:
                stock_name = a_tag.text.strip()  # Extracts the text from the <a> tag, which is the stock name
                stock_names.append(stock_name)

        print(stock_names)  # Or return stock_names if you want to use the list outside the function
        
        
    finally:
        driver.quit()  # Make sure to quit the driver to close the browser window
    
    # make a list of stock names in a txt file
    with open('amsterdam_stocks.txt', 'w') as file:
        for stock in stock_names:
            file.write(stock + '\n')
        
    return stock_names
    
get_amsterdam_stocks('https://live.euronext.com/en/markets/amsterdam/equities/list')