import yaml
import time
import requests
from body import get_info, sign_in, check_for_updates

# Telegram bot function to send messages
def send(message, token, chat_id):
    message_url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(message_url)

if __name__ == '__main__':

	# Load configuration from YAML file
    with open('to_change.yaml', 'r') as file:
        info = yaml.safe_load(file)

    driver = sign_in(info['id'], info['password'], info['url'])
    course = get_info(driver)

	# Continuously check for updates
    while True:
        time.sleep(info['interval'])
        message, status, course = check_for_updates(driver, course)

        if status:
            send(message, info['token'], info['chat_id'])
