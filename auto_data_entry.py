import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# Endpoint URL 
houserental_url = "https://appbrewery.github.io/Zillow-Clone/" # Example
googleforms_url = "YOUR GOOGLE FORMS LINK"

# Find specific data in Zillow Clone Site return address, price, link-list
def find_properties_data(url):
    response = requests.get(url).text
    webpage = BeautifulSoup(response, "html.parser")
    all_properties = webpage.select(selector="#grid-search-results > ul > li")

    address_list = [item.find("address").get_text().strip() for item in all_properties]
    price_list = [item.find("span", {"data-test":"property-card-price"}).get_text().split("/")[0].strip("+") for item in all_properties]
    link_list = [item.find("a").get("href") for item in all_properties]
    
    return address_list, price_list, link_list

# Entry data to google forms
def fill_forms(addr:list, price:list, link:list):
    counter = 0
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(googleforms_url)
    time.sleep(3)

    for index in range(len(addr)):
        address_response = driver.find_element(By.XPATH, value='YOUR GOOGLE FORMS QUESTION XPATH')
        address_response.send_keys(addr[index])

        price_response = driver.find_element(By.XPATH, value='YOUR GOOGLE FORMS QUESTION XPATH')
        price_response.send_keys(price[index])

        link_response = driver.find_element(By.XPATH, value='YOUR GOOGLE FORMS QUESTION XPATH')
        link_response.send_keys(link[index])

        submit_button = driver.find_element(By.XPATH, value='YOUR GOOGLE FORMS QUESTION XPATH')
        submit_button.click()
        time.sleep(1)
        
        counter +=1

        if counter < len(addr):
            reentry_link = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            reentry_link.click()
        else:
            print(f"All {counter} entries are completed")
            driver.quit()

addr_list, price_list, link_list = find_properties_data(houserental_url)
fill_forms(addr_list, price_list, link_list)