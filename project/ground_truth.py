from common import run_algorithm, clean, generate_setup
import matplotlib.pyplot as plt
import os


def main():
    algos = ['dejmps', 'bbpssw', 'epl']
    results = {}
    for alg in algos:
        results[alg] = []

    to_try = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # to_try = [0.2, 0.4, 0.6, 0.8, 1.0]
    for gate_fidelity in to_try:
        for entanglement_fidelity in to_try:
            print(f'Trying setup {gate_fidelity=} and {entanglement_fidelity=}')
            clean(algos)
            generate_setup(algos, gate_fidelity, entanglement_fidelity)
            fidelities = []
            for alg in algos:
                print(f'Running {alg}')
                fidelity = run_algorithm(alg, true_fidelity=True)
                fidelities.append((alg, fidelity))
            best_alg = max(fidelities, key=lambda pair: pair[1])[0]
            results[best_alg].append([gate_fidelity, entanglement_fidelity])

    for alg in sorted(k for k in results):
        xs = [x[0] for x in results[alg]]
        ys = [x[1] for x in results[alg]]
        plt.scatter(xs, ys, label=alg)
    plt.xlabel('Gate fidelity')
    plt.ylabel('Entanglement fidelity')
    plt.legend()
    plt.savefig(os.path.join('out', f'ground_truth.png'))
    plt.clf()


if __name__ == '__main__':
    main()
