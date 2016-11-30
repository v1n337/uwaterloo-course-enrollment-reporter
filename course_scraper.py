import requests
from bs4 import BeautifulSoup
import smtplib


url = "https://info.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?sess=1171&level=grad&subject=CS&cournum="

course_list = ["848", "846"]
alerts_to = ["vinjohn10@gmail.com"]

response = requests.get(url)

soup = BeautifulSoup(response.text, "lxml")

#print(soup.select("table"))
bs = BeautifulSoup(str(soup.select("table")), "lxml")

all_rows = bs.select("tr")
course_information_list = list()

# print course_list[0]
for i in xrange(len(all_rows)):
	if "CS" in str(all_rows[i]):
		for course in course_list:
			if course in str(all_rows[i]):
				course_information_list.append(str(all_rows[i+1]))

# print course_information_list

course_dict = dict()
for i in xrange(len(course_information_list)):
	bs = BeautifulSoup(course_information_list[i], "lxml")
	(cap, enrolled) = \
		(bs.select("td")[1].select("table")[0].select("tr")[1].select("td")[6].text, 
		 bs.select("td")[1].select("table")[0].select("tr")[1].select("td")[7].text)

	course_dict[course_list[i]] = (cap, enrolled)

print course_dict

course_messages = []
for course in course_dict.keys():
	(cap, enrolled) = course_dict[course]
	seats_left = int(cap) - int(enrolled)
	if seats_left > 0:
		course_messages.append("Course " + str(course) + " has " + str(seats_left) + " seats open!")

print course_messages

msg_list = [ "From: vinjohn10@gmail.com", "To: you@gmail.com", "Subject: Course enrollment report", ""]
msg_list.extend(course_messages)
msg = "\r\n".join(msg_list)

try:
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login("vinjohn10", "xxxxxxxx")
	server.sendmail("vinjohn10@gmail.com", alerts_to, msg)
	server.quit()
	print "Successfully sent email"
except Exception as e:
	print "Error: unable to send email"
	print e
