from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

def get_the_data(id, password):
	driver = webdriver.Chrome()
	'''  ensures that the Chrome browser window stays open even after the WebDriver object is closed '''
	options = Options()
	options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(options= options)
	actions = ActionChains(driver)

	''' enter the kbs system '''
	driver.get("https://kampus.izu.edu.tr/login")

	driver.find_element(By.NAME, "username").send_keys(id)
	passw = driver.find_element(By.NAME, "password")
	passw.send_keys(password)
	passw.send_keys(Keys.RETURN)

	''' enter the grade page '''
	time.sleep(5)
	grade_url = driver.find_element(By.LINK_TEXT, "Sınav Sonuçları")
	grade_url.click()

	''' extracting data from course table by order '''
	time.sleep(5)
	incele_buttons = driver.find_elements(By.LINK_TEXT, "İncele")
	for button in incele_buttons:
		button.click()
		actions.send_keys(Keys.PAGE_DOWN).perform()
		time.sleep(1)

	course_table = []

	grade_columns = grade_table.find_element(By.CLASS_NAME, )
	grade_table = driver.find_element(By.CSS_SELECTOR, ".table.table-striped.table-bordered.table-hover")
	rows = grade_table.find_elements(By.TAG_NAME, "tr")
	for row in rows:
		columns = row.find_elements(By.TAG_NAME, "td")
		row_data = [column.text for column in columns]
		course_table.append(row_data)
	return driver, course_table,

