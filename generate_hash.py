import bcrypt

password_student = "student123"
password_warden = "warden123"

hashed_student = bcrypt.hashpw(password_student.encode('utf-8'), bcrypt.gensalt())
hashed_warden = bcrypt.hashpw(password_warden.encode('utf-8'), bcrypt.gensalt())

print("Student hash:", hashed_student.decode())
print("Warden hash:", hashed_warden.decode())
