import requests
from models import CreateSession, Enemy,SpecialTraits, ActionsText, Action

r = requests.get("http://www.dnd5eapi.co/api/monsters/1")

monster = r.json()

session = CreateSession()
enemy=Enemy(
    name = monster['name'],
size = monster['size'],
type = monster['type'],
alignment = monster['alignment'],
ac = monster['armor_class'],
armorType = 'natural armor', #not showing up
hp = monster['hit_dice'], #is wrong tho
speed = monster['speed'],
STR = monster['strength'],
DEX = monster['dexterity'],
CON = monster['constitution'],
INT = monster['intelligence'],
WIS = monster['wisdom'],
CHA = 18,#monster['charisma'],
challenge = monster['challenge_rating'],
senses = monster['senses'],
languages = monster['languages'])

session.add(enemy)
x = session.query(Enemy).filter_by(name=enemy.name).first()

for i in monster['special_abilities']:
    st = SpecialTraits(enemyid=x.id,title=i['name'],description=i['desc'])
    session.add(st)

for i in monster['actions']:

    if ":" in i['desc']:
        xtype= i['desc'].split(':')[0]
        desc= i['desc'].split(':')[1]
    else:
        xtype = None
        desc = i['desc']

    at = ActionsText(enemyid=x.id,title=i['name'],actionType=xtype,description=desc)
    session.add(at)

for i in monster['actions']:
    if 'damage_dice' in i:
        xtype= i['desc'].split(':')[0]
        action=Action(enemyid=x.id,
                        name=i['name'],
                        type=xtype,
                        attackBonus=f"+{i['attack_bonus']}",
                        damage=f"{i['attack_bonus']}+{i['damage_bonus']}",
                        range="5 ft.",
                        targetMax="one target",
                        damageType="Bludgeoning") #no damage type for now
        session.add(action)


session.commit()
session.close()