from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
import time
import smtplib, ssl

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

link = 'https://canvas.eur.nl/courses/33300/discussion_topics/'

# set up email
port = 465
password = 'PSW' # Outgoing mail psw goes here
sender_email = "jkb.pyt@gmail.com" # Outgoing mail user goes here
receiver_email = "jkrasauskas@gmail.com" # Receiver mail user goes here


def format_mail(msg):
    final_msg = "Link: {} \n\n".format(msg[-1])
    return final_msg + "\n\n*** New entry: ***\n".join(msg[0:-1])


def send_mail(msg):
    subject = 'New entries'
    fmt = 'Subject: {}\r\n \n\n{}'
    emsg = """\ 
    \n
    %s
    """ % (str(msg))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, fmt.format(subject, format_mail(msg)).encode('utf-8'))
        print('mail sent.')
    return


def log_in():
    driver.get('https://canvas.eur.nl/courses/33300/discussion_topics/215291')
    elem = driver.find_element_by_xpath('//*[@id="idp-picker"]/div[2]/div[2]/a[2]')
    elem.click()
    elem = driver.find_element_by_xpath('//*[@id="userNameInput"]')
    elem.send_keys('USERNAME_GOES_HERE') # Enter username
    elem = driver.find_element_by_xpath('//*[@id="passwordInput"]')
    elem.send_keys('PASSWORD_GOES_HERE') # Enter password
    elem = driver.find_element_by_xpath('//*[@id="submitButton"]')
    elem.click()


def find_new_elem_text(link, extension, latest_number):
    driver.get(link + extension)
    old_len = latest_number  # len(driver.find_elements_by_class_name('entry'))
    driver.refresh()
    time.sleep(10)
    try:
        elems = driver.find_elements_by_class_name('entry')
        #print(elems)
    except NoSuchElementException:
        print('not found')
    if len(elems) > old_len:
        diff = len(elems) - old_len
        new_elems_text = []
        for i in range(len(elems) - diff, len(elems)):
            new_elem_id = elems[i].get_attribute('id')
            #print(new_elem_id)
            new_elems_text.append(driver.find_element_by_xpath("//*[@id='" + new_elem_id + "']/article/div[1]").text)

        new_elems_text.append(link + extension)
        send_mail(new_elems_text)  # perduoda list'a su textais, ir issiuncia mail'a
    old_len = len(elems)
    return old_len


def main():
    log_in()
    time.sleep(2)
    links_numbers = {'215294': 0, '215290': 0, '215289': 0}
    try:
        while True:
            for i in links_numbers:
                links_numbers[i] = find_new_elem_text(link, i, links_numbers[i])
                print(links_numbers)
                print(links_numbers[i])
    except Exception as e:
        driver.close()
        print(e)


main()
