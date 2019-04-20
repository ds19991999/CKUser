#!/usr/bin/python3
# -*- coding:utf-8 -*-
#fuction:server

from hashlib import sha1
import_flag = True
try:
	from ckuser.sqlhelper.MySQLHelper import MySQLHelp
	from ckuser.sqlhelper.RedisHelper import RedisHelp
	from ckuser import *
	conf = config.config()
except Exception:
	import_flag = False
if import_flag == True:
	pass
else:
	from sqlhelper.MySQLHelper import MySQLHelp
	from sqlhelper.RedisHelper import RedisHelp
	from config import *
	import client
	conf = config()

mysql_ip = conf['mysql_ip']
mysql_database = conf['mysql_database']
mysql_user = conf['mysql_user']
mysql_passwd = conf['mysql_passwd'] 
redis_ip = conf['redis_ip']

def user_name_pro():
	"""加密用户名"""
	user_name_temp = input("输入用户名：")
	s1 = sha1()
	s1.update(user_name_temp.encode("utf-8"))
	user_name_pro = s1.hexdigest()
	return user_name_pro

def user_add():
	"""添加用户"""
	client.register()

def user_del():
	"""删除用户"""
	try:
		user_name_temp = user_name_pro()
		params = [user_name_temp]

		sql='update userinfors set isdelete=1 where name=%s'
		helper=MySQLHelp(mysql_ip,mysql_database,mysql_user,mysql_passwd)
		helper.cud(sql,params)

		r = RedisHelp(redis_ip)
		r.delete(str(user_name_temp))
	except Exception:
		print("删除错误！")	

def user_find():
	"""查找用户"""
	user_name_temp = user_name_pro()
	result_redis = client.check_redis_name(user_name_temp)
	s = [0,0]
	if result_redis != None:
		print("该用户存在!")
		s[0] = True
	else:
		result_mysql = client.check_mysql_name(user_name_temp)
		if (len(result_mysql)!=0) and (result_mysql[0][1]==b'\x00'):
			print("该用户存在！")
			client.save_to_redis(user_name_temp,result_mysql[0][0])
			s[0] = True 
		elif (len(result_mysql)!=0) and (result_mysql[0][1]==b'\x01'):
			print("该用户已被删除!")
			s[0] = False
		else:
			print("该用户不存在！")
			s[0] = False
	s[1] = user_name_temp
	return s

def user_update():
	"""更新用户"""
	flag = user_find()

	if flag[0] == True:
		print("现在开始修改新的用户信息！")
		user_name,user_passwd=client.user_info()
		result_redis = client.check_redis_name(user_name)	
		if result_redis != None and user_name != flag[1] :
			print("该用户已经存在，请重新选择用户名！")
		else:		
			result_mysql = client.check_mysql_name(user_name)
			if len(result_mysql)!=0 and user_name != flag[1]:
				print("该用户名已经存在，请重新选择用户名！")	
			else:		
				client.user_update(user_name,user_passwd)
				client.save_to_redis(user_name,user_passwd)

def main():
	#user_del()
	user_find()
	#user_update()
	#user_add()

if __name__ == '__main__':
	main()
