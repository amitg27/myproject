from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
import base64
import os
from openai import OpenAI  # modern usage

# Initialize OpenAI client
client = OpenAI(api_key="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")  # OR use os.getenv("OPENAI_API_KEY")

# Setup Selenium
service = Service(r'c:\credentials\chromedriver.exe')  # adjust path if needed
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

# Step 1: Open the page and get CAPTCHA image
driver.get("https://investorservice.cfmmc.com")
time.sleep(5)

captcha_img = driver.find_element(By.ID, "imgVeriCode")
captcha_img.screenshot("captcha_raw.png")

# Step 2: Convert image to base64
with open("captcha_raw.png", "rb") as image_file:
    base64_img = base64.b64encode(image_file.read()).decode("utf-8")

# Step 3: Send to GPT-4 Vision
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Extract the CAPTCHA text from this image. Return only the text."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_img}"}}
            ]
        }
    ],
    max_tokens=10,
)

# Step 4: Print the result
captcha_text = response.choices[0].message.content.strip()
print("Extracted CAPTCHA Text:", captcha_text)

# Cleanup
driver.quit()
