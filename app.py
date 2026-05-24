from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'secret123'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'akmk@123#^'
app.config['MYSQL_DB'] = 'employee_db'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
            (username, email, password)
        )
        mysql.connection.commit()
        cur.close()

        return redirect('/login')

    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cur.fetchone()
        cur.close()

        if user:
            session['loggedin'] = True
            session['email'] = email
            return redirect('/dashboard')

    return render_template('login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()

    total = len(employees)

    return render_template(
        'dashboard.html',
        employees=employees,
        total=total
    )


# Employee List
@app.route('/employees')
def employees():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()

    return render_template('employees.html', employees=data)


# Add Employee
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO employees(name,email,department,salary) VALUES(%s,%s,%s,%s)",
            (name, email, department, salary)
        )

        mysql.connection.commit()
        cur.close()

        return redirect('/employees')

    return render_template('add_employee.html')


# Edit Employee
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        salary = request.form['salary']

        cur.execute(
            "UPDATE employees SET name=%s,email=%s,department=%s,salary=%s WHERE id=%s",
            (name, email, department, salary, id)
        )

        mysql.connection.commit()
        return redirect('/employees')

    cur.execute("SELECT * FROM employees WHERE id=%s", [id])
    employee = cur.fetchone()

    return render_template('edit_employee.html', employee=employee)


# Delete Employee
@app.route('/delete/<id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id=%s", [id])

    mysql.connection.commit()
    return redirect('/employees')


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)


