import pymysql
from app import app
from datetime import datetime
from Config import mysql
from flask import jsonify
from flask_bcrypt import Bcrypt, check_password_hash
from flask import flash, request, session
from werkzeug.security import generate_password_hash, check_password_hash

bcrypt = Bcrypt()


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# @app.route('/register', methods=['POST'])
# def register():
#     username = request.json.get('username', None)
#     Password = request.json.get('Password', None)

#     if not username:
#         return 'Missing Username', 400
#     if not Password:
#         return 'Missing Password', 400

#     hashed = bcrypt.hashpw(Password.encode('utf-8'), bcrypt.gensalt())
#     user = User(username=username, Password=hashed)

#     mysql.session.add(user)
#     mysql.session.commit()

#     return 'welcome {username}'

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('username', None)
#     Password = request.json.get('Password', None)

#     if not username:
#         return 'Missing Username', 400
#     if not Password:
#         return 'Missing Password', 400

#     user = User.query.filter_by(username=username).first()
#     if not User:
#         return 'user not found', 400

#     if Bcrypt.checkpw(Password.encode('utf-8'), User.Password):
#         return f'welcome back {username}'
#     else:
#         return ' wrong password'

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return jsonify({'message': 'You are already logged in', 'username': username})
    else:
        resp = jsonify({'message': 'Unauthorized'})
        resp.status_code = 401
        return resp


@app.route('/login', methods=['POST'])
def login():
    conn = None;
    cursor = None;

    try:
        _json = request.json
        _username = _json['username']
        _password = _json['Password']

        # validate the received values
        if _username and _password:
            # check user exists
            conn = mysql.connect()
            cursor = conn.cursor()

            sql = "SELECT username, Password FROM User WHERE username=%s"
            sql_where = (_username,)

            cursor.execute(sql, sql_where)
            row = cursor.fetchone()

            if row:
                if bcrypt.check_password_hash(row[1], _password):
                    session['username'] = row[0]
                    print("LoggedIn Successfully", row, _password)
                    resp = jsonify({'message': 'You are logged in successfully', "status": 200})
                    return resp
            else:
                print("Not LoggedIn")
                resp = jsonify({'message': 'Bad Request - invalid password'})
                resp.status_code = 400
                return resp
        else:
            print("row Not Found")
            resp = jsonify({'message': 'Bad Request - invalid credendtials'})
            resp.status_code = 400
            return resp
    except Exception as e:
        print(e)
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()


# @app.route('/login', methods=['POST'])
# def login():
# 	conn = None;
# 	cursor = None;

# 	try:
# 		_json = request.json
# 		_username = _json['username']
# 		_password = _json['Password']

# 		# validate the received values
# 		if _username and _password:
# 			#check user exists			
# 			conn = mysql.connect()
# 			cursor = conn.cursor()

# 			sql = "SELECT username, Password FROM User WHERE username=%s"
# 			sql_where = (_username,)

# 			cursor.execute(sql, sql_where)
# 			row = cursor.fetchone()

# 			if row :
# 				if check_password_hash(row[2], _password):
# 					session['username'] = row[1]
# 					#cursor.close()
# 					#conn.close()
# 					return jsonify({'message' : 'You are logged in successfully'})
# 				else:
# 					resp = jsonify({'message' : 'Bad Request - invalid password'})
# 					resp.status_code = 400
# 					return resp
# 		else:
# 			resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
# 			resp.status_code = 400
# 			return resp

# 	except Exception as e:
# 		print(e)

# 	finally:
# 		if cursor and conn:
# 			cursor.close()
# 			conn.close()

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message': 'You successfully logged out'})


@app.route('/adduser', methods=['POST'])
def add_User():
    try:
        _json = request.json
        _username = _json['username']
        _Password = _json['Password']
        _Role = _json['Role']
        if _username and _Password and _Role and request.method == 'POST':
            sqlQuery = "INSERT INTO User(username, Password, Role) VALUES(%s, %s, %s)"
            bindData = (_username, bcrypt.generate_password_hash(_Password), _Role)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/users')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT username, Password, Role, Is_active FROM User")
        userRows = cursor.fetchall()
        respone = jsonify(userRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user/<username>')
def user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT username,Password, Role, Is_active FROM User WHERE username =%s", username)
        userRow = cursor.fetchone()
        respone = jsonify(userRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addstudent', methods=['POST'])
def add_student():
    try:
        _json = request.json
        _Pid = _json['Pid']
        _First_Name = _json['First_Name']
        _Last_Name = _json['Last_Name']
        _Email = _json['Email']
        _Dept_Code = _json['Dept_Code']
        _Course_Name = _json['Course_Name']
        _CGPA = _json['CGPA']
        _Semester = _json['Semester']
        _Description = _json['Description']
        _DOB = _json['DOB']
        _password = _json['password']
        if _Pid and _First_Name and _Last_Name and _Email and _Dept_Code and _Course_Name and _CGPA and _Semester and _Description and _DOB and _password and request.method == 'POST':
            sqlQuery = "REPLACE INTO Students(Pid, First_Name, Last_Name, Email, Dept_Code, Course_Name, CGPA, Semester, Description, DOB, password) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            sqlQueryUser = "REPLACE INTO User( username, password, Role, Is_active) VALUES(%s, %s, 'Student', 1)"
            bindData = (
            _Pid, _First_Name, _Last_Name, _Email, _Dept_Code, _Course_Name, _CGPA, _Semester, _Description, _DOB,
            bcrypt.generate_password_hash(_password))
            bindUserData = (_Email, bcrypt.generate_password_hash(_password))
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            cursor.execute(sqlQueryUser, bindUserData)
            conn.commit()
            respone = jsonify('student added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/students')
def students():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT Pid, Email, Dept_Code, Course_Name, DOB, CGPA, Semester, Description, password FROM Students")
        studentRows = cursor.fetchall()
        respone = jsonify(studentRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/student/<Email>')
def student(Email):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT Pid, First_Name, Last_Name, Email, Dept_Code, Course_Name, CGPA, Semester, Description, DOB FROM Students WHERE Email =%s",
            Email)
        studentRow = cursor.fetchone()
        respone = jsonify(studentRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/Department/<Dept_Code>')
def Department(Dept_Code):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT Dept_Code, Dept_Name FROM Department WHERE Dept_Code =%s", Dept_Code)
        deptRow = cursor.fetchone()
        respone = jsonify(deptRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addcompany', methods=['POST'])
def add_Company():
    try:
        _json = request.json
        _Company_Name = _json['Company_Name']
        _Email = _json['Email']
        _locations = _json['locations']
        _website = _json['website']
        _password = _json['password']
        if _Company_Name and _Email and _locations and _website and _password and request.method == 'POST':
            sqlQuery = "Replace INTO Company(Company_Name, Email, locations, website, password) VALUES(%s, %s, %s, %s, %s)"
            sqlQueryUser = "REPLACE INTO User( username, password, Role, Is_active) VALUES(%s, %s, 'Company', 1)"
            bindData = (_Company_Name, _Email, _locations, _website, bcrypt.generate_password_hash(_password))
            bindUserData = (_Email, bcrypt.generate_password_hash(_password))
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            cursor.execute(sqlQueryUser, bindUserData)
            conn.commit()
            respone = jsonify('Company added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/companies')
def companies():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT Company_Name, locations, website, Email FROM Company")
        companyRows = cursor.fetchall()
        respone = jsonify(companyRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/company/<int:id>')
def company(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT Id, Name, Location, website, Email FROM Company WHERE id =%s", id)
        companyRow = cursor.fetchone()
        respone = jsonify(companyRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addjobposting', methods=['POST'])
def add_jobposting():
    try:
        _json = request.json
        _Id = _json['Id']
        _Company_id = _json['Company_id']
        _Eligibility = _json['Eligibility']
        _Application_Close_Date = _json['Application_Close_Date']
        _Location = _json['Location']
        _Job_Description = _json['Job_Description']
        if _Id and _Company_id and _Eligibility and _Application_Close_Date and _Location and _Job_Description and request.method == 'POST':
            sqlQuery = "Replace INTO Job_Posting(Id, Company_id, Eligibility, Application_Close_Date, Location, Job_Description) VALUES(%s, %s, %s, %s, %s, %s)"
            bindData = (_Id, _Company_id, _Eligibility, _Application_Close_Date, _Location, _Job_Description)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Job Posted successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/jobs')
def jobs():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "select Company_Name, Eligibility, Application_Open_Date, Application_Close_Date, Location, Job_Description from Job_Posting left join Company on Company.Id=Job_Posting.Company_id;")
        jobRows = cursor.fetchall()
        respone = jsonify(jobRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


# @app.route('/jobs')
# def jobs():
#     try:
#         conn = mysql.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         cursor.execute("select Company_Name, Eligibility, Application_Open_Date, Application_Close_Date, Location, Job_Description from job_posting")
#         jobRows = cursor.fetchall()
#         respone = jsonify(jobRows)
#         respone.status_code = 200
#         return respone
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         conn.close()

@app.route('/job/<int:id>')
def job(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT Id, Company_id, Eligibility, Application_Open_Date, ,Application_Close_Date, Location, Job_Description FROM Job_Posting WHERE id =%s",
            id)
        jobRow = cursor.fetchone()
        respone = jsonify(jobRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/applicationforjob', methods=['POST'])
def applicationforjob():
    try:
        _json = request.json
        _Company_Name = _json['Company_Name']
        _Eligibility = _json['Eligibility']
        _Application_Open_Date = _json['Application_Open_Date']
        _Application_Close_Date = _json['Application_Close_Date']
        _Location = _json['Location']
        _Job_Description = _json['Job_Description']
        _username = _json['username']
        if _Company_Name and _Eligibility and _Application_Open_Date and _Application_Close_Date and _Location and _Job_Description and _username and request.method == 'POST':
            sqlQuery = "REPLACE INTO applied_application(Company_Name, Eligibility, Application_Open_Date, Application_Close_Date, Location, Job_Description, username) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            bindData = (
            _Company_Name, _Eligibility, _Application_Open_Date, _Application_Close_Date, _Location, _Job_Description,
            _username)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('application added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/addjobapplication', methods=['POST'])
def add_jobapplication():
    try:
        _json = request.json
        _Job_Posting_id = _json['Job_Posting_id']
        _student_id = _json['student_id']
        _Application_Date = _json['Application_Date']
        if _Job_Posting_id and _student_id and _Application_Date and request.method == 'POST':
            sqlQuery = "REPLACE INTO Job_Applications(Job_Posting_id, student_id, Application_Date) VALUES(%s, %s, %s)"
            bindData = (_Job_Posting_id, _student_id, _Application_Date)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Job_application added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/jobapplications')
def jobapplications():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "select Student_id,Company_Name, Location, Job_Description, Application_Date from Job_Applications ja left join Job_Posting jp on ja.Job_Posting_id=jp.Id join Company c on jp.Company_id=c.Id;")
        jobapplicationRows = cursor.fetchall()
        respone = jsonify(jobapplicationRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/jobapplication/<student_id>')
def jobapplication(student_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT Job_Posting_id, student_id, Application_Date FROM Job_Applications WHERE student_id =%s",
                       student_id)
        jobapplicationRow = cursor.fetchone()
        respone = jsonify(jobapplicationRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/placements')
def placement():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql,cursors.DictCursor)
        cursor.execute("SELECT c.Company_Name, p.student_id, d.Dept_Name, p.Job_Profile, p.Placement_Status, p.salary from Placements p INNER JOIN Company c ON c.Id = p.Company_id INNER JOIN Department d ON d.Dept_Code = p.Dept_Code;")
        placementRow = cursor.fetchone()
        respone = jsonify(placementRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.run(debug=True)
