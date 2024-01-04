from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

class Website:
    def __init__(self):
        self.xpath = "/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/form/div/div[1]/div/div[2]/div/div/div/fieldset/ul/li[1]/div/div/div/div/label/div/div/span[1]/div/span/div"
        self.url = "https://soc0.ru/"
        self.username = None
        self.password = None

        self.driver = webdriver.Chrome("C:\\chromedriver.exe")
        self.driver.get(self.url)

    def wait_for_element(self, xpath):
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            print("Loading took too much time!")
            return False

    def login(self):
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[2]/div/div[3]/section[2]/div/div/div[2]/div[2]/form/input").send_keys(
            self.username)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[2]/div/div[3]/section[2]/div/div/div[2]/div[3]/form/input").send_keys(
            self.password)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[2]/div/div[3]/section[2]/div/div/div[2]/button").click()

    def goto_quiz(self):
        # click economics section than click resume first quiz than clicks lets go button
        self.driver.get("https://soc0.ru/")
        self.wait_for_element("/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[3]/div/button")
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[3]/div/button").click()

    def answer(self):
        xpath_check_button = "/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div[2]/button"

        # while wrong text is present
        correct = 0
        index = 1
        do = True
        while do or (self.driver.find_element_by_xpath(xpath_check_button).text == "Check again") or (self.driver.find_element_by_xpath(xpath_check_button).text == "Check"):
            do = False
            print(self.xpath)
            self.driver.find_element_by_xpath(self.xpath).click()
            self.driver.find_element_by_xpath(xpath_check_button).click()

            if self.driver.find_element_by_xpath(xpath_check_button).text == "Next question":
                correct += 1
                print(f"Correct! Number: {correct}")

                replaceable = index
                index = 1
                self.xpath = self.xpath.replace("li[" + str(replaceable) + "]", "li[" + str(index) + "]")
                self.driver.find_element_by_xpath(xpath_check_button).click()
                do = True
            else:
                replaceable = index
                index += 1
                self.xpath = self.xpath.replace("li[" + str(replaceable) + "]", "li[" + str(index) + "]")
                self.driver.find_element_by_xpath(xpath_check_button).click()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Введите свой логин:")
    return "get_username"

def get_username(update, context):
    username = update.message.text
    context.user_data["username"] = username
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите свой пароль:")
    return "get_password"

def get_password(update, context):
    password = update.message.text
    context.user_data["password"] = password
    website = Website()
    website.username = context.user_data["username"]
    website.password = context.user_data["password"]
    website.login()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы успешно вошли. Начинаю прохождение квиза...")
    website.goto_quiz()
    website.answer()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Квиз завершен.")
    return ConversationHandler.END

def get_quiz(update, context):
    if "username" not in context.user_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, введите свой логин с помощью команды /start.")
        return ConversationHandler.END
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите свой пароль:")
    return "get_password" 
