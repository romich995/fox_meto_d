from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

UserModel = get_user_model()

class Wallet(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    objects = models.Manager()
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(balance__gte=0),
                name='%(app_label)s_%(class)s_balance>=0'
            )
        ]


class Transaction(models.Model):
    from_wallet = models.ForeignKey(Wallet, related_name="from_transactions", null=True, on_delete=models.SET_NULL)
    to_wallet = models.ForeignKey(Wallet, related_name="to_transactions", null=True, on_delete=models.SET_NULL)
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(transfer_amount__gt=0),
                name='%(app_label)s_%(class)s_transfer_amount>0'
            )
        ]