import psycopg2
import common_postgres as pg
            
def add_userinfo(username,email,password):
  if check_username_email(username,email):
    print("登録済みです")
  else:
    res = pg.exec('INSERT INTO user_info (username, email, password) VALUES (%s,%s,%s)',(username,email,password))
    print (res)
  
def add_file(user_id,file_name,url):
  res = pg.exec('INSERT INTO file_info (file_name, user_id, url) VALUES (%s,%s,%s)',(file_name,user_id,url))
  
def get_dbinfo():
  res = pg.select('SELECT * FROM user_info')
  print (res)

def get_fileinfo(user_id):
  res = pg.select('SELECT * FROM file_info WHERE user_id = %s',(user_id,))
  print(res)
  return res
   
def check_username_email(username,email):
  print (username,email)
  res = pg.select("SELECT * FROM user_info WHERE username = %s AND email = %s",(username, email))
  if len(res) > 0:
    return True
  else:
    return False
    
def check_email_password(email,passwd):
    res = pg.select("SELECT * FROM user_info WHERE email = %s AND password = %s",(email, passwd))
    print(res)
    if len(res) > 0:
      return res[0][0]
    else:
      return False

def get_hashedpasswd(email):
  res = pg.select_fetchone("SELECT password FROM user_info WHERE email = %s",(email,))
  if res == None:
    return ''
  else:
    return res["password"]
  

def get_username_byid(user_id):
    res = pg.select("SELECT username FROM user_info WHERE user_id = %s",(user_id,))
    print(res)
    if len(res) > 0:
      return res[0][0]
    else:
      return ""

def get_userinfo(user_id):
    res = pg.select("SELECT * FROM user_info WHERE user_id = %s",(user_id,))
    if len(res) > 0:
      return res[0]
    else:
      return ""

def get_userinfo_by_email(email):
    res = pg.select("SELECT * FROM user_info WHERE email = %s",(email,))
    if len(res) > 0:
      return res[0]
    else:
      return ""
    
def get_username(email):
    res = pg.select("SELECT username FROM user_info WHERE email = %s",(email,))
    print(res)
    if len(res) > 0:
      return res[0][0]
    else:
      return ""
         
def create_info():
  info = {
    "username": "rie",
    "email": "rie@yahoo.co.jp",
    "password": "rierie"    
  }
  return info

def main():
  
  add_userinfo("rie","rie4@yahoo.co.jp","rierie")
  get_dbinfo()
  #print(check_username_email("rie",'rie@yahoo.co.jp'))

#main()