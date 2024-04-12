import matplotlib.pyplot as plt  # note that matplotlib must be installed with `pip install matplotlib` in the env.
import os


def is_significant(gate_fidelity, entanglement_fidelity, threshold):
    # diffs calculate using the ground_truth.py script
    diffs = [(0.1, 0.1, 0.00016112250000002715), (0.1, 0.2, 0.0003969900000000137), (0.1, 0.3, 0.000707602500000043),
             (0.1, 0.4, 0.001092960000000004), (0.1, 0.5, 0.0015530625000000353), (0.1, 0.6, 0.002087910000000026),
             (0.1, 0.7, 0.0026975025000000596), (0.1, 0.8, 0.0033818400000000803), (0.1, 0.9, 0.0041409225000000605),
             (0.1, 1.0, 0.004974749999999972), (0.2, 0.1, 0.0006278399999999906), (0.2, 0.2, 0.0015513600000000294),
             (0.2, 0.3, 0.0027705600000000052), (0.2, 0.4, 0.004285440000000029), (0.2, 0.5, 0.006096000000000046),
             (0.2, 0.6, 0.00820224), (0.2, 0.7, 0.010604160000000057), (0.2, 0.8, 0.013301760000000024),
             (0.2, 0.9, 0.016295039999999955), (0.2, 1.0, 0.019583999999999963), (0.3, 0.1, 0.0013493024999999548),
             (0.3, 0.2, 0.0033497100000000057), (0.3, 0.3, 0.006001222499999986), (0.3, 0.4, 0.009303839999999952),
             (0.3, 0.5, 0.013257562499999986), (0.3, 0.6, 0.017862390000000034), (0.3, 0.7, 0.023118322499999955),
             (0.3, 0.8, 0.02902536), (0.3, 0.9, 0.0355835025), (0.3, 1.0, 0.042792749999999935),
             (0.4, 0.1, 0.002237760000000033), (0.4, 0.2, 0.005591039999999964), (0.4, 0.3, 0.010059839999999959),
             (0.4, 0.4, 0.01564415999999999), (0.4, 0.5, 0.022343999999999947), (0.4, 0.6, 0.030159360000000024),
             (0.4, 0.7, 0.03909024), (0.4, 0.8, 0.049136639999999926), (0.4, 0.9, 0.06029856),
             (0.4, 1.0, 0.07257600000000003),
             (0.5, 0.1, 0.0031640625000000366), (0.5, 0.2, 0.007968750000000052), (0.5, 0.3, 0.014414062500000074),
             (0.5, 0.4, 0.022500000000000048), (0.5, 0.5, 0.03222656249999997), (0.5, 0.6, 0.043593750000000014),
             (0.5, 0.7, 0.05660156250000009), (0.5, 0.8, 0.07125000000000004), (0.5, 0.9, 0.08753906250000001),
             (0.5, 1.0, 0.10546874999999997), (0.6, 0.1, 0.003951360000000015), (0.6, 0.2, 0.010045439999999989),
             (0.6, 0.3, 0.018282239999999977), (0.6, 0.4, 0.02866176000000001), (0.6, 0.5, 0.04118400000000011),
             (0.6, 0.6, 0.055848960000000086), (0.6, 0.7, 0.07265664), (0.6, 0.8, 0.09160703999999992),
             (0.6, 0.9, 0.11270016),
             (0.6, 1.0, 0.13593599999999997), (0.7, 0.1, 0.004367002500000022), (0.7, 0.2, 0.011220510000000045),
             (0.7, 0.3, 0.02056052250000004), (0.7, 0.4, 0.032387040000000034), (0.7, 0.5, 0.046700062499999945),
             (0.7, 0.6, 0.06349959), (0.7, 0.7, 0.08278562249999999), (0.7, 0.8, 0.10455816000000007),
             (0.7, 0.9, 0.1288172025),
             (0.7, 1.0, 0.15556275000000003), (0.8, 0.1, 0.0041126400000000285), (0.8, 0.2, 0.010690559999999932),
             (0.8, 0.3, 0.01973375999999996), (0.8, 0.4, 0.031242240000000032), (0.8, 0.5, 0.04521599999999998),
             (0.8, 0.6, 0.061655039999999994), (0.8, 0.7, 0.08055936000000014), (0.8, 0.8, 0.10192895999999979),
             (0.8, 0.9, 0.12576384000000013), (0.8, 1.0, 0.15206399999999992), (0.9, 0.1, 0.002812522500000081),
             (0.9, 0.2, 0.007402590000000042), (0.9, 0.3, 0.013770202499999967), (0.9, 0.4, 0.02191535999999994),
             (0.9, 0.5, 0.03183806250000004), (0.9, 0.6, 0.04353830999999986), (0.9, 0.7, 0.05701610249999989),
             (0.9, 0.8, 0.07227144000000008), (0.9, 0.9, 0.08930432250000009), (0.9, 1.0, 0.10811475000000015),
             (1.0, 0.1, 0.0),
             (1.0, 0.2, 0.0), (1.0, 0.3, 0.0), (1.0, 0.4, 5.551115123125783e-17), (1.0, 0.5, 0.0), (1.0, 0.6, 0.0),
             (1.0, 0.7, 0.0), (1.0, 0.8, 0.0), (1.0, 0.9, 0.0), (1.0, 1.0, 0.0)]

    for (pg, pe, diff) in diffs:
        if pg == gate_fidelity and pe == entanglement_fidelity:
            return diff >= threshold
    return False


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


def main(iterations, threshold=0.05):
    fig, ax = plt.subplots(ncols=len(iterations), figsize=(5 * len(iterations), 5))
    for i, iteration in enumerate(iterations):
        axes = ax[i]
        iteration = iteration - 1 if iteration != -1 else -1
        # to_try = [0.2, 0.4, 0.6, 0.8, 1.0]
        to_try = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        alg_results = {}
        correct = total = 0
        for gate_fidelity in to_try:
            for entanglement_fidelity in to_try:
                if not is_significant(gate_fidelity, entanglement_fidelity, threshold):
                    continue
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
                    total += 1
                    if best == 'bbpssw' or (best == 'dejmps' and gate_fidelity == 1.0):
                        correct += 1
                except FileNotFoundError as ex:
                    print(f'File {save_file} not found')

        accuracy = round(correct / total * 100)
        for alg in sorted(k for k in alg_results):
            xs = [x[0] for x in alg_results[alg]]
            ys = [x[1] for x in alg_results[alg]]
            axes.scatter(xs, ys, label=alg)
        axes.set_title(f'{iteration + 1} iterations, accuracy={accuracy}%')
        axes.set_xlabel('Gate fidelity')
        axes.set_ylabel('Entanglement fidelity')
        axes.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join('out', f'aggregated_all.png'))
    plt.show()
    plt.clf()


if __name__ == '__main__':
    # run with threshold=0.0 for full results
    main([10, 100, -1], threshold=0.05)
