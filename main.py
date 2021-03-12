import requests
from bs4 import BeautifulSoup
import xlwt
from dotenv import load_dotenv
import os

load_dotenv()
wb = xlwt.Workbook()
urlLogin = 'https://fit.ba/student/login.aspx?ReturnUrl=%2fstudent'

post_data = {
    '__EVENTARGUMENT': '',
    '__EVENTTARGET': '',
    '__EVENTVALIDATION': 'T2tqUteiKvcKeBQ28nNzR7E3pEhefZB48PuRpoXOnGVP8xtah5EjKTDrQOlBGFCB5u4jrrwY/CT4yYSagoDsZe0e3CLmMyaHuzHEEaKPhw4ihUAcKgCsiOgawlhvyoqTYdo6EVL+7khor9RdVcyRkEUfPc0YUcuwmbY/6EN9HKtZdkSKZz0WuzYUdfkAAIjH4ODOPX58ids/mRau4fN0Jyo6HkqqX2SYk11POe1FiU1R/Br0DqHNOd0q4ZSBv8bvjjpsaEnR3ZffeOJSY6R8UO9pZb2+c5RNBK1N67InhWk=',
    '__VIEWSTATE': 'nfpoDqXm+Sq8TZjgSFnFAJIIi8QWDdsGln0pkrnd4uX59v5j4kAw1/ORvRFWu78YynHvaZAMVJXA/Yl4H2GbZQmXgWPJ6WPgZTM4nZriOE5lmJ08kWYfchWaj5bl/4BBEaErFxYz8EkSVw9Y1l4aHtnMg4R/ps0pZE/cnlYVxnLR4iHjCBcJ3OrHLKGjTL6JGd652UuhymZznq//wBIeWoikuXcLc4MZ0dwGYidabv5OdV3oP0pJnfCAXKyZcPZs6U6pKCf4GHoWEpMtiJBD3KEEqYtnAgRkKDq2l2L3esiWYF1SrqPG4UR8Nf1cTyS2voBW+1ACa0uA216Sx+q/tDQ8tqSonAu63JpY2z+OO2L+LXb9p/ZuhnCdeKPo50hzWtcyypR1jZ9qSEYyh0/xbvo8irNSxlgeBG7QvHWCTPd0rPe854WMQzDhwSv2g/Wey9sp4hwKwhX8j8x/vmrIjod4zQvwE7y5Mgrz+wFHJ5t8nwSs1kr1RBe/BnisbrV4uKmJ8mHNuectNEu4bk+eyOkf0XRbDQtHRwmqYi/vu9mfsjFOZGDKVo6U/Wf48k+kLNo11bVMpZlO+cwySgqfZXn3s5oSYOybqQoytpOagHXDgaq38sR1ez4n3QWoX6wtuWRe1B9keD/fuyVfMZuiOGCEEpZOAWBxBVjYLd/QAZYVMB8TRrtLrKNQiHAOmsux+WlQiHFgWCP27tx32V9zaGsJWed0MShIAeqaMdseXaXA1nEv7go7X+9pKNWRxv35F83/3R18R5yLqD3HFAZu7EXJdnzmNrGeJmIkZAtsQPY4ZOFt/jnfaqSi4g8QzsUYQkNXF3GcQHC6YrgW9QvSY3PLA6ExPgycO4dPBKAHh0fWAaYVCdMjaKTp4ZXbJsgXnGr66F4Yy3QMvH/uU6JTF+mWguR2qLDq6BV/YDYsM7c6jvIqPmZuNrfaxclXPCXg',
    '__VIEWSTATEGENERATOR': '630CEE1E',
    'btnPrijava': 'Prijava',
    'listInstitucija': '1',
    'txtBrojDosijea': os.getenv("USER_INDEX_NUMBER"),
    'txtLozinka': os.getenv("USER_PASSWORd")
}

post_headers = {
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

response = requests.post(url=urlLogin, data=post_data, headers=post_headers)

result = BeautifulSoup(response.content, 'html.parser')

ws = wb.add_sheet('Sheet 1')

print(result.title.text.strip())

if result.title.text.strip() == 'DLWMS - Studentski online servis':
    news_list = result.select('ul', _class="newslist")
    count = 0
    for news in news_list:
        link = news.select_one('a', _class="linkButton")
        if link and link.has_attr('href') and link["href"].startswith('obavijesti'):
            print('https://fit.ba/student/' + link["href"])
            ws.write(count, 0, 'https://fit.ba/student/' + link["href"])
            count += 1
else:
    response = requests.post(url=urlLogin, data=post_data, headers=post_headers)

wb.save('scrape.xls')
