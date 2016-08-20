# By: incognybble
# Created: 4th Sept 2015
# Last modified: 20th Aug 2016

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import re
#from datetime import datetime
import getpass


PAUSE = 5

class scopal():

    def __init__(self, username, p, stop='', card="", filename='', b=''):
        
        self.browser = None
        
        if (b.strip()=="2" or b.strip().lower()=="chrome"):
            self.browser = webdriver.Chrome()
        else:
            self.browser = webdriver.Firefox()
            
        self.homepage = "https://www.opal.com.au/"
        self.username = username
        self.p = p
        self.main_window = self.browser.window_handles[0]
        self.filename = filename
        self.card = card

        if self.filename == '':
            self.filename = "opal.csv"

        if stop == '':
            f = open(self.filename, "w")
            f.write("idn,day,date,time,mode,from,to,journey,notes,cost,discount,fare\n")
            f.close()
            self.stop = None
        else:
            self.stop = stop


    def run(self):
        self.browser.get(self.homepage)

        self.type_in_name("h_username", self.username)
        self.type_in_name("h_password", self.p)
        self.click_by_attr("input", "value", "Log in")

        # check for error message
        if (not self.check_in_source("username or password does not match") and not self.check_in_source("account is blocked")):

            if self.card != "":
                self.select_by_id("selectCardIndex", self.card)

            self.click_by_link_text("Opal activity")

            # strip data from source
            cont = self.get_data()
            
            # click the next one if possible
            while self.check_in_source("Next page") and cont == True:
                self.click_by_id("next")
                cont = self.get_data()

            self.click_by_link_text("Log Out")
            self.browser.switch_to.alert.accept()
            time.sleep(PAUSE)
            self.browser.switch_to_window(self.main_window)
            
        else:
            print "Try different username/password."
            
        self.browser.quit()

    def get_data(self):
        tbody = re.findall('<tbody.+?tbody', self.browser.page_source, re.DOTALL)

        if len(tbody) == 0:
            raise Exception("tbody regex failed")

        tbody = tbody[0]+">"
        tbody = tbody.replace("<br />", " ")
        tbody = re.sub('<img .+?alt="(?P<mode>\w+)" .+?>', '<img alt="\g<mode>" />',tbody)
        tbody = re.sub("[\s\n\t]+", " ", tbody)
        tbody = re.sub("\xad", "", tbody)
        tbody = re.sub('(?P<time>\d+:\d+)</td><td class="center"></td>', '\g<time></td><td class="center"><img alt="blank" /></td>', tbody)
        tbody = re.sub('nowrap"></td>', 'nowrap">$0.00</td>', tbody)
        tbody = re.sub("&amp;", "&", tbody)
        
        # strip via regex
        rows=re.findall("<tr.*?>.+?</tr>", tbody)

        if len(rows) == 0:
            raise Exception("Could not find rows")
        
        for row in rows:
            data = re.findall('<td.*?>(\d+)</td><td class="date-time">([\w\s:\/]+)</td>.+?alt="([\w\s]+)".+?transaction-summary hyphenate.+?>([\w\s\-\&,\.\(\)]+)<.+?center">([\d\s]*?)</td><td>(.*?)</td>.+?(\-?\$\d+\.\d+).+?(\-?\$\d+\.\d+).+?(\-?\$\d+\.\d+)', row)

            if len(data) == 0:
                print row
                raise Exception("Could not find row")
            else:
                data = data[0]

            if self.stop != None:
                # The journeys are in reverse order.
                # So the numbers go down each page.
                # Eventually, it will be lower than the stop point.
                if int(data[0]) <= int(self.stop):
                    return False
                
            self.save_data(data)

        return True

    def save_data(self, data):
        (idn, datestr, mode, where, journey, notes, cost, discount, fare) = data

        # this works. It's just overkill.
        #d = datetime.strptime(datestr, '%a %d/%m/%Y %H:%M')

        d = datestr.split()
        
        f = open(self.filename, "a")
        
        s = idn + ","
        s = s + d[0] + "," + d[1] + "," + d[2] + ","
        
        if mode == "blank":
            if where.startswith("Top up"):
                mode = "top up"
                fr = where.replace("Top up - ", "")
                to = ""
            else:
                mode = ""
                fr = where
                to = ""
        elif where.startswith("Tap on reversal"):
            notes = "Tap on reversal"
            fr = where.replace("Tap on reversal - ", "")
            to = ""
        else:
            (fr, to) = where.split(" to ")

        if (fr.endswith("LR")) and (mode == "train"):
            mode = "light rail"
            fr = fr.replace(" LR", "")
            if to.endswith("LR"):
                to = to.replace(" LR", "")
        elif (to.endswith("LR")) and (mode == "train"):
            mode = "light rail"
            to = to.replace(" LR", "")

        if fr.find(",") > -1:
            fr = '"' + fr + '"'
        if to.find(",") > -1:
            to = '"' + to + '"'
            
        s = s + mode + "," + fr + "," + to + ","
        s = s + journey.strip() + ","
        s = s + notes.strip() + "," + cost + "," + discount + "," + fare
        s = s + "\n"

        f.write(s)
        f.close()
        print idn

    def check_in_source(self, text):
        html_source = self.browser.page_source
        return (html_source.find(text) > -1)

    def click_by_id(self, elem_id):
        elem = self.browser.find_element_by_id(elem_id)
        elem.click()
        time.sleep(PAUSE)

    def click_by_link_text(self, text):
        elem = self.browser.find_element_by_link_text(text)
        elem.click()
        time.sleep(PAUSE)
        
    def click_by_attr(self, field_type, attr, value):
        elem = self.browser.find_element_by_xpath("//"+field_type+"[@"+attr+"='"+value+"']")  
        elem.click()
        time.sleep(PAUSE)

    def type_in_name(self, elem_name, text):
        elem = self.browser.find_element_by_name(elem_name)
        elem.clear()
        elem.send_keys(text + Keys.TAB)
        time.sleep(PAUSE)

    def select_by_id(self, select_id, option_val):
        elem = self.browser.find_element_by_xpath("//select[@id='"+select_id+"']/optgroup/option[contains(text(), '"+option_val+"')]")
        elem.click()
        time.sleep(PAUSE)

if __name__ == "__main__":
    username = ''
    p = ''

    while len(username.strip()) == 0:
        username = raw_input("Username: ")

    while len(p.strip()) == 0:
        p = getpass.getpass("Pass: ")
        
    card = raw_input("Card (optional): ")
    stop = raw_input("Stop (optional): ")
    filename = raw_input("Output file (optional): ")

    b = raw_input("Browser (optional)\n[1] Firefox (default)\n[2] Chrome: ")
        
    o = scopal(username, p, stop, card, filename, b)
    o.run()
