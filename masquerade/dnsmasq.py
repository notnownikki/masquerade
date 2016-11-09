import os
import psutil
import signal


PROCNAME = 'dnsmasq'

def send_sighup():
    for proc in psutil.process_iter():
        if proc.name() == PROCNAME and proc.uids()[0] == os.getuid():
            proc.send_signal(signal.SIGHUP)
