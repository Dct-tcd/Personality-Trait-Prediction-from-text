from selenium.webdriver import Chrome, Firefox, ChromeOptions, FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from Predict import Predictor
import datetime
import yaml

class FBScraper():
    def __init__(self, email, password, profile, status=4, scroll_time=7, browser='Chrome'):
        self.first_email = email
        self.first_password = password
        self.first_profile_url = profile
        self.number_status = status
        self.scroll_time = scroll_time
        self.name = profile.split("/")[3]

        self.set_browser(browser)
        self.dic_status = {}

    def set_browser(self, browser):
        if browser == 'Chrome':
            options = ChromeOptions()
            options.add_argument("--disable-notifications")
            self.browser = Chrome(options=options)
        elif browser == 'Firefox':
            profile = FirefoxProfile()
            profile.set_preference("dom.webnotifications.enabled", False)
            self.browser = Firefox(firefox_profile=profile)
        else:
            raise ValueError("Unsupported browser")

    def open_fb(self):
        url = 'http://www.facebook.com/'
        self.browser.get(url)

        email = self.browser.find_element(By.ID, 'email')
        password = self.browser.find_element(By.ID, 'pass')

        email.send_keys(self.first_email)
        password.send_keys(self.first_password)
        password.send_keys(Keys.RETURN)
    
    # def open_ln(self):
    #     from selenium import webdriver

    #     # Initialize ChromeDriver
    #     driver = webdriver.Chrome()
    #     import  time
    #     driver.get('https://www.linkedin.com')
    #     #locate email form by_class_name
    #     username = driver.find_element(By.ID, "session_key")
    #     # send keys(0) to simulate keystrokes
    #     username.send_keys ("tcd16112002@gmail.com")
    #     # sleep for 0.5 seconds
    #     # sleep(0.5)
    #     # locate password form by_class_name
    #     password = driver.find_element(By.ID,'session_password')
    #     # send keys() to simulate key strokes
    #     password.send_keys('Dev2002@')
    #     # sleep(0.5)
    #     # locate submit button by xpath
    #     sign_in_button = driver.find_element(By.XPATH,'//* [@type="submit"]')
    #     # . click() to mimic button click
    #     sign_in_button.click()
    #     sleep(10)
        
            
    def searched_statuses(self):
        self.browser.get(self.first_profile_url)
        time.sleep(self.scroll_time)

        print("--------Searching Post--------")
        all_posts = self.browser.find_elements(By.CSS_SELECTOR, "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs")
        dic_status = {}
        print(all_posts,"all posts")
        ind=0
        for post in all_posts:
            try:
                # post_time_element = post.find_element(By.CSS_SELECTOR, 'abbr')
                # post_time = post_time_element.get_attribute('title')
                # user_content_element = post.find_element(By.CSS_SELECTOR, "div.userContent")
                # para_elements = user_content_element.find_elements(By.CSS_SELECTOR, 'p')
                para_elements = post.text
                print( para_elements ,"post\n")
                if para_elements:
                    text = ''
                    text += para_elements + ' '
                    print('Number: ' + str(ind) + '\n' + 'Status: ' + text + '\n')

                    dic_status[ind] = text
                ind+=1   
            except Exception as e:
                print(f"Error processing post: {e}")

        print("Finished creating Statuses for: " + str(self.name))

        print("Final Dic: " + str(dic_status))
        
        with open('post.txt', 'a') as save:
            for text in dic_status.values():
                save.write(text + '\n')

    def predict_Face(self):
        p = Predictor()
        with open('post.txt', 'r') as f:
            mensaje = f.read()
            print(mensaje)

        r = p.predict([mensaje])
        return r
    
    def predict_vals(self):
        p = Predictor()
        with open('post.txt', 'r') as f:
            mensaje = f.read()
            print(mensaje)
            
        r = p.predicts([mensaje])
        return r

def ExecFace():
    with open('Fb_login_creds.yaml', 'r') as credlog:
        try:
            yread = yaml.load(credlog, Loader=yaml.FullLoader)
            password = yread['password']
            email = yread['email']
            profile = yread['profile_url']
        except yaml.YAMLError as exc:
            print(exc)

    FBS = FBScraper(email=email, password=password, profile=profile, browser='Chrome')
    FBS.open_fb()
    FBS.searched_statuses()
    p = FBS.predict_Face()
    
    print("Prediction: " + str(p))
    return p

 
def Grapher():
    with open('Fb_login_creds.yaml', 'r') as credlog:
        try:
            yread = yaml.load(credlog, Loader=yaml.FullLoader)
            password = yread['password']
            email = yread['email']
            profile = yread['profile_url']
        except yaml.YAMLError as exc:
            print(exc)

    FBS = FBScraper(email=email, password=password, profile=profile, browser='Chrome')
    op = FBS.predict_vals()
    
    print("Prediction: " + str(op))
    return op 
    

if __name__ == '__main__':
    ExecFace()
    Grapher()
