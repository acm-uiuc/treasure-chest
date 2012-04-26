from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from treasureapp.models import Account, Transaction, Accessor
from treasureapp.forms import AccountForm, TransactionForm

from treasureapp.authenticators import authenticate_account, authenticate_transaction

import treasureapp.signals

# Basic content handlers

def index(request):
	"""
	Render the main page of the Treasure Chest application.
	"""

	context = RequestContext(request, {"section":"index"})
	return render_to_response("index.html", context)

def help(request):
	"""
	Render the main page of the help contents.
	"""

	context = RequestContext(request, {"section":"help"})
	return render_to_response("help/index.html", context)

# Account handlers

@login_required
def account_list(request):
	"""
	Render the listing of all accounts.

	On GET, it will return a listing of all accounts.
	"""

	# Recover the groups the accessor is in
	request_user = request.user
	groups = request_user.groups.all()

	account_list = Account.objects.all()
	return_list = []

	# TODO: Figure out how to grab this without linear search
	for account in account_list:
		# Check if the user can actually read this account
		accessor_list = Accessor.objects.filter(group__in=groups, account=account)
		if len(accessor_list):
			return_list.append(account)

	context = RequestContext(request, {"section":"accounts",
		"account_list":return_list})
	return render_to_response("accounts/list.html", context)

@login_required
def account_detail(request, account_id):
	"""
	Show details of a specific account.

	On GET, it will return details on the account numbered account_id.
	"""

	# Grab the account (or 404, of course)
	account = get_object_or_404(Account, pk=account_id)

	# Check that the user can access it, or 403
	if not authenticate_account(request.user, account):
		raise PermissionDenied()

	# Pass it back out to the renderer
	context = RequestContext(request, {"section":"accounts",
		"account":account})
	return render_to_response("accounts/detail.html", context)

@login_required
def account_create(request, *args, **kargs):
	"""
	Allow the user to create a new account.

	On GET, it will return a form to create a new account.
	On POST, it will use the post data to add an account to the database.
	"""

	if request.method == 'POST':
		# If a POST request, try to validate and save the new account
		# Failures fall through to returning the old form with errors
		account_form = AccountForm(request.POST)
		if account_form.is_valid():
			new_account = account_form.save()
			return HttpResponseRedirect('/account')
	else:
		# If GET request, return the form to make a new account
		account_form = AccountForm()

	# Update the CSRF token
	kargs.update(csrf(request))
	context = RequestContext(request, dict(section="accounts",
		form=account_form, **kargs))
	return render_to_response("accounts/form.html", context)

@login_required
def account_update(request, account_id, *args, **kargs):
	"""
	Update an individual account.

	On GET, it will return a form to update the account.
	On POST, it will update information about the account.
	"""

	account = get_object_or_404(Account, pk=account_id)

	# Check that the user can access it, or 403
	if not authenticate_account(request.user, account):
		raise PermissionDenied()

	if request.method == 'POST':
		# Try to validate and update
		account_form = AccountForm(request.POST, instance=account)
		if account_form.is_valid():
			account = account_form.save()
			return HttpResponseRedirect('/account')
	else:
		# Populate the form with the current account's data
		account_form = AccountForm(instance=account)

	# Pass back the form we have, after updating CSRF
	kargs.update(csrf(request))
	context = RequestContext(request, dict(section="accounts",
		form=account_form, **kargs))
	return render_to_response("accounts/form.html", context)

# Transaction handlers

@login_required
def transaction_list(request):
	"""
	Render the listing of all transactions.

	On GET, it will return a listing of all transactions.
	"""

	transaction_list = Transaction.objects.all()

	context = RequestContext(request, {"section":"transactions",
		"transaction_list":transaction_list})
	return render_to_response("transactions/list.html", context)

@login_required
def transaction_detail(request, transaction_id):
	"""
	Show details of a specific transaction.

	On GET, it will return details on the transaction with the given id.
	"""

	# Grab the transaction (or 404, of course)
	transaction = get_object_or_404(Transaction, pk=transaction_id)

	# Pass it back out to the renderer
	context = RequestContext(request, {"section":"transactions",
		"transaction":transaction})
	return render_to_response("transactions/detail.html", context)

@login_required
def transaction_create(request, *args, **kargs):
	"""
	Allow the user to create a new transaction.

	On GET, it will return a form to create a new transaction.
	On POST, it will use the post data to add a transaction to the database.
	"""

	if request.method == 'POST':
		transaction_form = TransactionForm(request.POST)
		if transaction_form.is_valid():
			transaction = transaction_form.save(commit=False)

			# Check that the user can make this transaction
			if not authenticate_transaction(request.user, transaction):
				raise PermissionDenied()

			transaction.save()

			return HttpResponseRedirect('/transaction')
	else:
		transaction_form = TransactionForm()

	# Update the CSRF token
	kargs.update(csrf(request))
	context = RequestContext(request, dict(section="transactions",
		form=transaction_form, **kargs))
	return render_to_response("transactions/form.html", context)

@login_required
def transaction_update(request, transaction_id, *args, **kargs):
	"""
	Update an individual transaction.

	On GET, it will return a form to update the transaction.
	On POST, it will update information about the transaction.
	"""

	# Grab the transaction (or 404, of course)
	transaction = get_object_or_404(Transaction, pk=transaction_id)

	# Check that the user can update both of the involved accounts
	if not authenticate_transaction(request.user, transaction):
		raise PermissionDenied()

	if request.method == 'POST':
		# Try to validate and update
		transaction_form = TransactionForm(request.POST, instance=transaction)
		if transaction_form.is_valid():
			return HttpResponseRedirect('/transaction')
	else:
		# Populate the form with the current transaction data
		transaction_form = TransactionForm(instance=transaction)

	# Pass back the form we have, after updating CSRF
	kargs.update(csrf(request))
	context = RequestContext(request, dict(section="transactions",
		form=transaction_form, **kargs))
	return render_to_response("transactions/form.html", context)
