# Quantum entanglement protocol selection as a multi-armed bandit problem

**Author:** Jan Warchocki

*This project was done as part of the Quantum Communication and Cryptography course at Delft University of Technology.*

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

## Notes

The files `project/expert_setting.py` and `project/thompson_sampling.py` can be safely ignored. They were used in some early 
experiments or have not been finished. They are left as they could be used for future work (especially Thompson sampling, see
the paper).

All three protocols introduce extra classical communication. This is necessary for synchronization during ground truth
computation. This synchronization does not functionally change the distillation protocols and can be skipped during the 
analysis of the protocols.
