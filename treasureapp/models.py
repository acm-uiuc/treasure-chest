from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class AccountGroup(models.Model):
	name = models.CharField(max_length=30)
	members = models.ManyToManyField(User)

	def __unicode__(self):
		return self.name

class Account(models.Model):
	"""
	An account represents a real-world source of money

	name - A name for the account
	description - An optional memo for the account
	balance - Cached balance for the account
	"""

	name = models.CharField(max_length = 200)
	description = models.TextField(blank=True)
	balance = models.DecimalField(max_digits = 30, decimal_places = 2,
			blank=True)

	accessors = models.ManyToManyField(AccountGroup)

	def __unicode__(self):
		"""
		Return a unicode representation of an account object.

		Returns a unicode string containing the account name.
		"""

		return self.name

	def update_balance(self):
		"""
		Calculate the balance for the account.

		Iterates through all transactions in the account to compute the
		available account balance.

		Returns the current account balance.
		"""

		balance = 0
		for transaction in Transaction.objects.all():
			amount = transaction.amount

			# Subtract for transactions out, add for transactions in
			if transaction.from_acct == self:
				balance -= amount
			# In case of from_acct == to_acct, balance is unchanged
			if transaction.to_acct == self:
				balance += amount

		# Update the cached balance
		self.balance = balance
		self.save()

		return balance

	def clean(self):
		"""
		Clean out account data before creation.
		"""

		# Force the balance on create to be zero
		self.update_balance()

class Transaction(models.Model):
	"""
	A transaction object represents money entering or exiting an account

	from_acct - The account the transaction is coming out of
	to_acct - The account the transaction is going into
	amount - Change in account balance
	description - An optional description of the transaction
	"""

	from_acct = models.ForeignKey(Account, related_name='from_acct')
	to_acct = models.ForeignKey(Account, related_name='to_acct')
	amount = models.DecimalField(max_digits = 10, decimal_places = 2)
	description = models.TextField(blank=True)

	def __unicode__(self):
		"""
		Return a unicode representation of a transaction object.

		Returns a unicode string of the form "Transaction from <account>
			to <account> for <amount>".
		"""

		strout = self.from_acct.__unicode__() \
				+ " to "                       \
				+ self.to_acct.__unicode__()   \
				+ " for "                      \
				+ str(self.amount)

		return strout
