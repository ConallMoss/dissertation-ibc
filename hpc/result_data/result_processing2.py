# %%
import matplotlib.pyplot as plt
import numpy as np

# %%
def read_results(dataset, alg,run="run1"):
    with open(f"./{run}/slurm_results/{dataset}/{dataset}-{alg}.txt") as f:
        x = f.read()
    return x

# %%
def get_stats(dataset, alg, run, max_results=100):
    raw_results = read_results(dataset=dataset, alg=alg, run=run)
    a = raw_results.split("Run times:\n")
    init_mem = float(a[0].split("\nM: ")[1].replace('\n', ''))

    blocks = a[1].split("\n\n")[0:max_results+10]
    stats = []
    for block in blocks:
        d = {}
        items = [i.split(": ") for i in block.split("\n")]
        for item in items:
            d[item[0]] = float(item[1])
        if set(d.keys()) == {'M', 'RS', 'T'}:
            stats.append(d)

    return stats, init_mem
# %%
def process_stats(stats, init_mem):
    pass
