import os
from flask import Flask,render_template, request, url_for, session
from flask_mysqldb import MySQL
import re 

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'calibration'
mysql = MySQL(app)

@app.route("/")
def index():
    #return render_template("index.html", message="Hello Flask!");    
    return render_template("index.html", message="Hello Flask!", contacts = ['c1', 'c2', 'c3', 'c4', 'c5']);

#All ablut login and session. Takenfrom other site.
@app.route('/login')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s and active=True', (username, password, ))
        account = cursor.fetchone()
        
        #print ("account=",account)
        if account:
            #print ("accountID=", account[0])
            session['loggedin'] = True
            #session['id'] = account['id']
            session['session_id'] = account[0]
            #session['username'] = account['username']
            session['username'] = account[1]
            session['role'] = account[4]
            msg = 'Logged in successfully ! Session on'
            if session['role'] in ('admin'):
               return render_template('index_admin.html', msg = msg, session_id=session['session_id'], session_username=session['username'], roll=session['roll'])
            else:
               return render_template('index_login.html', msg = msg, session_id=session['session_id'], session_username=session['username'], roll=session['roll'])
        else:
            msg = 'Incorrect username / password !'
    return render_template('login_login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('session_id', None)
    session.pop('username', None)
    #return redirect(url_for('/login'))
    return render_template('login_login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

#manage user profile: user psw, contant no, email, address, User_id(not editable), active, roll
@app.route('/profile', methods =['GET', 'POST'])
def profile():
    msg = ''
    errflg= ''
    if request.method == 'POST' and 'username' in request.form :
        username = request.form['username']
        new_psw = request.form['new_psw']
        rep_new_psw = request.form['rep_new_psw']
        old_psw = request.form['old_psw']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        #print("Form contains :",username,old_psw, new_psw, rep_new_psw, account, account[2])
        #print('compare old-psw=',old_psw,' and ',account[2])
        if account:
            msg = 'Account exists !'
            if not re.match(r'[A-Za-z0-9]+', new_psw):
                msg = 'New Password must contain only characters and numbers !'
                errflg = 'error'
            if new_psw != rep_new_psw :
                msg= 'psw and repeat psw should be same !'
                errflg = 'error' 
            if old_psw != account[2] :
                print ('MSG=',old_psw, account[2])
                msg = 'Incorrect current password' 
                errflg = 'error'      
            if errflg:
                print ("error in form.") 
            else:    
                print ("can insert values of new psw")
                msg='Success Change password !'
                #INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
                cursor = mysql.connection.cursor()
                cursor.execute(('UPDATE accounts set password=%s where id = %s'), (new_psw, account[0]))
                mysql.connection.commit()
                
        else:
            msg = 'You should have account registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('changepsw.html', msg = msg)    


# Display all vender list in table
@app.route('/select_vender')
def select_vender():
    if 'session_id' in session:  
        sessionid = session['session_id']
        session_role = session['role']
        print ("in vender sessionid= ",sessionid)
        print("session_Id = ",sessionid)
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT name, vender_id, address FROM vender")
        data = cursor.fetchall()
        venderid = request.args.get('venderid')
        if session_role == 'admin':
            return render_template('select_vender.html', data=data, venderid=venderid, roll=session_role)
        else:
            return  render_template('select_vender.html', data=data, venderid=venderid, roll=session_role)  
    else:  
        return '<p>Please login first</p>' 
    

@app.route('/select_dept')
def select_dept():
    if 'session_id' in session:  
        sessionid = session['session_id'] 
        print ("in dept sessionid= ",sessionid) 
        sel = request.args.get('dept')
        venderid = request.args.get('venderid')
        cursor = mysql.connection.cursor()
        #cursor.execute("SELECT equ_name, equ_parameter_id  FROM equipment")
        cursor.execute("SELECT department_name, department_id FROM department")
        data = cursor.fetchall()
        return render_template('select_dept.html', data=data, deptid=sel, venderid=venderid)
    else:  
        return '<p>Please login first</p>' 
    #sel = request.args.get('vender')
    #cursor = mysql.connection.cursor()
    #cursor.execute("SELECT department_name, department_id FROM department")
    #data = cursor.fetchall()
    #return render_template('select_dept.html', data=data, venderid=sel)    

@app.route('/select_equip')
def select_equip():
    if 'session_id' in session:  
        sessionid = session['session_id']
        sel = request.args.get('deptid')
        venderid = request.args.get('venderid')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT equ_name, equ_parameter_id  FROM equipment")
        data = cursor.fetchall()
        return render_template('select_equip.html', data=data, deptid=sel, venderid=venderid) 
    else:  
        return '<p>Please login first</p>'

# get comma seperated record and show in table
@app.route('/hosplist')
def hosplist():
    equipid = request.args.get('equipment')
    print ("EQP=",equipid)
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT parameter_name FROM equ_parameter_reg where equ_parameter_id=%s",(equipid,))
    data = cursor.fetchall()
    s = "-"
    for row in data:
        print(row)  
        s=s.join(row)
        rowx = s.split(',')           

    return render_template('hosplist.html', data=rowx)


@app.route('/parameter_input')
def parameter_input():
    if 'session_id' in session: 
       deptid = request.args.get('deptid')
       venderid = request.args.get('venderid')
       equipmentid = request.args.get('equipmentid')
       cursor = mysql.connection.cursor()
       cursor.execute('SELECT equ_name, equ_parameter_id FROM equipment where equ_id =%s',(equipmentid,))
       #equ_name = cursor.fetchone()
       data = cursor.fetchall()
       for row in data:
            equ_name = row[0]
            equ_parameter_id = row[1]

       print ('EQUIP=',equ_name, equ_parameter_id)
       cursor.execute("SELECT parameter_name FROM equ_parameter_reg where equ_parameter_id=%s",(equ_parameter_id,))
       data = cursor.fetchall()
       s = "-"
       for row in data:
           print(row)  
           s=s.join(row)
           rowx = s.split(',')           
           return render_template('parameter_input.html', data=rowx, venderid=venderid, deptid=deptid, equipmentid=equipmentid, equ_name=equ_name)
    else:  
        return '<p>Please login first.</p>'

@app.route('/save_reading',methods=['GET', 'POST'])
def save_reading():
     if request.method == 'POST' :
        #equipmentid = request.args.get('equipmentid')
        equipmentid = request.form['equipmentid']
        return equipmentid


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)