from django.shortcuts import render_to_response
from django.template import RequestContext

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
