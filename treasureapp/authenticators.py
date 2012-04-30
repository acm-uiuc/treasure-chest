from treasureapp.models import Account, Transaction, AccountGroup

def authenticate_account(user, account):
	"""
	Ensure that the given user can update this account.
	"""

	groups = user.accountgroup_set.all()
	accessor_list = account.accessors.filter(id__in=groups)

	if len(accessor_list) > 0:
		return True

	return False


def authenticate_transaction(user, transaction):
	"""
	Ensure that the given user can make/modify this transaction.
	"""

	from_acct = transaction.from_acct
	to_acct = transaction.to_acct

	groups = user.accountgroup_set.all()
	from_accessor = from_acct.accessors.filter(id__in=groups)
	to_accessor = to_acct.accessors.filter(id__in=groups)

	if len(from_accessor) > 0 and len(to_accessor) > 0:
		return True

	return False

def authenticate_group(user, group):
	"""
	Ensure that the given user can modify this group.
	"""

	groups = user.accountgroup_set.all()
	if groups:
		return True

	return False
