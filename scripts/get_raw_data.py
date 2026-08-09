from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

driver.get("https://impds.nic.in/sale/")

wait = WebDriverWait(driver, 20)

fps_items = driver.find_elements(By.XPATH, "//*[contains(text(),'1585')]")

print("FPS Elements Found:", len(fps_items))

first_fps = fps_items[0]

print("Clicking:", first_fps.text)

first_fps.click()

input("Did the right panel update? Press Enter...")

driver.quit()

fps_items = driver.find_elements(By.XPATH, "//*[contains(text(),'1585')]")

print("FPS Elements Found:", len(fps_items))

for i, fps in enumerate(fps_items[:5]):
    print(i + 1, fps.text)

input("Press Enter to close...")

driver.quit()