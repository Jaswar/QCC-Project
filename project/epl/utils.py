# assume order of qubits is A1 B1 A2 B2
import numpy as np


def get_probability_and_fidelity(dm, state):
    target_state = np.matrix(np.array([1, 0, 0, 1]).reshape(-1, 1) / np.sqrt(2))

    m00 = np.matrix(np.array(state).reshape(-1, 1))
    m00 = m00 @ m00.H
    m00 = np.kron(np.eye(4), m00)
    assert m00.shape == dm.shape

    rho = m00.H @ dm @ m00
    p = float(np.trace(rho).real)
    rho = rho / p
    rho = partial_trace(rho, [2, 3])
    f = target_state.H @ rho @ target_state
    f = float(np.array(f)[0][0].real)
    return p, f


# taken from https://github.com/Qiskit/qiskit/blob/0517a9d7da91923a99bdaaf51b81d3251a5dec39/qiskit/tools/qi/qi.py#L133
def partial_trace(dm, indices):
    dm = np.array(dm)
    dimensions = [2 for _ in range(int(np.log2(dm.shape[0])))]
    trace_systems = sorted(indices, reverse=True)
    for j in trace_systems:
        # Partition subsystem dimensions
        dimension_trace = int(dimensions[j])  # traced out system
        left_dimensions = dimensions[:j]
        right_dimensions = dimensions[j + 1:]
        dimensions = left_dimensions + right_dimensions
        # Contract remaining dimensions
        dimension_left = int(np.prod(left_dimensions))
        dimension_right = int(np.prod(right_dimensions))

        # Reshape input array into tri-partite system with system to be
        # traced as the middle index
        dm = dm.reshape([
            dimension_left, dimension_trace, dimension_right, dimension_left,
            dimension_trace, dimension_right
        ])
        # trace out the middle system and reshape back to a matrix
        dm = dm.trace(axis1=1,
                       axis2=4).reshape(dimension_left * dimension_right,
                                        dimension_left * dimension_right)
    return dm
