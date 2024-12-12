from flask import Flask, render_template, url_for, request
import sqlite3
from image_dataset import create_dataset
from recognition_image import Recognition
from recognition_video import Recognition_video

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS records(file TEXT, name TEXT, age TEXT, dob TEXT, gender TEXT, md TEXT)"""
cursor.execute(command)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/matching', methods = ['POST', 'GET'])
def matching():
    if request.method == 'POST':
        file = request.form['file']

        path = 'static/test/'+file
        res = Recognition(path)
        if res == 'unknown':
            return render_template('matching.html', msg="records not found on this face")  
        else:
            connection = sqlite3.connect('user_data.db')
            cursor = connection.cursor()
            cursor.execute("select * from records where name = '"+res+"'")
            result = cursor.fetchone()
            return render_template('matching.html', result=result) 

    return render_template('matching.html')

@app.route('/video', methods = ['POST', 'GET'])
def video():
    if request.method == 'POST':
        file = request.form['file']

        path = 'static/test/'+file
        res = Recognition_video(path)
        if res == 'unknown':
            return render_template('matching.html', msg="records not found on this face")  
        else:
            connection = sqlite3.connect('user_data.db')
            cursor = connection.cursor()
            cursor.execute("select * from records where name = '"+res+"'")
            result = cursor.fetchone()
            return render_template('matching.html', result=result) 

    return render_template('matching.html')


@app.route('/live')
def live():
    res = Recognition_video(0)
    if res == 'unknown':
        return render_template('matching.html', msg="records not found on this face")  
    else:
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        cursor.execute("select * from records where name = '"+res+"'")
        result = cursor.fetchone()
        return render_template('matching.html', result=result)

@app.route('/details', methods = ['POST', 'GET'])
def details():
    if request.method == 'POST':
        file = request.form['file']

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        cursor.execute("select * from records where name = '"+file+"'")
        result = cursor.fetchone()
        if result:
            return render_template('details.html', result=result) 
        else:
            return render_template('details.html', msg='resords not found on this name') 
    return render_template('details.html')

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        data = request.form
        keys = []
        values = []
        for key in data:
            values.append(data[key])
            keys.append(key)
        print(keys)
        print(values)

        path = 'static/test/'+values[0]
        res = create_dataset(path, values[1])
        if res == 'found':
            connection = sqlite3.connect('user_data.db')
            cursor = connection.cursor()

            cursor.execute("insert into records values(?,?,?,?,?,?)", values)
            connection.commit()

            return render_template('upload.html', msg="Data uploaded succeessfully")   
        else:
            return render_template('upload.html', msg="Face not found")

    return render_template('upload.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            return render_template('userlog.html')
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('userlog.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
