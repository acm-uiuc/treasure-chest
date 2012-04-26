from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from treasureapp.authenticators import authenticate_group

@login_required
def group_manager(request, *args, **kwargs):
	request_user = request.user
	groups = request_user.groups.all()


	context = RequestContext(request, {"section":"groups",
		"groups":groups})
	return render_to_response("groups/list.html", context)

@login_required
def group_detail(request, group_id, *args, **kwargs):
	request_user = request.user
	group = get_object_or_404(Group, pk=group_id)

	if not authenticate_group(request_user, group):
		raise PermissionDenied()

	context = RequestContext(request, {"section":"groups"
		})
	return render_to_response("groups/list.html", context)
