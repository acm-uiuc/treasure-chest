from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required

from treasureapp.models import AccountGroup
from treasureapp.forms import AccountGroupForm
from treasureapp.authenticators import authenticate_group

@login_required
def group_manager(request, *args, **kwargs):
	"""
	Render the main page for the group manager.
	"""

	request_user = request.user
	groups = request_user.accountgroup_set.all()


	context = RequestContext(request, {"section":"groups",
		"groups":groups})
	return render_to_response("groups/list.html", context)

@login_required
def group_detail(request, group_id, *args, **kwargs):
	"""
	Render the details page for a specific group.
	"""

	request_user = request.user
	group = get_object_or_404(AccountGroup, pk=group_id)

	if not authenticate_group(request_user, group):
		raise PermissionDenied()

	group_members = group.members.all()

	context = RequestContext(request, {"section":"groups",
		"group":group,
		"members":group_members})
	return render_to_response("groups/detail.html", context)

@login_required
def group_create(request, *args, **kwargs):
	"""
	Create a new group.

	On GET, returns the form for creating a new group.
	On POST, attempts to validate and create a new group.
	"""

	if request.method == 'POST':
		group_form = AccountGroupForm(request.POST)
		if group_form.is_valid():
			group_form.save()
			return HttpResponseRedirect('/group')
	else:
		group_form = AccountGroupForm()

	# Update the CSRF token
	kwargs.update(csrf(request))
	context = RequestContext(request, dict(section="groups",
		form=group_form, **kwargs))
	return render_to_response("groups/form.html", context)

@login_required
def group_update(request, group_id, *args, **kwargs):
	"""
	Update an existing group.

	On GET, returns the update form for the existing group.
	On POST, attempts to validate and update the group.
	"""

	group = get_object_or_404(AccountGroup, pk=group_id)

	if not authenticate_group(request.user, group):
		raise PermissionDenied()

	if request.method == 'POST':
		group_form = AccountGroupForm(request.POST, instance=group)
		if group_form.is_valid():
			group_form.save()
			return HttpResponseRedirect('/group')
	else:
		group_form = AccountGroupForm(instance=group)

	# Update the CSRF token
	kwargs.update(csrf(request))
	context = RequestContext(request, dict(section="groups",
		form=group_form, **kwargs))
	return render_to_response("groups/form.html", context)
