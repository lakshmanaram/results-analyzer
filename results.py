from decimal import Decimal
import pickle
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
num = 10
def gpafunc(l,h,list):
    l-=0.001
    h+=0.001
    no=1
    for i in list:
        if(i!='NotAvailable'):
            if(Decimal(i["GPA"])>=l) & (Decimal(i["GPA"])<=h):
                print str(no).rjust(3),"  ",i["name"].ljust(35).replace(' ','-'),"->",i["GPA"]
                no+=1
def checkrno(rno):
    print "Checking roll number - Please Wait"
    driver = webdriver.Firefox()
    driver.get("http://www.nitt.edu/prm/nitreg/ShowRes.aspx")
    r=0
    flag=0
    while(flag==0):
        try:
            r+=1
            elem = driver.find_element_by_id('TextBox1')
            elem.send_keys(Keys.CONTROL+'a')
            elem.send_keys(rno)
            elem.send_keys(Keys.RETURN)
            driver.find_element_by_id('Dt1').send_keys(Keys.ARROW_DOWN)
            driver.close()
            return 1
        except:
            if r>8:
                driver.close()
                return 0
        
your_rno=raw_input("Enter your complete roll number    :")
if (checkrno(your_rno)==0):
    print "Either the result is not available for your number OR you have entered an improper roll number"
    print "Close this screen & restart the program. Please Enter proper roll number the next time"
    sys.exit()
rno = your_rno
code = []
subs = []
cred = []
if(os.path.isfile("sem2.txt")):
    with open("sem2.txt",'rb') as f:
        student_list = pickle.load(f)
    code = student_list[0]["code"]
    subs = student_list[0]["subs"]
    cred = student_list[0]["cred"]
    strength = len(student_list)
else:
    strength = input("Enter class strength          :")+1
    print "PLEASE DO NOT DISTURB THE FIREFOX BROWSER. This may take few minutes, Let it run in the background"
    driver = webdriver.Firefox()
    driver.get("http://www.nitt.edu/prm/nitreg/ShowRes.aspx")
    student_list = []
    rn=1
    repeat =0
    while(rn<strength):
        try:
            repeat+=1
            student={}
            rno = rno[:-3]+format(rn,'03d')
            grade = []
            att=[]
            elem = driver.find_element_by_id('TextBox1')
            elem.send_keys(Keys.CONTROL+'a')
            elem.send_keys(rno)
            elem.send_keys(Keys.RETURN)
            driver.find_element_by_id('Dt1').send_keys(Keys.ARROW_DOWN)
            driver.find_element_by_id('Dt1').send_keys(Keys.RETURN)
            name = str(driver.find_element_by_xpath("//span[@id='LblName']").text)
            GPA = str(driver.find_element_by_xpath("//span[@id='LblGPA']/b/font").text)
            num = len(driver.find_elements_by_xpath("//table[@id='DataGrid1']/tbody/tr"))
            for i in range(2,num+1):
                list_elements = driver.find_elements_by_xpath("//table[@id='DataGrid1']/tbody/tr["+str(i)+"]/td")            
                if(rn==1):
                    code.append(str(list_elements[1].text))
                    subs.append(str(list_elements[2].text))
                    cred.append(str(list_elements[3].text))
                grade.append(str(list_elements[4].text))
                att.append(str(list_elements[5].text))
            student["name"]=name
            student["rno"]=rno
            student["grade"]=grade
            student["GPA"]=GPA
            student["attendance"]=att
            if rn==1:
                student["code"] = code
                student["subs"] = subs
                student["cred"] = cred
            student_list.append(student)
            repeat = 0
        except NoSuchElementException:
            if repeat<=6:
                rn-=1
            else:
                student_list.append("NotAvailable")
                repeat=0
        rn+=1
    driver.close()
    with open("sem2.txt",'wb') as f:
        pickle.dump(student_list,f)
    print "Scraping part is DONE.\nsem2.txt file has been created and the data is stored in that file."
flag1=0
while(flag1==0):
    flag1=1
    print "\nGRADE ANALYSIS:"
    print "1.  By GPA:"
    print "2.  Find those with GPA greater than or equal to you :P (Roll number wise)"
    print "3.  Find your friend's GPA"
    print "4.  Entire Class Result(Roll number wise)"
    print "5.  Entire Class Result(Rank wise)"
    print "6.  Exit"
    #print ".  Subject"
    x=input("TYPE RESPECTIVE OPTION NUMBER AND PRESS ENTER  :")
    if x==1:
        flag=0
        while(flag==0):
            flag=1
            print "1.  9-10\n2.  8-9\n3.  7-8\n4.  6-7\n5.  5-6\n6.  Others\n"
            y=input("ENTER CHOICE :")
            if y==1:
                gpafunc(9,10,student_list)
            elif y==2:
                gpafunc(8,9,student_list)
            elif y==3:
                gpafunc(7,8,student_list)
            elif y==4:
                gpafunc(6,7,student_list)
            elif y==5:
                gpafunc(5,6,student_list)
            elif y==5:
                gpafunc(0,5,student_list)
            else:
                flag=0
    elif x==2:
        if student_list[int(your_rno[6:])-1]=='NotAvailable':
            print "GPA Not Available"
        else:
            gpafunc(float(student_list[int(your_rno[6:])-1]["GPA"]),10,student_list)
    elif x==3:
        friend_no = int(raw_input("Enter friend's roll no. only the last 3 digits  :"))
        if(friend_no<=strength)&(friend_no>0):
            friend = student_list[friend_no-1]
            if(friend != 'NotAvailable'):
                print "\n",friend["name"]
                for i in range(num-1):
                    print code[i].ljust(7),subs[i].ljust(35),"->",friend["grade"][i],"  attendance:",friend["attendance"][i].rjust(2)
##                    print "->",friend["grade"][i],"  attendance:"
                print "GPA is".ljust(43),":",friend["GPA"],"\n"
            else:
                print "NotAvailable"
        else:
            print "Incorrect Roll number"
    elif x==4:
        no=1
        for i in student_list:
            if(i!='NotAvailable'):
                print str(no).rjust(3),"  ",i["name"].ljust(35).replace(' ','-'),"->",i["GPA"]
            else:
                print str(no).rjust(3),"  ",'Not Available'
            no+=1
    elif x==5:
        new_list=student_list
        i=0
        while i<len(new_list):
            if new_list[i] =='NotAvailable':
                new_list=new_list[:i]+new_list[i+1:]
            i+=1
        for i in range(len(new_list)):
            temp_obj = new_list[i]
            temp = new_list[i]["GPA"]
            j=i-1
            while (temp>new_list[j]["GPA"])&(j>=0):
                new_list = new_list[:j+1]+new_list[j+2:]
                new_list.insert(j+1,new_list[j])
                j-=1
            new_list = new_list[:j+1]+new_list[j+2:]
            new_list.insert(j+1,temp_obj)
        no=1
        for i in range(len(new_list)):
            j=new_list[i]
            print str(no).rjust(3),"  ",j["name"].ljust(35).replace(' ','-'),"->",j["GPA"]
            if i<len(new_list)-1:
                if j["GPA"]==new_list[i+1]["GPA"]:
                    no-=1
            no+=1
    elif x==6:
        print 'Thanks for using this script :)'
        break
    else:
        print "Please Enter a valid input"
    ch = raw_input("\nAny more querries?(y/n)  :")
    if ch=='y':
        flag1=0
    elif ch!='n':
        print "\n Enter valid input :/"
        flag1=0
    else:
        print 'Thanks for using this script :)'
