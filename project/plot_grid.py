import matplotlib.pyplot as plt  # note that matplotlib must be installed with `pip install matplotlib` in the env.
import os


def get_best_choice(lines):
    line = lines[-1]
    line = line[1:-1]
    line = line.replace('Agent', '').replace('<', '').replace('>', '')
    split = line.split(',')
    results = []
    for i in range(0, len(split), 2):
        alg = split[i].strip()
        result = split[i + 1].strip()
        prob = float(result.split(': ')[-1])
        results.append((alg, prob))
    results = sorted(results, key=lambda x: x[1], reverse=True)
    return results[0][0]


def main():
    to_try = [0.2, 0.4, 0.6, 0.8, 1.0]
    alg_results = {}
    for gate_fidelity in to_try:
        for entanglement_fidelity in to_try:
            save_file = f'run_g{round(gate_fidelity, 2)}_e{round(entanglement_fidelity, 2)}.txt'
            with open(os.path.join('out', 'mba', save_file)) as f:
                lines = f.read().split('\n')
            lines = [line for line in lines if line != '']
            best = get_best_choice(lines)
            if best not in alg_results:
                alg_results[best] = []
            alg_results[best].append((gate_fidelity, entanglement_fidelity))

    for alg in alg_results:
        xs = [x[0] for x in alg_results[alg]]
        ys = [x[1] for x in alg_results[alg]]
        plt.scatter(xs, ys, label=alg)
    plt.title('Best distillation algorithms')
    plt.xlabel('Gate fidelity')
    plt.ylabel('Entanglement fidelity')
    plt.legend()
    plt.savefig(os.path.join('out', 'aggregated.png'))
    plt.show()


if __name__ == '__main__':
    main()


