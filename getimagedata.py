import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# Step 1: Open the browser and page
service = Service(r"c:\pyprojects\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://investorservice.cfmmc.com")
time.sleep(5)

# Step 2: Extract image as Base64 using canvas
js_script = """
var img = document.getElementById("imgVeriCode");
var canvas = document.createElement("canvas");
canvas.width = img.width;
canvas.height = img.height;
var ctx = canvas.getContext("2d");
ctx.drawImage(img, 0, 0, img.width, img.height);
return canvas.toDataURL("image/png").substring(22);  // Strip "data:image/png;base64,"
"""
img_base64 = driver.execute_script(js_script)

# Step 3: Save Base64 to file
with open("captcha_exact.png", "wb") as f:
    f.write(base64.b64decode(img_base64))

print("Exact CAPTCHA image saved as captcha_exact.png")
time.sleep(5)

driver.quit()
