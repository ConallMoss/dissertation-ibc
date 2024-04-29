# %%
import matplotlib.pyplot as plt
import numpy as np

# %%
def read_results(dataset, alg,run="run1"):
    with open(f"./{run}/slurm_results/{dataset}/{dataset}-{alg}.txt") as f:
        x = f.read()
    return x

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
            continue
        stats.append(d)

    fstats = {
        'RS': [],
        'T': [],
        'M': [],
        "E": []
    }
    for stat in stats:
        for k in ["RS", "T", "M"]:
            fstats[k].append(stat[k])
    
    return {k: np.array(fstats[k]) for k in ["RS", "T", "M"]}, init_mem


def get_dataset_stats(dataset, run, max_results):
    algs = ("iCentral", "iCentral_p", "LeeBCC")
    
    iCentral_stats, iCentral_mem = get_stats(dataset, "iCentral", run, max_results)
    LeeBCC_stats, LeeBCC_mem = get_stats(dataset, "LeeBCC", run, max_results)
    iCentral_p_stats, iCentral_p_mem = get_stats(dataset, "iCentral_p", run, max_results)

    iCentral_times = iCentral_stats["T"]
    LeeBCC_times = LeeBCC_stats["T"]
    iCentral_p_times = iCentral_p_stats["T"]

    lens = [len(i) for i in [iCentral_times, LeeBCC_times, iCentral_p_times]]
    #print(lens)
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
def plot_relative_times(dataset_stats, graph_datasets):
    
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

plot_relative_times(dataset_stats, datasets_big)

# %%
def plot_relative_times2(dataset_stats, graph_datasets, algs):
    
    num_datasets = len(graph_datasets)
    num_algorithms = len(algs)

    barWidth = 0.35

    r = np.arange(num_datasets)
    plt.style.use('seaborn-v0_8-white')
    # Create bars
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, alg in enumerate(algs):
        means = [dataset_stats[dataset][alg][0] for dataset in graph_datasets]
        std_devs = [dataset_stats[dataset][alg][1] for dataset in graph_datasets]
        
        ax.bar(r + i * barWidth, means, yerr=std_devs, width=barWidth, label=alg, capsize=5, color=alg_cols[alg], linewidth=0.5, ecolor="black", capstyle="butt", error_kw={"elinewidth": 2, "capsize": 5, 'markeredgewidth':1})

    # Add horizontal line at y=0
    ax.axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    # Add labels, title and legend
    ax.set_xlabel('Dataset', fontweight='bold', fontsize=12)
    ax.set_ylabel('Mean', fontweight='bold', fontsize=12)
    ax.set_title('Mean and Standard Deviation for Algorithms by Dataset', fontweight='bold', fontsize=14)
    ax.set_xticks(r + (barWidth * num_algorithms) / 2 - 0.1) 
    ax.set_xticklabels(graph_datasets, rotation=45, ha='right')
    ax.legend()

    # Adjust layout and save plot
    plt.margins(0.05)  # Reduce extra margin
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin
    plt.tight_layout()
    plt.savefig('bar_chart.png', dpi=300)
    plt.show()


plot_relative_times2(dataset_stats, datasets, algs = ("iCentral", "LeeBCC", "iCentral_p"))
#plot_relative_times2(dataset_stats, datasets2, algs = ("iCentral", "iCentral_p"))
#plot_relative_times2(dataset_stats, datasets, algs = ("iCentral_mem", "LeeBCC_mem"))


# %%
datasets = ("chess", "elec", "email-EuAll", "facebook-combined", "linux", "pajek-erdos", "slashdot-threads", "sx-mathoverflow", "topology", "wikispeedia")
datasets = ("email-EuAll", "linux", "topology", "sx-mathoverflow", "slashdot-threads", "chess",  "elec",  "facebook-combined", "wikispeedia", "pajek-erdos")
datasets2 = ("email-EuAll", "linux", "slashdot-threads", "sx-mathoverflow", "topology", "elec", "chess", "wikispeedia", "pajek-erdos")

algs = ("iCentral", "iCentral_p", "LeeBCC")
runs = ("run5_lcc")

alg_cols = {
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

dataset_stats = {}
for d in datasets:
    dataset_stats[d] = get_dataset_stats(d, "run5_lcc", 200) 


# %%
plot_times(dataset_stats, datasets)

# %%
datasets_big = ("email-EuAll", "linux",  "slashdot-threads", "sx-mathoverflow", "topology") #larger
datasets_small = ("chess", "elec", "facebook-combined", "pajek-erdos", "wikispeedia") #small


plot_times(dataset_stats, datasets_big)
plot_times(dataset_stats, datasets_small)
# %%
datasets_1 = ("email-EuAll", "linux")
datasets_2 = ("slashdot-threads", "sx-mathoverflow", "topology")
datasets_3 = ("chess", "elec", "wikispeedia") 
datasets_4 = ("facebook-combined", "pajek-erdos")

plot_times(dataset_stats, datasets_1)
plot_times(dataset_stats, datasets_2)
plot_times(dataset_stats, datasets_3)
plot_times(dataset_stats, datasets_4)

# %%
#removed facebook combined, sx-mathoverflow
datasets2 = ("chess", "elec", "email-EuAll", "linux", "pajek-erdos", "slashdot-threads", "topology", "wikispeedia")

plot_base_comp(dataset_stats, datasets2)
# %%
plot_relative_times(dataset_stats, datasets2)
# %%
plot_times(dataset_stats, datasets_big)
# %%
