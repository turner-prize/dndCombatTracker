import requests
from models import CreateSession, Enemy,SpecialTraits, ActionsText, Action, LedgendaryAction


def GetMonster(monsterID):
    r = requests.get(f"http://www.dnd5eapi.co/api/monsters/{monsterID}")
    monster = r.json()
    session = CreateSession()
    x = session.query(Enemy).filter_by(name=monster['name']).first()
    if not x:
        if 'actions' in monster:
            enemiesTable(monster,session)
            specialAbilitiesTable(monster,session)
            actionsTextTable(monster,session)
            actionsTable(monster,session)
            ledgendaryActionsTable(monster,session)
            session.commit()
            session.close()
            print(f"{monster['name']} added!")
        else:
            print(f"{monster['name']} already exists!")


def enemiesTable(monster,session):
    hpmod = int(int(monster['hit_dice'].split('d')[0]) * int(((int(monster['constitution']) - 10) / 2)))
    enemy=Enemy(
                name = monster['name'],
                size = monster['size'],
                type = monster['type'],
                alignment = monster['alignment'],
                ac = monster['armor_class'],
                armorType = 'natural armor', #not showing up
                hp = f"{monster['hit_dice']}+{hpmod}",
                speed = monster['speed'],
                STR = monster['strength'],
                DEX = monster['dexterity'],
                CON = monster['constitution'],
                INT = monster['intelligence'],
                WIS = monster['wisdom'],
                CHA = monster.get('charisma',None),
                challenge = monster['challenge_rating'],
                senses = monster['senses'],
                languages = monster['languages'],
                damage_vulnerabilities= monster['damage_vulnerabilities'],
                damage_resistances= monster['damage_resistances'],
                damage_immunities= monster['damage_immunities'],
                condition_immunities= monster['condition_immunities'])

    session.add(enemy)

def specialAbilitiesTable(monster,session):
    x = session.query(Enemy).filter_by(name=monster['name']).first()
    if 'special_abilities' in monster:
        for i in monster['special_abilities']:
            st = SpecialTraits(enemyid=x.id,title=i['name'],description=i['desc'])
            session.add(st)

def actionsTextTable(monster,session):
    x = session.query(Enemy).filter_by(name=monster['name']).first()
    for i in monster['actions']:
        if ":" in i['desc']:
            xtype= i['desc'].split(':')[0]
            desc= i['desc'].split(':')[1]
        else:
            xtype = None
            desc = i['desc']
        at = ActionsText(enemyid=x.id,title=i['name'],actionType=xtype,description=desc)
        session.add(at)

def actionsTable(monster,session):
    x = session.query(Enemy).filter_by(name=monster['name']).first()
    for i in monster['actions']:
        if 'damage_dice' in i:
            xtype= i['desc'].split(':')[0]

            if 'damage_bonus' in i:
                damage=f"{i['damage_dice']}+{i['damage_bonus']}"
            else:
                damage=f"{i['damage_dice']}"

            action=Action(enemyid=x.id,
                            name=i['name'],
                            attackBonus=f"+{i['attack_bonus']}",
                            damage=damage,
                            targetMax="one target", #no target numbers for now
                            damageType="Bludgeoning") #no damage type for now
            session.add(action)

def ledgendaryActionsTable(monster,session):
    x = session.query(Enemy).filter_by(name=monster['name']).first()
    if 'legendary_actions' in monster:
        for i in monster['legendary_actions']:
            la = LedgendaryAction(enemyid=x.id,title=i['name'],description=i['desc'])
            session.add(la)



for i in range(1,300):
    GetMonster(i)