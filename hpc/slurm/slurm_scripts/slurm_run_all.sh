#!/bin/bash

sbatch slurm_run_ego-facebook-all.peta4-icelake
sbatch slurm_run_pajek_erdos_all.peta4-icelake
sbatch slurm_run_slashdot-threads-all.peta4-icelake

sbatch slurm_run_email-EuAll-iCentral_p.peta4-icelake
sbatch slurm_run_email-EuAll-iCentral.peta4-icelake
sbatch slurm_run_email-EuAll-LeeBCC.peta4-icelake

sbatch slurm_run_epinions-iCentral_p.peta4-icelake
sbatch slurm_run_epinions-iCentral.peta4-icelake
sbatch slurm_run_epinions-LeeBCC.peta4-icelake

sbatch slurm_run_elec-iCentral.peta4-icelake
sbatch slurm_run_elec-iCentral_p.peta4-icelake
sbatch slurm_run_elec-LeeBCC.peta4-icelake

sbatch slurm_run_facebook_combined_iCentral.peta4-icelake
sbatch slurm_run_facebook_combined_iCentral_p.peta4-icelake
sbatch slurm_run_facebook_combined_LeeBCC.peta4-icelake