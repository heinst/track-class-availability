import urllib
from bs4 import BeautifulSoup
import sys

def load_class_information():

    classes = open('ClassesToTrack.txt', 'r')
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
    classes.close()
    return classesToTrack

def getWebTmsData():

    classes = load_class_information()
    for i in range(0, len(classes)):
        url = classes[i][0]
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
                if crn != '13980':
                    return False
            if t.text == "Subject Code":
                subj = t.findNext('td').text
                if subj != 'CS':
                    return False
            if t.text == "Course Number":
                courseNum = t.findNext('td').text
                if courseNum != '281':
                    return False
            if t.text == "Section":
                section = t.findNext('td').text
                if section != '063':
                    return False
            if t.text == "Credits":
                creds = t.findNext('td').text
                if creds != '0.00':
                    return False
            if t.text == "Title":
                title = t.findNext('td').text
                if title != 'Systems Architecture':
                    return False
            if t.text == "Instructor(s)":
                instructor = t.findNext('td').text
                if instructor != 'Constantine Katsinis':
                    return False
            if t.text == "Max Enroll":
                maxEnrollNum = t.findNext('td').text
                if maxEnrollNum != '25':
                    return False
            if t.text == "Enroll":
                curEnrollNum = t.findNext('td').text
                if curEnrollNum != '21':
                    return False
            if t.text == "Section Comments":
                sectionComments = t.findNext('td').findNext('table').findNext('tr').findNext('td').text
                if sectionComments != 'Also register for a lecture':
                    return False

        urlData.close()
    return True

def writeTestTxtFile():
    stringToWrite = 'https://duapp2.drexel.edu/webtms_du/app?component=courseDetails&page=CourseList&service=direct&sp=ZH4sIAAAAAAAAADWLTQ6CMBBGR4w%2Fa%2BNeLmChBlYuNa7YGLnASCekpkVoB2Xlibyad7CG%2BC3f9977AzPvYEOqF8rRQEZox%2BJJV7ZeKGQUJTkL4yYRTAtYYMWltsSwLm74wMR3JvkBz2jbfQFLDsnhroKxGg2DTZ1c2Omm%2Fv9H8lUHL4iGtmWY71KZyTwEJzQmPvfoghTLbCvzL1UDVXGkAAAA&sp=SCI&sp=SCS&sp=S13980&sp=S281&sp=5,opens,tests@drexel.edu,test'
    classes = open('ClassesToTrack.txt', 'w')
    classes.write(stringToWrite)
    classes.close()

writeTestTxtFile()
didPass = getWebTmsData()

if didPass == True:
    sys.exit(0)
else:
    sys.exit(1)

