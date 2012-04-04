from django.db import models
from django.contrib.auth.models import User, Group

class Account(models.Model):
    """
    An account represents a real-world source of money

    name - A name for the account
    """

    name = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.name

    def get_balance(self):
        """
        Calculate the balance for the account.

        Iterates through all transactions in the account to compute the
        available account balance.

        Returns the current account balance.
        """
        balance = 0
        for transaction in Transaction.objects.all():
            amount = transaction.amount

            # Subtract for transactions out, add for transactions in
            if transaction.from_acct == self:
                balance -= amount
            # In case of from_acct == to_acct, balance is unchanged
            if transaction.to_acct == self:
                balance += amount

        return balance

class Transaction(models.Model):
    """
    A transaction object represents money entering or exiting an account

    from_acct - The account the transaction is coming out of
    to_acct - The account the transaction is going into
    owner - The group performing the transaction
    amount - Change in account balance
    description - An optional description of the transaction
    """

    from_acct = models.ForeignKey(Account, related_name='from_acct')
    to_acct = models.ForeignKey(Account, related_name='to_acct')
    owner = models.ForeignKey(Group)
    amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    description = models.TextField(blank=True)

    def __unicode__(self):
        strout = self.from_acct.__unicode__() \
               + " to "                       \
               + self.to_acct.__unicode__()   \
               + " for "                      \
               + str(self.amount)

        return strout
