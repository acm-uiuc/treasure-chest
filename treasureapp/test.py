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

        Create an account for testing.
        """

        self.equity = Account.objects.create(name="Test Equity",
                description="An account for money to come out of", balance=0)
        self.account = Account.objects.create(name="Test Account",
                description="An account for testing", balance=0)

    def test_transaction_interact(self):
        """
        Test that creating transactions and running get_balance works.
        """

        pass

if __name__ == '__main__':
    unittest.main()
