from treasureapp.models import Account, Transaction, Accessor, \
		AccountGroup, GroupMember
from django.contrib import admin

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Accessor)
admin.site.register(AccountGroup)
admin.site.register(GroupMember)
