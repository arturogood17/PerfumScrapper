from dataclasses import dataclass
from bs4 import BeautifulSoup
from seleniumbase import sb_cdp, SB
from selenium.webdriver.common.keys import Keys
import html, json, time
import utils

def Parser_Druni(perfum_query: str):
    sb = sb_cdp.Chrome()
    element : any = ""
    href : str = Google_Search(sb, perfum_query, utils.stores.DRUNI)
    sb.open(href)
    sb.click('button:contains("Rechazar")')
    time.sleep(2)
    element = sb.get_text('span[x-text*="precioRef +"]')
    elements = element.split("€/")
    price, volume = elements[0], elements[1]
    print("DRUNI")
    print("Price:", price)
    print("Vol:", volume)
    print("-------------")
    sb.quit()

def Parser_Primor(perfum_query: str):
    sb = sb_cdp.Chrome()
    element : any = ""
    href : str = Google_Search(sb, perfum_query, utils.stores.PRIMOR)
    sb.open(href)
    sb.click('button:contains("Rechazar")')
    time.sleep(2)
    element: str = sb.get_text('script:contains("function initConfigurableSwatchOptions_112406()")')
    firs_index = element.find('{"attributes"')
    final_index = element.find("priceFormat")
    element = element[firs_index:final_index - 2] + "}"
    dict_json: dict[str,str] = json.loads(element)
    id: str = ""
    for ids in dict_json["attributes"]["854"]["options"]:
        if ids["label"] == "100":
            id = ids["products"][0]
            break
    price: str = dict_json["optionPrices"][id]["finalPrice"].get("amount")
    print("PRIMOR")
    print("Price:", price)
    print("Vol: 100 ml")
    print("-------------")
    sb.quit()


def Parser_Douglas(perfum_query: str):
    with SB(uc=True, ad_block= True) as sb:
        sb.activate_cdp_mode(utils.stores.DOUGLAS)
        sb.sleep(4)
        sb.cdp.click('#usercentrics-root')
        sb.cdp.gui_press_keys("\t\t\t\t\t ")
        sb.type('input[role="searchbox"]', perfum_query)
        sb.click('button[data-testid="typeAhead-search-button"]')
        sb.sleep(5)
        

def Google_Search(sb, product: str, store: str) -> any:
    print(f"Producto a buscar en {store.upper()}: {product}")
    process_product: list[str] = product.split()
    query: str = ""
    for w in process_product:
        query += f"{w}+"
    query += store
    url= "https://www.google.com/search?q=" + query
    sb.activate_cdp_mode(url)
    sb.uc_gui_click_captcha(frame="iframe", retry=False, blind=False)
    sb.sleep(2)
    sb.reconnect(0.1)
    if sb.is_element_present("#W0wltc"):
        sb.click("#W0wltc")
    sb.wait_for_element(".zReHs")
    href = sb.get_attribute(".zReHs", "href")
    assert store.lower() in href
    return href


# Parser_Primor("acqua di gio profondo eau de parfum")
# Parser_Druni("acqua di gio profondo eau de parfum")
Parser_Douglas("acqua di gio profondo eau de parfum")

# En el modo headless, funciona a veces sí, a veces no. Quizá pueda reintentar 2 veces a ver si funciona,
# si no, usar el modo normal que no da probelmas
# Agregado a TODO