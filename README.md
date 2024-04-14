# Quantum entanglement protocol selection as a multi-armed bandit problem

**Author:** Jan Warchocki

## Prerequisites

On top of the default libraries that come with the provided VM, `matplotlib` and `numpy` need to be installed. 
Please check the `requirements.txt` for the exact preferred versions.

It should also be possible to just create a virtual environment with this file, but this has not been tested. 

Please create directories `out` and `out/mba` in the `project` folder.

## How to run

To run the EXP3 algorithm, it is sufficient to run `python mba_setting.py` within the `project` directory 
and in the virtual environment. Please ensure that the path in line 63 is correct (should point to `out/mba`).

To plot the best selected protocol by EXP3, the script `plot_grid.py` must be run. Please ensure that 
the file path in line 79 of that script is correct (should point to `out/mba`). 

To get the ground truth expectation values (and the differences), it is sufficient to run `python ground_truth.py` in the `project` directory
in the virtual environment. This will generate plots `ground_truths.png` and `differences.png` in the `out` directory.
