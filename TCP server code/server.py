    #!/usr/bin/env python
    # Python Network Programming Cookbook,Second Edition -- Chapter - 1
    
import socket
import sys
import random
    
host = 'localhost'
data_payload = 2048
backlog = 5
port = 9900
    
def echo_server(port):
  """ A simple echo server """
  # Create a TCP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # Enable reuse address/port 
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  # Bind the socket to the port
  server_address = ('localhost', 9900)
  print ("Starting up echo server  on %s port %s" % server_address)
  sock.bind(server_address)
  # Listen to clients, backlog argument specifies the max no. of queued connections
  sock.listen(backlog)
  materials = [["cement", 1000, 75, 50], ["bricks", 1000, 10, 5], ["rods", 1000, 20, 4.5], ["screws", 1000, 5, 0.5], ["mortar", 1000, 10, 15]]
  backorder = [] 
  booking_num = 0
  while True:
    cost = 0
    num_materials = 0
    items = ""
    missing = ""  
    num_missing = 0
    dcost = 0
    discount = False
    x = 2   
    carbon_out = 0
    carbon_message = ""
    print("Waiting to receive message from client")
    client, address = sock.accept() 
    data = client.recv(data_payload)
    if data: 
      order = data.decode("utf-8").split()
      if order[0] == "backorder":
        receipt = str(backorder)
      elif order[0] == "stock":
        receipt = str(materials)
      else: # the main logic
        while num_materials != (len(order) - 3)/2 :
          material = order[x + 1].lower()
          amount = int(order[x])
          found = False
          surplus = False
          x = x + 2
          for i in range(len(materials)): # adjusts stock levels
            if materials[i][0] == material:
              found = True
              num_materials = num_materials + 1
              if materials[i][1] >= amount: # for when the ordered material is within stock levels
                materials[i][1] = materials[i][1] - amount
                cost = cost + (amount * materials[i][2])
                items = items + " " + str(amount) + " " + material
                carbon_out = carbon_out + (materials[1][3] * amount) 
              else: # for when a surplus amount is given
                surplus = True
                current = materials[i][1]
                cost = cost + (current * materials[i][2])
                overflow = amount - current
                items = items + " " + str(current) + " " + material
                missing = missing + " " + str(overflow) + " " + material 
                num_missing = num_missing + 1
                m = []
                m.append(booking_num)
                m.append(material)
                m.append(overflow)
                backorder.append(m)
                carbon_out = carbon_out + (materials[i][3] * amount) 
              if material == "bricks": # environment messages
                carbon_message = carbon_message + "Environmentally friendly alternatives to traditional fired clay bricks include compressed earth blocks "
              elif material == "cement":
                carbon_message = carbon_message + "Environmentally friendly alternatives to traditional cement include low-carbon materials like fly ash, slag, and hempcrete "
              elif material == "screws":
                carbon_message = carbon_message + "Environmentally friendly alternatives to screws are to use recycled screws "
              elif material == "rods":
                carbon_message = carbon_message + "Environmentally friendly alternatives to traditional metal rods include bamboo "
              else:
                carbon_message = carbon_message + "Environmentally friendly mortar alternatives to traditional mortar include hydraulic lime mortar "
              break
        if cost > 12000 or num_materials > 4 or num_missing > 2: # discount for when requirements are met
          dcost = cost * 0.8
          discount = True
        currency = order[len(order)-1].lower() # curency conversion
        if order[len(order)-1] == "dollars" or order[len(order)-1] == "dollar":
          cost = cost * 1.34
        elif order[len(order)-1] == "euros" or order[len(order)-1] == "euro":
          cost = cost * 1.16
        else:
          currency = "pounds"
        cost = "{:.2f}".format(cost) # format the string so it has 2dp
        if found == False:
          receipt = "Material not found"
        elif surplus == True:
          receipt = ("Order num: " + str(booking_num) + " Builder " + order[0] + " ID " + order[1] + " ordered " + items + " this costs " + str(cost) + " " + currency + " You will be charged and will receive the remaining " + missing + " when we produce them. The carbon footprint for this order is " + str(carbon_out) + " "  + carbon_message)
        elif discount == True:
          receipt = ("Order num: " + str(booking_num) + " Builder " + order[0] + " ID " + order[1] + " ordered " + items + " this costs " + str(cost) + " " + currency + " due to meeting the criteria for a 20% discount the new cost is " + str(dcost) + " " + currency + " the carbon footprint for this order is " + str(carbon_out) + " " + carbon_message)
        else:
          receipt = ("Order num: " + str(booking_num) + " Builder " + order[0]+ " ID " + order[1] + " ordered " + items + " this costs " + str(cost) + " " + currency + " the carbon footprint for this order is " + str(carbon_out) + " " + carbon_message)
          booking_num = booking_num + 1
      r = random.randint(0,6)
      if r == 6:
        for j in range(len(materials)): # Restock all materials
            materials[j][1] += 1000
        fulfilled = []
        for k in range(len(backorder)): # Process backorders
            order_id, material_name, qty_needed = backorder[k]
            for j in range(len(materials)):
                if materials[j][0] == material_name:
                    available = materials[j][1]
                    if available >= qty_needed:
                        materials[j][1] -= qty_needed
                        fulfilled.append(k)
                    else:
                        backorder[k][2] -= available
                        materials[j][1] = 0
                    break
        for index in sorted(fulfilled, reverse=True): # Remove fulfilled backorders
            backorder.pop(index)

      client.send(receipt.encode("utf-8"))
      client.close()

    
if __name__ == '__main__':
  #given_args = parser.parse_args() 
  port =9900
  echo_server(9900)
