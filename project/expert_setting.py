import subprocess
import yaml
import os
import numpy as np


def get_output(name):
    with open(os.path.join(name, 'log', 'LAST', 'results.yaml')) as stream:
        try:
            loaded = yaml.safe_load(stream)
            fidelity = loaded['app_alice']
        except yaml.YAMLError as ex:
            print(ex)
    return fidelity


def run_algorithm(name):
    fidelity = 0.0
    try:
        subprocess.run([f'cd {name} && netqasm simulate --formalism=dm'], shell=True, timeout=60)
        fidelity = get_output(name)
    except subprocess.TimeoutExpired as ex:
        print(f'{name} expired after 30 seconds!')
    return fidelity


class Expert(object):

    def __init__(self, name):
        self.name = name
        self.total_loss = 0

    def run(self):
        print(f'Running {self.name}')
        loss = -run_algorithm(self.name)
        self.total_loss += loss

    def __str__(self):
        return f'Agent<{self.name}, {round(self.total_loss, 2)}>'


class Master(object):

    def __init__(self, algos, num_iter=100):
        self.num_iter = num_iter
        self.experts = [Expert(name) for name in algos]
        self.probabilities = np.ones(len(self.experts)) / len(self.experts)
        self.iterations = []

    def run(self):
        for i in range(1, self.num_iter + 1):
            for expert in self.experts:
                expert.run()
            cumulative_loss = sum(np.exp(-expert.total_loss) for expert in self.experts)
            for j, expert in enumerate(self.experts):
                self.probabilities[j] = np.exp(-expert.total_loss) / cumulative_loss
            self.iterations.append(str(self))
            print(f'Iteration {i}: {self}')

    def save(self, out_path):
        with open(out_path, 'w') as file:
            file.write('\n'.join(self.iterations))

    def __str__(self):
        return '[' + ', '.join(f'{expert}: {round(self.probabilities[i], 2)}' for i, expert in enumerate(self.experts)) + ']'


def clean(algos):
    for alg in algos:
        subprocess.run(f"rm -r {os.path.join(alg, 'log')}", shell=True)


def generate_setup(algos, gate_fidelity, entanglement_fidelity):
    for alg in algos:
        with open(os.path.join(alg, 'network.yaml')) as stream:
            try:
                loaded = yaml.safe_load(stream)
                for node in loaded['nodes']:
                    node['gate_fidelity'] = float(gate_fidelity)
                for link in loaded['links']:
                    link['fidelity'] = float(entanglement_fidelity)
            except yaml.YAMLError as ex:
                print(ex)

        with open(os.path.join(alg, 'network.yaml'), 'w') as stream:
            yaml.dump(loaded, stream)


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
            master.save(os.path.join('out', 'expert', save_file))


if __name__ == '__main__':
    main()

