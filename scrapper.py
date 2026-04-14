from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time
import re

driver = webdriver.Firefox()

driver.get("https://www.ceneo.pl/Laptopy")

time.sleep(3)

cookie = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div[1]/div/div[2]/button[1]")
cookie.click()

time.sleep(3)

# potencjalnie wez to zmien pozniej tak, aby pobieralo tylko linki / jeden element 
# z linkiem zamiast 5 do tego samego produktu
next_btn = 1
database_laptops = []

while next_btn:
    next_btn = driver.find_elements(By.CLASS_NAME, "pagination__next")
    next_page = next_btn[0].get_attribute("href") if next_btn else None

    laptops = driver.find_elements(By.CLASS_NAME, "go-to-product")
    links = [l.get_attribute("href") for l in laptops][::5]

    print(links)
    #later change this for loop, so it iterates through len(links)
    for i in range(len(links)):
        driver.get(links[i])
        
        time.sleep(3)

        button = driver.find_element(By.CSS_SELECTOR, "li.page-tab.spec")
        button.click()

        table_elements_sum = []
        product_info = []

        product_name = driver.find_element(By.CLASS_NAME, "product-top__product-info__name")
        product_description = driver.find_element(By.CLASS_NAME, "product-top__product-info__tags")

        #this part can be separate function later
        tbodies = driver.find_elements(By.CSS_SELECTOR, "tbody")
        for tbody in tbodies:
            rows = tbody.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row")
            table_elements_sum.append(len(rows))

        #extracts laptop product 
        product_spec_headers = driver.find_elements(By.CLASS_NAME, "product-spec__group__header")
        product_spec_names = driver.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row__name")
        product_spec_values = driver.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row__value")

        product_data = {"id": i}

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




        time.sleep(3)
    driver.get(next_page)
    next_btn = False



#product_name
#product_description
#info_about_product
#   brand
#   model
#   procesor
#       rodzina_procesora
#       model_procesora
#       liczba_rdzeni_procesora
#   ekran
#       przekatna_ekranu
#       rozdzielczosc_ekranu
#       czestotliwosc_odswiezania
#   pamiec_RAM
#       pamiec_ram
#       typ_pamieci_ram??
#   dysk_twardy
#       rodzaj dysku
#       pojemnosc_dysku_twardego
#   karta_graficzna
#       producent_karty_graficznej
#       model_kart_graficznej
#       ilosc_pamieci_RAM
#       rodzaj_karty_graficznej
#   komunikacja
#       zlacza
#       komunikacja
#   fizyczne
#       wysokosc
#       szerokosc
#       glebokosc
#       waga
#       kolor
#       material
#   oprogramowanie
#       system_operacyjny
#   dodatkowe_informacje
#       funkcje_dodatkowe
#       multimedia
#       kod_producenta
#       typ_urzadzenia???
#company_offers
#   [company_name, rating_rate, rating_count, price]

time.sleep(3)

driver.quit()