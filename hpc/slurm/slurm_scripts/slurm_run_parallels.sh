#!/bin/bash

sbatch parallel-elec/slurm_run_elec-parallel-2.peta4-icelake
sbatch parallel-elec/slurm_run_elec-parallel-4.peta4-icelake
sbatch parallel-elec/slurm_run_elec-parallel-8.peta4-icelake
sbatch parallel-elec/slurm_run_elec-parallel-16.peta4-icelake
sbatch parallel-elec/slurm_run_elec-parallel-32.peta4-icelake
sbatch parallel-elec/slurm_run_elec-parallel-64.peta4-icelake
