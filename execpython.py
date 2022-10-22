#Python 3.x
import psycopg2
from datetime import datetime, timedelta

mydb = psycopg2.connect(user="postgres",
                                  password="12345",
                                  host="localhost",
                                  database="linkedin")
								
print('Getting last data...')
                                
mycursor = mydb.cursor()

sqlcheckpostexist = "select idpost from metrics where datetime  > current_timestamp + (-15 * interval '1 minute')"

#valsqlcheckpostexist = idpost
mycursor.execute(sqlcheckpostexist)

postresult = mycursor.rowcount

if postresult == 0:

    print('Needed to pull data....')

    from numpy.random import randint

    randint = randint(0, 1000000, 1)[0]

    randint = str(randint)

    mycursor = mydb.cursor()

    startdatetime = str(datetime.now())
    exectype = 'LogExec'
    execstatus = 'Running'

    sqllogsstart = "INSERT INTO executionlogs (idexec, startdatetime, exectype, execstatus) VALUES (%s, %s, %s, %s)"
    vallogsstart = (randint,startdatetime,exectype, execstatus)
    mycursor.execute(sqllogsstart, vallogsstart)

    mydb.commit()
    
    print('Executing RPA...')

    #exec('RpaGetLinkedinPostsMetricsPostgreSqlAutoLoop.py')
    exec(open("RpaGetLinkedinPostsMetricsPostgreSqlAutoLoop.py").read())
    
    print('Finished RPA...')
    
    mycursor = mydb.cursor()

    finisheddatetime = str(datetime.now())
    execstatus = 'Finished'

    sqllogsfinished = "UPDATE executionlogs SET finisheddatetime = %s, execstatus = %s WHERE idexec = " + randint
    vallogsfinished = (finisheddatetime,execstatus)
    
    mycursor.execute(sqllogsfinished, vallogsfinished)

    mydb.commit()

else:
    
    print('Not needed to get data...')

    exit