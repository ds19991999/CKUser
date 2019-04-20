#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
mysql> desc userinfors;
+----------+----------+------+-----+---------+----------------+
| Field    | Type     | Null | Key | Default | Extra          |
+----------+----------+------+-----+---------+----------------+
| id       | int(11)  | NO   | PRI | NULL    | auto_increment |
| name     | char(40) | YES  |     | NULL    |                |
| passwd   | char(40) | YES  |     | NULL    |                |
| isdelete | bit(1)   | YES  |     | b'0'    |                |
+----------+----------+------+-----+---------+----------------+
"""

def config():
	config={
		'mysql_ip':'localhost',
		'mysql_database':'python3',
		'mysql_user':'root',
		'mysql_passwd':'passwd', 
		'redis_ip':'localhost'
	}
	return config
	