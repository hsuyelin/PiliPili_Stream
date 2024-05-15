#!/usr/bin/env python3

# -*- coding: utf-8 -*-


import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# 禁用不安全请求警告
urllib3.disable_warnings(InsecureRequestWarning)


# noinspection PyBroadException
class RequestUtils:
	"""
	简单的 HTTP 请求工具类，封装了常用的 GET 和 POST 请求方法
	"""

	def __init__(self,
				 headers=None,
				 cookies=None,
				 session=None,
				 timeout=None,
				 referer=None,
				 accept_type=None):
		"""
		初始化 RequestUtils 对象

		Parameters:
		- headers (dict): 请求头信息
		- cookies (str or dict): 请求携带的 cookies
		- session (requests.Session): 请求的会话对象
		- timeout (float): 请求超时时间
		- referer (str): 请求头中的 referer
		- accept_type (str): 请求头中的 Accept 类型
		"""
		self.__headers = headers if isinstance(headers, dict) else {}
		if "Content-Type" not in self.__headers:
			self.__headers.update({"Content-Type": "application/json; charset=utf-8"})
		self.__cookies = self.cookie_parse(cookies) if isinstance(cookies, str) else cookies
		self.__session = session
		if referer:
			self.__headers.update({"referer": referer})
		self.__timeout = timeout
		if accept_type:
			self.__headers.update({"Accept": accept_type})

	def update_headers(self, headers):
		"""
		更新请求头信息

		Parameters:
		- headers (dict): 包含新请求头信息的字典

		Example:
		```
		request_util = RequestUtils()
		new_headers = {'User-Agent': 'Mozilla/5.0'}
		request_util.update_headers(new_headers)
		```
		"""
		if not headers or not isinstance(headers, dict):
			return
		self.__headers.update(headers)

	def post(self, url, data=None, json=None):
		"""
		发送 POST 请求

		Parameters:
		- url (str): 请求的 URL
		- data (dict or str): 请求携带的数据
		- json (dict): 请求携带的 JSON 数据

		Returns:
		- requests.Response or None: 请求的响应对象或 None（发生异常时）
		"""
		if json is None:
			json = {}

		try:
			if self.__session:
				return self.__session.post(url,
										   data=data,
										   verify=False,
										   headers=self.__headers,
										   timeout=self.__timeout,
										   json=json)
			else:
				return requests.post(url,
									 data=data,
									 verify=False,
									 headers=self.__headers,
									 timeout=self.__timeout,
									 json=json)
		except requests.exceptions.RequestException:
			return None

	def get(self, url, params=None):
		"""
		发送 GET 请求

		Parameters:
		- url (str): 请求的 URL
		- params (dict): 请求携带的参数

		Returns:
		- str or None: 请求的响应内容（字符串）或 None（发生异常时）
		"""
		try:
			if self.__session:
				response = self.__session.get(url,
											  verify=False,
											  headers=self.__headers,
											  timeout=self.__timeout,
											  params=params)
			else:
				response = requests.get(url,
										verify=False,
										headers=self.__headers,
										timeout=self.__timeout,
										params=params)
			return str(response.content, 'utf-8')
		except requests.exceptions.RequestException:
			return None

	def get_res(self, url, params=None, allow_redirects=True, raise_exception=False):
		"""
		发送 GET 请求，返回完整的响应对象

		Parameters:
		- url (str): 请求的 URL
		- params (dict): 请求携带的参数
		- allow_redirects (bool): 是否允许重定向
		- raise_exception (bool): 是否抛出异常

		Returns:
		- requests.Response or None: 请求的响应对象或 None（发生异常时）
		"""
		try:
			if self.__session:
				return self.__session.get(url,
										  params=params,
										  verify=False,
										  headers=self.__headers,
										  cookies=self.__cookies,
										  timeout=self.__timeout,
										  allow_redirects=allow_redirects)
			else:
				return requests.get(url,
									params=params,
									verify=False,
									headers=self.__headers,
									cookies=self.__cookies,
									timeout=self.__timeout,
									allow_redirects=allow_redirects)
		except requests.exceptions.RequestException:
			if raise_exception:
				raise requests.exceptions.RequestException
			return None

	def post_res(self, url, data=None, params=None, allow_redirects=True, files=None, json=None):
		"""
		发送 POST 请求，返回完整的响应对象

		Parameters:
		- url (str): 请求的 URL
		- data (dict or str): 请求携带的数据
		- params (dict): 请求携带的参数
		- allow_redirects (bool): 是否允许重定向
		- files (dict): 上传的文件
		- json (dict): 请求携带的 JSON 数据

		Returns:
		- requests.Response or None: 请求的响应对象或 None（发生异常时）
		"""
		try:
			if self.__session:
				return self.__session.post(url,
										   data=data,
										   params=params,
										   verify=False,
										   headers=self.__headers,
										   cookies=self.__cookies,
										   timeout=self.__timeout,
										   allow_redirects=allow_redirects,
										   files=files,
										   json=json)
			else:
				return requests.post(url,
									 data=data,
									 params=params,
									 verify=False,
									 headers=self.__headers,
									 cookies=self.__cookies,
									 timeout=self.__timeout,
									 allow_redirects=allow_redirects,
									 files=files, json=json)
		except requests.exceptions.RequestException:
			return None

	@staticmethod
	def cookie_parse(cookies_str, array=False):
		"""
		解析 cookies 字符串为字典或数组

		Parameters:
		- cookies_str (str): cookies 字符串
		- array (bool): 是否返回数组形式

		Returns:
		- dict or list: 解析后的 cookies 字典或数组
		"""
		if not cookies_str:
			return {}

		cookie_dict = {}
		cookies = cookies_str.split(';')

		for cookie in cookies:
			cookie_str = cookie.split('=')
			if len(cookie_str) > 1:
				cookie_dict[cookie_str[0].strip()] = cookie_str[1].strip()

		if array:
			cookies_list = []
			for cookieName, cookieValue in cookie_dict.items():
				cookies = {'name': cookieName, 'value': cookieValue}
				cookies_list.append(cookies)
			return cookies_list

		return cookie_dict

	@staticmethod
	def check_response_is_valid_json(response):
		"""
		检查响应内容是否为有效的 JSON 格式

		Parameters:
		- response: 响应对象，通常是 HTTP 请求返回的响应

		Returns:
		- bool: 如果响应内容为有效的 JSON 格式，则返回 True，否则返回 False
		"""
		content_type = response.headers.get('Content-Type', '')
		return 'application/json' in content_type
