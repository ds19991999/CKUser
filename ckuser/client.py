#!/usr/bin/python3
# -*- coding:utf-8 -*-
#fuction:client

from hashlib import sha1
import_flag = True
try:
	from ckuser.sqlhelper.MySQLHelper import MySQLHelp
	from ckuser.sqlhelper.RedisHelper import RedisHelp
	from ckuser.config import *
except Exception:
	import_flag = False
if import_flag == True:
	pass
else:
	from sqlhelper.MySQLHelper import MySQLHelp
	from sqlhelper.RedisHelper import RedisHelp
	from config import *

conf = config()
mysql_ip = conf['mysql_ip']
mysql_database = conf['mysql_database']
mysql_user = conf['mysql_user']
mysql_passwd = conf['mysql_passwd'] 
redis_ip = conf['redis_ip']

def user_info():
	"""加密返回用户输入信息"""
	user_name = input("请输入用户名：")
	user_passwd = input("请输入密码：")
	s1 = sha1()
	s2 = sha1()
	s1.update(user_name.encode("utf-8"))
	s2.update(user_passwd.encode("utf-8"))
	user_name_pro = s1.hexdigest()
	user_passwd_pro = s2.hexdigest()
	return user_name_pro,user_passwd_pro

def check_mysql_name(user_name_temp):	
	"""查询用户表"""
	sql='select passwd,isdelete from userinfors where name=%s'
	params=[user_name_temp]
	helper=MySQLHelp(mysql_ip,mysql_database,mysql_user,mysql_passwd)
	result=helper.all(sql,params)
	return result

def check_redis_name(user_name_temp):
	"""查询用户表"""
	try:
		r = RedisHelp(redis_ip)
		result = r.get(user_name_temp)
		return result.decode('utf-8') # None or user_passwd_pro
	except Exception as msg:
		pass

def save_to_redis(user_name_temp,user_passwd_temp):
	"""保存用户信息到redis"""
	r = RedisHelp(redis_ip)
	r.set(user_name_temp,user_passwd_temp)

def user_insert(user_name_temp,user_passwd_temp):
	"""插入用户表"""
	sql='insert into userinfors(name,passwd) values(%s,%s)'
	params=[user_name_temp,user_passwd_temp]
	helper=MySQLHelp(mysql_ip,mysql_database,mysql_user,mysql_passwd)
	helper.cud(sql,params)

def user_update(user_name_temp,user_passwd_temp):
	"""更新用户表"""
	sql='update userinfors set passwd=%s where name=%s'
	params=[user_passwd_temp,user_name_temp]
	helper=MySQLHelp(mysql_ip,mysql_database,mysql_user,mysql_passwd)
	helper.cud(sql,params)

def update():
	"""用户信息更新"""
	flag = login()
	if flag[0] == True:
		print("现在开始修改新的用户信息！")
		user_name_pro,user_passwd_pro=user_info()
		result_redis = check_redis_name(user_name_pro)	
		if result_redis != None and user_name_pro != flag[1]:
			print("该用户已经存在，请重新选择用户名！")	
		else:		
			result_mysql = check_mysql_name(user_name_pro)
			if len(result_mysql)!=0 and user_name_pro != flag[1]:
				print("该用户名已经存在，请重新选择用户名！")
			else:		
				user_update(user_name_pro,user_passwd_pro)
				save_to_redis(user_name_pro,user_passwd_pro)

def register():
	"""用户信息注册"""
	user_name_pro,user_passwd_pro=user_info()
	result_redis = check_redis_name(user_name_pro)
	if result_redis != None:
		print("该用户已经存在，请重新选择用户名！")
	else:		
		result_mysql = check_mysql_name(user_name_pro)
		if (len(result_mysql)!=0) and (result_mysql[0][1]==b'\x00'):
			print("该用户已经存在，请重新选择用户名！")
			save_to_redis(user_name_pro,user_passwd_pro)	
		elif (len(result_mysql)!=0) and (result_mysql[0][1]==b'\x01'):
			print('该用户已被删除，请注册新用户名!')
		else:
			user_insert(user_name_pro,user_passwd_pro)
			save_to_redis(user_name_pro,user_passwd_pro)
			print("恭喜，注册成功！")

def login():
	"""用户信息登录"""
	user_name_pro,user_passwd_pro=user_info()
	result_redis = check_redis_name(user_name_pro)
	s = [0,0]
	if result_redis == user_passwd_pro:
		print('登录成功!')
		s[0] = True
	elif result_redis == None:
		result_mysql = check_mysql_name(user_name_pro)
		if result_mysql==None:
			print("该用户不存在！")
			s[0] =  False
		elif result_mysql[0][1]==b'\x01':
			print('该用户已被删除，请注册新用户名!')
			s[0] = False
		elif result_mysql[0][1]==b'\x00' and result_mysql[0][0]==user_passwd_pro:
			print('登录成功!')
			save_to_redis(user_name_pro,user_passwd_pro)
			s[0] = True
		else:
		    print('密码错误!')
		    s[0] = False
	elif result_redis != user_passwd_pro:
		print('密码错误!')
		s[0] = False
	s[1] = user_name_pro
	return s

def main():
	login()
	#register()
	#update()

if __name__ == '__main__':
	main()
