from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()

'''  ensures that the Chrome browser window stays open even after the WebDriver object is closed '''
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options= options)
actions = ActionChains(driver)
''' enter the kbs system '''
driver.get("https://kampus.izu.edu.tr/login")

Username = driver.find_element(By.NAME, "username")
Username.send_keys("030722088@std.izu.edu.tr")

password = driver.find_element(By.NAME, "password")
password.send_keys("Narin.78")
password.send_keys(Keys.RETURN)

''' enter the grade page '''
time.sleep(5)
grade_url = driver.find_element(By.LINK_TEXT, "Sınav Sonuçları")
grade_url.click()
time.sleep(5)

incele_buttons = driver.find_elements(By.LINK_TEXT, "İncele")
for button in incele_buttons:
	button.click()
	actions.send_keys(Keys.PAGE_DOWN).perform()
	time.sleep(1)
course_table = []

grade_table = driver.find_element(By.CSS_SELECTOR, ".table.table-striped.table-bordered.table-hover")
rows = grade_table.find_elements(By.TAG_NAME, "tr")
for row in rows:
	columns = row.find_elements(By.TAG_NAME, "td")
	row_data = [column.text for column in columns]
	course_table.append(row_data)

for data in course_table:
    print(data)
