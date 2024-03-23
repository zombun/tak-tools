import takproto
import socket
from time import sleep


cot = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2024-03-22T20:10:44.000Z' start='2024-03-22T18:10:44.000Z' stale='2024-03-24T18:11:11.000Z' how='h-e'>
    <point lat='60.120809' lon='24.417518' hae='26.767999' ce='9999999.0' le='9999999.0' />
    <detail>
        <uid Droid='Eliopoli HQ'/>
        <contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/>
        <__group name='Yellow' role='HQ'/><status battery='100'/>
        <takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/>
        <track speed='0.00000000' course='0.00000000'/>
    </detail>
</event>
"""

buf = takproto.xml2proto(cot)
print(buf)

interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
allips = [ip[-1][0] for ip in interfaces]

msg = buf
while True:

    for ip in allips:
        print(f'sending on {ip}')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind((ip,0))
        # sock.sendto(msg, ("192.168.68.114", 6969))
        sock.sendto(msg, ("239.2.3.1", 6969))
        sock.close()

    sleep(5)


