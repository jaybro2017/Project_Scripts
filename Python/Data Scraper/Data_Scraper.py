import time
import re
import os
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#windows uses the following: reload(sys) and sys.setdefaultencoding('utf-8')
reload(sys)
sys.setdefaultencoding('utf-8')

website='http://community.cew.org/network/members/advanced-search'

early_career="MainCopy_ctl13_MyDemographics_a3fb03e9295d42428a9a8ef8c273531bChk_0"
mid_career="MainCopy_ctl13_MyDemographics_9cee5fde2f4942749e7785b9c8efc1d4Chk_1"
senior_management="MainCopy_ctl13_MyDemographics_1b1b3265d69b48949f78e76ed9327a6fChk_2"


username="email"
password="pass"

emailid="CEWLoginControl_txtEmailAddress"
passid="CEWLoginControl_txtPassword"
loginid="CEWLoginControl_btnLogin"

filterquery="MainCopy_ctl21_ResultsPerPage"
filter100="//select[@name='ctl00$MainCopy$ctl21$ResultsPerPage']/option[text()='100 per page']"
filter50="//select[@name='ctl00$MainCopy$ctl21$ResultsPerPage']/option[text()='50 per page']"
filter20="//select[@name='ctl00$MainCopy$ctl21$ResultsPerPage']/option[text()='20 per page']"
find_contacts="MainCopy_ctl21_FindContacts"
search_box="ctl00$MainCopy$ctl09$FindCountryCode"
page2="MainCopy_ctl21_Pager_Repeater1_PageLink_1"
headers=['First Name','Last Name','Company','Jobtitle','Email','Country']
resultfile="recordsfound.csv"

def CheckFile(f):
    if os.path.isfile(f):
     return True
    else:
     return False

def csv_writerheader(path):
    #windows uses (path,'ab')
    #linux users (path,'a',newline='',encoding='utf8')
    with open(path,'ab') as csvfile:
    #with open(path,'a',newline='',encoding='utf8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, lineterminator='\n')
        writer.writeheader()


def WriteCsv(list, results):
    #windows uses (path,'ab')
    #linux uses(results, 'a', newline='', encoding='utf8')
    exist = CheckFile(results)

    try:
        if exist:
            # print (list)
            print ("File Exists")
        else:
            print ("File does not exist")
            csv_writerheader(results)
        with open(results, 'ab') as csvfile:
        #with open(results,'a',newline='',encoding='utf8') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            try:
                writer.writerow(list)
            except IOError as er:
                print ("Could not write file:")
                print (er)
    except IOError as ere:
        print ("Could not open file:")
        print (ere)


 
def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 5)
    return driver
 
 
def login(driver, user,passw):
    driver.get(website)
    try:
        emailbox=driver.wait.until(EC.presence_of_element_located(
            (By.ID, emailid)))
        passbox = driver.wait.until(EC.presence_of_element_located(
            (By.ID, passid)))
        loginbutton = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, loginid)))
        emailbox.send_keys(user)
        passbox.send_keys(passw)
        loginbutton.click()
    except TimeoutException:
        print("Box or Button not found in login")

def search():
    #driver.get(website)
    try:
        checkbox1=driver.wait.until(EC.element_to_be_clickable(
            (By.ID, early_career)))
        checkbox2 = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, mid_career)))
        checkbox3 = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, senior_management)))
        findbutton = driver.wait.until(EC.element_to_be_clickable(
            (By.ID, find_contacts)))
        country="(Country)"
        topics="Advertising,Brand Manager,Consulting,Creative,Early Career,Mid Career,Senior Management,E-commerce,Editorial,Evaluations,Finance,Human Resources,Internet Marketing"
        SearchQuery1(topics,country)
        #checkbox1.click()
       # checkbox2.click()
       # checkbox3.click()
        #findbutton.click()
        
        #query100=driver.wait.until(EC.element_to_be_clickable(
          #  (By.XPATH, filter1)))
        #query100.click()
        #time.sleep(5)

        #pagebutton = driver.wait.until(EC.element_to_be_clickable(
          #  (By.ID, page2)))


       # for i in range(0,99):
        #    CompanyData(i)

       # pagebutton.click()
        #time.sleep(2)
       # for i in range(0,99):
        #    CompanyData(i)



        
    except TimeoutException:
        print("Box or Button not found in search")

def PageSelector(page):
    pagebutton = driver.wait.until(EC.element_to_be_clickable(
        (By.ID, page)))
    pagebutton.click()
    time.sleep(3)


def QuerySelector(filter):
    querydriver=driver.wait.until(EC.element_to_be_clickable(
        (By.XPATH, filter)))
    querydriver.click()

def FindMembers(submitquery):
    querie=submitquery
    submitfind=driver.wait.until(EC.element_to_be_clickable(
               (By.ID, querie)))
    submitfind.click()

def ShowRecords(element):
    querie=element
    RecordCount = driver.wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, element)))
    count=RecordCount.text
    sum=count[-5:]
    print sum
    #num=re.sub("[0-9]+"," ",sum)
    #print num
    if ('*' in sum):
        newsum=sum.replace("*","")
    else:
        newsum=sum

    #total=int(num)
    total=[int(s) for s in newsum.split() if s.isdigit()]
    str1=''.join(str(e) for e in total)
    totalit=int (str1)
    print totalit
    return totalit

def SearchBox(element,country):
    filtercountries = "//select[@name='{0}']/option[text()='{1}']".format(element,country)
    querydriver = driver.wait.until(EC.element_to_be_clickable(
        (By.XPATH, filtercountries)))
    querydriver.click()




def SearchQuery1(titles,country):
    print titles
    #Country
    SearchBox(search_box,country)

    for title in titles.split(','):
        print title
        querie=("input[title='%s']" %title)
        checkboxone = driver.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, querie)))
        checkboxone.click()
    FindMembers(find_contacts)
    CountRecordsTotal=ShowRecords("span#MainCopy_ctl21_ShowingLabel")



    if CountRecordsTotal<=20:
        print "Total number of records is less than 20"
        countotal = CountRecordsTotal
        for i in range(0, countotal):
            CompanyData(i)
    elif CountRecordsTotal <= 50:
        print "Total number of records is less than 50"
        # QuerySelector(filter100)
        countleft = CountRecordsTotal - 20
        countotal = CountRecordsTotal - countleft
        print countotal
        print countleft
        for i in range(0, countotal):
            CompanyData(i)
        PageSelector(page2)
        for i in range(0, countleft):
            CompanyData(i)
    elif CountRecordsTotal <= 100:
        print "Total number of records is less than 100"
        QuerySelector(filter50)
        countleft = CountRecordsTotal - 50
        countotal = CountRecordsTotal - countleft
        print countotal
        print countleft
        for i in range(0, countotal):
            CompanyData(i)
        PageSelector(page2)
        for i in range(0, countleft):
            CompanyData(i)
    elif CountRecordsTotal<=200:
        print "Total number of records is less than 200"
        QuerySelector(filter100)
        countleft = CountRecordsTotal - 100
        countotal=CountRecordsTotal - countleft
        print countotal
        print countleft
        for i in range(0,countotal):
            CompanyData(i)
        PageSelector(page2)
        for i in range(0,countleft):
            CompanyData(i)
    elif CountRecordsTotal>200:
        print "Total number of records is greater than 200 , missing information please try again with the search"
        QuerySelector(filter100)
        acount=CountRecordsTotal-200
        bcount=CountRecordsTotal-acount
        countleft = bcount - 100
        countotal = bcount - countleft
        print countotal
        print countleft
        for i in range(0, countotal):
            CompanyData(i)
        PageSelector(page2)
        for i in range(0, countleft):
            CompanyData(i)




    else:
        print "Was not able to print any records"

    #for i in range(0, 99):
        #CompanyData(i)






def CompanyData(num):
    l=[]
    print '\n'
    DisplayName("a#MainCopy_ctl21_Contacts_DisplayName_%d" %num,l)
    CompanyName("div#MainCopy_ctl21_Contacts_CompanyNamePanel_%d" % num,l)
    CompanyTitle("div#MainCopy_ctl21_Contacts_CompanyTitlePanel_%d" % num,l)
    EmailContact("a#MainCopy_ctl21_Contacts_EmailAddress_%d" %num,l)
    CountryName("div#MainCopy_ctl21_Contacts_Addr1Panel5_%d" % num,l)

    print l
    WriteCsv(l,resultfile)

    del l[:]





def DisplayName(element,list):
    #driver.get(website)
    try:
        #displaynamecss="a#MainCopy_ctl21_Contacts_DisplayName_0"
        #displayname="MainCopy_ctl21_Contacts_DisplayName_0"
        NamePerson = driver.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, element))).text

        #NamePerson=driver.find_element_by_id(displayname)
        #result=NamePerson.get_attribute('innerHTML')
        #print element
        print NamePerson
        if NamePerson !="":
            words=NamePerson.split(' ')
            fname=words[0]
            lname=words[1]
            print fname
            print lname
            list.append(fname)
            list.append(lname)
            #print NamePerson.get_attribute('innnerHTML')
            #print NamePerson.get_attribute('value')
            text="Text Found"
            return NamePerson
        else:
            print "No text found for display Name"
            list.append("none")
            list.append("none")
            return NamePerson
        #print result
    except TimeoutException:
        print("Was unable to get Display name")
        text="Text not found"
        list.append("none")
        list.append("none")
        return False

def EmailContact(element,list):

    try:

        NamePerson = driver.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, element)))
        print NamePerson.text
        if NamePerson.text !="":
            list.append(NamePerson.text)
            text="Text Found"
            return text
        else:
            print "No text found for Email Contact"
            list.append("none")
        #print result
    except TimeoutException:
        print("Was unable to get Email Contact")
        text="Text not found"
        list.append("none")
        return text

def CompanyName(element,list):

    try:

        NamePerson = driver.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, element)))
        print NamePerson.text
        if NamePerson.text !="":
            list.append(NamePerson.text)
            text="Text Found"
            return text
            #print result
        else:
            print "No text found for Company Name"
            list.append("none")
    except TimeoutException:
        print("Was unable to get Company name")
        text="Text not found"
        list.append("none")
        return text

def CompanyTitle(element,list):

    try:

        NamePerson = driver.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, element)))
        print NamePerson.text
        if NamePerson.text !="":
            list.append(NamePerson.text)
            text="Text Found"
            return text
            #print result
        else:
            print "No text found for display Name"
            list.append("none")
    except TimeoutException:
        print("Was unable to get Company Title")
        text="Text not found"
        list.append("none")
        return text

def CountryName(element,list):

    try:

        NamePerson = driver.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, element)))
        print NamePerson.text
        if NamePerson.text !="":
            list.append(NamePerson.text)
            text="Text Found"
            return text
            #print result
        else:
            print "No text found for display Name"
            list.append("none")

    except TimeoutException:
        print("Was unable to get Country Name")
        list.append("none")
        text="Text not found"
        return text

 
 
if __name__ == "__main__":
    driver = init_driver()
    login(driver,username,password)
    time.sleep(5)
    #driver.quit()
    search()
    time.sleep(5)
    #CompanyInfo(driver)