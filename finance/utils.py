
from django.conf import settings

import hmac
import hashlib
from django.utils.http import urlencode

BCH = "BCH"
BLK = "BLK"
BTC = "BTC"
DASH = "DASH"
DGB = "DGB"
DOGE = "DOGE"
ETC = "ETC"
ETH = "ETH"
LTC = "LTC"

CURRENCY_CHOICES = (
    (BCH, 'Bitcoin Cash'),
    (BLK, 'BlackCoin'),
    (BTC, 'Bitcoin'),
    (DASH, 'Dash'),
    (DOGE, 'Dogecoin'),
    (ETH, 'Ether'),

)


def get_coins_list():
    coins = getattr(settings, 'COINPAYMENTS_ACCEPTED_COINS', None)
    if not coins:
        coins = CURRENCY_CHOICES
    return coins


def create_ipn_hmac(request):
    ipn_secret = getattr(settings, 'COINPAYMENTS_IPN_SECRET', None)
    encoded = urlencode(request).encode('utf-8')
    hash = hmac.new(bytearray(ipn_secret, 'utf-8'), encoded, hashlib.sha512).hexdigest()
    return hash
