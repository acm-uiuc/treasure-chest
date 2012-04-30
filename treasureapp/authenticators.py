from treasureapp.models import Account, Transaction, Accessor, \
		AccountGroup, GroupMember

def authenticate_account(user, account):
	"""
	Ensure that the given user can update this account.
	"""

	groups = GroupMember.objects.filter(member=user)
	accessor_list = Accessor.objects.filter(group__in=groups, account=account)

	if len(accessor_list) > 0:
		return True

	return False


def authenticate_transaction(user, transaction):
	"""
	Ensure that the given user can make/modify this transaction.
	"""

	from_acct = transaction.from_acct
	to_acct = transaction.to_acct

	groups = GroupMember.objects.filter(member=user)
	from_accessor = Accessor.objects.filter(group__in=groups, account=from_acct)
	to_accessor = Accessor.objects.filter(group__in=groups, account=to_acct)

	if len(from_accessor) > 0 and len(to_accessor) > 0:
		return True

	return False

def authenticate_group(user, group):
	"""
	Ensure that the given user can modify this group.
	"""

	groups = GroupMember.objects.filter(member=user, group=group)
	if groups:
		return True

	return False
