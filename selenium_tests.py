from selenium import webdriver
import time

browser = webdriver.Firefox()
browser.get('http://127.0.0.1:5000/')
element = browser.find_element_by_id('calculate')
element.click()
value = browser.find_element_by_id('result_worker')
while value.text == '' or value.text == '0':
    value = browser.find_element_by_id('result_worker')
    time.sleep(1)
print "The password brutted by connected client: {0}".format(value.text)
browser.close()




