# Using wakeonlan, send magic packet to my main computer to wake it from sleep

from wakeonlan import send_magic_packet
import scriptsconfig as cfg

send_magic_packet(cfg.pc_macaddress)

print("Computer woken from lan")