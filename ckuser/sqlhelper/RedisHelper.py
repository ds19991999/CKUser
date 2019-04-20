#!/usr/bin/python3
# -*- coding:utf-8 -*-
from redis import *

class RedisHelp(object):
	"""docstring foRedisHelpme"""
	def __init__(self,host,port=6379):
		super(RedisHelp, self).__init__()
		self.__redis=StrictRedis(host,port)
	def set(self,key,value):
		self.__redis.set(key,value)
	def get(self,key):
		return self.__redis.get(key)
	def delete(self,key):
		return self.__redis.delete(key)
