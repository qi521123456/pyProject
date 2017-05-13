from flask import Flask
from flask import render_template, redirect,url_for
from flask import request,session
import os
import pymongo
from flask_bootstrap import Bootstrap
client=pymongo.MongoClient(host="127.0.0.1",port=27017)
coll=client['user']['accounts']
print("hello"+str(coll.find_one())+"\n"+str(coll.count()))
app = Flask(__name__)

@app.before_request
def before_action():
    print(request.path)
    if request.path.find('.ico')==-1:
        if not request.path=='/login':
            if not 'username' in session:
                session['newurl']=request.path
                return redirect(url_for('login'))

@app.route('/login', methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        #if request.form['username'] == 'admin':
        if coll.find_one({'username': request.form['username']}):
            #return redirect(url_for('home', username=request.form['username']))
            session['username'] = request.form['username']
            if 'newurl' in session:
                newurl = session['newurl']
                session.pop('newurl', None)
                return redirect(newurl)
            else:
                return redirect('/home')
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)

@app.route('/home')
def home():
    return render_template('home.html', username=session['username'])
    #return render_template('home.html', username=request.args.get('username'))

@app.route('/test')
def test():
    if 'username' in session:
        return render_template('test.html')
    else:
        session['newurl'] = 'test'
        return redirect(url_for('login'))
@app.route('/user')
def user():
    return render_template('user.html')

app.secret_key = os.urandom(24)#为了让session有效，需要设置一个key
bootstrap = Bootstrap(app)
if __name__ == '__main__':
    app.debug = True
    #app.run()
    app.run(host='0.0.0.0')