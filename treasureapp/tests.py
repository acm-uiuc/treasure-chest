#! /usr/bin/env python

from django.utils import unittest

# Import things we need to test
from django.db import models
from django.contrib.auth.models import User, Group
from treasureapp.models import Account, Transaction

class AccountTests(unittest.TestCase):
    """
    Set of tests for the Account model.

    Tests both the account model and its interactions with the transaction
    module.
    """

    def setUp(self):
        """
        Set up the testing environment.

        Create an accounts and groups for testing.
        """

        self.equity = Account.objects.create(name="Test Equity",
                description="An account for money to come out of", balance=0)
        self.account = Account.objects.create(name="Test Account",
                description="An account for testing", balance=0)

        self.group = Group.objects.create(name="Dylan Group")

    def test_transaction_interact(self):
        """
        Test that creating transactions and running get_balance works.
        """

        # Move 4000 into main account
        transaction1 = Transaction.objects.create(from_acct=self.equity,
            to_acct=self.account, owner = self.group, amount=4000.00,
            description="Opening balance")
        # Move 200 out of main account
        transaction2 = Transaction.objects.create(from_acct=self.account,
            to_acct=self.equity, owner=self.group, amount=200.00,
            description="Purchase of drugs")
        # Move 3000 nowhere (from account into account)
        transaction3 = Transaction.objects.create(from_acct = self.account,
            to_acct=self.account, owner=self.group, amount=3000.00,
            description="Laundering Money")

        acct_computed_balance = self.account.get_balance()
        acct_cached_balance = self.account.balance
        equi_computed_balance = self.equity.get_balance()
        equi_cached_balance = self.equity.balance

        self.assertEqual(acct_computed_balance, 3800.00)
        self.assertEqual(acct_computed_balance, acct_cached_balance)

        self.assertEqual(equi_computed_balance, -3800.00)
        self.assertEqual(equi_computed_balance, equi_cached_balance)

if __name__ == '__main__':
    unittest.main()
