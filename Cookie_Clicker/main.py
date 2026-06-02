import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
driver=webdriver.Chrome(options=chrome_options)

driver.get("https://ozh.github.io/cookieclicker/")

try:
    WebDriverWait(driver,10).until(
        EC.element_to_be_clickable((By.ID,"langSelect-EN"))
    ).click()
except TimeoutException:
    print("Language Selection not found")

try:
    big_cookie = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "bigCookie"))
    )
except TimeoutException:
    print("The big cookie element was not found within 10 seconds.")

upgrade_time=time.perf_counter()
program_start=time.perf_counter()

while True:
    big_cookie = driver.find_element(By.ID, "bigCookie")
    big_cookie.click()

    if (time.perf_counter()-upgrade_time)>=5:
        max_price = float('-inf')
        max_product = None
        products = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
        for product in products:
            product_price=product.find_element(By.CSS_SELECTOR,".content .price").text.strip()
            price = int(product_price.replace(",", ""))

            if price>max_price:
                max_price=price
                max_product=product

        if max_product:
            driver.execute_script(
                "arguments[0].click();",
                max_product
            )
        upgrade_time = time.perf_counter()

    if (time.perf_counter()-program_start)>=300:
        total_cookie = driver.find_element(By.ID, "cookies").text
        print(total_cookie)
        driver.quit()
        break
