import math
from netqasm.sdk.external import get_qubit_state
from utils import get_probability_and_fidelity


def bbpssw_protocol_alice(q1, q2, alice, socket):
    """
    Implements Alice's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    a, avg_fidelity = bbpssw_gates_and_measurement_alice(q1, q2, alice, socket)
    alice.flush()
    a = int(a)

    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    socket.send(str(a))
    b = int(socket.recv())

    return a == b, avg_fidelity


def bbpssw_gates_and_measurement_alice(q1, q2, alice, socket):
    """
    Performs the gates and measurements for Alice's side of the BBPSSW protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :return: Integer 0/1 indicating Alice's measurement outcome
    """
    q1.cnot(q2)
    alice.flush()
    q1.cnot(q2)
    ####################################################################################
    # note that this communication is to synchronize Alice and Bob before get_qubit_state
    # otherwise the state is random and depends on who performs their gates earlier
    # this piece of code does not change the functionality of the protocol
    socket.recv()
    state = get_qubit_state(q1, reduced_dm=False)
    p00, f00 = get_probability_and_fidelity(state, [1, 0, 0, 0])
    p11, f11 = get_probability_and_fidelity(state, [0, 0, 0, 1])
    mix = p00 * f00 + p11 * f11
    socket.send('done')
    ####################################################################################
    m = q2.measure()
    return m, mix


def bbpssw_protocol_bob(q1, q2, bob, socket):
    """
    Implements Bob's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    b = bbpssw_gates_and_measurement_bob(q1, q2, bob, socket)
    bob.flush()
    b = int(b)

    # Write below the code to send measurement result to Alice, receive measurement result from Alice and check if protocol was successful
    a = int(socket.recv())
    socket.send(str(b))

    return a == b


def bbpssw_gates_and_measurement_bob(q1, q2, bob, socket):
    """
    Performs the gates and measurements for Bob's side of the BBPSSW protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :return: Integer 0/1 indicating Bob's measurement outcome
    """
    q1.cnot(q2)
    ####################################################################################
    # note that this communication is to synchronize Alice and Bob before get_qubit_state
    # otherwise the state is random and depends on who performs their gates earlier
    # this piece of code does not change the functionality of the protocol
    bob.flush()
    socket.send('ready')
    socket.recv()
    ####################################################################################
    m = q2.measure()
    return m

