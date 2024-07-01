import network
import socket
import os
import mdns

# Connect to the AP
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('unreliablecode.net', '@DiahSayang<3')

# Wait for the connection to be established
while not sta.isconnected():
    pass

print('Connected to AP with IP:', sta.ifconfig()[0])

# Set up the access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='PCR', authmode=network.AUTH_OPEN)

print('Access Point configuration:', ap.ifconfig())

# Set up mDNS
hostname = "hotspot.pcr.ac.id"
mdns_server = mdns.Server()
mdns_server.start(hostname, "PCR Hotspot")
mdns_server.addService("_http", "_tcp", 80)

# Function to serve the HTML page from the filesystem
def serve_html():
    with open('index.html', 'r') as f:
        return f.read()

# Set up the socket to listen for incoming connections
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Main loop to handle incoming connections
while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    
    request = cl.recv(1024)
    print('Request:', request)
    
    response = serve_html()
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
