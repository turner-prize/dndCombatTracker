from flask import Flask, render_template, jsonify, request
import itertools
from enemies import Enemy
import json
app = Flask(__name__)

weapons =   [{'name':'Scimitar','type':'Melee','attackBonus':'+4','range':'5 ft.','targetMax':1,'damage':'1d6+2','damageType':'slashing'},
             {'name':'Shortbow','type':'Ranged','attackBonus':'+4','range':'80/320 ft.','targetMax':1,'damage':'1d6+2','damageType':'peircing'}]

weapons2 =   [{'name':'Bigger Scimitar','type':'Melee','attackBonus':'+4','range':'5 ft.','targetMax':1,'damage':'1d6+2','damageType':'slashing'},
             {'name':'Bigger Shortbow','type':'Ranged','attackBonus':'+4','range':'80/320 ft.','targetMax':1,'damage':'1d6+2','damageType':'peircing'}]

Goblin1=Enemy('goblin1','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=weapons)
Goblin2=Enemy('goblin2','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=weapons)
Goblin3=Enemy('goblin3','small','humanoid(goblinoid)','neutral evil',15,'2d6','30ft.',8,14,10,10,8,8,weapons=weapons2)

mylist = [Goblin1,Goblin2,Goblin3]
refdict = {i.name:i for i in mylist}
    
mylist.sort(key=lambda x: int(x.initiative), reverse=True)
x = itertools.cycle(mylist)

@app.route('/attack', methods=['POST'])
def attack(): 
    attacker=refdict[request.form['attacker']]
    print(attacker.name)
    for i in attacker.weapons:
        print(i.name)
        #if i.name == request.form['weapon']:
        #    activeweapon=i
    #target=refdict[request.form['target']]
    #attacker.Attack(activeweapon,target)
    return render_template('section.html',mylist=mylist,nextitem=attacker)

@app.route('/attack2', methods=['POST'])
def attack2(): 
    #attacker=refdict[request.form['attacker']]
    #print(attacker.name)
    #for i in attacker.weapons:
    #    print(i.name)
        #if i.name == request.form['weapon']:
        #    activeweapon=i
    #target=refdict[request.form['target']]
    #attacker.Attack(activeweapon,target)
    return jsonify(result=100)

@app.route('/nextItem')
def nextItem(): 
	return render_template('section.html',mylist=mylist,nextitem=next(x))

@app.route('/')
def index():
	return render_template('index.html',mylist=mylist,nextitem=next(x))

if __name__ == '__main__':
    app.run(debug=True)