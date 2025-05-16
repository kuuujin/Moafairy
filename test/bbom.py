from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)

browser.get('https://www.ppomppu.co.kr/hotdeal/')
actions = browser.find_element(By.CSS_SELECTOR , 'body')

Itemselector  = "div.wrapper > div.contents > div.container > div > div.hotDeal_goods > ul > li > p > a:nth-child(2)"
Priceselector  = "div.wrapper > div.contents > div.container > div > div.hotDeal_goods > ul > li > p > span:nth-child(1)"
Linkselector = "div.wrapper > div.contents > div.container > div > div.hotDeal_goods > ul > li > div.view > a"

def crawling(count):
    items, prices, links = [], [], []

    for _ in range(count):
        for i in browser.find_elements(By.CSS_SELECTOR, Itemselector):
            items.append(i.text)
        for i in browser.find_elements(By.CSS_SELECTOR, Priceselector):
            prices.append(i.text)
        for i in browser.find_elements(By.CSS_SELECTOR, Linkselector):
            links.append(i.get_attribute("href"))
        actions.send_keys(Keys.END)
        time.sleep(2)

    return items, prices, links



def main():
    items, prices, links = crawling(2)
    print("가져온 상품 수: ", len(items))
    for i in range(len(items)):
        print("상품: ", items[i])
        print("가격: ", prices[i])
        print("주소: ", links[i])
        print('\n')
    
if __name__=="__main__":
    main()