from flask import Flask,url_for
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'hello world!'
@app.route('/hello')
def hello():
    return 'welcome...'
@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username
@app.route('/post/<int:qiiq>')
def show_post(qiiq):
    return 'Post %d' % qiiq
if __name__ == '__main__':
    app.debug = True
    app.run()