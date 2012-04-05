from django.forms import Form, ModelForm

from treasureapp.models import Account, Transaction

class AccountForm(ModelForm):
    """
    A basic form for creating or updating an account.
    """

    class Meta:
        model = Account
        # User cannot directly edit cached balance
        fields = ('name', 'description')

class TransactionForm(ModelForm):
    """
    A basic form for creating or updating a transaction.
    """

    class Meta:
        model = Transaction
        fields = ('from_acct', 'to_acct', 'amount', 'owner', 'description')
