#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import multiprocessing, time, random, datetime
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

import datetime
from subprocess import call
import time, json


class GNIB:
    def __init__(self):
        self.today = datetime.datetime.now().day
        self.__url = "https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm"
        profile = webdriver.FirefoxProfile()
        #profile.set_preference("font.size.variable.x-western", 10)
        #profile.set_preference("font.size.variable.x-unicode", 10)
        profile.set_preference("browser.fullscreen.autohide", True)
        profile.set_preference("layout.css.devPixelsPerPx", "0.8")

        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(firefox_options=options, firefox_profile=profile)

        self.driver.maximize_window()
        self.__data = {}
        '''
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(chrome_options=options)
        '''

    def checkMonth(self):
        elements = self.driver.find_elements_by_xpath('//td[contains(@class,"day")]')
        available_days = []

        for i in range(len(elements)):
            try:
                text = elements[i].text
                # Click the particular data to check if it is clickable
                elements[i].click()
                time.sleep(0.5)
                # If the date is clickable, we need to click button going back                # to the previous schedule tap
                self.driver.find_element_by_xpath('//input[@id="Appdate"]').click()
                time.sleep(0.5)

                #print("Checking {}...".format(text))

                if self.driver.find_element_by_xpath('//td[contains(@class, "active day")]').text == text:
                    print("{} is available!".format(text))
                    available_days.append(text)
                    elements = self.driver.find_elements_by_xpath('//td[contains(@class,"day")]')
            except WebDriverException:
                #print("{} Element is not clickable".format(text))
                continue
            #print("current id: {}, total: {}".format(i, len(elements)))
        return list(set(available_days))


    def checkSlot(self):
        self.driver.get(self.__url)
        self.driver.execute_script("document.body.style.zoom='50%'")
        time.sleep(1)
 
        # Find the element on Category selection
        category_element = self.driver.find_element_by_id('Category')
        category_element.click()
        time.sleep(0.5)
        # Choose study category
        study_element = self.driver.find_element_by_xpath('//option[@value="Study"]')
        study_element.click()
        time.sleep(0.5)

        # Find the element on Subcategory selection
        sub_category_element = self.driver.find_element_by_id('SubCategory')
        sub_category_element.click()
        time.sleep(0.5)
        # Choose Master subcategory
        master_sub_category_element = self.driver.find_element_by_xpath('//select[@id="SubCategory"]//option[@value="Masters"]')
        master_sub_category_element.click()
        time.sleep(1)

        # Date of Brith
        self.driver.find_element_by_id('DOB').click()
        time.sleep(1.5)
        table_element = self.driver.find_element_by_xpath('//table[@class="table-condensed"]')
        self.driver.find_element_by_xpath('//span[contains(text(), "2009")]').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//span[contains(text(), "Jan")]').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//td[contains(text(), "28")]').click()
        time.sleep(0.5)


        # Confirmation on GNIB card
        self.driver.find_element_by_id('ConfirmGNIB').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//option[@value="Renewal"]').click()

        # Input GNIB number
        gnib_number_form_element = self.driver.find_element_by_id('GNIBNo')
        gnib_number_form_element.send_keys("I78193432")
        time.sleep(0.5)


        # Input expiry date
        expiry_form_element = self.driver.find_element_by_id('GNIBExDT')
        expiry_form_element.click()
        print("find out expiry form!")
        # click year
        #self.driver.find_element_by_xpath('//div[@class="datepicker-years"]/*/span[contains(text(), "2018")]').click()
        self.driver.find_element_by_xpath('//span[contains(text(), "2018")]').click()
        time.sleep(0.5)
        # click month
        self.driver.find_element_by_xpath('//span[contains(text(), "Dec")]').click()
        time.sleep(0.5)
        # click day
        self.driver.find_element_by_xpath('//td[contains(text(), "30")]').click()
        print("Filled expiry form!")
        time.sleep(0.5)

        # Confirm all above
        self.driver.find_element_by_id('UsrDeclaration').click()
        time.sleep(0.5)

        # Given name
        self.driver.find_element_by_id('GivenName').send_keys("Peng")
        # Surname
        self.driver.find_element_by_id('SurName').send_keys("Ye")

        # Nationality
        self.driver.find_element_by_id('Nationality').click()
        self.driver.find_element_by_xpath('//option[contains(text(), "China")]').click()
        
        # Email
        self.driver.find_element_by_id('Email').send_keys("peng.ye@ucdconnect.ie")
        self.driver.find_element_by_id('EmailConfirm').send_keys("peng.ye@ucdconnect.ie")
        # Familly
        element = self.driver.find_element_by_id('FamAppYN')
        element.click()
        time.sleep(0.5)
        print("clicked Familly!")
        self.driver.find_element_by_xpath('//select[@id="FamAppYN"]/option[contains(text(), "No")]').click()
       
        # passport
        self.driver.find_element_by_id('PPNoYN').click()
        self.driver.find_element_by_xpath('//select[@id="PPNoYN"]/option[contains(text(), "Yes")]').click()
        self.driver.find_element_by_id('PPNo').send_keys("E93312971")

        # Look for appointment
        self.driver.find_element_by_id('btLook4App').click()

        # Search for appointments by
        self.driver.find_element_by_id('AppSelectChoice').click()
        self.driver.find_element_by_xpath('//select[@id="AppSelectChoice"]/option[contains(text(), "specific date")]').click()

        self.driver.find_element_by_id('Appdate').click()
        date_element = self.driver.find_element_by_xpath('//th[@class="datepicker-switch"]')
        print("Available days on {}".format(date_element.text))
        text_file = "monitor.log"
        currentTime = datetime.datetime.now()
        days = self.checkMonth()
        message = "{}: {}".format(date_element.text, days)
        self.__data[date_element.text] = [currentTime, days]
        if len(days) > 0:
            list(map(print,days))[0]

        with open(text_file, "a") as f:
            f.write("{} | {}\n".format(currentTime, message))
        f.close()
        time.sleep(1)

        # Click next page
        while True:
            try:
                self.driver.find_element_by_xpath('//div[@class="datepicker-days"]//th[@class="next"]').click()
                date_element = self.driver.find_element_by_xpath('//th[@class="datepicker-switch"]')
                print("Available days on {}".format(date_element.text))
                days = self.checkMonth()
                message = "{}: {}".format(date_element.text, days)
                self.__data[date_element.text] = [currentTime, days]
                with open(text_file, "a") as f:
                    f.write("{} | {}\n".format(currentTime, message))
                f.close()
                time.sleep(1)
            except Exception:
                break

        '''
        # Check "I am not robot
        self.driver.find_element_by_xpath('//div[@class="rc-anchor-center-container"]/label[@id="recaptcha-anchor-label"]').click()
        '''
        self.driver.quit()
        
        with open("/tmp/gnib.json", 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.__data, f, ensure_ascii=False))


if __name__ == '__main__':
    # claen up firefox processes first
    call(["pkill", "firefox"])
    print("firefox processes were clean up!")
    time.sleep(1)
    mygnib = GNIB()
    mygnib.checkSlot()
