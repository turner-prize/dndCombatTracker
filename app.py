from flask import Flask, render_template, jsonify, request
import itertools

app = Flask(__name__)

mylist = ['banana','apple','orange']
x = itertools.cycle(mylist)

@app.route('/nextItem')
def nextItem(): 
	#return jsonify(mylist=mylist,nextitem=next(x))
	return render_template('section.html',mylist=mylist,nextitem=next(x))

@app.route('/')
def index():
	return render_template('index.html',mylist=mylist,nextitem=next(x))


if __name__ == '__main__':
    app.run(debug=True)