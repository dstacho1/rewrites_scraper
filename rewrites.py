from bs4 import BeautifulSoup
import smtplib
import config

from selenium import webdriver

"""
TO DO:
    - look into storing pw safely
    - scheduling the scrip using cronjobs
    - hosting the script on desktop, heroku, or a raspberry pi?
    - search seperately for beginner and intermediate level essays

    - did this appear
"""


def rewrites_login():
    # open and login to rewrites.
    username = config.EMAIL_ADDRESS
    password = config.PASSWORD_RE  # how to store pw safely, environmental variables?, keyring? bit 64?

    url = "https://www.rewrites.me/users/sign_in"

    driver = webdriver.Chrome("/Users/damian/Downloads/chromedriver")

    driver.get(url)

    # login to the site using credentials
    driver.find_element_by_id("user_email").send_keys(username)
    driver.find_element_by_id("user_password").send_keys(password)
    driver.find_element_by_name("commit").click()

    # navigate to url and get the html code
    driver.get("https://www.rewrites.me/")
    html = driver.page_source

    return html


def rewrites_scrape(html):
    # scrapes the html and returns the amount of post items currently on the site.
    soup = BeautifulSoup(html, "lxml")

    post_items_list = soup.find_all("div", class_="postItem")  # learn to check for only beginner tag posts
    return len(post_items_list)


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


def make_email(post_items_currently):
    # only send the email if there are 2 or more essays to grade
    if post_items_currently > 2:
        subject = "{} essays to check".format(post_items_currently)
        msg = "There are currently {} essays on https://www.rewrites.me/".format(post_items_currently)
        send_email(subject, msg)


post_items_currently = rewrites_scrape(rewrites_login())
make_email(post_items_currently)
