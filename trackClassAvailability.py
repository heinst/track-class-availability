import urllib
from bs4 import BeautifulSoup
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
        try:
            url = splitLine[0]
            avail = splitLine[1]
            email = splitLine[2]
            password = splitLine[3]
        except:
            print 'Error getting necessary data from ClassesToTrack.txt.'
            print 'Make sure all lines are in the correct format: url,closes,email,password or url,opens,email,password'
            sys.exit(1)
        temp.append(url)
        temp.append(avail)
        temp.append(email)
        temp.append(password)
        classesToTrack.append(temp)
    return classesToTrack

def stop_tracking_classes(classesToStopTracking):
    classesToTrack = open('ClassesToTrack.txt', 'r')
    trackedClasses = classesToTrack.readlines()
    classesToTrack.close()
    classesToTrack = open('ClassesToTrack.txt', 'w')
    newTrackedList = []
    for c in trackedClasses:
        newTrackedList.append(c)

    for i in range(0, len(trackedClasses)):
        for j in range(0, len(classesToStopTracking)):
            if trackedClasses[i] == classesToStopTracking[j]:
                newTrackedList.remove(classesToStopTracking[j])
            elif trackedClasses[i] == classesToStopTracking[j].strip('\n'):
                newTrackedList.remove(classesToStopTracking[j].strip('\n'))

    for i in range(0, len(newTrackedList)):
        if i == len(newTrackedList) - 1:
            c = newTrackedList[i].strip('\n')
            classesToTrack.write(c)
        else:
            if '\n' in newTrackedList[i]:
                classesToTrack.write(newTrackedList[i])
            else:
                classesToTrack.write(newTrackedList[i] + '\n')



#This main scrapes the html for all the information you could ever dream of having about the class.
#More can be added, although I don't think there is anymore information. This then checks the status
#of the class and will then send an email with all the information it just gathered. The email will
#tell the user if the class is opened or closed.

def main():
    classes = load_class_information()
    classesToStopTracking = []
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
                creds = t.findNext('td').text
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
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = email
                msg['To'] = email

                html = '<html>'\
                    '<style>'\
                        'table' \
                        '{' \
                            'border-collapse'
                html = html + ': '
                html = html + 'collapse;'
                html = html + '}' \
                        'table,th,td' \
                        '{'
                html = html + 'border'
                html = html + ': '
                html = html + '1px solid black;'
                html = html + '}'

                html = html + '</style>' \
                    '<body>' \
                        '<table>'\
                            '<tr>'\
                                '<th align="left">CRN</th>'\
                                '<td align="left">{0}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Subject Code</th>'\
                                '<td align="left">{1}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Course Number</th>'\
                                '<td align="left">{2}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section</th>'\
                                '<td align="left">{3}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Credits</th>'\
                                '<td align="left">{4}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Title</th>'\
                                '<td align="left">{5}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Instructor(s)</th>'\
                                '<td align="left">{6}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Max Enroll</th>'\
                                '<td align="left">{7}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Enroll</th>'\
                                '<td align="left">{8}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section Comments</th>'\
                                '<td align="left">{9}</td>'\
                            '</tr>'\
                        '</table>'\
                     '</body>' \
                    '</html>'.format(crn, subj, courseNum, section, creds, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                part2 = MIMEText(html, 'html')
                msg.attach(part2)
                server.sendmail(email, email, msg.as_string())
                server.close()
                classesToStopTracking.append(url + ',' + closeOrOpen + ',' + email + ',' + password + '\n')

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
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = email
                msg['To'] = email

                html = '<html>'\
                    '<style>'\
                        'table' \
                        '{' \
                            'border-collapse'
                html = html + ': '
                html = html + 'collapse;'
                html = html + '}' \
                        'table,th,td' \
                        '{'
                html = html + 'border'
                html = html + ': '
                html = html + '1px solid black;'
                html = html + '}'

                html = html + '</style>' \
                    '<body>' \
                        '<table>'\
                            '<tr>'\
                                '<th align="left">CRN</th>'\
                                '<td align="left">{0}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Subject Code</th>'\
                                '<td align="left">{1}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Course Number</th>'\
                                '<td align="left">{2}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section</th>'\
                                '<td align="left">{3}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Credits</th>'\
                                '<td align="left">{4}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Title</th>'\
                                '<td align="left">{5}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Instructor(s)</th>'\
                                '<td align="left">{6}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Max Enroll</th>'\
                                '<td align="left">{7}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Enroll</th>'\
                                '<td align="left">{8}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section Comments</th>'\
                                '<td align="left">{9}</td>'\
                            '</tr>'\
                        '</table>'\
                     '</body>' \
                    '</html>'.format(crn, subj, courseNum, section, creds, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                part2 = MIMEText(html, 'html')
                msg.attach(part2)
                server.sendmail(email, email, msg.as_string())
                server.close()
                classesToStopTracking.append(url + ',' + closeOrOpen + ',' + email + ',' + password + '\n')

        if '@drexel.edu' in email.lower():
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

                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = email
                msg['To'] = email

                html = '<html>'\
                    '<style>'\
                        'table' \
                        '{' \
                            'border-collapse'
                html = html + ': '
                html = html + 'collapse;'
                html = html + '}' \
                        'table,th,td' \
                        '{'
                html = html + 'border'
                html = html + ': '
                html = html + '1px solid black;'
                html = html + '}'

                html = html + '</style>' \
                    '<body>' \
                        '<table>'\
                            '<tr>'\
                                '<th align="left">CRN</th>'\
                                '<td align="left">{0}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Subject Code</th>'\
                                '<td align="left">{1}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Course Number</th>'\
                                '<td align="left">{2}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section</th>'\
                                '<td align="left">{3}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Credits</th>'\
                                '<td align="left">{4}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Title</th>'\
                                '<td align="left">{5}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Instructor(s)</th>'\
                                '<td align="left">{6}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Max Enroll</th>'\
                                '<td align="left">{7}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Enroll</th>'\
                                '<td align="left">{8}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section Comments</th>'\
                                '<td align="left">{9}</td>'\
                            '</tr>'\
                        '</table>'\
                     '</body>' \
                    '</html>'.format(crn, subj, courseNum, section, creds, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                part2 = MIMEText(html, 'html')
                msg.attach(part2)
                server.sendmail(email, email, msg.as_string())
                server.close()
                classesToStopTracking.append(url + ',' + closeOrOpen + ',' + email + ',' + password + '\n')
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
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = email
                msg['To'] = email

                html = '<html>'\
                    '<style>'\
                        'table' \
                        '{' \
                            'border-collapse'
                html = html + ': '
                html = html + 'collapse;'
                html = html + '}' \
                        'table,th,td' \
                        '{'
                html = html + 'border'
                html = html + ': '
                html = html + '1px solid black;'
                html = html + '}'

                html = html + '</style>' \
                    '<body>' \
                        '<table>'\
                            '<tr>'\
                                '<th align="left">CRN</th>'\
                                '<td align="left">{0}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Subject Code</th>'\
                                '<td align="left">{1}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Course Number</th>'\
                                '<td align="left">{2}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section</th>'\
                                '<td align="left">{3}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Credits</th>'\
                                '<td align="left">{4}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Title</th>'\
                                '<td align="left">{5}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Instructor(s)</th>'\
                                '<td align="left">{6}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Max Enroll</th>'\
                                '<td align="left">{7}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Enroll</th>'\
                                '<td align="left">{8}</td>'\
                            '</tr>'\
                            '<tr>'\
                                '<th align="left">Section Comments</th>'\
                                '<td align="left">{9}</td>'\
                            '</tr>'\
                        '</table>'\
                     '</body>' \
                    '</html>'.format(crn, subj, courseNum, section, creds, title, instructor, maxEnrollNum, curEnrollNum, sectionComments)
                part2 = MIMEText(html, 'html')
                msg.attach(part2)
                server.sendmail(email, email, msg.as_string())
                server.close()
                classesToStopTracking.append(url + ',' + closeOrOpen + ',' + email + ',' + password + '\n')

    stop_tracking_classes(classesToStopTracking)

main()

#The main could be run on a cron job (Linux and Mac OS X), on a Windows built in timer or on a 
#in program timer like so:

#schedule.every(1).hour.do(main)
#while True:
#    schedule.run_pending()
#    time.sleep(1)
