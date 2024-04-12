import os
import numpy as np
from common import run_algorithm, clean, generate_setup


class Action(object):

    def __init__(self, name):
        self.name = name
        self.failures = 0
        self.successes = 0

    def run(self):
        print(f'Running {self.name}')
        reward = run_algorithm(self.name)
        if np.random.random() < reward:
            self.successes += 1
        else:
            self.failures += 1

    def sample(self):
        return np.random.beta(self.successes + 1, self.failures + 1)

    def __str__(self):
        return f'Action<{self.name}, {self.successes}, {self.failures}>'


class Master(object):

    def __init__(self, algos, num_iter=500):
        self.num_iter = num_iter
        self.actions = [Action(name) for name in algos]
        self.iterations = []

    def run(self):
        for i in range(1, self.num_iter + 1):
            thetas = [action.sample() for action in self.actions]
            action = self.actions[np.argmax(thetas)]
            action.run()
            self.iterations.append(str(self))
            print(f'Iteration {i}: {self}')

    def save(self, out_path):
        with open(out_path, 'w') as file:
            file.write('\n'.join(self.iterations))

    def __str__(self):
        return '[' + ', '.join(f'{action}' for action in enumerate(self.actions)) + ']'


def main():
    algos = ['epl', 'bbpssw', 'dejmps']
    to_try = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # to_try = [0.2, 0.4, 0.6, 0.8, 1.0]
    for gate_fidelity in to_try:
        for entanglement_fidelity in to_try:
            print(f'Trying setup {gate_fidelity=} and {entanglement_fidelity=}')
            clean(algos)
            generate_setup(algos, gate_fidelity, entanglement_fidelity)
            master = Master(algos)
            master.run()
            save_file = f'run_g{round(gate_fidelity, 2)}_e{round(entanglement_fidelity, 2)}.txt'
            master.save(os.path.join('out', 'mba', save_file))


if __name__ == '__main__':
    main()

