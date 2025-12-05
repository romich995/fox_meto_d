from django.db import transaction
from rest_framework import serializers
from decimal import Decimal

from transactional_system_core.models import Transaction, Wallet
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['from_wallet', 'to_wallet', 'transfer_amount']

    def create(self, validated_data):
        with transaction.atomic():
            from_wallet: Wallet = validated_data['from_wallet']
            to_wallet: Wallet = validated_data['to_wallet']

            if from_wallet.balance < validated_data['transfer_amount']:
                raise ValueError("Insufficient funds")
            if validated_data['transfer_amount'] <= Decimal('1000.00'):
                transaction_ = Transaction(
                    **validated_data
                    )
                from_wallet.balance -= transaction_.transfer_amount
                to_wallet.balance += transaction_.transfer_amount
            else:
                admin_wallet: Wallet = Wallet.objects.get(pk=1)
                comission = (validated_data['transfer_amount'] * Decimal('0.1')).quantize(Decimal('1.00'))
                validated_data['transfer_amount'] -= comission

                transaction_ = Transaction(
                    **validated_data
                )
                from_wallet.balance -=  transaction_.transfer_amount
                to_wallet.balance += transaction_.transfer_amount

                comission_transaction = Transaction(
                    from_wallet=validated_data["from_wallet"],
                    to_wallet=admin_wallet,
                    transfer_amount=comission
                )
                from_wallet.balance -= comission
                admin_wallet.balance += comission

                comission_transaction.save()
                admin_wallet.save()

            from_wallet.save()
            to_wallet.save()
            transaction_.save()


