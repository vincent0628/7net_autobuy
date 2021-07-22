#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from selenium import webdriver
# driver.get(URL)
MOBILE = ""
PASSWORD = ""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageEnhance
import pytesseract
import re
import time
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


driver = webdriver.Chrome('./chromedriver')
URL="https://shop.7-11.com.tw/shop/rui005.faces?kw=%FDa%FD%FD%FD%FD%FDa%FDZ%FD%FD&ID=101200203573&pi=0"
# URL="https://shop.7-11.com.tw/shop/rui005.faces?ID=101200116642&kw=%E8%88%92%E8%B7%91&pi=0"
driver.get(URL)
wait = WebDriverWait(driver, 3)

try:
    wait.until(EC.presence_of_element_located((By.ID, "item_qty")))
except TimeoutException:
    print("Time exceeded!")
    
    
select = Select(driver.find_element_by_id('item_qty'))

candidate = 12

while True:
    try:
        # print(candidate)
        select.select_by_index(str(candidate))
        break
    except Exception:
        if candidate > 1:
            candidate -= 1
        else:
            candidate = 12
            time.sleep(1)
            driver.refresh()

element = wait.until(EC.element_to_be_clickable((By.ID, 'icon_impay')))
element.click()

element = wait.until(EC.element_to_be_clickable((By.ID, 'GM_loginBtn')))
element.click()


driver.find_element_by_id("mobile").send_keys(MOBILE)
driver.find_element_by_id("passwd_d").send_keys(PASSWORD)

try:
    img = wait.until(EC.presence_of_element_located((By.ID, "imgVerify")))
except TimeoutException:
    print("Time exceeded!")
    
with open('Logo.png', 'wb') as file:
    imgVerify = driver.find_element_by_id('imgVerify')
    file.write(imgVerify.screenshot_as_png)
    
while not driver.current_url == "https://shop.7-11.com.tw/shop/rui006.faces" :
    try :
        code = None 
        correct_len = 0
        count = 0
        origin_img = Image.open('Logo.png')  # 图像增强，二值化
        sharp_img = ImageEnhance.Contrast(origin_img).enhance(2.0)
        
        # while code == None or not correct_len==5:
            # sharp_img = ImageEnhance.Contrast(sharp_img).enhance(1.5)
        sharp_img.save("Logo_enhance.png")
        sharp_img.load()  # 对比度增强
        code = pytesseract.image_to_string(sharp_img).strip()
        code = re.match(r'^([\s\d]+)$', code)
        print(code)
        correct_len = len(str(code.group(0)))
        driver.find_element_by_id("verifyCode").send_keys(str(code.group(0)))
        element = wait.until(EC.element_to_be_clickable((By.ID, 'loginBtn')))
        element.click()
        time.sleep(1)
    except :
        with open('Logo.png', 'wb') as file:
            imgVerify = driver.find_element_by_id('imgVerify')
            file.write(imgVerify.screenshot_as_png)
        print("write new file")
        time.sleep(2)

            
print("login already")
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'Next')))
element.click()
print("購物明細")


select = Select(driver.find_element_by_id('couponP5'))
try:
    select.select_by_index(1)
except Exception:
    pass

time.sleep(1)
# radio1 = wait.until(EC.element_to_be_clickable((By.ID , 'radio1')))
# radio1.click()
# radio2 = wait.until(EC.element_to_be_clickable((By.ID , 'store_opt4')))
# radio2.click()
driver.find_element_by_css_selector("input[type='radio'][value='02']").click()
driver.find_element_by_css_selector("input[type='radio'][value='199430']").click()



try:
    element = wait.until(EC.element_to_be_clickable((By.ID , 'next')))
    element.click()
except Exception:
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'Next')))
    element.click()
    
time.sleep(1)
try:
    element = wait.until(EC.element_to_be_clickable((By.ID , 'next')))
    element.click()
except Exception:
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'Next')))
    element.click()

