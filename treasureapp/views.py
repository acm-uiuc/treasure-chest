from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def index(request):
    """
    Render the main page of the Treasure Chest application.
    """

    context = RequestContext(request, {})
    return render_to_response("index.html", context)
