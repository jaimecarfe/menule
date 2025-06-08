import bcrypt

password = b"admin1234"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed.decode())