from django.db import models
from django.contrib.auth.models import User, Group

class Account(models.Model):
    """
    An account represents a real-world source of money

    name - A name for the account
    balance - Amount of money in the account
    """

    name = models.CharField(max_length = 200)
    balance = models.DecimalField(max_digits = 10, decimal_places = 2)

    def __unicode__(self):
        return self.name

class Transaction(models.Model):
    """
    A transaction object represents money entering or exiting an account

    from_acct - The account the transaction is coming out of
    to_acct - The account the transaction is going into
    owner - The group performing the transaction
    amount - Change in account balance
    description - An optional description of the account balance
    """

    from_acct = models.ForeignKey(Account, related_name='from_acct')
    to_acct = models.ForeignKey(Account, related_name='to_acct')
    owner = models.ForeignKey(Group)
    amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    description = models.TextField(blank=True)
