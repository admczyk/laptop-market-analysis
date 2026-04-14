from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

def check_if_store_exists(stores, domain):
    if len(stores) == 0:
        return True
    for store in stores:
        if store["domain"] == domain:
            return False
    return True


driver = webdriver.Firefox()

driver.get("https://www.ceneo.pl/Laptopy")

time.sleep(3)

cookie = driver.find_element(By.CLASS_NAME, "js_cookie-consent-agree")
cookie.click()

time.sleep(3)

next_btn = True
tm = 4

product_id = 1
store_id = 1
products = []
offers = []
stores = []

while next_btn:
    next_btn = driver.find_elements(By.CLASS_NAME, "pagination__next")
    next_page = next_btn[0].get_attribute("href") if next_btn else None

    laptops = driver.find_elements(By.CLASS_NAME, "go-to-product")
    links = [l.get_attribute("href") for l in laptops][::5]

    for i in range(len(links)):
        driver.get(links[i])
        
        time.sleep(tm)

        el = driver.find_elements(By.ID, "notifications-toast")
        popup_visible = any(e.is_displayed() for e in el)

        if popup_visible:
            decline = driver.find_element(By.CLASS_NAME, "button.js_notification_no")
            decline.click()
            tm = 1

        # store_product_offers = []

        all_stores = driver.find_elements(By.CLASS_NAME, "product-offer__store-with-product")
        for store in all_stores:
            store_logo = store.find_elements(By.CLASS_NAME, "store-logo")

            if not store_logo:
                continue

            domain = store_logo[0].find_element(By.CSS_SELECTOR, "img").get_attribute("alt")

            # will be using it later, when writing logic for calculating mean product rating
            # store_offer_link = store_logo[0].get_attribute("href")
            # store_product_offers.append(store_offer_link)

            price = store.find_element(By.CLASS_NAME, "price").get_attribute("textContent")

            # later make it separate function
            if check_if_store_exists(stores, domain): 
                dot_idx = domain.find(".")
                store_name = domain[:dot_idx]

                store_rating = store.find_elements(By.CLASS_NAME, "screen-reader-text")
                if not store_rating:
                    store_rating = 0
                    store_reviews_count = 0
                else:
                    store_rating = store_rating[0].get_attribute("textContent")
                    comma_idx = store_rating.find(",")
                    store_rating = store_rating[comma_idx - 1:comma_idx + 2]

                    store_reviews_count = store.find_element(By.CLASS_NAME, "link").get_attribute("textContent")
                    store_reviews_count = store_reviews_count[:-7]

                store_data = {
                    "id": store_id,
                    "name": store_name,
                    "domain": domain,
                    "rating_score": store_rating,
                    "rating_count": store_reviews_count
                }

                stores.append(store_data)
                store_id += 1

            s = [s["id"] for s in stores if s["domain"] == domain]
            print(s)
            
            offer_data = {
                "product_id": product_id,
                "store_id": s[0],
                "price": price,
                "currency": "PLN"
            }

            offers.append(offer_data)

        time.sleep(tm)

        button = driver.find_element(By.CSS_SELECTOR, "li.page-tab.spec")
        button.click()

        table_elements_sum = []

        #this part can be separate function later
        tbodies = driver.find_elements(By.CSS_SELECTOR, "tbody")
        for tbody in tbodies:
            rows = tbody.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row")
            table_elements_sum.append(len(rows))

        #extracts laptop product 
        product_spec_headers = driver.find_elements(By.CLASS_NAME, "product-spec__group__header")
        product_spec_names = driver.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row__name")
        product_spec_values = driver.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row__value")

        product_data = {"id": product_id}

        start = 0
        end = 0
        for i in range(len(product_spec_headers) + 1):
            start = end
            end += table_elements_sum[i]
            if i == 0 or i == len(product_spec_headers):
                for key, value in zip(product_spec_names[start:end], product_spec_values[start:end]):
                    product_data[key.text] = value.text
            else:
                sub_attributes = {}
                for key, value in zip(product_spec_names[start:end], product_spec_values[start:end]):
                    key = key.text
                    value = value.text

                    if "?" in key:
                        key = key[:-2]

                    if ", " in value:
                        value = value.split(", ")
                    
                    sub_attributes[key] = value
                product_data[product_spec_headers[i].text] = sub_attributes

        products.append(product_data)
    
        product_id += 1
        time.sleep(2)
    driver.get(next_page)
    next_btn = False

print(stores)
print(offers)
print(products)




with open("./data/raw/products_data.JSON", "w", encoding="utf-8") as file:
    json.dump(products, file, ensure_ascii=False, indent=4)

with open("./data/raw/offers_data.JSON", "w", encoding="utf-8") as file:
    json.dump(offers, file, ensure_ascii=False, indent=4)

with open("./data/raw/stores_data.JSON", "w", encoding="utf-8") as file:
    json.dump(stores, file, ensure_ascii=False, indent=4)


time.sleep(3)

driver.quit()