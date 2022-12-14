#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import random
import string
import time
import re
from datetime import datetime
from datetime import timedelta
from typing import Any

import pyfiglet
import requests as requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from email_validate import validate

# Variable for program
directory_script = os.path.abspath('')
index_i = 0

USE_DEL_PROXY = False
ALL_MAILS_PATH = directory_script + '/mails.txt'
GOOD_MAILS_PATH = directory_script + '/good.txt'
BAD_MAILS_PATH = directory_script + '/bad.txt'
PROXY_LIST_PATH = directory_script + '/proxy_list.txt'
LEN_PASSWORD = 12
MAX_LEN_NICKNAME = 14
CREATIVE = ['i liked you',
            'Girls for one night',
            'Register and call me',
            'Hot girl are looking for sex for 1 night',
            'Looking for a man 20-45',
            'Horny girls are waiting for you',
            'Hi handsome i after a shower wanna see?']
MAIN_URL = 'https://newdatingshere.life/?u=dfrkte4&o=v8dpkz7&t='

PROGRAM_NAME = 'CHATZY'
SERVER = 'REPLIT 1'
PUSH_CHAT_ID = '-1001703526876'
ERROR_CHAT_ID = '-1001656173344'
BOT_ID = '5130975486:AAF4z76SYX1GrzsbLOPp5UWOPGB90VKcBzw'

# Color setting for _color_log function
header = '\033[95m'
green = '\033[32m'
red = '\033[31m'
yellow = '\033[33m'
normal = '\033[0m'
red_bold = '\033[1m\033[4m\033[31m'
green_bold = '\033[1m\033[4m\033[32m'


# Color log
def _color_log(text, color):
    d = datetime.now()
    color_text = '{}[%Y-%m-%d %H:%M:%S] - {} {}'.format(color, str(text), normal)
    return print(d.strftime(color_text))


# Generate nickname
def _get_nick() -> str:
    r = requests.get('https://randomuser.me/api/?nat=us')
    json_text = json.loads(r.text)
    results = json_text['results'][0]['name']['last']
    nick = results.lower() + str(random.randint(10, 99)) + ''.join(
        random.choice(string.ascii_lowercase) for _ in range(3))
    while len(nick) > MAX_LEN_NICKNAME:
        nick = nick[1:]
    return nick


# Finding an element and acting on it(click, search, clear)
def _search_and_action_in_browser(locator: str, locator_text: str, action: str, exception_text: str, waiting_time: int):
    visible = False
    count = 0
    while not visible:
        if count >= waiting_time:
            raise Exception(exception_text)
        if locator == 'css_selector':
            search = driver.find_elements(By.CSS_SELECTOR, locator_text)
        elif locator == 'xpath':
            search = driver.find_elements(By.XPATH, locator_text)
        else:
            raise Exception('Unknown locator, select or CSS_SELECTOR or XPATH')

        if len(search) != 0:
            time.sleep(0.5)
            if action == 'click' and locator == 'css_selector':
                driver.find_element(By.CSS_SELECTOR, locator_text).click()
            elif action == 'click' and locator == 'xpath':
                driver.find_element(By.XPATH, locator_text).click()

            elif action == 'clear' and locator == 'css_selector':
                driver.find_element(By.CSS_SELECTOR, locator_text).clear()
            elif action == 'clear' and locator == 'xpath':
                driver.find_element(By.XPATH, locator_text).clear()

            elif action == 'search' and locator == 'css_selector':
                driver.find_element(By.CSS_SELECTOR, locator_text)

            elif action == 'search' and locator == 'xpath':
                driver.find_element(By.XPATH, locator_text)
            visible = True
        else:
            time.sleep(1)
            count += 1


def _send_text_in_browser(locator: str, locator_text: str, text: str, exception_text: str) -> None:
    visible = False
    count = 0
    while not visible:
        if count >= 20:
            raise Exception(exception_text)

        if locator == 'css_selector':
            search = driver.find_elements(By.CSS_SELECTOR, locator_text)
        elif locator == 'xpath':
            search = driver.find_elements(By.XPATH, locator_text)
        else:
            raise Exception('Unknown locator, select or CSS_SELECTOR or XPATH')

        if len(search) != 0:
            time.sleep(1)
            if locator == 'css_selector':
                driver.find_element(By.CSS_SELECTOR, locator_text).send_keys(text)
            elif locator == 'xpath':
                driver.find_element(By.XPATH, locator_text).send_keys(text)
            else:
                raise Exception('Unknown locator, select or CSS_SELECTOR or XPATH')
            visible = True
        else:
            time.sleep(1)
            count += 1


# Close under windows
def _close_under_windows() -> None:
    while len(driver.window_handles) == 1:
        time.sleep(1)
    if len(driver.window_handles) > 1:
        for _ in range(len(driver.window_handles) - 1):
            main_page = driver.window_handles[-1]
            driver.switch_to.window(main_page)
            driver.close()
            time.sleep(0.5)
        main_page = driver.window_handles[0]
        driver.switch_to.window(main_page)
    time.sleep(0.5)


def _url_shorten(url: str) -> Any:
    data = {'url': url,
            'from': '',
            'a': 'add'}
    headers = {'Accept': 'application/xml, text/xml, */*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Referer': 'https://u.to/',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'}
    r = requests.post('https://u.to/', data=data, headers=headers)
    message = r.text
    if len(re.findall(r'_blank\\\">(https://u\.to/[A-Za-z0-9_-]+)</a>', r.text)) != 0:
        short_url = re.search(r'_blank\\\">(https://u\.to/[A-Za-z0-9_-]+)</a>', r.text).group(1)
        return short_url, message
    else:
        return 'BAD', message


def _del_bad_proxy_and_rewrite(all_proxy_list: list, proxy_url: str, path_proxy_list: str) -> None:
    if USE_DEL_PROXY:
        new_proxy_list = []
        for i in all_proxy_list:
            if i != proxy_url:
                new_proxy_list.append(i)
            else:
                pass
        with open(path_proxy_list, 'w') as fp:
            for item in new_proxy_list:
                fp.write("%s\n" % item)
    else:
        pass


def _send_msg_to_tg(msg: str, chat_id: str) -> None:
    text = f'Program {PROGRAM_NAME} Server - {SERVER}. {msg}'
    url = f'https://api.telegram.org/bot{BOT_ID}/sendMessage?chat_id={chat_id}&text={text}'
    requests.get(url)


def main() -> None:
    global driver, index_i
    # Get working variable
    try:
        nick = _get_nick()
    except:
        _send_msg_to_tg('Не удалось получить ник', ERROR_CHAT_ID)
        raise Exception('Failed to get nickname')

    # Start setup webdriver
    try:
        start_time = time.monotonic()
        options = webdriver.ChromeOptions()
        options.add_argument("--mute-audio")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('blink-settings=imagesEnabled=false')
        options.add_argument('--disable-notifications')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--enable-webgl-draft-extensions")
        options.add_argument("--ignore-gpu-blocklist")

        # Don't save password
        options.add_experimental_option('prefs',
                                        {
                                            'credentials_enable_service': False,
                                            'profile': {'password_manager_enabled': False},
                                            'intl.accept_languages': 'en,en_US'
                                        }
                                        )

        driver = webdriver.Chrome(
            #executable_path=directory_script + '/chromedriver',
            options=options
        )
        # List of blocked image formats
        img_format_list = [
            '*.svg*', '*.png*', '*.jpg*', '*.jpeg*', '*.bmp*', '*.gif*',
            '*.tif*', '*.ico*', '*google-analytics.com*'
        ]
        # Do not upload images or websites
        driver.execute_cdp_cmd('Network.setBlockedURLs', {'urls': img_format_list})
        driver.execute_cdp_cmd('Network.enable', {})

        end_time = time.monotonic()
        text = 'Time download webdriver - {}'.format(timedelta(seconds=end_time - start_time))
        _color_log(text, yellow)

        # Connect to the site and fill in the data
        for _ in range(10):
            # Read user's files
            all_mail_list = open(ALL_MAILS_PATH).read().splitlines()
            good_mail_list = open(GOOD_MAILS_PATH).read().splitlines()
            bad_mail_list = open(BAD_MAILS_PATH).read().splitlines()
            proxy_list = open(PROXY_LIST_PATH).read().splitlines()

            if len(all_mail_list) < 10:
                _send_msg_to_tg(f'Список с адресами закончился', ERROR_CHAT_ID)
            # Delete duplicates
            verified_list = set(all_mail_list) - set(good_mail_list) - set(bad_mail_list)
            verified_list = list(verified_list)

            # Load random proxy
            random_proxy = random.choice(proxy_list)
            if len(re.findall(r'https?', random_proxy)) == 0:
                try:
                    driver.set_page_load_timeout(15)
                    driver.get(f'https://{random_proxy}')
                except:
                    _del_bad_proxy_and_rewrite(proxy_list, random_proxy, PROXY_LIST_PATH)
                    _color_log(f'Не удалось загрузить прокси сайт - {random_proxy}', red)
                    break
            else:
                try:
                    driver.set_page_load_timeout(15)
                    driver.get(random_proxy)
                except:
                    _del_bad_proxy_and_rewrite(proxy_list, random_proxy, PROXY_LIST_PATH)
                    _color_log(f'Не удалось загрузить прокси сайт - {random_proxy}', red)
                    break
            time.sleep(0.5)
            # Enter website address
            try:
                driver.set_page_load_timeout(20)
                _send_text_in_browser('xpath', '//input', 'http://www.chatzy.com/', 'Not found INPUT')
                time.sleep(0.5)
                driver.find_element(By.XPATH, '//input').send_keys(Keys.ENTER)

                time.sleep(3)
                if len(driver.find_elements(By.XPATH, '//button[@id="reload-button"]')) != 0:
                    driver.find_element(By.XPATH, '//button[@id="reload-button"]').click()
                    time.sleep(1)
            except:
                _del_bad_proxy_and_rewrite(proxy_list, random_proxy, PROXY_LIST_PATH)
                _color_log(f'На прокси сайте не удалось найти поле для ввода. Прокси - {random_proxy}', red)
                break
            # Find logo Chatzy
            try:
                _search_and_action_in_browser('xpath', '//img[@alt="Chatzy Logo"]', 'search', 'Not open CHATZY', 15)
                _color_log(f'Загрузили CHATZY. Прокси - {random_proxy}', header)
                time.sleep(1)
                if len(driver.find_elements(By.XPATH, '//h1[@style="color:red;"]')) != 0:
                    _del_bad_proxy_and_rewrite(proxy_list, random_proxy, PROXY_LIST_PATH)
                    _color_log(f'Сайт {random_proxy} не поддерживает js', red)
                    break
            except:
                _del_bad_proxy_and_rewrite(proxy_list, random_proxy, PROXY_LIST_PATH)
                _color_log(f'Не удалось загрузить CHATZY. Прокси - {random_proxy}', red)
                break
            # Find button accept
            if len(driver.find_elements(By.CSS_SELECTOR, '#__cpsButtonOk')) != 0:
                driver.find_element(By.CSS_SELECTOR, '#__cpsButtonOk').click()
                time.sleep(0.5)

            message_box = '//label[contains(text(),"Message:")]/following-sibling::span/textarea'
            name = '//label[contains(text(),"Your name:")]/following-sibling::span/input'
            title = '//label[contains(text(),"Title/subject:")]/following-sibling::span/input'
            invite_email = '//label[contains(text(),"Invite email:")]/following-sibling::span/input'
            send_button = '//input[@value="Create my chat"]'

            # Enter nickname
            _send_text_in_browser('xpath', name, nick, 'Not found NAME input')
            time.sleep(0.5)
            # Clear message box
            driver.find_element(By.XPATH, title).send_keys(Keys.CONTROL, 'a')
            time.sleep(0.5)
            driver.find_element(By.XPATH, title).send_keys(Keys.DELETE)
            # Enter title
            random_creative = random.choice(CREATIVE)
            elem = driver.find_element(By.XPATH, title)
            js_add_text_to_input = """
            var elm = arguments[0], txt = arguments[1];
            elm.value += txt;
            elm.dispatchEvent(new Event('change'));
            """
            driver.execute_script(js_add_text_to_input, elem, random_creative)
            time.sleep(0.5)

            # Validate email address
            good_validate_emails_list = []
            while len(good_validate_emails_list) != 5:
                for i in verified_list:
                    if len(good_validate_emails_list) == 5:
                        break
                    validation = validate(email_address=i,
                                          check_format=True,
                                          check_blacklist=True,
                                          check_dns=True,
                                          dns_timeout=10,
                                          check_smtp=False,
                                          smtp_debug=False)
                    if validation:
                        good_validate_emails_list.append(str(i))
                    else:
                        with open(BAD_MAILS_PATH, 'a') as fp:
                            fp.write("%s\n" % i)

            elements_str = ' '.join(good_validate_emails_list)
            # Clear email box
            driver.find_element(By.XPATH, invite_email).send_keys(Keys.CONTROL, 'a')
            time.sleep(0.5)
            driver.find_element(By.XPATH, invite_email).send_keys(Keys.DELETE)
            # Enter email addresses
            elem = driver.find_element(By.XPATH, invite_email)
            js_add_text_to_input = """
            var elm = arguments[0], txt = arguments[1];
            elm.value += txt;
            elm.dispatchEvent(new Event('change'));
            """
            driver.execute_script(js_add_text_to_input, elem, elements_str)
            time.sleep(0.5)

            words = ['fuck me', 'love', 'sex', 'anal', 'milf']
            fonts = ['3-d', '3x5', '5x7', '5x8', '6x9', '6x10', 'arrows', 'avatar', 'banner']

            # Create random creative
            creative_list = ''.join(random_creative)
            new_creative = ''
            for i in creative_list:
                new_creative = new_creative + i

            shorten_url = MAIN_URL + PROGRAM_NAME + f'_' + random_creative.replace(' ', '_')
            shorten_url_list = _url_shorten(shorten_url)
            shorten_url = shorten_url_list[0].replace('https://', '')
            answer = shorten_url_list[1]

            # Create text for email
            rand_font = random.choice(fonts)
            result = pyfiglet.figlet_format(random.choice(words), font=rand_font)
            emoji_list = ['🥰', '😘', '💋', '💛', '🧡', '💜', '💙', '💚', '💞', '💕', '💝', '💘', '💖', '💗', '💓', '💔', ]
            random_emoji = random.choice(emoji_list) * 3
            letters = string.ascii_lowercase
            rand_string = ''.join(random.choice(letters) for _ in range(random.randint(6, 15)))

            text = f'{new_creative} {random_emoji} {shorten_url}&{rand_string} {random_emoji}\n{result}'
            if len(text) > 600:
                _color_log(f'Текст более 600 симолов - {text}\n {words} {fonts}', red)

            # Waiting for the site to load
            try:
                _search_and_action_in_browser('xpath', message_box, 'click', 'Not found message box', 10)
                time.sleep(0.5)
                # Clear message box
                driver.find_element(By.XPATH, message_box).send_keys(Keys.CONTROL, 'a')
                time.sleep(0.5)
                driver.find_element(By.XPATH, message_box).send_keys(Keys.DELETE)
            except:
                _color_log(f'Не удалось очистить message_box. Прокси - {random_proxy}', red)
                break

            # Add random text to message box
            try:
                elem = driver.find_element(By.XPATH, message_box)
                js_add_text_to_input = """
                var elm = arguments[0], txt = arguments[1];
                elm.value += txt;
                elm.dispatchEvent(new Event('change'));
                """
                driver.execute_script(js_add_text_to_input, elem, text)
                time.sleep(0.5)
            except:
                _color_log(f'Не удалось ввести текст в message_box. Прокси - {random_proxy}', red)
                break

            try:
                # Click to create room
                _search_and_action_in_browser('xpath', send_button, 'click', 'Do not find CREATE CHAT button', 5)
                time.sleep(1)
                if len(driver.find_elements(By.XPATH, '//img[@src="/elements/icon32/error.png"]')) != 0:
                    _del_bad_proxy_and_rewrite(proxy_list, random_proxy, PROXY_LIST_PATH)
                    _color_log(f'Не удалось отправить сообщения. Прокси - {random_proxy}', red)
                    try:
                        text_error = driver.find_element(By.XPATH, '(//div/p)[2]').text
                        _color_log(text_error, red)
                    except:
                        _color_log(f'Не получилось получить текст с ошибкой', red)
                    break
            except:
                _color_log(f'Не удалось нажать на кнопу Создать Комнату', red)

            room_create_xpath = '//h2[contains(text(),"Room Created")]'
            # Looking for a message about creating a room
            try:
                _search_and_action_in_browser('xpath', room_create_xpath, 'search', 'Do not create Room', 10)
            except:
                _del_bad_proxy_and_rewrite(proxy_list, random_proxy, PROXY_LIST_PATH)
                _color_log(f'Не удалось найти room_create_xpath', red)
                break

            if len(driver.find_elements(By.XPATH, room_create_xpath)) > 0:
                if shorten_url != 'BAD':
                    _color_log(f'Ответ от сервера сокращения ссылок - {shorten_url}', header)
                    time.sleep(0.5)
                    try:
                        _search_and_action_in_browser('xpath', '//input[@value="OK"]', 'click', 'Not found OK btn', 10)
                    except:
                        _color_log(f'Не дождались кнопки ОК после создания комнаты', red)
                    text = f'{random_creative} https://{shorten_url}'
                    try:
                        _send_text_in_browser('xpath', '//form/span/input', text, 'Do not found INPUT')
                    except:
                        _color_log(f'Не получилось ввести сообщение в комнате', red)
                    time.sleep(0.5)
                    try:
                        _search_and_action_in_browser('xpath', '(//form/a/img)[5]', 'click', 'Do not found SEND BTN',
                                                      10)
                    except:
                        _color_log(f'Не получилось отправить сообщение в комнату', red)
                    index_i += 5
                    _color_log(f'Send {str(index_i)} mail\'s', green)
                    _send_msg_to_tg(f'Отправили {str(index_i)} сообщений', PUSH_CHAT_ID)
                    # Write sent emails to a file
                    with open(GOOD_MAILS_PATH, 'a') as fp:
                        for item in good_validate_emails_list:
                            fp.write("%s\n" % item)
                else:
                    _color_log(f'Failed to get shortened link. Message - {answer}', red)
                    _send_msg_to_tg(f'Не удалось сократить ссылку. MSG - {answer}', ERROR_CHAT_ID)

            else:
                _color_log('Не удалось отправить сообщение', red)
                _send_msg_to_tg(f'Не удалось отправить сообщение', ERROR_CHAT_ID)
                break
    except:
        pass
    
    finally:
        driver.close()
        driver.quit()


while True:
    main()
