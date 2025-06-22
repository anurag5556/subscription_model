from flask import Flask, render_template, request, redirect
import cx_Oracle
from datetime import datetime, timedelta

app = Flask(__name__)

# Oracle Database connection with python
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
conn = cx_Oracle.connect(user="SYSTEM", password="Anurag@123", dsn=dsn)

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT id, name, phone, joining_date, subscription_type, subscription_duration FROM subscribers")
    rows = cur.fetchall()

    subscribers = []
    for row in rows:
        join_date = row[3]
        duration = row[5]
        end_date = join_date + timedelta(days=duration)
        days_left = (end_date - datetime.now()).days

        subscribers.append({
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "type": row[4],
            "days_left": days_left
        })

    return render_template("index.html", subscribers=subscribers)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    phone = request.form['phone']
    joining_date = request.form['joining_date']
    subscription_type = request.form['subscription_type']
    duration = int(request.form['subscription_duration'])

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO subscribers (name, phone, joining_date, subscription_type, subscription_duration)
        VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'), :4, :5)
    """, (name, phone, joining_date, subscription_type, duration))
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
