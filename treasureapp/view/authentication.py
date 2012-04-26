from django.contrib.auth.decorators import login_required

@login_required
def group_manager(*args, **kwargs):
	pass
