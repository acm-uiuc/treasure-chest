from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from treasureapp.models import Transaction
from treasureapp.forms import TransactionForm

from treasureapp.authenticators import authenticate_transaction

@login_required
def transaction_detail(request, transaction_id):
	"""
	Show details of a specific transaction.

	On GET, it will return details on the transaction with the given id.
	"""

	# Grab the transaction (or 404, of course)
	transaction = get_object_or_404(Transaction, pk=transaction_id)

	# Pass it back out to the renderer
	context = RequestContext(request, {"section":"accounts",
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
	context = RequestContext(request, dict(section="accounts",
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
	context = RequestContext(request, dict(section="accounts",
		form=transaction_form, **kargs))
	return render_to_response("transactions/form.html", context)
