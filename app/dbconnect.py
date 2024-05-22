import pymysql
from config import dbconfig

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

