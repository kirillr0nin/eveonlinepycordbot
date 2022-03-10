from tkinter import N
import requests
import json

def wallet():
    with open('token.json', 'r') as token_file:
        d = json.load(token_file)
        access_token = d['access_token']
    headers = {
            "Authorization": "Bearer {}".format(access_token)
        }
    res = requests.get('https://esi.evetech.net/latest/characters/2115788560/wallet/', headers=headers)
    data = res.json()
    return data

def get_skills():
    #16622 - 274 - Accounting
    #3446 - 274 - Broker Relations
    #16597 - 274 - Advanced Broker Relations
    with open('token.json', 'r') as token_file:
        d = json.load(token_file)
        access_token = d['access_token']
    headers = {
            "Authorization": "Bearer {}".format(access_token)
        }
    res = requests.get('https://esi.evetech.net/latest/characters/2115788560/skills/', headers=headers)
    data = res.json()
    #with open('skills.json', 'w') as skills:
    #   print(data, file=skills)
    broker = 3446
    acc = 16622
    abr = 16597
    acclvl = parse_accounting(acc=acc, data=data)
    brokerlvl = parse_broker(broker=broker, data=data)
    abrlvl = parse_abr(abr=abr, data=data)
    skills = {
        'skills' : [
            {
                "accounting" : acclvl,
                "broker_relations" : brokerlvl,
                "advanced_broker_relations" : abrlvl,
            }
        ]
    }
    with open('skills.json', 'w') as skills_file:
        r = json.dumps(skills)
        print(r, file=skills_file)
    levels = "Accounting: {} , Broker: {} , ABR: {}".format(acclvl, brokerlvl, abrlvl)
    return levels

def get_standings():
    with open('token.json', 'r') as token_file:
        d = json.load(token_file)
        access_token = d['access_token']
    headers = {
            "Authorization": "Bearer {}".format(access_token)
        }
    res = requests.get('https://esi.evetech.net/latest/characters/2115788560/standings/', headers=headers)
    data = res.json()
    #with open('standings.json', 'w') as standings:
    #   print(data, file=standings)
    caldarinavy = 1000035
    caldaristate = 500001
    faction = parse_faction(caldaristate=caldaristate, data=data)
    navy = parse_corp(caldarinavy=caldarinavy, data=data)
    standings = {
        'standings' : [
            {
                "caldari_navy" : navy,
                "caldari_state" : faction,
            }
        ]
    }
    with open('standings.json', 'w') as standings_file:
        b = json.dumps(standings)
        print(b, file=standings_file)
    standing = "Caldary Faction: {}, Caldary Navy: {}".format(faction, navy)
    return standing

def brokerfee():
    with open('skills.json', 'r') as skills_file:
        d = json.load(skills_file)
        broker = d['skills'][0]['broker_relations']
        accounting = d['skills'][0]['accounting']
    with open('standings.json', 'r') as standings_file:
        d = json.load(standings_file)
        faction = d['standings'][0]['caldari_state']
        corp = d['standings'][0]["caldari_navy"]
    res = 0.03-(0.003 * broker)-(0.0003 * faction)-(0.0002 * corp)
    sales = 0.08 - 0.0088 * accounting
    return res, sales

def trade(buy, sell):
    with open('skills.json', 'r') as skills_file:
        d = json.load(skills_file)
        broker = d['skills'][0]['broker_relations']
        accounting = d['skills'][0]['accounting']
    with open('standings.json', 'r') as standings_file:
        d = json.load(standings_file)
        faction = d['standings'][0]['caldari_state']
        corp = d['standings'][0]["caldari_navy"]
    broker = 0.03-(0.003 * broker)-(0.0003 * faction)-(0.0002 * corp)
    sales = 0.08 - 0.0088 * accounting
    buyorder = buy + (buy * broker)
    sellorder = sell - ((sell * sales) + (sell * broker))
    profit = sellorder - buyorder
    percprofit = (buyorder / sellorder) * 100
    return profit

def parse_faction(caldaristate, data):
    for standing in data:
        if standing['from_id'] == caldaristate:
            cldrstanding = standing['standing']
            if cldrstanding > 0:
                return cldrstanding
            else:
                n = 0
                return n
        else:
            n = 0
            return n
def parse_corp(caldarinavy, data):
    for standing in data:
        if standing['from_id'] == caldarinavy:
            navystanding = standing['standing']
            if navystanding > 0:
                return navystanding
            else:
                n = 0
                return n
        else:
            n = 0
            return n

def parse_accounting(acc, data):
    for skill in data['skills']:
        if skill['skill_id'] == acc:
            acclvl = skill['trained_skill_level']
            if acclvl > 0:
                return acclvl
            else:
                n = 0
                return n


def parse_broker(broker, data):
    for skill in data['skills']:
        if skill['skill_id'] == broker:
            brokerlvl = skill['trained_skill_level']
            if brokerlvl > 0:
                return brokerlvl
            else:
                n = 0
                return n


def parse_abr(abr, data):
    for skill in data['skills']:
        if skill['skill_id'] == abr:
            abrlvl = skill['trained_skill_level']
            if abrlvl > 0:
                return abrlvl
            else:
                n = 0
                return n