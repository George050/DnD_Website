from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


spells = list()
classes = list()
races = list()
backgrounds = list()

op = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.get('https://dnd.su/spells/')  # ссылка на сайт с заклинаниями
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(0.5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

res_spells = driver.find_elements(By.CLASS_NAME, "cards_list__item")
for i in res_spells:
    spells.append((i.find_element(By.CLASS_NAME, "cards_list__item-name").get_attribute('innerHTML'),
                   i.find_element(By.CLASS_NAME, "cards_list__item-prefix").find_element(By.TAG_NAME, "span").
                   get_attribute("innerHTML")))

driver.get('https://dnd.su/class/') # ссылка на сайт с классами
sleep(0.5)
for i in driver.find_elements(By.XPATH, "/html/body/main/div/div/div/section[2]/div/div[1]/div"):
    for j in i.find_elements(By.CLASS_NAME, "article_title"):
        classes.append(j.get_attribute("innerHTML"))

driver.get('https://dnd.su/race/') # ссылка на сайт с расами
sleep(0.5)
for i in driver.find_elements(By.XPATH, "//*[@id='races']/div[1]/div"):
    for j in i.find_elements(By.CLASS_NAME, "article_title"):
        races.append(j.get_attribute("innerHTML"))

driver.get('https://dnd.su/backgrounds/') # ссылка на сайт с происхождениями
sleep(0.5)
for i in driver.find_elements(By.XPATH, "//*[@id='body']/main/div/div/div/section[2]/div[2]/div/div/div"):
    for j in i.find_elements(By.CLASS_NAME, "list-item-title"):
        backgrounds.append(j.get_attribute("innerHTML"))
driver.close()
backgrounds.sort()
spells = sorted(spells, key=lambda x: int(x[1]))
