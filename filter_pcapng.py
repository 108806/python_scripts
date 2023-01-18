from scapy.all import *
iplist = ['1.3.3.7','1.1.1.1']
pcap =  rdpcap('desktop_client_eth.pcapng')

filtered = []

#Filter ops
for packet in pcap:
	if packet.haslayer(IP) and (packet[IP].src in iplist or packet[IP].dst in iplist):
		filtered.append(packet)
		print('Saving:', packet.summary())
	else:
		print('Deleting:', packet.summary())

#Write results:
wrpcap('filtered_desktop_client_eth.pcapng', filtered)
