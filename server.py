import struct
import sys
import socket
import select
import hashlib

def create_struct(short_int1, long_int1, long_int2, str_32_byte):
    # This function will be used to create a universal struct object
    message = struct.pack('!HLL32s', short_int1, long_int1, long_int2, str_32_byte)
    return message
    

def open_struct(struct_obj):
    # This function will be used to open a universal struct object
    message = struct.unpack('!HLL32s', struct_obj)
    return message  # Returns array [short, long, long, 32-byte string]


def create_acknowledgement(input_n):
    # This function retrieves the S value from the initialization message
    # Then, return acknowledgement message
    
    # Write your logic
    return message


def check_initialization(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        num_hash_requests = socket.ntohl(TODO)  # Block sizes this client will send
        type_val = socket.ntohs(TODO)
        if type_val != TODO:
            print("SERVER: Invalid Type Value")
            return False
        return num_hash_requests
    except:
        print("SERVER: Invalid Data Format")
        return False
    
def check_hash_request(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        type_val = socket.ntohs(TODO)
        if type_val != TODO:
            print("SERVER: Invalid Type Value")
            return False 
        return initial_message # Struct Object
    except:
        print("SERVER: Invalid Data Format")
        return False


def get_hashed_data(hash_request):
    # This function will receive an unpacked struct representing our hash request
    # Then, return hashed data and hash response

    # Extract variables
    request_type = TODO  # HashRequest Type
    request_i = TODO  # HashRequest i
    request_len = TODO  # HashRequest Length
    request_payload = TODO + TODO  # HashRequest Data + UTF-8 Encoded Salt

    hash_and_salt = TODO
    request_i = TODO
    return create_struct(TODO)


def start_server(port):
    # This function will create our TCP Server Socket, start listening, then return the Socket Object

    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setblocking(0)  # Allow multiple connections
    tcp_server_socket.bind(('',port))  # Start listening!
    tcp_server_socket.listen(5)  # 10 is the max number of queued connections allowed
    return tcp_server_socket


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Variables we need
    if len(sys.argv) < 3:
        print("Improper command line arguments\nExiting program...")
        sys.exit(1)
    print(int(sys.argv[2]))
    print(sys.argv[4])
    server_port = int(sys.argv[2]) # Extract server port from command line arguments
    hash_salt = sys.argv[4] # Extract salt value from command line arguments

    server_socket = start_server(server_port)
    clients = [server_socket]
    n_sizes = {}
    print("Server listening...")

    ## WRITE YOUR CODE TO IMPLEMENT SERVER SIDE PROTOCOL LOGIC
    ## USE select() to handle multiple clients




    
