import urllib
from bs4 import BeautifulSoup
import smtplib
import sys
import schedule

#This loads the class information from the text file. If it can't open the ClassesToTrack.txt,
#it will then ask for information and create it. The program will then quit. The user has to re-run
#the program, then it will read in the appropriate information and create a list of lists
#(a list of all the classes and then in each sub-list is all the class information).

def load_class_information():
    # Determines if there was a failure in opening the file
   
    try:
        classes = open('ClassesToTrack.txt', 'r')
    except:
        print('ClassesToTrack.txt not found or hasn\'t been created.')
        url = str(raw_input('Please enter the URL to the direct section you want to track on WebTMS: '))
        if 'webtms' not in url:
            while True:
                url = str(raw_input('Please enter the URL to the direct section you want to track on WebTMS: '))
                if 'webtms' in url:
                    break

        opensOrCloses = str(raw_input('Would you like to be notified when a section Opens or Closes (Enter opens or closes): '))
        if opensOrCloses.lower() != 'opens':
            if opensOrCloses.lower() != 'closes':
                while True:
                    opensOrCloses = str(raw_input('Would you like to be notified when a section Opens or Closes (Enter opens or closes): '))
                    if opensOrCloses.lower() == 'opens' or opensOrCloses.lower() == 'closes':
                        break

        email = str(raw_input('Enter an @drexel.edu or @gmail.com email address: '))
        if '@gmail.com' in email.lower():
            if '@drexel.edu' in email.lower():
                while True:
                    email = str(raw_input('Enter an @drexel.edu or @gmail.com email address: '))
                    if '@gmail.com' in email.lower() or '@drexel.edu' in email.lower():
                        break

        password = str(raw_input('Enter the password for {0}: '.format(email)))

        stringToWrite = url +',' + opensOrCloses + ',' + email + ',' + password

        if not url and not opensOrCloses:
            print('Please provide valid input or re-run the script')

        classes = open('ClassesToTrack.txt', 'w')
        classes.write(stringToWrite)
        classes.close()
        
        # We know the file had just been created, so open it instead of forcing the user to re-run
        classes = open('ClassesToTrack.txt', 'r')
   
    if not classes:
        print "There are no classes to track. Please add classes then re-run the script"
        sys.exit(0)
        
    classesToTrack = []
    for l in classes:
        temp = []
        splitLine = l.split(',')
        url = splitLine[0]
        avail = splitLine[1]
        email = splitLine[2]
        password = splitLine[3]
        temp.append(url)
        temp.append(avail)
        temp.append(email)
        temp.append(password)
        classesToTrack.append(temp)
    return classesToTrack

#This main scrapes the html for all the information you could ever dream of having about the class.
#More can be added, although I don't think there is anymore information. This then checks the status
#of the class and will then send an email with all the information it just gathered. The email will
#tell the user if the class is opened or closed.

#THIS METHOD SHOULD BE BROKEN UP MORE!

def main():
    classes = load_class_information()
    for i in range(0, len(classes)):
        url = classes[i][0]
        closeOrOpen = classes[i][1]
        email = classes[i][2]
        password = classes[i][3]
        try:
            urlData = urllib.urlopen(url)
        except:
            print('Couldn\'t connect to URL.')
        data = str(urlData.readlines())
        bs = BeautifulSoup(data)
    
        # These variables are still in scope even though they are set in the
        # for loop
        for t in bs.findAll('td', attrs={'class': 'tableHeader'}):
            if t.text == "CRN":
                crn = t.findNext('td').text
            if t.text == "Subject Code":
                subj = t.findNext('td').text
            if t.text == "Course Number":
                courseNum = t.findNext('td').text
            if t.text == "Section":
                section = t.findNext('td').text
            if t.text == "Credits":
                credits = t.findNext('td').text
            if t.text == "Title":
                title = t.findNext('td').text
            if t.text == "Instructor(s)":
                instructor = t.findNext('td').text
            if t.text == "Max Enroll":
                maxEnrollNum = t.findNext('td').text
            if t.text == "Enroll":
                curEnrollNum = t.findNext('td').text
            if t.text == "Section Comments":
                sectionComments = t.findNext('td').findNext('table').findNext('tr').findNext('td').text


        urlData.close()
        if '@gmail.com' in email.lower():

            if (curEnrollNum == 'CLOSED' and closeOrOpen == 'closes'):

                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                password = password.strip('\n\t')
                try:
                    server.login(email, password)
                except:
                    print 'Invalid login information, please check the password and email for {0}.'.format(email)
                    break
                subject = subj + ' ' + courseNum + ' ' + 'Section: ' + section + ' closed!'
                text = 'CRN:\t\t\t%s\nSubject Code:\t\t%s\nCourse Number:\t\t%s\nSection:\t\t\t%s\nCredits:\t\t%s\nTitle:\t\t\t%s\nInstructor(s):\t\t%s\nMax Enroll:\t\t\t%s\nEnroll:\t\t\t\t%s\nSection Comments:\t%s\n' % (crn, subj, courseNum, section, credits, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                message = 'Subject: %s\n\n%s' % (subject, text)
                server.sendmail(email, email, message)
                server.close()

            if (curEnrollNum != 'CLOSED' and closeOrOpen == 'opens'):
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                password = password.strip('\n\t')
                try:
                    server.login(email, password)
                except:
                    print 'Invalid login information, please check the password and email for {0}.'.format(email)
                    break
                subject = subj + ' ' + courseNum + ' ' + 'Section: ' + section + ' opened!'
                text = 'CRN:\t\t\t%s\nSubject Code:\t\t%s\nCourse Number:\t\t%s\nSection:\t\t\t%s\nCredits:\t\t%s\nTitle:\t\t\t%s\nInstructor(s):\t\t%s\nMax Enroll:\t\t\t%s\nEnroll:\t\t\t\t%s\nSection Comments:\t%s\n' % (crn, subj, courseNum, section, credits, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                message = 'Subject: %s\n\n%s' % (subject, text)
                server.sendmail(email, email, message)
                server.close()

        if '@drexel.edu' in email.lower():
            curEnrollNum = 'CLOSED'
            closeOrOpen = 'closes'
            if (curEnrollNum == 'CLOSED' and closeOrOpen == 'closes'):

                server = smtplib.SMTP('smtp.mail.drexel.edu:587')
                server.ehlo()
                server.starttls()
                password = password.strip('\n\t')
                try:
                    server.login(email, password)
                except:
                    print 'Invalid login information, please check the password and email for {0}.'.format(email)
                    break
                subject = subj + ' ' + courseNum + ' ' + 'Section: ' + section + ' closed!'
                text = 'CRN:\t\t\t%s\nSubject Code:\t\t%s\nCourse Number:\t\t%s\nSection:\t\t\t%s\nCredits:\t\t%s\nTitle:\t\t\t%s\nInstructor(s):\t\t%s\nMax Enroll:\t\t\t%s\nEnroll:\t\t\t\t%s\nSection Comments:\t%s\n' % (crn, subj, courseNum, section, credits, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                message = 'Subject: %s\n\n%s' % (subject, text)
                server.sendmail(email, email, message)
                server.close()

            if (curEnrollNum != 'CLOSED' and closeOrOpen == 'opens'):
                server = smtplib.SMTP('smtp.mail.drexel.edu:587')
                server.ehlo()
                server.starttls()
                password = password.strip('\n\t')
                try:
                    server.login(email, password)
                except:
                    print 'Invalid login information, please check the password and email for {0}.'.format(email)
                    break
                subject = subj + ' ' + courseNum + ' ' + 'Section: ' + section + ' opened!'
                text = 'CRN:\t\t\t%s\nSubject Code:\t\t%s\nCourse Number:\t\t%s\nSection:\t\t\t%s\nCredits:\t\t%s\nTitle:\t\t\t%s\nInstructor(s):\t\t%s\nMax Enroll:\t\t\t%s\nEnroll:\t\t\t\t%s\nSection Comments:\t%s\n' % (crn, subj, courseNum, section, credits, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                message = 'Subject: %s\n\n%s' % (subject, text)
                server.sendmail(email, email, message)
                server.close()

main()

#The main could be run on a cron job (Linux and Mac OS X), on a Windows built in timer or on a 
#in program timer like so:

#schedule.every(1).hour.do(main)
#while True:
#    schedule.run_pending()
#    time.sleep(1)
