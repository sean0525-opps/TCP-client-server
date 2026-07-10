#!/usr/bin/env python 
# Source Python Network Programming Cookbook,Second Edition -- Chapter - 1 

import socket  
host = 'localhost' 
 
def echo_client(port): 
    """ A simple echo client """ 
    # Create a TCP/IP socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Connect the socket to the server 
    server_address = ('localhost', 9900)
    print("--------------------")
    print ("Connecting to %s port %s" % server_address) 
    sock.connect(server_address) 
     
    # Send data 
    try: 
        # Send data
        print('Enter your text: (in this order [Builder Name] [Builder Number] [Amount of Materials] [Construction Materials Required] [Currency Wish to Pay In]) ')
        message = input()
        material_list = ["cement", "bricks", "screws", "rods", "mortar"]
        message_parts = message.split()
        found = False
        correct = True
        if (len(message_parts) < 5 or len(message_parts) % 2 != 1) and message_parts[0] != "backorder" and message_parts[0] != "stock": # makes sure the input length is correct and gives exceptions to admin comands
          print("Invalid input format")
          correct = False
        if message_parts[1].isdigit() == False:
          print("Builder number must be an integer")
          correct = False
        if message_parts[2].isdigit() == False:
          print("Material amount must be an integer")
          correct = False
        x = 2
        num_materials = 0
        while num_materials < (len(message_parts) - 3) // 2:
          amount = message_parts[x]
          material = message_parts[x + 1].lower()
          if not amount.isdigit(): # check quantity is a number
            print("Invalid quantity")
            break
          found = False
          # check if material exists
          for i in range(len(material_list)):
            if material_list[i] == material:
              found = True
              break
          if found == False:
            print("Material not found")
            correct = False  
            break
          num_materials = num_materials + 1
          x = x + 2
               
        if message_parts[-1].lower() not in ["dollars", "dollar", "pounds", "pound", "euros", "euro"]:
          print("Currency required: Pounds, Euros or Dollars")
          correct = False
        if correct == True:
          print ("Sending to Server: %s :" % message) 
          sock.sendall(message.encode('utf-8')) 
          # Look for the response 
          amount_received = 0 
          amount_expected = len(message) 
          data = sock.recv(1024) 
          amount_received += len(data) 
          print ("Received from Server:", data.decode("utf-8"))
    except socket.error as e: 
        print ("Socket error: %s" %str(e)) 
    except Exception as e: 
        print ("Other exception: %s" %str(e)) 
    finally: 
        print ("Closing connection to the server") 
        sock.close() 
     
if __name__ == '__main__': 
    port = 9900 
    while True:
        echo_client(port) 
