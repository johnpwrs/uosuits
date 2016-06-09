#!/usr/bin/python

from aaaelasticmanager import ElasticIndex
from datetime import datetime
import json
import sys
import collections
import re

users = {}
properties = [
  'Range',
  'Owner',
  'Physical Damage',
  'Fire Damage',
  'Poison Damage',
  'Cold Damage',
  'Energy Damage',
  'Chaos Damage',
  'Cold Resist',
  'Damage Increase',
  'Defense Chance Increase',
  'Dexterity Bonus',
  'Durability',
  'Energy Resist',
  'Enhance Potions',
  'Faster Cast Recovery',
  'Faster Casting',
  'Fire Resist',
  'Hit Cold Area'
  'Hit Energy Area',
  'Hit Fire Area',
  'Hit Physical Area',
  'Hit Poison Area',
  'Hit Chance Increase',
  'Hit Curse',
  'Hit Dispel',
  'Hit Fatigue',
  'Hit Fireball',
  'Hit Harm',
  'Hit Life Leech',
  'Hit Lightning',
  'Hit Lower Attack',
  'Hit Lower Defense',
  'Hit Mana Drain',
  'Hit Mana Leech',
  'Hit Point Increase',
  'Hit Point Regeneration',
  'Hit Stamina Leech',
  'Intelligence Bonus',
  'Lower Mana Cost',
  'Lower Reagent Cost',
  'Lower Requirements',
  'Luck',
  'Mage Armor',
  'Mage Weapon',
  'Mana Increase',
  'Mana Regeneration',
  'Night Sight',
  'Physical Resist',
  'Poison Resist',
  'Reflect Physical Damage',
  'Self Repair',
  'Slayer',
  'Skill Bonus',
  'Spell Channeling',
  'Spell Damage Increase',
  'Stamina Increase',
  'Stamina Regeneration',
  'Strength Bonus',
  'Strength Requirement',
  'Swing Speed Increase',
  'Use Best Weapon Skill',
  'Weight',
  'Blood Drinker',
  'Battle Lust',
  'Casting Focus',
  'Damage Eater',
  'Poison Eater',
  'Fire Eater',
  'Energy Eater',
  'Kinetic Eater',
  'Cold Eater',
  'Weapon Damage',
  'Weapon Speed',
  'Ammo',
  'Crafted By',
  'Contents',
  'Reactive Paralyze',
  'Resonance',
  'Soul Charge',
  'Splintering Weapon',
  'Artifact Rarity',
  'Bane',
  'Balanced',
  'Blessed',
  'Brittle',
  'Cursed',
  'Damage Modifier',
  'Eleves Only',
  'Exceptional',
  'Gargoyles Only',
  'Increased Karma Loss',
  'Insured',
  'Lifespan',
  'Lower Ammo Cost',
  'Mana Burst',
  'Mana Phase',
  'No-Drop',
  'No-Trade',
  'One-Handed Weapon',
  'Owned By',
  'Rage Focus',
  'Two-Handed Weapon',
  'Velocity',
  'Weight Reduction',
  'Prized',
  'Massive',
  'Unweildy',
  'Cursed',
  'Antique',
  'Archery',
  'Chivalry',
  'Fencing',
  'Focus',
  'Mace Fighting',
  'Parrying',
  'Swordsmanship',
  'Tactics',
  'Wrestling',
  'Bushido',
  'Throwing',
  'Healing',
  'Veterinary',
  'Alchemy',
  'Evaluating Intelligence',
  'Evaluate Intelligence',
  'Inscription',
  'Magery',
  'Meditation',
  'Necromancy',
  'Resisting Spells',
  'Spellweaving',
  'Spirit Speak',
  'Mysticism',
  'Discordance',
  'Musicianship',
  'Peacemaking',
  'Provocation',
  'Begging',
  'Detecting Hidden',
  'Hiding',
  'Lockpicking',
  'Poisoning',
  'Remove Trap',
  'Snooping',
  'Stealing',
  'Stealth',
  'Ninjitsu',
  'Anatomy',
  'Animal Lore',
  'Animal Taming',
  'Camping',
  'Forensic Evaluation',
  'Herding',
  'Taste Identification',
  'Tracking',
  'Arms Lore',
  'Blacksmith',
  'Carpentry',
  'Cooking',
  'Item Identification',
  'Tailoring',
  'Tinkering',
  'Imbuing',
  'Fishing',
  'Mining',
  'Lumberjacking',
  'Fletching Bonus'
]
FULL_SET_PREFIX = "Only When Full Set Is Present"

with open('settings.json') as settings_file:
    settings = json.load(settings_file)

with open('mappings.json') as mappings_file:
    mappings = json.load(mappings_file)

user_start = False
equip_start = False
user_details = None
user_id = None
user_titles = []

def parse_user_data_new(line):
    global user_start
    global equip_start
    global user_details
    global user_id
    global user_titles
    
    user_details = line.split('$')
    date = user_details[0]
    time = user_details[1]
    date_time = datetime.strptime(
        date + ':' + time, 
        '%y%m%d:%H%M%S'
    )
    date_time = date_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    user_id = user_details[2]

    user_type = user_details[3].split(' ')[0]
    name = user_details[3].lstrip(user_type).strip()

    user_rep = None
    
    # the remaining details split from the input line
    # will contain a number of "titles" for the user
    # and the reputation of the user.  if the line is numeric,
    # we know it is the reputation 
    for i in range(4, len(user_details)):
        if user_details[i].isnumeric():
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

    # the original import sometimes didn't record a name 
    if name:
        users[user_id]['name'] = name
        if name not in users[user_id]['names']:
            users[user_id]['names'].append(name)
    
    users[user_id]['suits'].append({"found_date":date_time, "gear":[]})

    
    user_start = False
    equip_start = True

def parse_equipment_data_new(line):
    global user_start
    global equip_start
    global user_details
    global user_id
    global user_titles

    suit_index = len(users[user_id]['suits']) - 1
    gear = line.split('$')
    gear_id = gear[0]

    gear_name = gear[1]
    gear_properties = {"other":[]}
    is_set = False
  
    # being parsing gear information
    for i in range(2, len(gear)):
       
        # Make sure the information exists and is parseable
        if len(gear[i].strip()) > 0:
            
            # check if this item is part of a set,
            # but the full set is not present
            # if so, we nest this information into it's own object
            if FULL_SET_PREFIX in gear[i]:
                gear_properties[FULL_SET_PREFIX] = {}
                is_set = True
            
            # loop through all known prpoerties
            # and see if it matches the property we are looking at
            found_prop = False
            for property in properties:
                if property in gear[i]:
                    found_prop = True
                    
                    # Split property at property name
                    # index 1 will give us the property value
                    # If there is no value here, it's a property type that
                    # isn't given a numerical value
                    split_prop = gear[i].split(property)
                    if split_prop[1]:
                        if is_set:
                            gear_properties[FULL_SET_PREFIX][property] = split_prop[1].strip()
                        else:
                            if property in gear_properties:
                                gear_properties[property] = [
                                    gear_properties[property], 
                                    split_prop[1].strip()
                                ]
                            else:
                                gear_properties[property] = split_prop[1].strip()
                    else:
                        if is_set:
                            gear_properties[FULL_SET_PREFIX][property] = True
                        else:
                            gear_properties[property] = True
            # Record all properties we don't know about,
            # just in case
            if not found_prop:
                gear_properties["other"].append(gear[i])
                #gear_properties[gear[i]] = True

    users[user_id]['suits'][suit_index]['gear'].append({
       "name": gear_name,
       "id": gear_id,
       "properties": gear_properties,
       "src": line 
    })

def clean_suits():
    for user in users:
        del_indices = []
        suit_dupes = {}
        counter = 0

        for i in range(0, len(users[user]['suits'])):
            filter_suit_a = filter_suit(users[user]['suits'][i])
            filter_suit_counter = collections.Counter(filter_suit_a) 
            found_counter = False
            for key, val in suit_dupes.iteritems():
                if suit_dupes[key]['counter'] == filter_suit_counter:
                    found_counter = True
                    suit_dupes[key]['indexes'].append(i)
            
            if not found_counter:
                suit_dupes[counter] = {
                    'counter': filter_suit_counter,
                    'indexes': [i]
                }
                counter = counter + 1
      
        del_indices = []
        for key, val in suit_dupes.iteritems():
            if len(suit_dupes[key]['indexes']) > 1:
                del suit_dupes[key]['indexes'][0]
                for index in suit_dupes[key]['indexes']:
                    del_indices.append(index)
       
        del_indices.sort() 
        for index in reversed(del_indices):
            del users[user]['suits'][index]

def import_suits():
    global user_start
    global equip_start
    global user_details
    global user_id
    global user_titles
    
    user_start = False
    equip_start = False
    user_details = None
    user_id = None
    
    for line in open('suitnew14.txt', 'r'):
        line = unicode(line, errors='replace')
        user_titles = []
        line = line.strip().replace('\n', '')
        if line == '*****':
            user_start = True
            equip_start = False
            continue
        
        if user_start:
            parse_user_data_new(line)
            continue

        if equip_start:
            parse_equipment_data_new(line)

def calculate_totals():
    for user in users:
        for suit in users[user]['suits']:
            totals = {}
            set_pieces = []
            for gear in suit['gear']:
                for property_name, value in gear['properties'].iteritems():
                    if value == True:
                        continue
                    if isinstance(value, dict):
                        continue

                    # Pieces of gear part of full sets sometimes have
                    # a property listed twice.  We only want the total value
                    if isinstance(value, list):
                        for val in value:
                            if '(total)' in val:
                                value = val
                                break
                        if isinstance(value, list):
                            continue
                    if '(total)' in value:
                        value = value.rstrip('(total)').strip()
                    
                        if property_name in set_pieces:
                            continue
                        else:
                            set_pieces.append(property_name)
                    
                    value = value.rstrip('%')
                    value = value.lstrip('+')
                    try:
                      value = int(value)
                    except:
                      continue
                    
                    if property_name in totals:
                        totals[property_name] += value
                    else:
                        totals[property_name] = value
            suit['totals'] = totals

def get_user_bulk_req(user_id, user):
    bulk_request = ''
    bulk_request += json.dumps(
        {
            "create":{
                "_type":"user", 
                "_id":user_id, 
                "_index":"uosuits"
            }
        }
    )
    user_data = {
      "name": user['name'],
      "names": user['names'],
      "reputation":user['reputation']
    }
    bulk_request += '\n'
    bulk_request += json.dumps(user_data)
    bulk_request += '\n'
    return bulk_request

def get_user_update_req(user_id, user, user_doc):
    bulk_request = ''
    
    user_update = {"update":{"_index":"uosuits", "_type":"user", "_id":user_id}}
    update_doc = {"doc":{}} 
    
    es_name = user_doc['_source']['name']
    es_names = user_doc['_source']['names']
    
    if user['name'] != es_name: 
        update_doc['doc']['name'] = user['name']
   
    namesChanged = False 
    for name in user['names']:
        if name not in es_names:
            namesChanged = True 
            es_names.append(name)
    if namesChanged:
        update_doc['doc']['names'] = es_names
    if update_doc['doc']:
        bulk_request += json.dumps(user_update)
        bulk_request += '\n'
        bulk_request += json.dumps(update_doc)
        bulk_request += '\n'               
    return bulk_request
    
def get_user_suits(index, user):
    search_query = {
        "query": {
            "has_parent": {
                "parent_type": "user",
                "query": {
                    "ids": {
                        "values":[user] 
                    }
                }
            }
        },
        "size":100
    }

    return index.search(search_query, ['suits'])

def filter_suit(suit):
    filtered_suit = []
    if '_source' in suit:
        suit = suit['_source']
    for piece in suit['gear']:
        split_src = piece['src'].split('$')
        if len(split_src) > 1:
            if 'Rudder' == split_src[1]:
                continue
            if 'Ship' == split_src[1]:
                continue
        if 'Backpack' in piece['src']:
            continue
        filtered_suit.append(re.sub(r"Durability.*?\$", "", piece['src']))
    
    return filtered_suit



def update_elastic():
    index = ElasticIndex(
        'uosuits', 
        'https://search-suits-vbaatnpkzo5wgizkdelx64a2w4.us-west-2.es.amazonaws.com',
        port=443
    )

    #if not index.exists():
    #    result = index.create(settings, mappings)
    #    print result
    
    bulk_request = ''
    count = 0
    for user in users:
        if 'name' not in users[user]:
            continue
       
        user_doc = index.get_document('user', user)

        if '_source' not in user_doc:
            print "adding new user %s" %(users[user]['name'])
            bulk_request += get_user_bulk_req(user, users[user]) 
        else:
            user_update = get_user_update_req(user, users[user], user_doc)
            if len(user_update) > 0:
                bulk_request += user_update
                print "updating user info for %s" %(users[user]['name']) 
        
        es_user_suits = get_user_suits(index, user)['hits']['hits']
                  
        for suit in users[user]['suits']:
            add_suit = True
            filtered_suit = filter_suit(suit)
            for es_suit in es_user_suits:
                filtered_es_suit = filter_suit(es_suit)
                if collections.Counter(filtered_suit) == collections.Counter(filtered_es_suit):
                    add_suit = False
            
            if add_suit:
                print "adding new new suit for %s" %(users[user]['name'])
                suit['user_id'] = user
                bulk_request += json.dumps(
                    {
                        "create":{
                            "_type":"suits", 
                            "_parent":user, 
                            "_index":"uosuits"
                        }
                    }
                )
                bulk_request += '\n'
                bulk_request += json.dumps(suit)
                bulk_request += '\n'
        

        count = count + 1
        if count > 500 and len(bulk_request) > 0:
            print "sending bulk request"
            result = index.bulk_write(bulk_request)
            print result
            bulk_request = ''
            count = 0

    if len(bulk_request) > 0:
        print "sending bulk request"
        result = index.bulk_write(bulk_request)
        print result

if __name__ == '__main__':
    import_suits()
    clean_suits()
    calculate_totals()
    update_elastic()

