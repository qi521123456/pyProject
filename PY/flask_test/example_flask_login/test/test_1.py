from flask import Flask
from flask import request
from flask import abort
from flask_script import Manager
app = Flask(__name__)
manager = Manager(app)
@app.route('/')
def index():
    user_agent=request.headers.get('User-Agent')
    #return ('<h1>Hello World!,%s</h1>'% user_agent)
    return ('<h1>Bad Request</h1>',400)
@app.route('/user/<id>')
def user(id):
    u={}
    u['id']=id
    u['name']='xx'
    if not u:
        abort(404)
    return ('<h1>Hello,%s!</h1>' % u['name'])
if __name__ == '__main__':
    manager.run()