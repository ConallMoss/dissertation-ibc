#!/bin/bash

sbatch ego-facebook/slurm_run_ego-facebook-iCentral.peta4-icelake
sbatch ego-facebook/slurm_run_ego-facebook-iCentral_p.peta4-icelake
sbatch ego-facebook/slurm_run_ego-facebook-LeeBCC.peta4-icelake

sbatch pajek-erdos/slurm_run_pajek-erdos-iCentral.peta4-icelake
sbatch pajek-erdos/slurm_run_pajek-erdos-iCentral_p.peta4-icelake
sbatch pajek-erdos/slurm_run_pajek-erdos-LeeBCC.peta4-icelake

sbatch slashdot-threads/slurm_run_slashdot-threads-iCentral.peta4-icelake
sbatch slashdot-threads/slurm_run_slashdot-threads-iCentral_p.peta4-icelake
sbatch slashdot-threads/slurm_run_slashdot-threads-LeeBCC.peta4-icelake

sbatch slurm_run_email-EuAll-iCentral_p.peta4-icelake
sbatch slurm_run_email-EuAll-iCentral.peta4-icelake
sbatch slurm_run_email-EuAll-LeeBCC.peta4-icelake

sbatch slurm_run_epinions-iCentral_p.peta4-icelake
sbatch slurm_run_epinions-iCentral.peta4-icelake
sbatch slurm_run_epinions-LeeBCC.peta4-icelake

sbatch slurm_run_elec-iCentral.peta4-icelake
sbatch slurm_run_elec-iCentral_p.peta4-icelake
sbatch slurm_run_elec-LeeBCC.peta4-icelake

sbatch slurm_run_facebook_combined-iCentral.peta4-icelake
sbatch slurm_run_facebook_combined-iCentral_p.peta4-icelake
sbatch slurm_run_facebook_combined-LeeBCC.peta4-icelake