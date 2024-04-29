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
    if run == "run2":
        results = read_results(dataset=dataset, alg=alg, run=run)
        a = results.split("Run times:\n")[1].split("\n\n")
        if (dataset, alg, run) in[("topology", "iCentral_p", "run2")]:
            blocks = [i.split("\n") for i in a[20:20+max_results]]
        else:
            blocks = [i.split("\n") for i in a[:max_results]]
        times = []
        for block in blocks:
            if len(block) > 1 and len(block[1]) > 0:
                times.append(float(block[1]))
    elif run == "run1":
        results = read_results(dataset=dataset, alg=alg, run=run)
        a = results.split("Run times:\n")[1]
        if alg == "iCentral_p":
            pass
        else:
            pass

    times = np.array(times)
    m = np.mean(times)
    s = np.std(times)
    return m, s
# %%
x = read_results("chess", "iCentral", run="run2")
# %%
datasets = ("chess", "elec", "email-EuAll", "facebook-combined", "linux", "pajek-erdos", "slashdot-threads", "slashdot-zoo", "sx-mathoverflow", "topology", "wikispeedia")
algs = ("iCentral", "iCentral_p", "LeeBCC")
runs = ("run2")
# %%
results = {}

for d in datasets:
    dic = {}
    for a in algs:
        for r in runs:
            dic[a] = get_stats(d, a, "run2", 100)    
    results[d] = dic


# %%
x = np.arange(len(datasets))
width = 0.15

fig, ax = plt.subplots(layout="constrained")

multiplier = 0
for d in datasets:
    offset = width * multiplier
    vals = 1
    rects = ax.bar(x+offset, vals, width, label=d)
# %%
datasets = ("chess", "elec", "email-EuAll", "facebook-combined", "linux", "pajek-erdos", "slashdot-threads", "sx-mathoverflow", "topology", "wikispeedia")

datasets_big = ("linux",  "slashdot-threads", "sx-mathoverflow", "topology") #larger
datasets_small = ("chess", "elec", "facebook-combined", "pajek-erdos", "wikispeedia") #small
# %%
graph_dataset = datasets_small
r = np.arange(len(graph_dataset))
bar_width = 0.2
for i, alg in enumerate(algs):
    means = [results[d][alg][0] for d in graph_dataset]
    stdevs = [results[d][alg][1] for d in graph_dataset]
    plt.bar(r + i * bar_width, means, yerr=stdevs, width=bar_width, label=alg)

plt.xlabel('Dataset', fontweight='bold')
plt.ylabel('Mean', fontweight='bold')
plt.title('Mean and Standard Deviation for Algorithms by Dataset')
plt.xticks(r + bar_width, graph_dataset)
plt.legend()

plt.tight_layout()
plt.show()
# %%
for d in datasets:
    print(f"Dataset: {d}")
    print(f"-LeeBCC: {results[d]['LeeBCC'][0] / results[d]['iCentral'][0]}")
    print(f"-iCentral_p: {results[d]['iCentral'][0] / results[d]['iCentral_p'][0]}")
# %%
