from django.db.models.signals import post_save

from treasureapp.models import Account, Transaction

def balance_modify(sender, **kwargs):
	"""
	Update balances when a transaction is modified.

	Check which accounts will have balance changes as result of a transaction
	create, update, or delete, and update those accounts accordingly.
	"""

	# Grab the transaction updated, and the accounts related to it
	transaction = kwargs['instance']
	from_acct = transaction.from_acct
	to_acct = transaction.to_acct

	# Running update balance is thread safe, whereas direct modification of
	# the balance field is not
	from_acct.update_balance()
	to_acct.update_balance()

post_save.connect(balance_modify, sender=Transaction)
