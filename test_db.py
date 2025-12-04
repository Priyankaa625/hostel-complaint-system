import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Surbhi@07',
    database='hostel_complaints'
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM users WHERE username='student';")
user = cursor.fetchone()
print(user)

# Test password check
if user:
    if bcrypt.checkpw('student123'.encode('utf-8'), user['password'].encode('utf-8')):
        print("Password matches!")
    else:
        print("Password DOES NOT match!")
