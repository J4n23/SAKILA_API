import mysql.connector

credObj = {}

with open("credentials.txt") as f:
  file_contents = f.read().split('\n')
  for x in file_contents:
    if x:
      creds = x.split(': ')
      credObj[creds[0]] = creds[1]

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user = credObj["user"],
  password = credObj["password"],
  database="sakila"
)

mycursor = mydb.cursor(dictionary=True)
