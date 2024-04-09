from bbpssw import bbpssw_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
import numpy as np


def main(app_config=None):
    target_state = np.matrix(np.array([1, 0, 0, 1]).reshape(-1, 1) / np.sqrt(2))

    # Create a socket for classical communication
    socket = Socket(app_name='alice', remote_app_name='bob')

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket('bob')

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection('alice', epr_sockets=[epr_socket])

    # Create Alice's context, initialize EPR pairs inside it and call Alice's BBPSSW method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        q1, q2 = epr_socket.create(2)
        result, avg_fidelity = bbpssw_protocol_alice(q1, q2, alice, socket)
        state = get_qubit_state(q1, reduced_dm=False)
        fidelity = target_state.H @ state @ target_state
        fidelity = float(np.array(fidelity)[0][0].real) if result else 0.0
    return [fidelity, avg_fidelity]

if __name__ == "__main__":
    main()
