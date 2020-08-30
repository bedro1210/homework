import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb://test:test@13.209.80.137',27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}



data = requests.get('http://www.sogang.ac.kr/front/boardlist.do?bbsConfigFK=2', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('body > div > div > div:nth-child(2) > div > table > tbody > tr')

i = 0

for tr in trs:
    list_name = tr.select_one('td:nth-child(2) > div > a > span').text
    list_link = 'http://www.sogang.ac.kr' + tr.select_one('td:nth-child(2) > div > a').get('href')
    list_link = list_link.replace('¤t', '&current')
    list_day = tr.select_one('td:nth-child(5)').text.strip()

    doc = {
        'idx': i,
        'list_name': list_name,
        'list_link': list_link,
        'list_day': list_day
    }

    OldList = list(db.soganghelp.find({'idx': i}, {'_id': False}))

    if not OldList :
        db.soganghelp.insert_one(doc)
    else :
        db.soganghelp.update_one({'idx': i}, {"$set": doc});

    i = i + 1



data = requests.get('https://gonzaga.sogang.ac.kr/admin/board/list.jsp?board_nm=notice', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#contants > form > table.Notice_Board > tbody > tr')

i=0

for tr in trs:
    if i>0 :
        if i<31 :
            listName = tr.select_one('td.tdg.f_b').text.strip()
            listLink = 'https://gonzaga.sogang.ac.kr/home/sub04/index.jsp?board_nm=notice'

            doc = {
                'idx': i,
                'list_name': listName,
                'list_link': listLink,
            }



            db.gonzagahelp.update_one({'idx': i}, {"$set": doc});

    i=i+1



data = requests.get('http://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=dormitory&bbsConfigFK=1181', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

i = 0
a = 0

for title in soup.select('.title'):
    list_name = title.text
    list_link = 'http://scc.sogang.ac.kr' + title.get('href')

    doc = {
        'idx': i,
        'list_name': list_name,
        'list_link': list_link,
    }

    db.belhelp.update_one({'idx': i}, {"$set": doc});

    i = i + 1
    a = i

print (a)

data = requests.get('http://scc.sogang.ac.kr/front/cmsboardlist.do?siteId=dormitory&bbsConfigFK=1182', headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

a = a + 1

for title in soup.select('.title'):
    list_name = title.text
    list_link = 'http://scc.sogang.ac.kr' + title.get('href')

    doc = {
        'idx': a,
        'list_name': list_name,
        'list_link': list_link,
    }

    db.belhelp.update_one({'idx': i}, {"$set": doc});

    a = a + 1









@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/list', methods=['GET'])
def show_lists():
    lists = list(db.soganghelp.find({}, {'_id': False}))
    lists_two = list(db.gonzagahelp.find({}, {'_id' : False}))
    lists_three = list(db.belhelp.find({}, {'_id' : False}))
    return jsonify({'result': 'success', 'lists': lists, 'lists_two' : lists_two, 'lists_three' : lists_three})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



