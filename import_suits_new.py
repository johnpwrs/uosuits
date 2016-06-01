#!/usr/bin/python

from aaaelasticmanager import ElasticIndex
from datetime import datetime
import json
import sys

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

def parse_user_data(line):
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

    name = user_details[3].strip()

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

def parse_equipment_data(line):
    global user_start
    global equip_start
    global user_details
    global user_id
    global user_titles

    suit_index = len(users[user_id]['suits']) - 1
    gear = line.split('$')
    
    # ran into a few problems where this wasn't encoded correctly
    # skip if it we can't
    try: 
        gear[0] = gear[0].encode('utf-8')
    except:
        return 

    gear_name = gear[0]
    gear_properties = {"other":[]}
    is_set = False
  
    # being parsing gear information
    for i in range(1, len(gear)):
       
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
       "properties": gear_properties,
       "src": line 
    })



def import_suits_old():
    global user_start
    global equip_start
    global user_details
    global user_id
    global user_titles
    
    for line in open('suit2.txt', 'r'):
        line = unicode(line, errors='replace')
        user_titles = []
        line = line.strip().replace('\n', '')
        if line == '*****':
            user_start = True
            equip_start = False
            continue
        
        if user_start:
            parse_user_data(line)
            continue

        if equip_start:
           parse_equipment_data(line)

def clean_old_suits():
    for user in users:
        users[user]['suits'] = [users[user]['suits'][0]]

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
    
    for line in open('suit4.txt', 'r'):
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

def update_elastic():
    index = ElasticIndex(
        'uosuits', 
        'https://search-suits-vbaatnpkzo5wgizkdelx64a2w4.us-west-2.es.amazonaws.com',
        port=443
    )

    if not index.exists():
        result = index.create(settings, mappings)
        print result
    
    bulk_request = ''
    count = 0
    for user in users:
        if 'name' not in users[user]:
            continue
        bulk_request += json.dumps(
            {
                "create":{
                    "_type":"user", 
                    "_id":user, 
                    "_index":"uosuits"
                }
            }
        )
        user_data = {
          "name": users[user]['name'],
          "names": users[user]['names'],
          "reputation":users[user]['reputation']
        }
        bulk_request += '\n'
        #bulk_request += json.dumps(users[user])
        bulk_request += json.dumps(user_data)
        bulk_request += '\n'

        for suit in users[user]['suits']:
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
        if count > 500:
            result = index.bulk_write(bulk_request)
            print result
            bulk_request = ''
            count = 0

    if len(bulk_request) > 0:
        result = index.bulk_write(bulk_request)
        print result

if __name__ == '__main__':
    import_suits_old()
    clean_old_suits()
    import_suits()
    calculate_totals()
    update_elastic()

