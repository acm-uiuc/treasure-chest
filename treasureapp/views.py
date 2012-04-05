from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

# Basic content handlers

def index(request):
    """
    Render the main page of the Treasure Chest application.
    """

    context = RequestContext(request, {})
    return render_to_response("index.html", context)

def help(request):
    pass

# Account handlers

def account_list(request):
    """
    Render the listing of all accounts.

    On GET, it will return a listing of all accounts.
    On POST, it will create a new account.
    """

    context = RequestContext(request, {})
    return render_to_response("index.html", context)

def account_detail(request):
    """
    Handle the REST features on individual accounts.

    On GET, it will return details on the specific account.
    On POST, it will update information about the account.
    """

    context = RequestContext(request, {})
    return render_to_response("index.html", context)

def account_create(request):
    pass

def account_update(request):
    pass

# Transaction handlers

def transaction_list(request):
    pass

def transaction_detail(request):
    pass

def transaction_create(request):
    pass

def transaction_update(request):
    pass
