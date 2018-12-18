from flask import Flask, render_template, jsonify, request
from enemies import Enemy, Goblin1,Goblin2,Goblin3
from flask_sqlalchemy import SQLAlchemy
import itertools



app = Flask(__name__)
db = SQLAlchemy(app)

InitiativeOrder = [Goblin1,Goblin2,Goblin3]
refdict = {i.name:i for i in InitiativeOrder} #ref dictionary for class lookup
    
InitiativeOrder.sort(key=lambda x: int(x.initiative), reverse=True)
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

@app.route('/')
def index():
	return render_template('index.html',mylist=InitiativeOrder,nextitem=next(CurrentTurn))

if __name__ == '__main__':
    app.run(debug=True)