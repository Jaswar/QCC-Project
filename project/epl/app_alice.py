from epl import epl_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket(app_name='alice', remote_app_name='bob')

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('bob')

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection('alice', epr_sockets=[epr_socket])

    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        pass

if __name__ == "__main__":
    main()
