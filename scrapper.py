from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

driver = webdriver.Firefox()

driver.get("https://www.ceneo.pl/Laptopy")

time.sleep(3)

cookie = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div/div[1]/div/div[2]/button[1]")
cookie.click()

time.sleep(3)

# laptop = driver.find_element(By.CLASS_NAME, "go-to-product")
# laptop.click()

# time.sleep(5)

# driver.back()

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
    for link in links[:3]:
        driver.get(link)
        
        time.sleep(3)

        button = driver.find_element(By.CSS_SELECTOR, "li.page-tab.spec")
        button.click()

        product_name = driver.find_element(By.CLASS_NAME, "product-top__product-info__name")
        product_description = driver.find_element(By.CLASS_NAME, "product-top__product-info__tags")
        product_info = []
        spec_name = driver.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row__name")
        spec_value = driver.find_elements(By.CLASS_NAME, "product-spec__group__attributes__row__value")
        for i in range(len(spec_name)):
            print(spec_name[i].text + ': ' + spec_value[i].text)


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