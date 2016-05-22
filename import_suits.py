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
full_set = "Only When Full Set Is Present"

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
                #print name
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
            gear_properties = {}
            is_set = False
            for i in range(1, len(gear)):
                
                if len(gear[i].strip()) > 0:
                    try:
                        gear[i] = gear[i].encode('utf-8')
                    except:
                        continue

                    if full_set in gear[i]:
                        gear_properties[full_set] = {}
                        is_set = True
                    found_prop = False
                    for property in properties:
                        if property in gear[i]:
                            found_prop = True
                            split_prop = gear[i].split(property)
                            if split_prop[1]:
                              if is_set:
                                gear_properties[full_set][property] = split_prop[1].strip()
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
                                gear_properties[full_set][property] = True
                              else:
                                gear_properties[property] = True
                    if not found_prop:
                        #print gear[i]
                        gear_properties[gear[i]] = True
                    #gear_properties.append(gear[i])

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
            gear_properties = {}
            is_set = False
            for i in range(2, len(gear)):
                if len(gear[i].strip()) > 0:
                    try:
                        gear[i] = gear[i].encode('utf-8')
                    except:
                        continue
                    # They have a piece part of a set, but not the full set
                    if full_set in gear[i]:
                        gear_properties[full_set] = {}
                        is_set = True
                    found_prop = False
                    for property in properties:
                        if property in gear[i]:
                            found_prop = True
                            split_prop = gear[i].split(property)
                            if split_prop[1]:
                              if is_set:
                                gear_properties[full_set][property] = split_prop[1].strip()
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
                                gear_properties[full_set][property] = True
                              else:
                                gear_properties[property] = True
                    if not found_prop:
                        #print gear[i]
                        gear_properties[gear[i]] = True
                    #gear_properties.append(gear[i])

            users[user_id]['suits'][suit_index]['gear'].append({
               "id": gear_id,
               "name": gear_name,
               "properties": gear_properties 
            })
            #print line

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

if __name__ == '__main__':
    import_suits_old()
    clean_old_suits()
    import_suits()
    calculate_totals()

    #sys.exit(1) 
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
