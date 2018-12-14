from flask import Flask, jsonify, render_template, request
from diceroll import RollDice
app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/_roll_dice')
def roll_dice():
    dice = request.args.get('a', 0, type=str)
    print(dice)
    roll = RollDice(dice)
    return jsonify(result=roll)

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
	# run!
	app.run(debug=True)