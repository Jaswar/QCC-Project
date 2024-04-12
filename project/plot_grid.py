import matplotlib.pyplot as plt  # note that matplotlib must be installed with `pip install matplotlib` in the env.
import os


def get_best_choice(lines, iteration):
    line = lines[iteration]
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


def main(iteration):
    iteration = iteration - 1 if iteration != -1 else -1
    # to_try = [0.2, 0.4, 0.6, 0.8, 1.0]
    to_try = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    alg_results = {}
    for gate_fidelity in to_try:
        for entanglement_fidelity in to_try:
            save_file = f'run_g{round(gate_fidelity, 2)}_e{round(entanglement_fidelity, 2)}.txt'
            try:
                with open(os.path.join('out', 'mba_500', save_file)) as f:
                    lines = f.read().split('\n')
                lines = [line for line in lines if line != '']
                iteration = len(lines) - 1 if iteration == -1 else iteration
                best = get_best_choice(lines, iteration)
                if best not in alg_results:
                    alg_results[best] = []
                alg_results[best].append((gate_fidelity, entanglement_fidelity))
            except FileNotFoundError as ex:
                print(f'File {save_file} not found')

    for alg in sorted(k for k in alg_results):
        xs = [x[0] for x in alg_results[alg]]
        ys = [x[1] for x in alg_results[alg]]
        plt.scatter(xs, ys, label=alg)
    plt.title(f'Best distillation algorithms (iteration={iteration + 1})')
    plt.xlabel('Gate fidelity')
    plt.ylabel('Entanglement fidelity')
    plt.legend()
    plt.savefig(os.path.join('out', f'aggregated_{iteration + 1}.png'))
    plt.show()
    plt.clf()


if __name__ == '__main__':
    for it in [1, 5, 10, 20, 50, -1]:
        main(it)


