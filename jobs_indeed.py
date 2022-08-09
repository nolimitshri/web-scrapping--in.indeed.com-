import requests
from bs4 import BeautifulSoup
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

now = datetime.datetime.now()

url = "https://in.indeed.com/Software-Developer-jobs?vjk=a1ee0ab02de0d04e"
# url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

html_content = requests.get(url).text
# print(html_content)

soup = BeautifulSoup(html_content, "html.parser")
# print(soup)

cnt = soup.find_all("td", attrs={'class': 'resultContent'})

str1 = '<b>Top Indeed Jobs in Web Development:</b>\n'+'<br>'+'-'*50+'<br>'

for i ,tag in enumerate(cnt): 
    jobTitle = tag.find("h2", attrs={'class': 'jobTitle'}).text
    jobLocation = tag.find("div", attrs={'class': 'companyLocation'}).text
    companyName = tag.find("span", attrs={"class": 'companyName'}).text
    str1 += (str(i+1) + " :: <b>" + jobTitle + "</b>, Location: " + jobLocation + ", Company: <b>" + companyName + "</b>\n" + "<br>")

str1 += ('<br>'+'-'*50+'<br>')
str1 += (f'<a href="{url}">Check out</a>')
str1 += ('<br><br>End of message')

print(str1)

# email details
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '' # Sender's Email ID
TO = '' # Reciever's Email ID
PASS = '' # Password or App Password of Sender's Email ID

msg = MIMEMultipart()

msg['Subject'] = f'Software Jobs - India (in.indeed.com) [Automated Email] {str(now.day)}/{str(now.month)}/{str(now.year)}'

msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(str1, 'html'))

print("Initiating Server...")

server = smtplib.SMTP(SERVER, PORT)

# want to see error messages set to 1 or else 0
server.set_debuglevel(1)
server.ehlo()
# start a TLS connection
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email Sent...")

server.quit()