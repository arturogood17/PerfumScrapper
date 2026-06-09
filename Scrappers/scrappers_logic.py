from dataclasses import dataclass
from bs4 import BeautifulSoup
from seleniumbase import sb_cdp
import utils
import time

def Parser_Druni(perfum_query: str):
    driver = webdriver.Chrome()
    driver.get(url_druni)

    #Primero tienes que buscar en la barra de búsqueda de druni. O se puede hacer en google tambien? 

    element = driver.find_element(By.CLASS_NAME, "dfd-card-link")
    element.click()
    assert perfum_query in driver.title

    driver.quit()

def Google_Search(product: str, store: str) -> any:
    print("Producto a buscar en tienda: ", product + " " + store)
    process_product: list[str] = product.split()
    query: str = ""
    for w in process_product:
        query += f"{w}+"
    query += store
    sb = sb_cdp.Chrome()
    url= "https://www.google.com/search?q=" + query
    try: 
        sb.open(url)
        sb.sleep(2)
        sb.click("#W0wltc")
        href = sb.get_attribute(".zReHs", "href")
        assert store.lower() in href 
        return href
    finally:
        sb.driver.quit()

# Por ahora funciona la búsqueda de Google, pero si se usa el modo headless, no funciona.
# Agregado a TODO