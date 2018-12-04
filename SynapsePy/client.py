
from .http_client import HttpClient

from .users import Users
from .nodes import Nodes
from .transactions import Transactions
from .subscriptions import Subscriptions

from .user import User
from .node import Node
from .transaction import Trans
from .subscription import Subscription

from .endpoints import paths

import api.models.errors as api_errors

import sys
import json
import logging
import requests

class Client():
	""" Client Record """

	def __init__(self, **params):
		"""
		Args:
			client_id (str): API client id
			client_secret (str): API client secret
			fingerprint (str):
			ip_address (str):
			devmode (bool): switches between sandbox and production base_url
		"""
		self.client_id = params['client_id']
		self.client_secret = params['client_secret']
		
		self.http = HttpClient(
			client_id=params['client_id'],
			client_secret=params['client_secret'],
			fingerprint=params['fingerprint'],
			ip_address=params['ip_address'],
			base_url='https://uat-api.synapsefi.com/v3.1' if params['devmode'] else 'https://api.synapsefi.com/v3.1',
			logging=params.get('logging', False)
			)

		self.logger = self.get_log(params.get('logging', False))

	def update_headers(self, **kwargs):
		'''Updates session headers
		'''
		return self.http.update_headers(**kwargs)

	def get_log(self, enable):
		'''Enables/Disables logs
		Args:
			enable (bool): enables if True, disables if False
		Returns:
			logger (Logger): logging.Logger object used to debug
		'''
		logging.basicConfig()
		logger = logging.getLogger("__name__")
		logger.setLevel(logging.DEBUG)
		logger.disabled = not enable

		return logger

	def create_user(self, body):
		"""
		Args:
			body (json): user record
			json (json): JSON
		Returns:
			user (User): object containing User record
		"""
		self.logger.debug("Creating a new user")

		path = paths['users']
		response = self.http.post(path, body)
		
		return User(response, self.http, full_dehydrate=False)
	
	def create_subscription(self, webhook_url, scope):
		'''
		Args:
			webhook_url (str): subscription url
			scope (list of str): API call types to subscribe to
		Returns:
			
		'''
		self.logger.debug("Creating a new subscription")

		path = paths['subs']

		body = {
			'scope': scope,
			'url': webhook_url
		}

		return Subscription(self.http.post(path, body), self.http)

	def get_user(self, user_id, **params):
		"""Returns user object
		Args:
			user_id (Str): identification for user
		Returns:
			user (User): object containing User record
		"""
		self.logger.debug("getting a user")

		path = paths['users'] + '/' + user_id
		full_dehydrate = 'yes' if params.get('full_dehydrate') else 'no'
		response = self.http.get(path, full_dehydrate=full_dehydrate)
		return User(response, self.http, full_dehydrate=full_dehydrate)

	def get_subscription(self, sub_id):
		'''
		Args:
			sub_id (Str): subscription id
		Returns:
			(Subscription Object)
		'''
		self.logger.debug("getting a subscription")

		path = paths['subs'] + '/' + sub_id
		response = self.http.get(path)
		return Subscription(response, self.http)

	def get_all_users(self, **params):
		"""Returns all user objects in a list
		Returns:
			(list of Json): json containing User records
		"""
		self.logger.debug("getting all users")

		path = paths['users']
		response = self.http.get(path, **params)
		return Users(response, self.http)

	def get_all_trans(self, **params):
		'''gets all client transactions
		Returns:
			(list of Transactions): list of all transaction records for client
		'''
		self.logger.debug("getting all transactions")
		
		path = paths['trans']
		response = self.http.get(path, **params)
		return Transactions(response, None, self.http)

	def get_all_nodes(self, **params):
		'''gets all client nodes
		Returns:
			(list of Nodes): list of all node records for client
		'''
		self.logger.debug("getting all nodes")
		
		path = paths['nodes']
		response = self.http.get(path)
		return Nodes(response, None, self.http)

	def get_all_subs(self, **params):
		'''
		'''
		self.logger.debug("getting all subscriptions")
		
		path = paths['subs']
		response = self.http.get(path, **params)
		return Subscriptions(response, self.http)

	def get_all_inst(self, **params):
		'''
		'''
		self.logger.debug("getting all institutions")
		
		path = paths['inst']
		response = self.http.get(path, **params)
		return response

	def issue_public_key(self, scope):
		'''
		Args:

		'''
		self.logger.debug("issuing a public key")
		
		path = paths['client']
		response = self.http.get(path, issue_public_key='YES', scope=scope)
		return response['public_key_obj']

