import threading
from spoofmac.util import random_mac_address
from spoofmac.interface import set_interface_mac


def test_print():
    timer = 1
    timer *= 3600
    threading.Timer(timer, test_print).start()
    target_mac = random_mac_address('randomize')
    set_interface_mac('Ethernet', target_mac)
    print "IP changing"

test_print()
