import struct
import sys
import socket


def create_struct(short_int1, long_int1, long_int2, str_32_byte):
    # This function will be used to create a universal struct object
    message = struct.pack('!HLL32s', short_int1, long_int1, long_int2, str_32_byte)
    return message
    

def open_struct(struct_obj):
    # This function will be used to open a universal struct object
    message = struct.unpack('!HLL32s', struct_obj)
    return message  # Returns array [short, long, long, 32-byte string]

def create_initialization(hash_requests):
    # This function will be used to create the initialization message to send to the server using struct
    # Then, return the message
    empty_binary = TODO
    message = create_struct(TODO)
    return message


def create_hash_request(hash_count, block_size, current_block):
    # This function will create a Hash Request
    # Then, return the message as a struct obj

    hash_count = TODO
    block_len = TODO
    struct_hash_message = create_struct(TODO)

    return struct_hash_message


def check_acknowledgement(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        type_val = socket.ntohs(TODO)
        if type_val != TODO:
            print("CLIENT: Invalid Type Value")
            return False
        return TODO # Returns the Length from Ack Message
    except:
        print("CLIENT: Invalid Data Format")
        return False


def check_hash_response(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        type_val = socket.ntohs(TODO)
        if type_val != TODO:
            print("CLIENT: Invalid Type Value")
            return False
        return TODO # Returns Struct Object
    except:
        print("CLIENT: Invalid Data Format")
        return False


def connect_server(ip, port):
    # This function will be used to create a socket and connect to server
    # Then, return the socket object

    ## TODO - Write logic to connect to the server

    print("Connected to server!")
    return tcp_socket


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Variables we need from the command line
    server_ip = TODO  # Extract server IP
    server_port = TODO  # Extract server port
    hash_block_size = TODO  # Extract S
    file_path = TODO  # Extract file path

    # Open our file from command line
    chosen_file = open(TODO)

    # Connect to the server!
    server_socket = connect_server(server_ip, server_port)

    # Initialization Message Portion
    # Write your logic for initilization message

    print("Initialization sent.")

    # Acknowledgement Message Verification (write your code below)
    

    # Let's keep track of hash count, and our new hashed data file
    # you can write the hash values received from the server in this file
    count = 0
    hashed_data = open(TODO)
    print("New Hashed File Created.")
    # Use a loop to send each block
    
    # Write your code to implement client's side protocol logic.


    # We're done - Let's close our open files and sockets
    print("Done! Closing files and sockets.")
    TODO  # New Hash Data File
    TODO  # Command Line File
    TODO  # Server Socket



