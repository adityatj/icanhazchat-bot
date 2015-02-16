import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import thread

__author__ = 'adityatj'
__version__ = 'v2'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}
cookie = str()
key = str()
custid = str()

def signin(user=None, passwd=None):
    r = requests.get('http://www.icanhazchat.com/signin', headers=headers)
    headers['Cookie'] = r.headers['set-cookie'].split(';')[0]
    if user != None and passwd != None:
        soup = BeautifulSoup(r.text)    
        payload = {'__LASTFOCUS'     : soup.select('#__LASTFOCUS')[0].attrs['value'],
                   '__EVENTTARGET'   : soup.select('#__EVENTTARGET')[0].attrs['value'],
                   '__EVENTARGUMENT' : soup.select('#__EVENTARGUMENT')[0].attrs['value'],
                   '__VIEWSTATE' : soup.select('#__VIEWSTATE')[0].attrs['value'],
                   '__VIEWSTATEGENERATOR' : soup.select('#__VIEWSTATEGENERATOR')[0].attrs['value'],
                   '__EVENTVALIDATION' : soup.select('#__EVENTVALIDATION')[0].attrs['value'],
                   'ctl00$ContentPlaceHolder1$btnSubmit' : 'Sign Me In',
                   'ctl00$ContentPlaceHolder1$txtAccountName' : user,
                   'ctl00$ContentPlaceHolder1$txtPassword1' : passwd}
        r = requests.post('http://www.icanhazchat.com/signin',
                          headers=headers,
                          data=payload,
                          allow_redirects=False)
        
        headers['Cookie'] += ';' + r.headers['set-cookie']
    print 'Sign in done!'

def joinroom(room, nick):
    r = requests.get('http://www.icanhazchat.com/?room=%s' % room, headers=headers)
    soup = BeautifulSoup(r.text)    
    payload = {'__LASTFOCUS'     : soup.select('#__LASTFOCUS')[0].attrs['value'],
               '__EVENTTARGET'   : soup.select('#__EVENTTARGET')[0].attrs['value'],
               '__EVENTARGUMENT' : soup.select('#__EVENTARGUMENT')[0].attrs['value'],
               '__VIEWSTATE' : soup.select('#__VIEWSTATE')[0].attrs['value'],
               '__VIEWSTATEGENERATOR' : soup.select('#__VIEWSTATEGENERATOR')[0].attrs['value'],
               '__EVENTVALIDATION' : soup.select('#__EVENTVALIDATION')[0].attrs['value'],
               'WHARBARGL1' : soup.select('#WHARBARGL1')[0].attrs['value'],
               'WHARBARGLpass' : soup.select('#WHARBARGLpass')[0].attrs['value'],
               'ctl00$ContentPlaceHolder1$backImgUrl' : soup.select('#ctl00_ContentPlaceHolder1_backImgUrl')[0].attrs['value'],
               'ctl00$ContentPlaceHolder1$btnLogin' : soup.select('#ctl00_ContentPlaceHolder1_btnLogin')[0].attrs['value'],
               'ctl00$ContentPlaceHolder1$txtUserName' : nick}
    cookie = soup.select('#WHARBARGL1')[0].attrs['value']
    r = requests.post('http://www.icanhazchat.com/?room=%s' % room,
                      headers=headers,
                      data=payload)
    r = requests.get('http://www.icanhazchat.com/%s' % room, headers=headers)
    soup = BeautifulSoup(r.text)
    key = soup.select('#WHARBARGL')[0].attrs['value']
    print 'Joined room: %s' % room
    return {'key' : key, 'cookie' : cookie}

def getuserslist():
    payload = {'keyString' : key,
               'cookie' : cookie}
    head = dict(headers)
    head['X-Requested-With'] = 'XMLHttpRequest'
    head['Content-Type'] = 'application/json;'
    r = requests.post('http://www.icanhazchat.com/chat.aspx/GetUserList',
                      headers=head,
                      data=json.dumps(payload))
    data = r.json()
    if data['d'] != '':
        print 'Users List:'
        for user in data['d'].split(','):
            print user
    
def updateuser():
    payload = {'keyString' : key}
    head = dict(headers)
    head['X-Requested-With'] = 'XMLHttpRequest'
    head['Content-Type'] = 'application/json;'
    r = requests.post('http://www.icanhazchat.com/chat.aspx/UpdateUser',
                      headers=head,
                      data=json.dumps(payload))
    data = r.json()
    if data['d'] != '' and data['d'] != None:
        print data['d']
        return data['d']

def sendmsg(msg):
    payload = {'keyString' : key,
               'msg' : msg}
    head = dict(headers)
    head['X-Requested-With'] = 'XMLHttpRequest'
    head['Content-Type'] = 'application/json;'
    r = requests.post('http://www.icanhazchat.com/chat.aspx/SendMessage',
                      headers=head,
                      data=json.dumps(payload))
    data = r.json()
    if data['d'] != '' and data['d'] != None:
        print data['d']
        return data['d']

def leaveroom():
    sendmsg('Okay Mortals, it\'s time for the God to address the Heaven\'s gathering. So, Bye for now!')
    payload = {'keyString' : key}
    head = dict(headers)
    head['X-Requested-With'] = 'XMLHttpRequest'
    head['Content-Type'] = 'application/json;'
    r = requests.post('http://www.icanhazchat.com/chat.aspx/LeaveRoom',
                      headers=head,
                      data=json.dumps(payload))
    if r.status_code == 200:
        print 'Left the room'

def signout():
    r = requests.get('http://www.icanhazchat.com/?signout=1',
                     headers=headers)
    head = dict(headers)
    head['Cookie'] = headers['Cookie'].split(';')[0]
    r = requests.get('http://www.icanhazchat.com/?signout=2',
                     headers=head)
    if r.status_code == 200:
        print 'Logged out!'
    
def godmsg(msg):
    global custid
    payload = {'input' : msg}
    if custid != '' or custid != None:
        payload['custid'] = custid
    godhead = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36'}
    r = requests.post('http://www.pandorabots.com/pandora/talk-xml?botid=923c98f3de35606b', data=payload, headers=godhead)
    soup = BeautifulSoup(r.text)
    result = soup.findAll('result')[0]
    if result.attrs['status'] == '0':
        if custid != '':
            result = soup.findAll('result')[0]
            custid = result.attrs['custid']
        return soup.findAll('that')[0].text.strip()
    
def replythread(user, msg):
    reply = godmsg(msg)
    print '@' + user + ' ' +reply
    msg = sendmsg('@' + user + ' ' +reply)
    if msg != None and '!god' in msg:
        user = msg.split(':')[0].split('|')[1]
        q = msg[msg.find('!god')+5:]
        thread.start_new_thread(replythread, (user, BeautifulSoup(q).text,))
    
#driver
try:
    signin('<username>', '<password>')
    d = joinroom('<roomname>', '<nickname>')
    key=d['key']
    cookie=d['cookie']
    getuserslist()
    sendmsg('Hello there Mortals! God here. Ask me anything. (Usage: !god<space><your question>)')
    while True:
        msg = updateuser()
        if msg != None and '!god' in msg:
            user = msg.split(':')[0].split('|')[1]
            q = msg[msg.find('!god')+5:]
            thread.start_new_thread(replythread, (user, BeautifulSoup(q).text,))
        sleep(1)
except:
    leaveroom()
    signout()


    
