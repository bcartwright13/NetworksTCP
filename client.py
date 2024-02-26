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
    empty_binary = b'\x00' * 32
    message = create_struct(0x1, hash_requests, 0, empty_binary)
    return message


def create_hash_request(hash_count, block_size, current_block):
    # This function will create a Hash Request
    # Then, return the message as a struct obj


    block_len = len(current_block)
    struct_hash_message = create_struct(0x3, hash_count, block_len, current_block)

    return struct_hash_message


def check_acknowledgement(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        type_val = initial_message[0]
        if type_val != 0x2:
            print("CLIENT: Invalid Type Value")
            return False
        return initial_message[2] # Returns the length from ack message
    except:
        print("CLIENT: Invalid Data Format")
        return False


def check_hash_response(encoded_data):
    try:
        initial_message = open_struct(encoded_data)
        
        type_val = initial_message[0]
        if type_val != 0x4:  # Checks if type is valid
            print("CLIENT: Invalid Type Value")
            return False
        return initial_message  # Proceed if the type value is correct.
    except Exception as e:
        print(f"CLIENT: Invalid Data Format: {e}")
        return False



def connect_server(ip, port):
    # This function will be used to create a socket and connect to server
    # Then, return the socket object

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((ip,port))

    print("Connected to server!")
    return tcp_socket



def get_sys_arg():
    # Loop through command-line arguments starting from 1, since sys.argv[0] is the script name
    for i in range(1, len(sys.argv)):  
        if sys.argv[i] == '-a':  # Server IP address
            server_ip = sys.argv[i + 1]
        elif sys.argv[i] == '-p':  # Server port
            server_port = int(sys.argv[i + 1])
        elif sys.argv[i] == '-s':  # Hash block size
            hash_block_size = int(sys.argv[i + 1])
        elif sys.argv[i] == '-f':  # File path
            file_path = sys.argv[i + 1]

    return server_ip, server_port, hash_block_size, file_path


if __name__ == '__main__':
    server_ip = None
    server_port = None
    hash_block_size = None
    file_path = None

    server_ip, server_port, hash_block_size, file_path = get_sys_arg()
    # Check if all required arguments were provided
    if not (server_ip and server_port and hash_block_size and file_path):
        print("Missing required arguments.")
        sys.exit(1)

    # Example usage
    print(f"Server IP: {server_ip}")
    print(f"Server Port: {server_port}")
    print(f"Hash Block Size: {hash_block_size}")
    print(f"File Path: {file_path}")
    # Open our file from command line
    with open(file_path, 'rb') as chosen_file:
        # Connect to the server!
        server_socket = connect_server(server_ip, server_port)

        # Sending initialization message
        init_message = create_initialization(hash_block_size)
        server_socket.send(init_message)
        print("Initialization message sent.")

        # Receiving Acknowledgement
        ack_data = server_socket.recv(1024)  # Adjust buffer size if necessary
        if check_acknowledgement(ack_data):
            print("Acknowledgment received.")
        else:
            print("Failed to receive valid acknowledgment.")
            server_socket.close()
            sys.exit(1)

        # Preparing to write hash values received from the server
        hashed_data_filename = "hashed_data_output.txt"
        with open(hashed_data_filename, 'w') as hashed_data:
            print("New Hashed File Created.")

            # Sending Hash Requests for each block of the file
            count = 0
            while True:
                current_block = chosen_file.read(hash_block_size)
                if not current_block:
                    
                    break  # End of file

                hash_request = create_hash_request(count, hash_block_size, current_block)
                server_socket.send(hash_request)

                # Receiving Hash Response
                hash_response_data = server_socket.recv(1024)  # Adjust buffer size if necessary
                hash_response = check_hash_response(hash_response_data)
                #Check if proper hash response
                if hash_response:
                    hash_value = hash_response[3]
                    hashed_data.write(f"Test Segment {count}: {hash_value.hex()}\n")
                else:
                    print("Failed to process hash response.")
                    break  # Exit on failure
                
                count += 1

            print(f"Hash requests for {count} blocks completed.")


