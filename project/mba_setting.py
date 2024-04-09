import os
import numpy as np
from common import run_algorithm, clean, generate_setup


class Expert(object):

    def __init__(self, name):
        self.name = name
        self.total_loss = 0

    def run(self, lr, prob):
        print(f'Running {self.name}')
        loss = -run_algorithm(self.name) / prob
        self.total_loss += lr * loss

    def __str__(self):
        return f'Agent<{self.name}, {round(self.total_loss, 4)}>'


class Master(object):

    def __init__(self, algos, num_iter=500):
        self.num_iter = num_iter
        self.experts = [Expert(name) for name in algos]
        self.probabilities = np.ones(len(self.experts)) / len(self.experts)
        self.iterations = []
        d = len(self.experts)
        self.lr = np.sqrt(2 * np.log(d) / (self.num_iter * d))
        print(f'Using {self.lr=}')

    def run(self):
        for i in range(1, self.num_iter + 1):
            index = np.random.choice([e for e in range(len(self.experts))], p=self.probabilities)
            expert, prob = self.experts[index], self.probabilities[index]
            expert.run(self.lr, prob)
            cumulative_loss = sum(np.exp(-expert.total_loss) for expert in self.experts)
            for j, expert in enumerate(self.experts):
                self.probabilities[j] = np.exp(-expert.total_loss) / cumulative_loss
            self.iterations.append(str(self))
            print(f'Iteration {i}: {self}')

    def save(self, out_path):
        with open(out_path, 'w') as file:
            file.write('\n'.join(self.iterations))

    def __str__(self):
        return '[' + ', '.join(f'{expert}: {round(self.probabilities[i], 4)}' for i, expert in enumerate(self.experts)) + ']'


def main():
    algos = ['epl', 'bbpssw', 'dejmps']
    # to_try = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    to_try = [0.2, 0.4, 0.6, 0.8, 1.0]
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

