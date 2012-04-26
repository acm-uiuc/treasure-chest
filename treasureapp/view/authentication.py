from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from treasureapp.authenticators import authenticate_group

@login_required
def group_manager(request, *args, **kwargs):
	"""
	Render the main page for the group manager.
	"""

	request_user = request.user
	groups = request_user.groups.all()


	context = RequestContext(request, {"section":"groups",
		"groups":groups})
	return render_to_response("groups/list.html", context)

@login_required
def group_detail(request, group_id, *args, **kwargs):
	"""
	Render the details page for a specific group.
	"""

	request_user = request.user
	group = get_object_or_404(Group, pk=group_id)

	if not authenticate_group(request_user, group):
		raise PermissionDenied()

	group_members = group.user_set.all()

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

	pass

@login_required
def group_update(request, group_id, *args, **kwargs):
	"""
	Update an existing group.

	On GET, returns the update form for the existing group.
	On POST, attempts to validate and update the group.
	"""

	pass
