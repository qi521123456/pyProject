from flask import Flask
from flask import render_template,request,redirect

app = Flask(__name__)

@app.before_request
def myredirect():
    if not request.path == '/':
        username = request.args.get('username')
        if not username:
            return redirect('/')
        else:
            print('success')

@app.route('/')
def hello_world():
    return 'Hello  World!'


@app.route('/name')
def hello_name():
    return 'this is name\n'

@app.route('/show')
def show():
    return 'this is show \n'

if __name__ == '__main__':
    app.debug = True
    app.run()