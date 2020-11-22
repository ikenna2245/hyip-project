
from celery.utils.log import get_task_logger
from celery import shared_task
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal
from django_coinpayments.models import Payment, CoinPaymentsTransaction
from django_coinpayments.exceptions import CoinPaymentsProviderError, TxInfoException
from .CoinPayments import CoinPayments
from .models import Deposit, D_History, Transaction

logger = get_task_logger(__name__)

@shared_task
def refresh_tx_info():
    caller = CoinPayments.get_instance()
    objects = Payment.objects.get_pending_payments().order_by('id')
    # 25 because of https://www.coinpayments.net/apidoc-get-tx-info
    paginator = Paginator(objects, 25)
    for page in paginator.page_range:
        chunk = paginator.page(page).object_list
        provider_txs_ids = [i.provider_tx.id for i in chunk]
        res = caller.get_tx_info_multi({'txid': '|'.join(provider_txs_ids)})
        if res['error'] == 'ok':
            results = res['result']
            for k, v in results.items():
                temp = CoinPaymentsTransaction.objects.filter(id=k).first()
                if not temp:
                    logger.error(
                        'CoinPaymentsTransaction with id %s received from API but not found in DB'.format(str(k)))
                else:
                    payment = temp.payment
                    t = Transaction.objects.get(transaction_id=payment.provider_tx)
                    d = Deposit.objects.get(transaction_id=payment.provider_tx)
                    d_h = D_History.objects.get(transaction_id=payment.provider_tx)
                    # Payments statuses: https://www.coinpayments.net/merchant-tools-ipn
                    # Safe statuses: 2 and >= 100
                    if v['status'] == 2 or v['status'] >= 100:
                        logger.info('Received payment for transaction {} - payment {} ({})'
                                    .format(str(k), str(payment.id), str(payment.amount)))
                        payment.amount_paid = payment.amount
                    else:
                        payment.amount_paid = Decimal(v['receivedf'])
                    if payment.amount_paid == payment.amount:
                        payment.status = Payment.PAYMENT_STATUS_PAID
                        payment.save()
                        t.approved = True
                        d.status = True
                        d_h.status = True
                        t.save()
                        d.save()
                        d_h.save()
        else:
            raise TxInfoException(res['error'])

@shared_task
def set_timeout_for_payments():
    objects = Payment.objects.mark_timed_out_payments()
    return [i.id for i in objects]

@shared_task
def set_interest_today():
    Deposits = Deposit.objects.filter(status = True)
    for deposit in Deposits:
        if deposit.plan == "Basic":
            deposit.interest_today = deposit.amount * 5/100
            deposit.interest_earnings += deposit.interest_today
            deposit.earning_today = deposit.amount + deposit.amount * 5/100
            deposit.total_earning = deposit.amount + deposit.interest_earnings
            deposit.save()
        if deposit.plan == "Business":
            deposit.interest_today = deposit.amount * 6/100
            deposit.interest_earnings += deposit.interest_today
            deposit.earning_today = deposit.amount + deposit.amount * 6/100
            deposit.total_earning = deposit.amount + deposit.interest_earningsings
            deposit.save()
        if deposit.plan == "Index":
            deposit.interest_today = deposit.amount * 8/100
            deposit.interest_earnings += deposit.interest_today
            deposit.earning_today = deposit.amount + deposit.amount * 8/100
            deposit.total_earning = deposit.amount + deposit.interest_earnings
            deposit.save()
        if deposit.plan == "Dynamic":
            deposit.interest_today = deposit.amount * 15/100
            deposit.interest_earnings += deposit.interest_today
            deposit.earning_today = deposit.amount + deposit.amount * 15/100
            deposit.total_earning = deposit.amount + deposit.interest_earnings
            deposit.save()
    logger.info("Interest For Today Calculated")


@shared_task
def set_matured_balance():
    list = Deposit.objects.all()
    for item in list:
        if item.mature_date <= timezone.now():
            item.matured = True
            item.status = False
            item.save()
            if item.matured:
                item.interest_today = 0.0
                item.save()
    logger.info("Matured Deposit Approved")
