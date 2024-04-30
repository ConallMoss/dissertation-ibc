#!/bin/bash

sbatch email-EuAll/slurm_run_email-EuAll-iCentral.peta4-icelake
sbatch email-EuAll/slurm_run_email-EuAll-LeeBCC.peta4-icelake

sbatch linux/slurm_run_linux-iCentral.peta4-icelake
sbatch linux/slurm_run_linux-LeeBCC.peta4-icelake

sbatch topology/slurm_run_topology-iCentral.peta4-icelake
sbatch topology/slurm_run_topology-LeeBCC.peta4-icelake

sbatch slashdot-threads/slurm_run_slashdot-threads-iCentral.peta4-icelake
sbatch slashdot-threads/slurm_run_slashdot-threads-LeeBCC.peta4-icelake

sbatch sx-mathoverflow/slurm_run_sx-mathoverflow-iCentral.peta4-icelake
sbatch sx-mathoverflow/slurm_run_sx-mathoverflow-LeeBCC.peta4-icelake