import pymysql
from pymysql.converters import escape_string
from config import dbconfig
from user import User
import datetime

def connection():
	"""Create database connection"""
	conn = pymysql.connect(host=dbconfig['host'],
			       user=dbconfig['user'],
			       password=dbconfig['pass'],
			       db=dbconfig['name'],
			       charset='utf8mb4',
			       cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn

def get_user(key):
	c, conn = connection()
	c.execute("SELECT * FROM users WHERE username=%s OR email=%s", [escape_string(str(key)), escape_string(str(key))])
	res = c.fetchone()
	if res is None:
		return None
	user_data = User()
	user_data.update(res)
	c.close()
	conn.close()
	return user_data

def get_user_by_id(key):
	c, conn = connection()
	c.execute("SELECT * FROM users WHERE user_id=%s", [escape_string(str(key))])
	res = c.fetchone()
	if res is None:
		return None
	user_data = User()
	user_data.update(res)
	c.close()
	conn.close()
	return user_data

def create_user(username, email, passwd):
	c, conn = connection()
	c.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", [escape_string(username), escape_string(passwd), escape_string(email)])
	conn.commit()
	c.close()
	conn.close()


def check_unique(username):
    c, conn = connection()
    c.execute("SELECT * FROM users WHERE username=%s", [escape_string(username)])
    res = c.fetchone()
    c.close()
    conn.close()
    if res:
        return False
    return True

def get_places_list():
	c, conn = connection()
	c.execute("SELECT place_id, place_name FROM places")
	res = c.fetchall()
	if res is None:
		return None
	places_list = res
	c.close()
	conn.close()
	return places_list

def get_place(place_id):
	c, conn = connection()
	c.execute("SELECT * FROM places WHERE place_id=%s", [escape_string(place_id)])
	res = c.fetchone()
	if res is None:
		return None
	c.close()
	conn.close()
	return res

def get_discovery(user_id, place_id):
	c, conn = connection()
	c.execute("SELECT discovery_date FROM discoveries WHERE user_id=%s AND place_id=%s", [escape_string(user_id), escape_string(place_id)])
	res = c.fetchone()
	c.close()
	conn.close()
	return res

def unlock_place(code, place_id, user_id):
	c, conn = connection()
	c.execute("SELECT place_id,points_value FROM places WHERE unlock_code=%s", [escape_string(code)])
	res = c.fetchone()
	if res is None:
		return "Wrong unlock code"
	c.execute("INSERT INTO discoveries (user_id, place_id, discovery_date) VALUES (%s, %s, %s) ", [escape_string(user_id), escape_string(place_id), str(datetime.datetime.now())])
	conn.commit()
	c.execute("UPDATE users SET points = points + %s WHERE user_id = %s", [res['points_value'], escape_string(user_id)])
	conn.commit()
	c.execute("UPDATE places SET points_value = points_value - 10 WHERE place_id = %s", [escape_string(place_id)])
	conn.commit()
	c.close()
	conn.close()

def get_top10_players():
	c, conn = connection()
	query = """
	    SELECT username,points
	    FROM users 
	    ORDER BY points DESC 
	    LIMIT 10
	"""
	c.execute(query)
	res = c.fetchall()
	c.close()
	conn.close()
	return res

def get_comments(place_id):
	c, conn = connection()
	c.execute("SELECT * FROM comments WHERE place_id=%s", [escape_string(place_id)])
	res = c.fetchall()
	for comment in res:
		user = get_user_by_id(comment["user_id"])
		comment["username"] = user["username"]
	if res is None:
		return []
	c.close()
	conn.close()
	return res

def add_comment(comment, place_id, user_id):
	c, conn = connection()
	c.execute("INSERT INTO comments (place_id, user_id, comment) VALUES (%s, %s, %s) ", [escape_string(place_id), escape_string(user_id), escape_string(comment)])
	conn.commit()
	c.close()
	conn.close()