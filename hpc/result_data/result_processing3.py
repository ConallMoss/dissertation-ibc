# %%
import matplotlib.pyplot as plt
import numpy as np

# %%
def read_results(dataset, alg,run="run1"):
    with open(f"./{run}/slurm_results/{dataset}/{dataset}-{alg}.txt") as f:
        x = f.read()
    return x

def get_stats(dataset, alg, run, max_results=100, run2=None):
    raw_results = read_results(dataset=dataset, alg=alg, run=run)
    a = raw_results.split("Run times:\n")
    init_mem = float(a[0].split("\nM: ")[1].replace('\n', ''))

    blocks = a[1].split("\n\n")[0:max_results]

    if run2 is not None:
        raw_results2 = read_results(dataset=dataset, alg=alg, run=run2)
        a2 = raw_results2.split("Run times:\n")
        #init_mem = float(a[0].split("\nM: ")[1].replace('\n', ''))
        blocks += a2[1].split("\n\n")[0:max_results]

    stats = []
    for i, block in enumerate(blocks):
        d = {}
        items = [i.split(": ") for i in block.split("\n")]

        for item in items:
            if len(item) == 1:
                continue
            if item[0] == "E":
                continue
            d[item[0]] = float(item[1])
        if set(d.keys()) != {'M', 'RS', 'T'} and i != max_results-1:
            continue
        stats.append(d)

    fstats = {
        'RS': [],
        'T': [],
        'M': [],
    }
    for stat in stats:
        for k in ["RS", "T", "M"]:
            fstats[k].append(stat[k])
    
    return {k: np.array(fstats[k]) for k in ["RS", "T", "M"]}, init_mem

def get_stats_edge(dataset, alg, run, max_results=100, run2=None):
    raw_results = read_results(dataset=dataset, alg=alg, run=run)
    a = raw_results.split("Run times:\n")
    init_mem = float(a[0].split("\nM: ")[1].replace('\n', ''))

    blocks = a[1].split("\n\n")[0:max_results]

    if run2 is not None:
        raw_results2 = read_results(dataset=dataset, alg=alg, run=run)
        a2 = raw_results.split("Run times:\n")
        #init_mem = float(a[0].split("\nM: ")[1].replace('\n', ''))
        blocks += a[1].split("\n\n")[0:max_results]

    stats = []
    for i, block in enumerate(blocks):
        d = {}
        items = [i.split(": ") for i in block.split("\n")]

        for item in items:
            if len(item) == 1:
                continue
            if item[0] != "E":
                d[item[0]] = float(item[1])
            else:
                d[item[0]] = item[1]
        if set(d.keys()) != {'M', 'RS', 'T', 'E'} and i != max_results-1:
            continue
        stats.append(d)

    fstats = {
        'RS': [],
        'T': [],
        'M': [],
        'E': []
    }
    for stat in stats:
        for k in ["RS", "T", "M", "E"]:
            fstats[k].append(stat[k])
    
    return fstats


def get_dataset_stats(dataset, run, max_results, run2=None):
    algs = ("iCentral", "iCentral_p", "LeeBCC")
    
    iCentral_stats, iCentral_mem = get_stats(dataset, "iCentral", run, max_results, run2)
    LeeBCC_stats, LeeBCC_mem = get_stats(dataset, "LeeBCC", run, max_results, run2)
    iCentral_p_stats, iCentral_p_mem = get_stats(dataset, "iCentral_p", run, max_results)

    iCentral_times = iCentral_stats["T"]
    LeeBCC_times = LeeBCC_stats["T"]
    iCentral_p_times = iCentral_p_stats["T"]

    lens = [len(i) for i in [iCentral_times, LeeBCC_times, iCentral_p_times]]
    print(dataset)
    print(lens)
    max_len = min(lens)

    

    iCentral_times = iCentral_times[:max_len]
    LeeBCC_times = LeeBCC_times[:max_len]
    iCentral_p_times = iCentral_p_times[:max_len]

    iCentral_mem = iCentral_stats["M"][:max_len]
    LeeBCC_mem = LeeBCC_stats["M"][:max_len]
    iCentral_p_mem = iCentral_p_stats["M"][:max_len]

    iCentral_mean, iCentral_stdev = np.mean(iCentral_times), np.std(iCentral_times)
    LeeBCC_mean, LeeBCC_stdev = np.mean(LeeBCC_times), np.std(LeeBCC_times)
    iCentral_p_mean, iCentral_p_stdev = np.mean(iCentral_p_times), np.std(iCentral_p_times)

    base_comp = np.divide(LeeBCC_times, iCentral_times)
    parallel_comp = np.divide(iCentral_times, iCentral_p_times)

    base_comp_mean, base_comp_stdev = np.mean(base_comp), np.std(base_comp)
    parallel_comp_mean, parallel_comp_stdev = np.mean(parallel_comp), np.std(parallel_comp)

    iCentral_mem_mean, iCentral_mem_stdev = np.mean(iCentral_mem), np.std(iCentral_mem)
    LeeBCC_mem_mean, LeeBCC_mem_stdev = np.mean(LeeBCC_mem), np.std(LeeBCC_mem)
    iCentral_p_mem_mean, iCentral_p_mem_stdev = np.mean(iCentral_p_mem), np.std(iCentral_p_mem)
    

    alg_time_stats = {
        "iCentral": (iCentral_mean, iCentral_stdev),
        "LeeBCC": (LeeBCC_mean, LeeBCC_stdev),
        "iCentral_p": (iCentral_p_mean, iCentral_p_stdev),
        "base_comp": (base_comp_mean, base_comp_stdev),
        "parallel_comp": (parallel_comp_mean, parallel_comp_stdev),
        "iCentral_mem": (iCentral_mem_mean, iCentral_mem_stdev),
        "LeeBCC_mem": (LeeBCC_mem_mean, LeeBCC_mem_stdev),
        "iCentral_p_mem": (iCentral_p_mem_mean, iCentral_p_mem_stdev)
    }

    return alg_time_stats

def plot_times(dataset_stats, graph_datasets):
    algs = ("iCentral", "LeeBCC", "iCentral_p")
    r = np.arange(len(graph_datasets))
    bar_width = 0.2
    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0] for dataset in graph_datasets]
        stdevs = [dataset_stats[dataset][alg][1] for dataset in graph_datasets]
        plt.bar(r + i * bar_width, means, yerr=stdevs, width=bar_width, label=alg, color=alg_cols[alg], capsize=5)

    plt.xlabel('Dataset', fontweight='bold')
    plt.ylabel('Mean', fontweight='bold')
    plt.title('Mean and Standard Deviation for Algorithms by Dataset')
    plt.xticks(r + bar_width, graph_datasets)
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_base_comp(dataset_stats, graph_datasets):
    comp = "base_comp"
    r = np.arange(len(graph_datasets))
    bar_width = 0.3
    means = [dataset_stats[dataset][comp][0] for dataset in graph_datasets]
    stdevs = [dataset_stats[dataset][comp][1] for dataset in graph_datasets]
    plt.bar(r+bar_width, means, yerr=stdevs, width=bar_width, label=comp, color=alg_cols[comp], capsize=2.5)

    plt.xlabel('Dataset', fontweight='bold')
    plt.ylabel('Mean', fontweight='bold')
    plt.title('Mean and Standard Deviation for Algorithms by Dataset')
    plt.xticks(r + bar_width, graph_datasets)
    plt.legend()

    plt.tight_layout()
    plt.show()

# %%
def plot_relative_times_old(dataset_stats, graph_datasets):
    
    algs = ("iCentral", "LeeBCC")
    r = np.arange(len(graph_datasets))
    bar_width = 0.3
    plt.style.use('seaborn-v0_8-white')
    #csfont = {'fontname':'Times New Roman'}
    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0]/dataset_stats[dataset]["iCentral"][0] for dataset in graph_datasets]
        stdevs = [dataset_stats[dataset][alg][1]/dataset_stats[dataset]["iCentral"][0] for dataset in graph_datasets]
        plt.bar(r + i * bar_width, means, yerr=stdevs, width=bar_width, label=alg, color=alg_cols[alg], capsize=5)
    plt.axhline(y = 1, color = 'k', linestyle = '--') 
    plt.xlabel('Dataset', fontweight='bold')
    plt.ylabel('Mean', fontweight='bold')
    plt.title('Mean and Standard Deviation for Algorithms by Dataset')
    plt.xticks(r + bar_width, graph_datasets)
    plt.legend()
    fig = plt.figure()
    
    plt.savefig("test2.pdf", format="png", bbox_inches="tight")
    #plt.tight_layout()
    plt.show()

#plot_relative_times(dataset_stats, datasets_big)

# %%
def plot_relative_times2(dataset_stats, graph_datasets, algs, base):
    
    num_datasets = len(graph_datasets)
    num_algorithms = len(algs)

    barWidth = 0.35

    r = np.arange(num_datasets)
    #plt.style.use('seaborn-v0_8-white')
    # Create bars
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0]/dataset_stats[dataset][base][0] for dataset in graph_datasets]
        std_devs = [dataset_stats[dataset][alg][1]/dataset_stats[dataset][base][0] for dataset in graph_datasets]
        
        ax.bar(r + i * barWidth, means, yerr=std_devs, width=barWidth, label=alg, capsize=5, color=alg_cols[alg], ecolor="black", capstyle="butt", error_kw={"elinewidth": 2, "capsize": 5, 'markeredgewidth':1})

    # Add horizontal line at y=0
    ax.axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    # Add labels, title and legend
    ax.set_xlabel('Dataset', fontweight='bold', fontsize=16)
    ax.set_ylabel('Mean', fontweight='bold', fontsize=16)
    ax.set_title('Mean and Standard Deviation for Algorithms by Dataset', fontweight='bold', fontsize=20)
    ax.set_xticks(r + (barWidth * num_algorithms) / 2 - 0.1) 
    ax.set_xticklabels(graph_datasets, rotation=30, ha='right', fontsize=14)
    for label in ax.get_yticklabels():
        label.set_fontsize(14)
    ax.legend(fontsize=14)

    # Adjust layout and save plot
    plt.margins(0.05)  # Reduce extra margin
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin
    plt.tight_layout()
    plt.savefig('bar_chart.png', dpi=300)
    plt.show()


#plot_relative_times2(dataset_stats, datasets2, algs = ("iCentral", "LeeBCC"))
#plot_relative_times2(dataset_stats, datasets2, algs = ("iCentral", "iCentral_p"))
#plot_relative_times2(dataset_stats, datasets, algs = ("iCentral_mem", "LeeBCC_mem"))


# %%
datasets = ("chess", "elec", "email-EuAll", "facebook-combined", "linux", "pajek-erdos", "slashdot-threads", "sx-mathoverflow", "topology", "wikispeedia")
datasets = ("email-EuAll", "linux", "topology", "sx-mathoverflow", "slashdot-threads", "chess",  "elec",  "facebook-combined", "wikispeedia", "pajek-erdos")
datasets2 = ("email-EuAll", "linux", "slashdot-threads", "sx-mathoverflow", "topology", "elec", "chess", "wikispeedia", "pajek-erdos")

algs = ("iCentral", "iCentral_p", "LeeBCC")
runs = ("run7_lcc")

alg_cols3 = {
    "iCentral": "#e41a1c",
    "LeeBCC": "#377eb8",
    "iCentral_p": "#4daf4a",
    "base_comp": "#984ea3",
    "parallel_comp": "#ff7f00",
    "iCentral_mem": "#e41a1c",
    "LeeBCC_mem": "#377eb8",
    "iCentral_p_mem": "#4daf4a",
}

alg_cols2 = {
    "iCentral": "#1b9e77",
    "LeeBCC": "#d95f02",
    "iCentral_p": "#7570b3",
    "base_comp": "#decbe4",
    "parallel_comp": "#fed9a6",
    "iCentral_mem": "#e41a1c",
    "LeeBCC_mem": "#377eb8",
    "iCentral_p_mem": "#4daf4a",
}

alg_cols4 = {
    "iCentral": "#FF9F9B",
    "LeeBCC": "#A1C9F4",
    "iCentral_p": "#8DE5A1",
    "base_comp": "#decbe4",
    "parallel_comp": "#fed9a6",
    "iCentral_mem": "#e41a1c",
    "LeeBCC_mem": "#377eb8",
    "iCentral_p_mem": "#4daf4a",
}

alg_cols = {
    "iCentral": "#C44E52",
    "LeeBCC": "#4C72B0",
    "iCentral_p": "#55A868",
    "base_comp": "#decbe4",
    "parallel_comp": "#fed9a6",
    "iCentral_mem": "#e41a1c",
    "LeeBCC_mem": "#377eb8",
    "iCentral_p_mem": "#4daf4a",
}

alg_cols = {
    "iCentral": "#D65F5F",
    "LeeBCC": "#4878D0",
    "iCentral_p": "#6ACC64",
    "base_comp": "#decbe4",
    "parallel_comp": "#fed9a6",
    "iCentral_mem": "#C44E52",
    "LeeBCC_mem": "#4C72B0",
    "iCentral_p_mem": "#55A868",
}


# dataset_stats = {}
# for d in datasets:
#     dataset_stats[d] = get_dataset_stats(d, "run5_lcc", 200) 


# # %%
# plot_times(dataset_stats, datasets)

# # %%
# datasets_big = ("email-EuAll", "linux",  "slashdot-threads", "sx-mathoverflow", "topology") #larger
# datasets_small = ("chess", "elec", "facebook-combined", "pajek-erdos", "wikispeedia") #small


# plot_times(dataset_stats, datasets_big)
# plot_times(dataset_stats, datasets_small)
# # %%
# datasets_1 = ("email-EuAll", "linux")
# datasets_2 = ("slashdot-threads", "sx-mathoverflow", "topology")
# datasets_3 = ("chess", "elec", "wikispeedia") 
# datasets_4 = ("facebook-combined", "pajek-erdos")

# plot_times(dataset_stats, datasets_1)
# plot_times(dataset_stats, datasets_2)
# plot_times(dataset_stats, datasets_3)
# plot_times(dataset_stats, datasets_4)

# # %%
# #removed facebook combined, sx-mathoverflow
# datasets2 = ("chess", "elec", "email-EuAll", "linux", "pajek-erdos", "slashdot-threads", "topology", "wikispeedia")

# plot_base_comp(dataset_stats, datasets2)
# # %%
# plot_relative_times_old(dataset_stats, datasets2)
# # %%
# plot_times(dataset_stats, datasets_big)
# # %%

# %%

#! -------------------------

def plot_relative_times(dataset_stats, graph_datasets, algs, base, name="test"):
    
    num_datasets = len(graph_datasets)
    num_algorithms = len(algs)

    barWidth = 0.35

    r = np.arange(num_datasets)
    #plt.style.use('seaborn-v0_8-white')
    # Create bars
    fig, ax = plt.subplots(figsize=(10, 6))
    def alg_name(a):
        if a == "LeeBCC":
            return "Lee-BCC"
        else:
            return a
    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0]/dataset_stats[dataset][base][0] for dataset in graph_datasets]
        std_devs = [dataset_stats[dataset][alg][1]/dataset_stats[dataset][base][0] for dataset in graph_datasets]
        
        ax.bar(r + i * barWidth, means, yerr=std_devs, width=barWidth, label=alg_rename[alg], capsize=5, color=alg_cols[alg], ecolor="black", capstyle="butt", error_kw={"elinewidth": 2, "capsize": 5, 'markeredgewidth':1})

    # Add horizontal line at y=0
    ax.axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    # Add labels, title and legend
    ax.set_xlabel('Dataset', fontweight=550, fontsize=14)
    ax.set_ylabel('Scaled Mean', fontweight=550, fontsize=14)
    ax.set_title('Average Running Time (Scaled)', fontweight='bold', fontsize=16, pad=15)
    ax.set_xticks(r + (barWidth * (num_algorithms-1)) / 2) 
    ax.set_xticklabels(graph_datasets, rotation=30, ha='right', fontsize=12)
    for label in ax.get_yticklabels():
        label.set_fontsize(12)
    ax.legend(fontsize=12)

    # Adjust layout and save plot
    plt.margins(0.05)  # Reduce extra margin
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin
    plt.tight_layout()
    plt.savefig(name, dpi=300)
    plt.show()


#plot_relative_times(dataset_stats, datasets2, algs = ("LeeBCC", "iCentral"), base="LeeBCC")

def plot_real_times(dataset_stats, graph_datasets, name="test"):
    algs = ("LeeBCC", "iCentral", "iCentral_p")
    num_datasets = len(graph_datasets)
    num_algorithms = len(algs)

    barWidth = 0.2

    r = np.arange(num_datasets)
    #plt.style.use('seaborn-v0_8-white')
    # Create bars
    fig, ax = plt.subplots(figsize=(10, 6))
    def alg_name(a):
        if a == "LeeBCC":
            return "Lee-BCC"
        else:
            return a
        
    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0] for dataset in graph_datasets]
        std_devs = [dataset_stats[dataset][alg][1] for dataset in graph_datasets]
        
        ax.bar(r + i * barWidth, means, yerr=std_devs, width=barWidth, label=alg_rename[alg], capsize=5, color=alg_cols[alg], ecolor="black", capstyle="butt", error_kw={"elinewidth": 2, "capsize": 5, 'markeredgewidth':1})

    # Add horizontal line at y=0
    #ax.axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    # Add labels, title and legend
    ax.set_xlabel('Dataset', fontweight=550, fontsize=14)
    ax.set_ylabel('Mean runtime (s)', fontweight=550, fontsize=14)
    ax.set_title('Average Algorithm Running Times', fontweight='bold', fontsize=16, pad=15)
    ax.set_xticks(r + (barWidth * num_algorithms) / 2 - 0.1) 
    ax.set_xticklabels(graph_datasets, rotation=30, ha='right', fontsize=12)
    for label in ax.get_yticklabels():
        label.set_fontsize(12)
    ax.legend(fontsize=12)

    # Adjust layout and save plot
    plt.margins(0.05)  # Reduce extra margin
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin
    plt.tight_layout()
    plt.savefig(name, dpi=300)
    plt.show()

def plot_real_mems(dataset_stats, graph_datasets, name="test"):
    algs = ("LeeBCC_mem", "iCentral_mem", "iCentral_p_mem")
    num_datasets = len(graph_datasets)
    num_algorithms = len(algs)

    barWidth = 0.2

    r = np.arange(num_datasets)
    #plt.style.use('seaborn-v0_8-white')
    # Create bars
    fig, ax = plt.subplots(figsize=(10, 6))
    alg_name = {"iCentral_mem": "iCentral", "LeeBCC_mem":"LeeBCC", "iCentral_p_mem":"iCentral_p"}
        
    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0] for dataset in graph_datasets]
        std_devs = [dataset_stats[dataset][alg][1] for dataset in graph_datasets]
        
        ax.bar(r + i * barWidth, means, yerr=std_devs, width=barWidth, label=alg_rename[alg], capsize=5, color=alg_cols[alg], ecolor="black", capstyle="butt", error_kw={"elinewidth": 2, "capsize": 5, 'markeredgewidth':1})

    # Add horizontal line at y=0
    #ax.axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    # Add labels, title and legend
    ax.set_xlabel('Dataset', fontweight=550, fontsize=14)
    ax.set_ylabel('Mean memory usage (MB)', fontweight=550, fontsize=14)
    ax.set_title('Average Algorithm Memory Usage', fontweight='bold', fontsize=16, pad=15)
    ax.set_xticks(r + (barWidth * num_algorithms) / 2 - 0.1) 
    ax.set_xticklabels(graph_datasets, rotation=30, ha='right', fontsize=12)
    for label in ax.get_yticklabels():
        label.set_fontsize(12)
    ax.legend(fontsize=12)

    # Adjust layout and save plot
    plt.margins(0.05)  # Reduce extra margin
    plt.subplots_adjust(bottom=0.1, left=0.1)  # Adjust bottom margin
    plt.tight_layout()
    plt.savefig(name, dpi=300)
    plt.show()

def plot_relative_mems(dataset_stats, graph_datasets, algs, base, name="test"):
    
    num_datasets = len(graph_datasets)
    num_algorithms = len(algs)

    barWidth = 0.35
    alg_name = {"iCentral_mem": "iCentral", "LeeBCC_mem":"LeeBCC", "iCentral_p_mem":"iCentral_p"}
    r = np.arange(num_datasets)
    #plt.style.use('seaborn-v0_8-white')
    # Create bars
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0]/dataset_stats[dataset][base][0] for dataset in graph_datasets]
        std_devs = [dataset_stats[dataset][alg][1]/dataset_stats[dataset][base][0] for dataset in graph_datasets]
        
        ax.bar(r + i * barWidth, means, yerr=std_devs, width=barWidth, label=alg_rename[alg], capsize=5, color=alg_cols[alg], ecolor="black", capstyle="butt", error_kw={"elinewidth": 2, "capsize": 5, 'markeredgewidth':1})

    # Add horizontal line at y=0
    ax.axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    # Add labels, title and legend
    ax.set_xlabel('Dataset', fontweight=550, fontsize=14)
    ax.set_ylabel('Scaled Mean', fontweight=550, fontsize=14)
    ax.set_title('Average Memory Usage (Scaled)', fontweight='bold', fontsize=16, pad=15)
    ax.set_xticks(r + (barWidth * (num_algorithms-1) / 2 )) 
    ax.set_xticklabels(graph_datasets, rotation=30, ha='right', fontsize=12)
    for label in ax.get_yticklabels():
        label.set_fontsize(12)
    ax.legend(loc=1, fontsize=12)

    # Adjust layout and save plot
    plt.margins(y=0.2)  # Reduce extra margin
    plt.subplots_adjust(bottom=0.1, left=0.1)  # Adjust bottom margin
    plt.tight_layout()
    plt.savefig(name, dpi=300)
    plt.show()


# %%

#datasets = ("email-EuAll", "linux", "topology", "sx-mathoverflow", "slashdot-threads", "chess",  "elec",  "facebook-combined", "wikispeedia", "pajek-erdos")
#datasets = ("email-EuAll", "linux", "topology", "sx-mathoverflow", "slashdot-threads", "chess",  "elec",  "wikispeedia")
datasets = ("email-EuAll", "slashdot-threads", "linux", "sx-mathoverflow", "topology", "elec", "chess", "wikispeedia")
datasets_big = ("email-EuAll", "slashdot-threads", "linux", "sx-mathoverflow", "topology",)
datasets_small = ("elec", "chess", "wikispeedia")

algs = ("iCentral", "iCentral_p", "LeeBCC")
run = "run7_lcc"

datasets_run2 = {"email-EuAll", "linux", "topology", "sx-mathoverflow", "slashdot-threads"}
run2 = "run9_extras"

dataset_stats = {}

for d in datasets:
    if d in datasets_run2:
        dataset_stats[d] = get_dataset_stats(d, run, 100, run2) 
    else:
        dataset_stats[d] = get_dataset_stats(d, run, 100)

alg_rename = {
    "iCentral": "iCentral",
    "LeeBCC": "Lee-BCC",
    "iCentral_p": "Parallel iCentral",
    "iCentral_mem": "iCentral",
    "LeeBCC_mem": "Lee-BCC",
    "iCentral_p_mem": "Parallel iCentral"
}    

# %%
plot_real_times(dataset_stats, datasets_big, name="figs/real_times_big.pdf")
# %%
plot_real_times(dataset_stats, datasets_small, name="figs/real_times_small.pdf")
# %%
plot_relative_times(dataset_stats, datasets, algs = ("LeeBCC", "iCentral"), base="LeeBCC", name="figs/rel_times_lee.pdf")
# %%
plot_relative_times(dataset_stats, datasets, algs = ("iCentral", "iCentral_p"), base="iCentral_p", name="figs/rel_times_para.pdf")
# %%
plot_real_mems(dataset_stats, datasets_big, name="figs/real_mems_big.pdf")
# %%
plot_real_mems(dataset_stats, datasets_small, name="figs/real_mems_small.pdf")

# %%
plot_relative_mems(dataset_stats, datasets, algs = ("LeeBCC_mem", "iCentral_mem"), base="LeeBCC_mem", name="figs/rel_mems_lee.pdf")
# %%
plot_relative_mems(dataset_stats, datasets, algs = ("iCentral_mem", "iCentral_p_mem"), base="iCentral_mem", name="figs/rel_mems_para.pdf")
# %%


# x = []
# for d in datasets:
#     x.append(dataset_stats[d]["LeeBCC"][0]/dataset_stats[d]["iCentral"][0])
x= [dataset_stats[d]["LeeBCC"][0]/dataset_stats[d]["iCentral"][0] for d in datasets]
print(sum(x)/len(x))

# %%
x= [dataset_stats[d]["iCentral"][0]/dataset_stats[d]["iCentral_p"][0] for d in datasets]
print(sum(x)/len(x))
# %%
x = []
for d in datasets:
    print(d)
    print(dataset_stats[d]["iCentral"][1])
    print(dataset_stats[d]["LeeBCC"][1])
    print(dataset_stats[d]["LeeBCC"][1]/dataset_stats[d]["iCentral"][1])
    x.append(dataset_stats[d]["iCentral"][1]/dataset_stats[d]["LeeBCC"][1])
# %%
dataset_bccperc = {
    "email-EuAll":0.16,
    "linux":0.90,
    "topology":0.679,
    "sx-mathoverflow":0.755,
    "slashdot-threads":0.382,
    "chess":0.878,
    "elec":0.677,
    "wikispeedia":0.982,
}

dataset_degree = {
    "email-EuAll":2.77,
    "linux":13.86,
    "topology":6.197,
    "sx-mathoverflow":16.11,
    "slashdot-threads":4.60,
    "chess":15.31,
    "elec":28.31,
    "wikispeedia":24.17,
}

graphs_data = {
    "email-EuAll": {
        "Nodes": 265214,
        "Edges": 365570,
        "LCC": {
            "Nodes": 224832,
            "Edges": 339925
        },
        "BCC": {
            "Nodes": 36106,
            "Edges": 151162
        },
        "Nodes_BCC_LCC": 0.16059101907201823,
        "Average_vertex_degree": 2.7567926278401593
    },
    "linux": {
        "Nodes": 30837,
        "Edges": 213747,
        "LCC": {
            "Nodes": 30817,
            "Edges": 213208
        },
        "BCC": {
            "Nodes": 27876,
            "Edges": 210197
        },
        "Nodes_BCC_LCC": 0.90456566181004,
        "Average_vertex_degree": 13.863021694717386
    },
    "topology": {
        "Nodes": 34761,
        "Edges": 107720,
        "LCC": {
            "Nodes": 34761,
            "Edges": 107720
        },
        "BCC": {
            "Nodes": 23592,
            "Edges": 96497
        },
        "Nodes_BCC_LCC": 0.6786916371795978,
        "Average_vertex_degree": 6.197750352406432
    },
    "sx-mathoverflow": {
        "Nodes": 24818,
        "Edges": 199973,
        "LCC": {
            "Nodes": 24668,
            "Edges": 187939
        },
        "BCC": {
            "Nodes": 18627,
            "Edges": 181884
        },
        "Nodes_BCC_LCC": 0.7551078320090806,
        "Average_vertex_degree": 16.115158352808447
    },
    "slashdot-threads": {
        "Nodes": 51083,
        "Edges": 117378,
        "LCC": {
            "Nodes": 51083,
            "Edges": 116573
        },
        "BCC": {
            "Nodes": 19506,
            "Edges": 84950
        },
        "Nodes_BCC_LCC": 0.3818491474658888,
        "Average_vertex_degree": 4.595579742771568
    },
    "chess": {
        "Nodes": 7301,
        "Edges": 55899,
        "LCC": {
            "Nodes": 7115,
            "Edges": 55779
        },
        "BCC": {
            "Nodes": 6250,
            "Edges": 54884
        },
        "Nodes_BCC_LCC": 0.8784258608573436,
        "Average_vertex_degree": 15.312696890836872
    },
    "elec": {
        "Nodes": 7118,
        "Edges": 100751,
        "LCC": {
            "Nodes": 7066,
            "Edges": 100667
        },
        "BCC": {
            "Nodes": 4786,
            "Edges": 98387
        },
        "Nodes_BCC_LCC": 0.6773280498160203,
        "Average_vertex_degree": 28.308794605226186
    },
    "facebook-combined": {
        "Nodes": 4039,
        "Edges": 88234,
        "LCC": {
            "Nodes": 4039,
            "Edges": 88234
        },
        "BCC": {
            "Nodes": 3698,
            "Edges": 85963
        },
        "Nodes_BCC_LCC": 0.9155731616736816,
        "Average_vertex_degree": 43.69101262688784
    },
    "wikispeedia": {
        "Nodes": 4179,
        "Edges": 50500,
        "LCC": {
            "Nodes": 4179,
            "Edges": 50500
        },
        "BCC": {
            "Nodes": 4105,
            "Edges": 50426
        },
        "Nodes_BCC_LCC": 0.9822924144532185,
        "Average_vertex_degree": 24.168461354391003
    },
    "pajek-erdos": {
        "Nodes": 6927,
        "Edges": 11850,
        "LCC": {
            "Nodes": 6927,
            "Edges": 11850
        },
        "BCC": {
            "Nodes": 2145,
            "Edges": 7067
        },
        "Nodes_BCC_LCC": 0.3096578605456908,
        "Average_vertex_degree": 3.421394543092248
    }
}

dataset_bcc_edge = {d: graphs_data[d]["BCC"]["Edges"]/graphs_data[d]["LCC"]["Edges"] for d in datasets}
# %%
comps = {d: dataset_stats[d]["LeeBCC"][0]/dataset_stats[d]["iCentral"][0] for d in datasets}
# %%
def thing(a):
    return 1-(1-a)**2

a = [comps[d] for d in datasets]
b = [(dataset_bcc_edge[d]) for d in datasets]
c = [dataset_degree[d] for d in datasets]
a2 = [comps[d] for d in datasets if d != "elec"]
b2 = [(dataset_bcc_edge[d]) for d in datasets if d != "elec"]
# %%
#plt.scatter(x=a, y=b)
#plt.plot(np.unique(a2), np.poly1d(np.polyfit(a2, b2, 1))(np.unique(a2)))
fig, ax = plt.subplots()
ax.scatter(x=a, y=b, c="tab:red", marker="x")

for i, txt in enumerate(datasets):
    if txt != "elec":
        ax.annotate(txt, (a[i], b[i]), xytext=(a[i]+0.025, b[i]-0.03))
    else:
        ax.annotate(txt, (a[i], b[i]), xytext=(a[i]-0.12, b[i]-0.03))
ax.plot(np.unique(a2), np.poly1d(np.polyfit(a2, b2, 1))(np.unique(a2)), c="tab:purple")

# Add labels, title and legend
ax.set_xlabel('iCentral/Lee-BCC speedup', fontweight=550, fontsize=10)
ax.set_ylabel('Relative BCC size to LCC (nodes)', fontweight=550, fontsize=10)
ax.set_title('Comparison of Speedup vs. Relative BCC size', fontweight=550, fontsize=12, pad=15)
ax.legend(["Datasets", "Line of Best Fit"], loc=1, fontsize=8)

# Adjust layout and save plot
plt.margins(y=0.2)  # Reduce extra margin
plt.subplots_adjust(bottom=0.1, left=0.1)  # Adjust bottom margin
plt.tight_layout()
plt.savefig('bar_chart.png', dpi=300)
plt.show()

#scipy.stats.linregress(a2, b2)
# %%
fig, ax = plt.subplots()
ax.scatter(x=a, y=c, c="tab:red", marker="x")

for i, txt in enumerate(datasets):
    if txt == "elec":
        ax.annotate(txt, (a[i], c[i]), xytext=(-3.5, -3.5), textcoords='offset points', ha='right', va='top')
    elif txt == "sx-mathoverflow":
        ax.annotate(txt, (a[i], c[i]), xytext=(-3.5, 0), textcoords='offset points', ha='right', va='bottom')
    elif txt == "wikispeedia":
        ax.annotate(txt, (a[i], c[i]), xytext=(5, 1), textcoords='offset points', ha='left', va='bottom')
    elif txt == "topology":
        ax.annotate(txt, (a[i], c[i]), xytext=(3.5, -3.5), textcoords='offset points', ha='left', va='top')
    else:
        ax.annotate(txt, (a[i], c[i]), xytext=(3.5, -3.5), textcoords='offset points', ha='left', va='top')
    
        
ax.plot(np.unique(a), np.poly1d(np.polyfit(a, c, 1))(np.unique(a)), c="tab:purple")

# Add labels, title and legend
ax.set_xlabel('iCentral/Lee-BCC speedup', fontweight=550, fontsize=10)
ax.set_ylabel('Average Node Degree', fontweight=550, fontsize=10)
ax.set_title('Comparison of Speedup vs. Average Node Degree', fontweight=550, fontsize=12, pad=15)
ax.legend(["Datasets", "Line of Best Fit"], loc=2, fontsize=8)

# Adjust layout and save plot
plt.margins(y=0.1)  # Reduce extra margin
plt.subplots_adjust(bottom=0.1, left=0.1)  # Adjust bottom margin
plt.tight_layout()
plt.savefig('figs/speedupVdegree.pdf', dpi=300)
plt.show()
# %%
fig, ax = plt.subplots()

raw_stats, _ = get_stats("wikispeedia", "iCentral", "run7_lcc", max_results=200)
ax.scatter(raw_stats["T"], raw_stats["RS"], marker="x", c="tab:blue")
ax.plot(np.unique(raw_stats["T"]), np.poly1d(np.polyfit(raw_stats["T"], raw_stats["RS"], 1))(np.unique(raw_stats["T"])), c="tab:orange")

ax.set_xlabel('iCentral Runtime (s)', fontweight=550, fontsize=10)
ax.set_ylabel('Recalculation Set Size', fontweight=550, fontsize=10)
ax.set_title('Comparison of Runtimes vs. Recalculation Set Size', fontweight=550, fontsize=12, pad=15)
ax.legend(["Edge Insertion", "Line of Best Fit"], loc=2, fontsize=8)

# Adjust layout and save plot
plt.margins(y=0.1)  # Reduce extra margin
plt.subplots_adjust(bottom=0.5, left=0.5)  # Adjust bottom margin
plt.tight_layout()
plt.savefig('figs/runtimeVrecalc.pdf', dpi=300)
plt.show()

# %%

#! also do a recalc size vs. time
#! BCC/LCC on edges instead

# %% 
# * Parallelisation 
def read_results_p(dataset,run="run9_extras"):
    with open(f"./{run}/slurm_results/parallels/{dataset}.txt") as f:
        x = f.read()
    return x

def get_stats_p(dataset, run, max_results=100):
    raw_results = read_results_p(dataset, "run9_extras")
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
        if set(d.keys()) != {'RS', 'T'} and i != max_results-1:
            continue
        stats.append(d)

    fstats = {
        'RS': [],
        'T': [],
    }
    for stat in stats:
        for k in ["RS", "T"]:
            fstats[k].append(stat[k])
    
    return {k: np.array(fstats[k]) for k in ["RS", "T"]}

p_datasets = [f"parallel-elec-{i}" for i in [2, 4, 8, 16, 32, 64]]
ps = [2, 4, 8, 16, 32, 64]
raw_p_stats = {i: get_stats_p(f"parallel-elec-{i}", "run9_extras")["T"] for i in [2, 4, 8, 16, 32, 64]}
p_means = [np.mean(raw_p_stats[i]) for i in ps]
p_speedup = [max(p_means)/i for i in p_means]
p_log = [np.log(i) for i in p_means]
# %%
plt.scatter(ps, p_speedup)
#plt.plot(np.unique(raw_stats["T"]), np.poly1d(np.polyfit(raw_stats["T"], raw_stats["RS"], 1))(np.unique(raw_stats["T"])), c="tab:orange")

# %%
ps2 = ps + [2]*100
p_speedup2 = p_speedup + [1]*100

fig, ax = plt.subplots()
ax.scatter(ps, p_speedup , marker="x", c="tab:green")

ax.plot(np.unique(ps2), np.poly1d(np.polyfit(ps2, p_speedup2, 1))(np.unique(ps2)), c="tab:red")
#regress = 0.7
ax.set_ylabel('Relative speedup (vs. 2 core)', fontweight=550, fontsize=10)
ax.set_xlabel('Number of cores', fontweight=550, fontsize=10)
ax.set_title('Scalability of Parallelised iCentral', fontweight=550, fontsize=12, pad=15)
ax.legend(["Run time", "Line of Best Fit"], loc=2, fontsize=8)

# Adjust layout and save plot
plt.margins(y=0.1)  # Reduce extra margin
plt.xticks(ps)
plt.subplots_adjust(bottom=0.5, left=0.5)  # Adjust bottom margin
plt.tight_layout()
plt.savefig('figs/coresVspeedup.pdf', dpi=300)
plt.show()
# %%
