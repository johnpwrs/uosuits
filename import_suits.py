#!/usr/bin/python

from aaaelasticmanager import ElasticIndex
from datetime import datetime
import json

users = {}

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

with open('mappings.json') as mappings_file:
    mappings = json.load(mappings_file)


def import_suits_old():
    user_start = False
    equip_start = False
    user_details = None
    user_id = None
    for line in open('suit2.txt', 'r'):
        user_titles = []
        line = line.strip().replace('\n', '')
        if line == '*****':
            user_start = True
            equip_start = False
            continue
        
        if user_start:
            user_details = line.split('$')
            date = user_details[0]
            time = user_details[1]
            date_time = datetime.strptime(
                date + ':' + time, 
                '%y%m%d:%H%M%S'
            )
            date_time = date_time.strftime('%Y-%m-%d:%H:%M:%S')
            user_id = user_details[2]

            name = user_details[3].strip()

            user_rep = None

            for i in range(4, len(user_details)):
                if unicode(user_details[i], 'utf-8').isnumeric():
                    user_rep = user_details[i]
                else:
                    user_titles.append(user_details[i])

            if user_id not in users:
                print name
                users[user_id] = {
                    "reputation": user_rep, 
                    "names":[], 
                    "suits":[]
                }
            
            if name:
                users[user_id]['name'] = name
                if name not in users[user_id]['names']:
                    users[user_id]['names'].append(name)
            
            users[user_id]['suits'].append({"found_date":date_time, "gear":[]})

            
            user_start = False
            equip_start = True
            continue

        if equip_start:
            suit_index = len(users[user_id]['suits']) - 1
            gear = line.split('$')
            try: 
                gear[0] = gear[0].encode('utf-8')
            except:
                continue 
            gear_name = gear[0]
            gear_properties = []
            for i in range(1, len(gear)):
                if len(gear[i].strip()) > 0:
                    try:
                        gear[i] = gear[i].encode('utf-8')
                    except:
                        continue
                    gear_properties.append(gear[i])

            users[user_id]['suits'][suit_index]['gear'].append({
               "name": gear_name,
               "properties": gear_properties 
            })

def clean_old_suits():
    for user in users:
        users[user]['suits'] = [users[user]['suits'][0]]

def import_suits():
    user_start = False
    equip_start = False
    user_details = None
    user_id = None
    for line in open('suit4.txt', 'r'):
        user_titles = []
        line = line.strip().replace('\n', '')
        if line == '*****':
            user_start = True
            equip_start = False
            continue
        
        if user_start:
            user_details = line.split('$')
            date = user_details[0]
            time = user_details[1]
            date_time = datetime.strptime(
                date + ':' + time, 
                '%y%m%d:%H%M%S'
            )
            date_time = date_time.strftime('%Y-%m-%d:%H:%M:%S')
            user_id = user_details[2]

            user_type = user_details[3].split(' ')[0]
            name = user_details[3].lstrip(user_type).strip()

            user_rep = None

            for i in range(4, len(user_details)):
                if unicode(user_details[i], 'utf-8').isnumeric():
                    user_rep = user_details[i]
                else:
                    user_titles.append(user_details[i])

            if user_id not in users:
                users[user_id] = {
                    "reputation": user_rep, 
                    "type": user_type,
                    "names":[], 
                    "suits":[]
                }
            
            if name:
                users[user_id]['name'] = name
                if name not in users[user_id]['names']:
                    users[user_id]['names'].append(name)
            
            users[user_id]['suits'].append({"found_date":date_time, "gear":[]})

            
            user_start = False
            equip_start = True
            continue

        if equip_start:
            suit_index = len(users[user_id]['suits']) - 1
            gear = line.split('$')
            gear_id = gear[0]
            try: 
                gear[1] = gear[1].encode('utf-8')
            except:
                continue 
            gear_name = gear[1]
            gear_properties = []
            for i in range(2, len(gear)):
                if len(gear[i].strip()) > 0:
                    try:
                        gear[i] = gear[i].encode('utf-8')
                    except:
                        continue
                    gear_properties.append(gear[i])

            users[user_id]['suits'][suit_index]['gear'].append({
               "id": gear_id,
               "name": gear_name,
               "properties": gear_properties 
            })
            #print line


if __name__ == '__main__':
    import_suits_old()
    clean_old_suits()
    import_suits()
    index = ElasticIndex(
        'uosuits', 
        'https://search-uosuits-zf2mqzjundzog3jg2xjzuqeaye.us-west-2.es.amazonaws.com',
        port=443
    )

    if not index.exists():
        result = index.create(settings, mappings)
        print result
    
    bulk_request = ''
    count = 0
    for user in users:
        bulk_request += json.dumps(
            {
                "create":{
                    "_type":"user", 
                    "_id":user, 
                    "_index":"uosuits"
                }
            }
        )
        bulk_request += '\n'
        bulk_request += json.dumps(users[user])
        bulk_request += '\n'

        count = count + 1
        if count > 500:
            result = index.bulk_write(bulk_request)
            print result
            bulk_request = ''
            count = 0

    if len(bulk_request) > 0:
        result = index.bulk_write(bulk_request)
        print result
