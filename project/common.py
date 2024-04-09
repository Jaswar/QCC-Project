import subprocess
import yaml
import os
import numpy as np


def get_output(name, true_fidelity):
    with open(os.path.join(name, 'log', 'LAST', 'results.yaml')) as stream:
        try:
            loaded = yaml.safe_load(stream)
            fidelity = loaded['app_alice'][1 if true_fidelity else 0]
        except yaml.YAMLError as ex:
            print(ex)
    return fidelity


def run_algorithm(name, true_fidelity=False):
    fidelity = 0.0
    try:
        subprocess.run([f'cd {name} && netqasm simulate --formalism=dm'], shell=True, timeout=60)
        fidelity = get_output(name, true_fidelity)
    except subprocess.TimeoutExpired as ex:
        print(f'{name} expired after 30 seconds!')
    return fidelity

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