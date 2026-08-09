from dataclasses import dataclass
from bs4 import BeautifulSoup
from seleniumbase import sb_cdp, SB
from selenium.webdriver.common.keys import Keys
import os, json, time
import utils


def Parser_Douglas(perfum_query: str):
    with SB(uc= True, ad_block = True) as sb:
        sb.activate_cdp_mode(utils.stores.DOUGLAS)
        sb.sleep(4.2)
        sb.cdp.click('#usercentrics-root')
        sb.cdp.gui_press_keys("\t\t\t\t\t ")
        sb.type('input[role="searchbox"]', perfum_query)
        sb.click('button[data-testid="typeAhead-search-button"]')
        sb.sleep(3)
        div_element = f'a[role="link"]'
        element = sb.find_element(div_element)
        sb.assert_in("100 ml", element.text, msg="Requested product couldn't be find in the store.")
        sb.goto(utils.stores.DOUGLAS + element.href)
        sb.sleep(6)


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
    temp_file = os.getcwd() + "/temp_file.txt"
    with SB(uc= True, ad_block = True) as sb:
        sb.activate_cdp_mode(utils.stores.PRIMOR)
        sb.sleep(4)
        sb.cdp.click('button[class="ambar-btn-decline flex-1"]')
        sb.type('input[inputmode="search"]', perfum_query)
        sb.cdp.click('button[data-test="search-button"]')
        sb.cdp.click('a[data-test="result-link"]')
        text_attribute = sb.get_attribute('#product_addtocart_form > script:nth-child(7)', "outerHTML")
        ini_json= text_attribute.index('{"attribute')
        fin_json = text_attribute.index('          )')
        product_data = json.loads(text_attribute[ini_json: fin_json]) #Es un diccionario

Parser_Primor("acqua di gio profondo eau de parfum")
# Parser_Druni("acqua di gio profondo eau de parfum")
# Parser_Douglas("acqua di gio profondo eau de parfum")

# En el modo headless, funciona a veces sí, a veces no. Quizá pueda reintentar 2 veces a ver si funciona,
# si no, usar el modo normal que no da probelmas
# Agregado a TODO