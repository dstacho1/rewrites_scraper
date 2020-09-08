from bs4 import BeautifulSoup
import smtplib
import config

from selenium import webdriver

"""
TO DO:
    - look into storing pw safely
    - scheduling the scrip using cronjobs
    - make the script accept any and all beginner level essays
"""


def rewrites_login():
    # open and login to rewrites.
    username = config.EMAIL_ADDRESS
    password = config.PASSWORD_RE  # how to store pw safely, environmental variables?, keyring? bit 64?

    url = "https://www.rewrites.me/users/sign_in"

    driver = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')
    

    driver.get(url)

    # login to the site using credentials
    driver.find_element_by_id("user_email").send_keys(username)
    driver.find_element_by_id("user_password").send_keys(password)
    driver.find_element_by_name("commit").click()

    # navigate to url and get the html code
    driver.get("https://www.rewrites.me/articles/waiting")    #"https://www.rewrites.me/"
    #driver.find_element_by_css_selector("a[href=topic-waiting]").click() # try to get to waiting tab
    driver.find_element_by_xpath('//a[contains(@href,"#topic-waiting")]').click() # try to get to waiting tab = GREAT SUCCESS! 
    html = driver.page_source

    return html


class Scrape:

    def __init__(self, html):

        # scrapes the html and returns the amount of post items currently on the site.
        self.soup = BeautifulSoup(html, "lxml")

        self.post_items_list = self.soup.find_all("div", class_="postItem")
        self.post_items_len = len(self.post_items_list)

        # scrapes for the exact number of beginner and intermediate posts currently on the site
        self.intermediate_count, self.beginner_count, self.advanced_count = 0, 0, 0
        for div in self.post_items_list:
            if div.find("a", "label").text == "intermediate":
                self.intermediate_count += 1
            elif div.find("a", "label").text == "beginner":
                self.beginner_count += 1
            elif div.find("a", "label").text == "advanced":  # double check this html!!!!!
                self.advanced_count += 1


def send_email(subject, msg):
    # send myself an email with the amount of post items currently on the site.
    try:
        server = smtplib.SMTP("smtp.gmail.com:587")  # define a client session object
        server.ehlo()  # establish a connection with the server
        server.starttls()  # put SMTP connection in TLS (Transport Layer Security) mode
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)  # get credentials
        message = "Subject: {}\n\n{}".format(subject, msg)
        server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, message)  # sender, reciever, message
        server.quit()
        print("Success: Email Sent!")
    except:
        print("Email failed to send.")


def email_data():
    return Scrape(rewrites_login())


def make_email():
    data = email_data()

    # only send the email if there is 1 or more essays to grade
    if data.post_items_len < 1:
        subject = "{} essays to check".format(data.post_items_len)
        msg = "There are currently {} essays on https://www.rewrites.me\n{} are beginner essays, {} are intermediate essays, and {} are advanced essays".format(data.post_items_len, data.beginner_count, data.intermediate_count, data.advanced_count)
        send_email(subject, msg)


make_email()
