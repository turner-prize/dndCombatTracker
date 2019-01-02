from flask import Flask, render_template, jsonify, request
from enemies import Enemy
from flask_sqlalchemy import SQLAlchemy
import itertools
import os
from models import createEnemyInstance,addToCombatTable,truncateCombatList,getCombatOrder,generateEnemiesList,generateHeroesList,referenceEnemyInstanceByName
from models import referenceEnemyInstance,createHeroInstance,getNextTurn,markTurn

mydir=os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(mydir,'combatTracker.db')}"
# db=SQLAlchemy(app)

truncateCombatList()

@app.route('/statBlock')
def statBlockTest():
    x=createEnemyInstance('Aboleth')
    return render_template('demo-two-column-inlined.html',enemy=x)

@app.route('/attack', methods=['POST'])
def attack():
    print(request.form)
    attacker = referenceEnemyInstanceByName(request.form['attacker[name]'])
    for i in attacker.actions:
        if i.actionName == request.form['action']:
            action=i
    target = referenceEnemyInstanceByName(request.form['target'])
    text = attacker.Attack(action,target)
    InitiativeOrder=getCombatOrder()
    return render_template('section.html',mylist=InitiativeOrder,nextitem=attacker,flavourText=text,enemy=attacker)

@app.route('/manualDamage', methods=['POST'])
def manualDamage():
    attacker = referenceEnemyInstanceByName(request.form['attacker[name]'])
    target = referenceEnemyInstanceByName(request.form['target'])
    damage = int(request.form['damage'])
    target.Damage(damage)
    InitiativeOrder=getCombatOrder()
    return render_template('section.html',mylist=InitiativeOrder,nextitem=attacker,enemy=attacker)

@app.route('/nextItem')
def nextItem():
    InitiativeOrder=getCombatOrder()
    x=getNextTurn()
    #error cropping up here, probs because its trying to referemce an enemy instance which has no enemy id.
    #might need to say 'if enemy id is null'
    current = referenceEnemyInstance(x)
    markTurn(x)
    return render_template('section.html',mylist=InitiativeOrder,nextitem=current,enemy=current)

@app.route('/chooseEnemies')
def chooseEnemies():
    enemiesList=generateEnemiesList()
    heroesList=generateHeroesList()
    return render_template('chooseEnemies.html',enemieslist=enemiesList,heroeslist=heroesList)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        enemy=request.form.get('enemy',None)
        if enemy:
            enemy=request.form['enemy'] #pass enemy name (string) to enemy variable
            enemy=createEnemyInstance(enemy) #use name of enemy (e.g. Goblin) to create a class instance of Enemy.
            addToCombatTable(enemy) #adds to combat list with an appended number to signify which instance of the enemy it is
        else:
            hero=request.form['hero']
            initiative=request.form['initiative']
            hero=createHeroInstance(hero)
            hero.SetInit(initiative)
            addToCombatTable(hero)
        enemiesList=generateEnemiesList()
        heroesList=generateHeroesList()
        return render_template('chooseEnemies.html',enemieslist=enemiesList,heroeslist=heroesList)
    else:
        InitiativeOrder=getCombatOrder()
        if InitiativeOrder: #if there is an initiative order list, it means players and enemies have been added.
            x=getNextTurn()
            current = referenceEnemyInstance(x) #creates another Enemy class instance with existing data to populate the html
            markTurn(x)
            for i in InitiativeOrder:
                print (i.enemyName)
            print(current.name)
            return render_template('index.html',mylist=InitiativeOrder,nextitem=current,enemy=current)
        else: #if there is no initiative order it's probably the first time you're opening the session
            return render_template('startPage.html')

if __name__ == '__main__':
    app.run(debug=True) #usereloader added as debug mode causes flask to run twice when loaded.

    #https://stackoverflow.com/questions/34009296/using-sqlalchemy-session-from-flask-raises-sqlite-objects-created-in-a-thread-c