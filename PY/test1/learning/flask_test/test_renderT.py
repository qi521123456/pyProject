from flask import Flask,render_template,url_for
app = Flask(__name__)
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    url_for('static', filename='style.css')
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.debug = True
    app.run()