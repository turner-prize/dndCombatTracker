from flask import Flask, render_template, jsonify, request
from enemies import Enemy, Goblin1,Goblin2,Goblin3
from flask_sqlalchemy import SQLAlchemy
import itertools
import os
from models import createEnemyInstance,addToCombatTable,getCombatOrder,generateEnemiesList


mydir=os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(mydir,'combatTracker.db')}"

x=createEnemyInstance('Goblin')
y=createEnemyInstance('Bandit')
z=createEnemyInstance('Drow')

InitiativeOrder = [x,y,z]

for i in InitiativeOrder:
    addToCombatTable(i)

refdict = {i.name:i for i in InitiativeOrder} #ref dictionary for class lookup

CurrentTurn = itertools.cycle(InitiativeOrder)

@app.route('/attack', methods=['POST'])
def attack():
    attacker=refdict[request.form['attacker[name]']]
    for i in attacker.weapons:
        if i.name == request.form['weapon']:
            activeweapon=i
    target=refdict[request.form['target']]
    attacker.Attack(activeweapon,target)
    return render_template('section.html',mylist=InitiativeOrder,nextitem=attacker)

@app.route('/nextItem')
def nextItem():
    return render_template('section.html',mylist=InitiativeOrder,nextitem=next(CurrentTurn))

@app.route('/chooseEnemies')
def chooseEnemies():
    enemiesList=generateEnemiesList()
    return render_template('chooseEnemies.html',enemieslist=enemiesList)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        print(request.form['enemy'])
        enemiesList=generateEnemiesList()
        return render_template('chooseEnemies.html',enemieslist=enemiesList)
    else:
	    return render_template('index.html',mylist=InitiativeOrder,nextitem=next(CurrentTurn))

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False) #usereloader added as debug mode causes flask to run twice when loaded.