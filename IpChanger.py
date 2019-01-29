from spoofmac.util import random_mac_address
from spoofmac.interface import set_interface_mac


target_mac = random_mac_address('randomize')
set_interface_mac('Ethernet', target_mac)
