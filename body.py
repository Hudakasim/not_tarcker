import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# Log in to the student system
def sign_in(id, password, url):
    options = Options()
	# Run browser in headless (invisible) mode
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)

	# Open login page & wait till the page load
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    username_input = wait.until(EC.element_to_be_clickable((By.NAME, "username")))
    username_input.send_keys(id)

    password_input = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(2)

    return driver

# Extract information
def get_info(driver):

	actions = ActionChains(driver)

	# Go to grade page
	actions.send_keys(Keys.PAGE_UP).perform()
	grade_url = driver.find_element(By.LINK_TEXT, "Sınav Sonuçları")
	grade_url.click()
	time.sleep(2)

	# Click to all "Incele" buttons to reveal details
	incele_buttons = driver.find_elements(By.LINK_TEXT, "İncele")
	for button in incele_buttons:
		button.click()
		actions.send_keys(Keys.PAGE_DOWN).perform()
		time.sleep(1)

	# Get complicated raw informatin table
	grade_table = driver.find_element(By.CSS_SELECTOR, "table.table-striped.table-bordered.table-hover")
	rows = grade_table.find_elements(By.TAG_NAME, "tr")

	# Dictionary to store courses_dict and their grades
	courses_dict = {}
	active_course = None
	# Extract the useful informations and add it to the dictionary
	for row in rows:
		columns = row.find_elements(By.TAG_NAME, "td")
		row_data = [col.text.strip() for col in columns]

		if not row_data or all(cell == '' for cell in row_data):
			continue

		if 'Detaylı Bilgi' in row_data[0]:
			continue

		# Course row
		if len(row_data) == 7 and 'İncele' in row_data[6]:
			course_name = row_data[1]
			active_course = course_name
			courses_dict[active_course] = []

		# Grade row
		elif active_course and row_data[0] in ["Vize 1", "Final 1", "Vize 2", "Kısa Sınav 1", "Proje 1"]:
			grade_type = row_data[0]
			grade = row_data[1]
			courses_dict[active_course].append(grade_type)
			courses_dict[active_course].append(grade)

	return courses_dict

# Check for any updates in grades
def check_for_updates(driver, courses_dict):
	message = ""
	status = False

	# Refresh the page to fetch new data
	new_courses_dict = get_info(driver)
	time.sleep(2)

	# Compare old and new grades
	for course in new_courses_dict:
		if course not in courses_dict:
			courses_dict[course] = []
		old = courses_dict.get(course)
		new = new_courses_dict[course]
		new_grades_for_this_course = []

		for sinav_turu, sinav_notu in zip(new[::2], new[1::2]):
			if sinav_turu not in old and sinav_turu in ["Vize 1", "Final 1", "Vize 2", "Kısa Sınav 1", "Proje 1"]:
				if sinav_notu.strip() != "":
					new_grades_for_this_course.append(f"- {sinav_turu}: {sinav_notu}")
					old.append(sinav_turu)
					status = True
		if new_grades_for_this_course:
			message += f"{course}\n ----------------------------\n"
			message += "\n".join(new_grades_for_this_course)
			message += "\n\n"

	return message, status, courses_dict

# read old data from file (if exists)
def load_old_data(filename="grades.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# write updated data to file
def save_old_data(data, filename="grades.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
