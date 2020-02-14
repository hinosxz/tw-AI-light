from client import *
import struct 

class Command:
    def __init__(self):
        pass

# class MOV(Command):
#     def __init__(self, sock, Species, **kwargs):
#         if len(kwargs)==0:
#             raise ValueError('You must move at least one group')
#         msg_to_send =  b'MOV'
#         for number in kwargs.keys():
#             for group in Species.groups():
#                 if number == group.get_size():
#                     try: 
#                         group.move(kwargs[number])
#                     except:
#                         pass
#                 elif number 
#         sock.send(msg_to_send)

class NME(Command):
    def __init__(self, sock, Player):
        msg_to_send = b'NME'
        msg_to_send += struct.pack("B", len(Player._name))
        msg_to_send += Player._name.encode()
        sock.send(msg_to_send)


