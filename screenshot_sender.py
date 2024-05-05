from time import sleep 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import smtplib
import ssl
import schedule
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

today = datetime.today().strftime("%Y-%m-%d")
yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
startOfTheMonth = datetime.today().strftime("%Y-%m-01")
yesterdayDay = datetime.strftime(datetime.now() - timedelta(1), '%d')
if int(yesterdayDay) < 10:
    yesterdayDay = yesterdayDay[1]

def emailsend(manager, client, sum):
    try:
        subject = "הכנסות כולל החזרות עד אתמול: " + client
        body = 'הכנסות כולל החזרות עד אתמול: ' + sum
        sender_email = "YOUR EMAIL"
        receiver_email = manager
        password = "YOUR PASSOWRD"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        filename = str(today)+"-"+client+".png"
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        message.attach(part)
        text = message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.zoho.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        print('email from ' + client + ' send to: ' + manager)
    except:
        print('email to ' + client + ' not sent')



def wordpress(manager, client, url, email, password):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1750, 770)
    browser.maximize_window()
    browser.implicitly_wait(15)
    browser.get(url)
    sleep(1)
    browser.find_element(By.ID, 'user_login').send_keys(email)
    browser.find_element(By.ID, 'user_pass').send_keys(password)
    browser.find_element(By.ID, 'wp-submit').click()
    sleep(2)
    try:
        browser.find_element(
            By.CSS_SELECTOR, '#wpbody-content > div.wrap.woocommerce > div.wp-die-message > a').click()
    except:
        print(client+" no need")
    sleep(2)
    browser.execute_script(
        "document.getElementsByClassName('stats_range')[0].scrollIntoView()")
    sleep(2)
    browser.save_screenshot(str(today)+"-"+client+".png")
    sleep(2)
    amount = float(browser.find_element(
        By.CSS_SELECTOR, '#poststuff > div > div.inside.chart-with-sidebar > div.chart-sidebar > ul.chart-legend > li:nth-child(1) > strong > span').text.replace('₪', '').replace(',', ''))
    returns = float(browser.find_element(
        By.CSS_SELECTOR, '#poststuff > div > div.inside.chart-with-sidebar > div.chart-sidebar > ul.chart-legend > li:nth-child(7) > strong > span').text.replace('₪', '').replace(',', ''))
    sum = amount + returns
    sum = str(sum)
    browser.close()
    print('wordpress ' + client + ' success')
    emailsend(manager, client, sum)


def wordpressdr(manager, client, url, urldr, email, password):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1750, 770)
    browser.maximize_window()
    browser.implicitly_wait(15)
    browser.get(url)
    sleep(1)
    browser.find_element(By.ID, 'user_login').send_keys(email)
    browser.find_element(By.ID, 'user_pass').send_keys(password)
    browser.find_element(By.ID, 'wp-submit').click()
    sleep(2)
    browser.get(urldr)
    sleep(2)
    try:
        browser.find_element(
            By.CSS_SELECTOR, '#wpbody-content > div.wrap.woocommerce > div.wp-die-message > a').click()
    except:
        print(client+" no need")
    sleep(2)
    browser.execute_script(
        "document.getElementsByClassName('stats_range')[0].scrollIntoView()")
    browser.save_screenshot(str(today)+"-"+client+".png")
    sleep(1)
    amount = float(browser.find_element(
        By.CSS_SELECTOR, '#poststuff > div > div.inside.chart-with-sidebar > div.chart-sidebar > ul.chart-legend > li:nth-child(1) > strong > span').text.replace('₪', '').replace(',', ''))
    returns = float(browser.find_element(
        By.CSS_SELECTOR, '#poststuff > div > div.inside.chart-with-sidebar > div.chart-sidebar > ul.chart-legend > li:nth-child(7) > strong > span').text.replace('₪', '').replace(',', ''))
    sum = amount + returns
    sum = str(sum)
    browser.close()
    print('wordpress ' + client + ' success')
    emailsend(manager, client, sum)


def shopify(manager, client, url, email, password):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.implicitly_wait(15)
    browser.get(url)
    sleep(1)
    browser.find_element(By.ID, 'account_email').send_keys(email)
    sleep(2)
    browser.find_element(By.ID, 'account_email').click()
    sleep(5)
    browser.find_element(By.XPATH, '//*[@id="account_lookup"]/button').click()
    sleep(2)
    browser.find_element(By.ID, 'account_password').send_keys(password)
    sleep(3)
    browser.find_element(
        By.XPATH, '//*[@id="login_form"]/div[2]/ul/button').click()
    sleep(5)
    browser.find_element(
        By.XPATH, '//*[@id="AppFrameMain"]/div/div/div[2]/section[2]/div/div[2]/div/button').click()
    sleep(2)
    browser.find_element(By.XPATH, "//button[text()='1']").click()
    yesterdayBtn = "//button[text()='"+yesterdayDay+"']"
    browser.find_element(By.XPATH, yesterdayBtn).click()
    sleep(1)
    browser.find_element(
        By.XPATH, '//*[@id="AppFrameMain"]/div/div/div[2]/section[2]/div/div[2]/div/button').click()
    sleep(1)
    browser.find_element(
        By.XPATH, '//*[@id="AppFrameMain"]/div/div/div[2]/section[2]/div/div[1]/div/button').click()
    sleep(1)
    browser.find_element(By.XPATH, "//button[text()='Online Store']").click()      
    sleep(1)
    browser.find_element(
        By.XPATH, '//*[@id="AppFrameMain"]/div/div/div[2]/section[4]/div/div[2]/table/tbody/tr[1]/td[2]').click()
    amount = str(float(browser.find_element(
        By.XPATH, '//*[@id="AppFrameMain"]/div/div/div[2]/section[4]/div/div[2]/table/tbody/tr[1]/td[2]').text.replace('₪', '').replace(',', '')))
    browser.save_screenshot(str(today)+"-"+client+".png")
    sleep(1)
    browser.close()
    print('shopify ' + client + ' success')
    emailsend(manager, client, amount)


def dynamicFunction(website, manager, client, name, email, password):
    try:
        if (website == 'wordpress'):
            url = 'https://'+client+'.co.il/wp-admin/admin.php?page=wc-reports&range=custom&start_date=' + \
                startOfTheMonth + '&end_date='+yesterday
            wordpress(manager, name, url, email, password)
        elif (website == 'shopify'):
            url = 'https://'+client+'.myshopify.com/admin'
            shopify(manager, name, url, email, password)
            
    except:
        print(name + ' dead')


def start():

    dynamicFunction("wordpress", "TO", "WEBSITE NAME", "WEBSITE NAME",    "USERNAME", "PASSWORD") 
    dynamicFunction("shopify", "TO","SHOPIFY NAME",  "WEBSITE NAME", "USERNAME", "PASSWORD") 
    
# schedule the function to run every day at 08:30
schedule.every().day.at("08:30").do(start())

# run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
