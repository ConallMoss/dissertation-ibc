# %%
import matplotlib.pyplot as plt
import numpy as np

# %%
def read_results(dataset, alg,run="run1"):
    with open(f"./{run}/slurm_results/{dataset}/{dataset}-{alg}.txt") as f:
        x = f.read()
    return x

# %%
def get_stats(dataset, alg, run, max_results=200):
    raw_results = read_results(dataset=dataset, alg=alg, run=run)
    a = raw_results.split("Run times:\n")
    init_mem = float(a[0].split("\nM: ")[1].replace('\n', ''))

    blocks = a[1].split("\n\n")[0:max_results]
    stats = []
    for i, block in enumerate(blocks):
        d = {}
        items = [i.split(": ") for i in block.split("\n")]
        for item in items:
            if len(item) == 1:
                continue
            d[item[0]] = float(item[1])
        if set(d.keys()) != {'M', 'RS', 'T'} and i != max_results-1:
            print("aaa")
            continue
        stats.append(d)

    return stats, init_mem

def flip_stats(stats):
    d = {
        'RS': [],
        'T': [],
        'M': []
    }
    for stat in stats:
        for k in ["RS", "T", "M"]:
            d[k].append(stat[k])
    return d
# %%
def mean_dev(data):
    data = np.array(data)
    m = np.mean(data)
    s = np.std(data)
    return m, s

def get_dataset_info(dataset, run, max_results=200):
    algs = ("iCentral", "iCentral_p", "LeeBCC")
    stats_dict = {}
    init_mems = {}
    lens = {}
    for alg in  algs:
        stats, init_mem = get_stats(dataset, alg, run, max_results)
        stats_dict[alg] = flip_stats(stats)
        init_mems[alg] = init_mem
        lens[alg] = len(stats)
    
    if len({lens[alg] for alg in algs}) != 1:
        print("len mismatch")

    alg_means = {} #alg -> mean
    alg_stdevs = {} #alg -> stdev
    base_comps = [] #list[comps]
    par_comps = [] #list[comps]
    base_comp_mean = 0 #comp_type -> mean
    base_comp_stdev = 0 #comp_type -> stdev

    

    for alg in algs:
        m, s = mean_dev(stats_dict[alg]['T'])
        alg_means[alg] = m
        alg_stdevs[alg] = s
    
    #* Lee vs. iCentral
    for lee, icen, icen_p in zip(stats_dict["LeeBCC"]["T"], stats_dict["iCentral"]["T"], stats_dict["iCentral_p"]["T"]):
        base_comps.append(lee/icen)
        par_comps.append(icen/icen_p)
    
    m, s = mean_dev(base_comps)
    base_comp_mean = m
    base_comp_stdev = s
    m, s = mean_dev(par_comps)
    par_comp_mean = m
    par_comp_mean = s

    mem_means = {}
    mem_stdevs = {}
    for alg in algs:
        m, s = mean_dev([i-init_mems[alg] for i in stats_dict[alg]['M']])
        mem_means[alg] = m
        mem_stdevs[alg] = s

    return lens






    

#* Results we want to get:
#* - Mean/dev of each algorithm
#* - mean/dev of LeeBCC/iCentral, iCentral/iCentral_p
#* - mean memory usage of each

# %%
datasets = ("chess", "elec", "email-EuAll", "facebook-combined", "linux", "pajek-erdos", "slashdot-threads", "sx-mathoverflow", "topology", "wikispeedia")
algs = ("iCentral", "LeeBCC", "iCentral_p")
# %%
#* test
stats, i = get_stats("chess", "iCentral", "run5_lcc")
# %%
