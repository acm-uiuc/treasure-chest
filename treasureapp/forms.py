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
