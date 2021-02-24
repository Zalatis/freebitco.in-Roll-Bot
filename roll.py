# coding=utf8
from time import sleep
from time import time
from datetime import timedelta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from countdown import countdown
import json
import sys
import os
from os import system
system('title '+ 'FreeBitco.in Bot' if os.name == 'nt' else '')
system('Mode con cols=70 lines=15' if os.name == 'nt' else '')

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

username = data['Username']
password = data['Password']
acapi = data['Anti-Captcha-API-KEY']
width = data['Width']
height = data['Height']
maximized = data['Maximized']

"""Get Exception Code
try:
    # code here
except: # catch *all* exceptions
    e = sys.exc_info()[0]
"""

def acp_api_send_request(driver, message_type, data={}):
    message = {
		# this receiver has to be always set as antiCaptchaPlugin
        'receiver': 'antiCaptchaPlugin',
        # request type, for example setOptions
        'type': message_type,
        # merge with additional data
        **data
    }
    # run JS code in the web page context
    # preceicely we send a standard window.postMessage method
    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))

def createBrowser():
    options = webdriver.ChromeOptions()
    options.add_extension("extensions/anticaptcha-plugin_v0.50.zip")
    options.add_extension("extensions/Adblock.zip")
    # Enable the option below to block images
    # options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    while True:
        try:
            if maximized == "oui" or maximized == "Oui" or maximized == "Yes" or maximized == "yes" or maximized == "o" or maximized == "y" or maximized == "true" or maximized == "True" or maximized == "1":
                options.add_argument("--start-maximized")
            break
        except:
            break
        else:
            break
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    # options.add_argument("--proxy-server=http://" + proxy)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    while True:
        try:
            driver.set_window_size(width, height)
            break
        except ValueError:
            break
    return driver

# Bot is starting here
def start_bot():
    # Opening main page
    while True:
        try:
            driver = createBrowser()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Ouverture de la page ...")
            driver.get('https://freebitco.in/')
            acp_api_send_request(driver,'setOptions',{'options': {'antiCaptchaApiKey': acapi}})
            break
        except:
            print('Erreur, ré-ouverture...')
            driver.quit()
            sleep(5)
            continue
    handles_before = driver.window_handles
    # Accept cookies
    while True:
        try:
            cookies = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'cc_btn_accept_all')))
            print('Fermeture du popup des cookies')
            cookies.click()
            break
        except:
            print('Erreur cookies')
            break
    # Close notifications popup
    while True:
        try:
            notifications = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'pushpad_deny_button')))
            print('Fermeture du popup notifications')
            notifications.click()
            break
        except:
            print('Erreur popup notifications')
            break
    while True:
        try:
            driver.execute_script("""document.querySelector("li.login_menu_button").click();""")
            print('Ouverture de la page de connexion')
            break
        except:
            print("Erreur lors de l'ouverture page de connexion")
            pass
    sleep(1)
    # Fill login form
    while True:
        try:
            print('Saisie de l\'utilisateur')
            input_username = driver.find_element_by_name('btc_address')
            input_username.send_keys(username)
            sleep(1)
            print('Saisie du mot de passe')
            input_password = driver.find_element_by_id('login_form_password')
            input_password.send_keys(password)
            sleep(1)
            print('Envoi du formulaire de connexion')
            login_btn = driver.find_element_by_id('login_button')
            login_btn.click()
            break
        except:
            print("Erreur lors du formulaire de connexion")
            break
    # Wait page to end loading
    while True:
        try:
            page_loaded = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, 'free_play_form_button')))
            break
        except:
            print("Le chargement de la page a mis plus de 1 minute, peut être un problème lié au site.")
            pass
    # Scroll and click on recaptcha
    while True:
        try:
            driver.execute_script("""window.scrollTo(0, document.body.scrollHeight);""")
            WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "/html/body/div[2]/div/div/div[8]/div[2]/div/div[2]/div[2]/form/div/div/div[1]/iframe")))
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
            break
        except:
            print('Erreur lors du clicque sur le recaptcha')
            break
    sleep(1)
    while True:
        try:
            load_recaptcha = WebDriverWait(driver, 300).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'recaptcha-checkbox-spinner')))
            driver.switch_to.default_content()
            challenge = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div')))
            if challenge.is_displayed():
                print('Lancement de la résolution du captcha')
                sleep(1)
                driver.switch_to.default_content()
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                element = WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'solved_flag')))
            else:
                driver.switch_to.default_content()
                element = WebDriverWait(driver, 300).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'solved_flag'))) # No Anti-Captcha Use
                driver.switch_to.default_content()
            break
        except:
            print("Le captcha a mis plus de 5 minutes à être résolu, peut être un problème lié au site.")
            sleep(2)
            driver.quit()
            sleep(5)
            start_bot()
    print("Captcha résolu !")
    sleep(1)
    while True:
        try:
            roll_btn = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, 'free_play_form_button')))
            roll_btn.click()
            print("Fin du roll !")
            break
        except:
            print("Impossible de trouver le bouton de roll")
            sleep(2)
            driver.quit()
            sleep(5)
            start_bot()
    sleep(1)
    driver.quit()
    print("Il est temps d'attendre 1h00")
    print('Temps restant :')
    countdown(mins=60, secs=00)
    sleep(2)

if __name__ == '__main__':
    start_bot()
    os.execv(sys.executable, ['python'] + sys.argv)