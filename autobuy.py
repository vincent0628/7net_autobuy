#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from selenium import webdriver
# driver.get(URL)


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from PIL import Image, ImageEnhance
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


driver = webdriver.Chrome('./chromedriver')
URL="https://shop.7-11.com.tw/shop/rui005.faces?kw=%FDa%FD%FD%FD%FD%FDa%FDZ%FD%FD&ID=101200203573&pi=0"
URL="https://shop.7-11.com.tw/shop/rui005.faces?ID=101200116642&kw=%E8%88%92%E8%B7%91&pi=0"
driver.get(URL)
wait = WebDriverWait(driver, 10)

try:
    wait.until(EC.presence_of_element_located((By.ID, "item_qty")))
except TimeoutException:
    print("Time exceeded!")

select = Select(driver.find_element_by_id('item_qty'))
select.select_by_value("5")

element = wait.until(EC.element_to_be_clickable((By.ID, 'icon_impay')))
element.click()

element = wait.until(EC.element_to_be_clickable((By.ID, 'GM_loginBtn')))
element.click()


driver.find_element_by_id("mobile").send_keys('')
driver.find_element_by_id("passwd_d").send_keys('')

try:
    img = wait.until(EC.presence_of_element_located((By.ID, "imgVerify")))
except TimeoutException:
    print("Time exceeded!")
with open('Logo.png', 'wb') as file:
    imgVerify = driver.find_element_by_id('imgVerify')
    file.write(imgVerify.screenshot_as_png)
    
code = None 
correct_len = 0
while code == None or not correct_len==5:
    origin_img = Image.open('Logo.png')  # 图像增强，二值化
    sharp_img = ImageEnhance.Contrast(origin_img).enhance(1.0)
    sharp_img.save("Logo_enhance.png")
    sharp_img.load()  # 对比度增强
    code = pytesseract.image_to_string(sharp_img).strip()
    code = re.match(r'^([\s\d]+)$', code)
    print(code)
    if code is None:
        origin_img = sharp_img
        continue
    correct_len = len(str(code.group(0)))
    # print(code.group(0))
    # print(correct_len)
driver.find_element_by_id("verifyCode").send_keys(str(code.group(0)))
element = wait.until(EC.element_to_be_clickable((By.ID, 'loginBtn')))
element.click()


print("login already")
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'Next')))
element.click()
print("購物明細")


driver.find_element_by_css_selector("input[type='radio'][value='02']").click()
driver.find_element_by_css_selector("input[type='radio'][value='199430']").click()

select = Select(driver.find_element_by_id('couponP5'))
try:
    select.select_by_index(1)
except Exception:
    pass

element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME , 'Next')))
element.click()


