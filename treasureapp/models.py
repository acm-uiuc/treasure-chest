from django.db import models
from django.contrib.auth.models import User, Group

class Account(models.Model):
    """
    An account represents a real-world source of money

    balance - Amount of money in the account
    """
    # TODO: break out where account max is defined
    balance = models.DecimalField(max_digits=10, decimal_places=2)

class Transaction(models.Model):
    """
    A transaction object represents money entering or exiting an account

    account - The account the transaction belongs to
    owner - The group performing the transaction
    amount - Change in account balance
    """
    account = models.ForeignKey(Account)
    owner = models.ForeignKey(Group)
    # TODO: break out constants
    balance = models.DecimalField(max_digits=6, decimal_places=2)
