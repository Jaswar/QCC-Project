from epl import epl_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state

def main(app_config=None):
    
    # Create a socket for classical communication
    socket = Socket(app_name='bob', remote_app_name='alice')

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('alice')

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection('bob', epr_sockets=[epr_socket])

    # Create Bob's context, initialize EPR pairs inside it and call Bob's EPL method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        q1, q2 = epr_socket.recv(2)
        result = epl_protocol_bob(q1, q2, bob, socket)
    return result

if __name__ == "__main__":
    main()
