import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

def enter_kbs(id, password, url):
	'''  ensures that the Chrome browser window stays open even after the WebDriver object is closed '''
	options = Options()
	options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(options= options)
	actions = ActionChains(driver)

	''' enter the kbs system '''
	driver.get(url)

	Username = driver.find_element(By.NAME, "username")
	Username.send_keys(id)

	password = driver.find_element(By.NAME, "password")
	password.send_keys(password)
	password.send_keys(Keys.RETURN)

	''' enter the grade page '''
	time.sleep(2)
	grade_url = driver.find_element(By.LINK_TEXT, "Sınav Sonuçları")
	grade_url.click()
	time.sleep(2)

	incele_buttons = driver.find_elements(By.LINK_TEXT, "İncele")
	for button in incele_buttons:
		button.click()
		actions.send_keys(Keys.PAGE_DOWN).perform()
		time.sleep(1)

	grade_table = driver.find_element(By.CSS_SELECTOR, "table.table-striped.table-bordered.table-hover")
	rows = grade_table.find_elements(By.TAG_NAME, "tr")

	return driver, rows

def get_info(rows):
	dersler = {}  # her ders için ayrı liste tutan sözlük
	aktif_ders = None

	for row in rows:
		columns = row.find_elements(By.TAG_NAME, "td")
		row_data = [col.text.strip() for col in columns]

		if not row_data or all(cell == '' for cell in row_data):
			continue

		if 'Detaylı Bilgi' in row_data[0]:
			continue

		# Eğer bu satır bir ders satırıysa
		if len(row_data) == 7 and 'İncele' in row_data[6]:
			ders_adi = row_data[1]
			aktif_ders = ders_adi
			dersler[aktif_ders] = []  # yeni ders için boş liste oluştur

		# Eğer not satırıysa ve bir aktif ders varsa
		elif ('Vize 1' or "Final 1" or "Vize 2" or "Kısa Sınav 1" or "Proje 1" in row_data[0]):
			sinav_turu = row_data[0]
			sinav_puani = row_data[1]
			dersler[aktif_ders].append(sinav_turu)
			dersler[aktif_ders].append(sinav_puani)

	for ders, notlar in dersler.items():
		print(f"\n📘 {ders}")
		i = 0
		for i in range(0, len(notlar), 2):
			sinav_adi = notlar[i]
			sinav_puani = notlar[i+1]
			print(f" - {sinav_adi}: {sinav_puani}")

	return dersler
