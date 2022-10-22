import pandas as pd
import numpy as np
import time
from datetime import date
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2

email = 'email@email.com'
password = 'password'

mydb = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host="localhost",
                                  database="linkedin")
							
							
#current date
today_date = str(date.today())
#Set days back for retrieving trades data
days_minus = 5 #1 days back

date_formated = datetime.strptime(today_date, "%Y-%m-%d")

#get days ago date_formated
from_date = date_formated - timedelta(days=days_minus)

print(from_date)


url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

#options = Options()
#options.add_argument('--headless')
#driver = webdriver.Chrome('chromedriver', chrome_options=options)
driver = webdriver.Chrome('chromedriver')
driver.get(url)

print('Initializing...' + str(datetime.now()))


#try:
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "session_key")))
#except:
#    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//button[@class='authwall-join-form__form-toggle--bottom form-toggle']")))
#    buttonsign = driver.find_element(By.XPATH,"//button[@class='authwall-join-form__form-toggle--bottom form-toggle']")
#    buttonsign.click()

print('Filling signin...' + str(datetime.now())) 
    
inputemail = driver.find_element(By.XPATH,"//input[@name='session_key']")
inputemail.send_keys(email)

inputpassword = driver.find_element(By.XPATH,"//input[@name='session_password']")
inputpassword.send_keys(password)

#inputsign = driver.find_element(By.XPATH,"//button[@class='sign-in-form__submit-button']")
#inputsign.submit()
inputsign = driver.find_element(By.XPATH,"//button[@data-litms-control-urn='login-submit']")
#inputsign = driver.find_element(By.XPATH,"//button[@class='sign-in-form__submit-button']")
inputsign.click()

print('Sucess filling Sign In...'+str(datetime.now()))

while True:

    i = 0

    try:    
        """
        i = i + 900
        
        if i > 10000:
            driver.close()
            time.sleep(10)
            exit 
        else:
            ''
        """
        
        from numpy.random import randint

        randint = randint(0, 1000000, 1)[0]

        randint = str(randint)

        mycursor = mydb.cursor()

        startdatetime = str(datetime.now())
        exectype = 'LogLoop'
        execstatus = 'Running'

        sqllogsstart = "INSERT INTO executionlogs (idexec, startdatetime, exectype, execstatus) VALUES (%s, %s, %s, %s)"
        vallogsstart = (randint,startdatetime,exectype, execstatus)
        mycursor.execute(sqllogsstart, vallogsstart)

        mydb.commit()

        print('Getting analytics shares...'+str(datetime.now()))

        url = 'https://www.linkedin.com/in/adrianrodriguezgutierrez/recent-activity/shares/'
        driver.get(url)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        shares = driver.find_elements(By.XPATH,"//div[@class='content-analytics-entry-point']/a")

        print('Success Getting analytics shares...'+str(datetime.now()))


        links = []

        for share in shares:
            href = share.get_attribute('href')
            links = np.append(links,href)


        for link in links:

            #print(link)

            #print('Scrapping link...'+str(datetime.now()))

            idpost = link[len(link)-20:-1]

            mycursor = mydb.cursor()

            sqlcheckpostexist = "SELECT idpost FROM posts WHERE idpost = " + str(idpost)
            #valsqlcheckpostexist = idpost
            mycursor.execute(sqlcheckpostexist)

            postresult = mycursor.rowcount

            if postresult == 0:

                sqlpost = "INSERT INTO posts (IdPost,Url) VALUES (%s, %s)"
                valpost = (idpost,link)
                mycursor.execute(sqlpost, valpost)

                mydb.commit()

                print('New post found...'+str(datetime.now()))

            else:
                ''

        mycursor = mydb.cursor()

        sqlcheckpostexist = "SELECT url FROM posts WHERE datetime >= '" + str(from_date) + "'"
        mycursor.execute(sqlcheckpostexist)

        posts = mycursor.fetchall()

        for post in posts:

            print('Getting post metrics...'+str(datetime.now()))

            urlmetrics = post[0]

            #print(link)

            postid = urlmetrics[len(urlmetrics)-20:-1]

            print('Scrapping postid...'+str(postid)+'...'+str(datetime.now()))


            driver.get(urlmetrics)

            impressionslidiv = driver.find_elements(By.XPATH,"//li[@class='member-analytics-addon-summary__list-item']/div/p")

            impressions = impressionslidiv[0].get_attribute('innerHTML').replace('<!---->','').replace(',','')

            gettext = text = driver.find_elements(By.XPATH,"//span[@dir='ltr']")[0]

            text = gettext.get_attribute('innerHTML').replace('<!---->','')

            text = text.replace('<!---->','').replace('<br>',' ').encode().decode()

            text = text[0:text.index('<span')]

            #print(text)

            reactions = driver.find_elements(By.XPATH,"//span[@class='member-analytics-addon__cta-list-item-text']")

            likes = reactions[0].get_attribute('innerHTML').replace(',','')
            comments = reactions[1].get_attribute('innerHTML').replace(',','')
            shares = reactions[2].get_attribute('innerHTML').replace(',','')

            #print(', Impressions: '+impressions +'- likes: '+likes+' comments: '+comments+' shared: '+ shared)

            mycursor = mydb.cursor()

            sqlcheckpostexist = "SELECT idpost FROM posts WHERE idpost = " + str(postid)
            #valsqlcheckpostexist = idpost
            mycursor.execute(sqlcheckpostexist)

            postresult = mycursor.rowcount

            #if postresult == 0:

            sqlpost = "UPDATE posts SET text = %s WHERE idpost = %s"
            valpost = (str(text),str(postid))
            mycursor.execute(sqlpost, valpost)

            mydb.commit()

            #else:
            #    ''

            mycursor = mydb.cursor()

            sqlmetrics = "INSERT INTO metrics (idpost,impressions,likes,comments,shares) VALUES (%s, %s, %s, %s, %s)"
            valmetrics = (postid,impressions,likes,comments,shares)
            mycursor.execute(sqlmetrics, valmetrics)

            mydb.commit()

            print('Success Getting post metrics...'+str(datetime.now()))

        print('Finished succesfully')
        
        mycursor = mydb.cursor()

        finisheddatetime = str(datetime.now())
        execstatus = 'Finished'

        sqllogsfinished = "UPDATE executionlogs SET finisheddatetime = %s, execstatus = %s WHERE idexec = " + randint
        vallogsfinished = (finisheddatetime,execstatus)
        mycursor.execute(sqllogsfinished, vallogsfinished)

        mydb.commit()

        """
        i = i + 900
        
        if i > 15000:
            exit 
        else:
            ''
        """

        time.sleep(900)

    except:

        exit
        #driver.close()

								  