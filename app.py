from flask import Flask, render_template, redirect, url_for,request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def user():
    return render_template('login.html')

@app.route('/search_full')
def search_full():
    return render_template('search_full.html')


if __name__ == '__main__':
    app.run(debug=True)