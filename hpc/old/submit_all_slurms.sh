#!/bin/bash

sbatch slurm_run_dataset.peta4-icelake -n pajek_erdos_iCentral -d pajek-erdos -r 1000 -p iCentral 
sbatch slurm_run_dataset.peta4-icelake -n pajek_erdos_all -d pajek-erdos -r 1000 -p all 
sbatch slurm_run_dataset.peta4-icelake -n pajek_erdos_all -d pajek-erdos -r 1000 -p all 


sbatch slurm_run_dataset.peta4-icelake -n facebook_combined-iCentral -d facebook_combined_all -r 1000 -p all 
sbatch slurm_run_dataset.peta4-icelake -n facebook_combined-all -d facebook_combined_all -r 1000 -p all 
sbatch slurm_run_dataset.peta4-icelake -n facebook_combined-all -d facebook_combined_all -r 1000 -p all 


sbatch slurm_run_dataset.peta4-icelake -n elec-all -d elec -r 1000 -p all
sbatch slurm_run_dataset.peta4-icelake -n elec-all -d elec -r 1000 -p all
sbatch slurm_run_dataset.peta4-icelake -n elec-all -d elec -r 1000 -p all


sbatch slurm_run_dataset.peta4-icelake -n ego-facebook -d ego-facebook -r 1000 -p all
sbatch slurm_run_dataset.peta4-icelake -n ego-facebook -d ego-facebook -r 1000 -p all
sbatch slurm_run_dataset.peta4-icelake -n ego-facebook -d ego-facebook -r 1000 -p all


sbatch slurm_run_dataset.peta4-icelake -n slashdot-threads -d slashdot-threads -r 1000 -p all
sbatch slurm_run_dataset.peta4-icelake -n ego-facebook -d ego-facebook -r 1000 -p all
sbatch slurm_run_dataset.peta4-icelake -n ego-facebook -d ego-facebook -r 1000 -p all


sbatch slurm_run_dataset.peta4-icelake -n epinions-iCentral -d epinions -r 1000 -p iCentral
sbatch slurm_run_dataset.peta4-icelake -n epinions-iCentral_p -d epinions -r 1000 -p iCentral_p
sbatch slurm_run_dataset.peta4-icelake -n epinions-LeeBCC -d epinions -r 1000 -p LeeBCC

sbatch slurm_run_dataset.peta4-icelake -n email-EuAll-iCentral -d email-EuAll -r 1000 -p iCentral
sbatch slurm_run_dataset.peta4-icelake -n email-EuAll-iCentral_p -d email-EuAll -r 1000 -p iCentral_p
sbatch slurm_run_dataset.peta4-icelake -n email-EuAll-LeeBCC -d email-EuAll -r 1000 -p LeeBCC
