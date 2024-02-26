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



def create_acknowledgement(num_hash_requests):
    # Assuming an acknowledgment message structure similar to create_struct
    # and the response length is 40 * num_hash_requests (as per your description)
    response_length = 40 * num_hash_requests
    return create_struct(0x2, 0, response_length, b'')



def check_initialization(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        num_hash_requests = socket.ntohl(initial_message[1])  # Block sizes this client will send
        type_val = socket.ntohs(initial_message[0])
        if type_val != 0x1:
            print("SERVER: Invalid Type Value")
            return False
        return num_hash_requests
    except:
        print("SERVER: Invalid Data Format")
        return False
    
def check_hash_request(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        type_val = socket.ntohs(initial_message[0])
        if type_val != 0x3:
            print("SERVER: Invalid Type Value")
            return False 
        return initial_message # Struct Object
    except:
        print("SERVER: Invalid Data Format")
        return False


def get_hashed_data(hash_request, hash_salt):
    
    request_type, request_i, request_len, request_payload = hash_request
    
    salt_encoded = hash_salt.encode('utf-8')
    data_to_hash = request_payload + salt_encoded
    

    hasher = hashlib.sha256()
    hasher.update(data_to_hash)
    hashed_data = hasher.digest()  
    
    return create_struct(0x4, request_i, 32, hashed_data)

#Read requests coming from the client
def read_requests(readable, input_sockets, responses_to_send):
    for s in readable:
        if s is server_socket:
            # Handle new connections
            client_socket, addr = server_socket.accept()
            print(f"Connected with {addr}")
            client_socket.setblocking(0)
            input_sockets.append(client_socket)
        else:
            # Handle data from a client
            try:
                data = s.recv(1024)
                
                if data:
                    # Process data
                    
                    hash_request = open_struct(data)
                    if hash_request[0] in [1, 3]:  
                        if hash_request[0] == 1:  # Initialization message
                            # Process initialization and prepare acknowledgment
                            print("Received initialization")
                            response = create_acknowledgement(hash_request[1])  
                            print("Returned Ack")
                        elif hash_request[0] == 3:  # HashRequest message
                            print(f'Received hash')
                            response = get_hashed_data(hash_request, hash_salt)
                        responses_to_send[s] = response
                    else:
                        print("Unknown request type received")
                else:
                    # Remove socket that's no longer connected
                    input_sockets.remove(s)
                    s.close()
            except socket.error as e:
                # Handle errors such as client disconnecting
                input_sockets.remove(s)
                s.close()

#Sends out responses that were stored from the readable function
def write_responses(writable, responses_to_send):
    for s in writable:
        if s in responses_to_send:
            try:
                s.send(responses_to_send[s])
                del responses_to_send[s]  # Remove from the dictionary once sent
            except socket.error as e:
                print(f"Error sending response: {e}")
                s.close()
                # Makes sure to remove from input_sockets and responses_to_send if an error occurs
                if s in input_sockets:
                    input_sockets.remove(s)
                if s in responses_to_send:
                    del responses_to_send[s]

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
    server_port = None
    hash_salt = None
    # Loop through command-line arguments to match them appropriatly
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-p':
            server_port = int(sys.argv[i + 1])
        elif sys.argv[i] == '-s':
            hash_salt = sys.argv[i + 1]
    
    if not (server_port and hash_salt):
        print("Missing required arguments")
        sys.exit(1)

    server_socket = start_server(server_port)
    input_sockets= [server_socket]
    requests = []
    n_sizes = {}
    print("Server listening...")
    responses_to_send = {}

    #Loop that enables multiple clients and requests using select
    while True:
        readable, writable, exceptional = select.select(input_sockets, list(responses_to_send.keys()), input_sockets, 0.1)
        read_requests(readable, input_sockets, responses_to_send)
        write_responses(writable, responses_to_send)





    
