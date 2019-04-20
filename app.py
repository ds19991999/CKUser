#!/usr/bin/python3
# -*- coding:utf-8 -*-
from ckuser import client,server
import os

def print_client_menu():
	print("用户菜单:")
	print("-"*25)
	print("0"+"-"*10+"显示用户菜单"+"-"*10)
	print("1"+"-"*10+"显示服务菜单"+"-"*10)
	print("2"+"-"*10+"用户登录系统"+"-"*10)
	print("3"+"-"*10+"用户修改信息"+"-"*10)
	print("4"+"-"*10+"用户注册信息"+"-"*10)
	print("6"+"-"*10+"退出系统")

def print_server_menu():
	print("服务菜单:")
	print("-"*25)
	print("0"+"-"*10+"显示用户菜单"+"-"*10)
	print("1"+"-"*10+"显示服务菜单"+"-"*10)
	print("2"+"-"*10+"添加用户帐号"+"-"*10)
	print("3"+"-"*10+"删除用户帐号"+"-"*10)
	print("4"+"-"*10+"修改用户帐号"+"-"*10)
	print("5"+"-"*10+"查找用户帐号"+"-"*10)
	print("6"+"-"*10+"退出系统")	

def server_oper():
	print_server_menu()
	while True:
		try:
			i = int(input("请输入操作符："))
			if i == 0:
				os.system("clear")
				break
			elif i == 1:
				os.system("clear")
				print_server_menu()
			elif i == 2:
				server.user_add()
			elif i == 3:
				server.user_del()
			elif i == 4:
				server.user_update()
			elif i == 5:
				server.user_find()
			elif i == 6:
				os.system("clear")
				os.system(exit())		
		except Exception as msg:
			os.system("clear")
			print_server_menu()
			print("输入错误!")
	client_oper()

def client_oper():
	print_client_menu()
	while True:
		try:
			i = int(input("请输入操作符："))
			if i == 0:
				os.system("clear")
				print_client_menu()
			elif i == 1:
				os.system("clear")
				break
			elif i == 2:
				client.login()
			elif i == 3:
				client.update()
			elif i == 4:
				client.register()
			elif i == 6:
				os.system("clear")
				os.system(exit())	
			else:
				os.system("clear")
				print_client_menu()
				print("输入错误!")
		except Exception:
			os.system("clear")
			print_client_menu()
			print("输入错误!")
	server_oper()

def main():
	# server.user_update()
	client_oper()

if __name__ == '__main__':
	main()
