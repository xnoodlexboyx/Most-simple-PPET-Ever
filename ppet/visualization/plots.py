import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def plot_uniqueness_histogram(hamming_distances, title="Uniqueness Histogram (Inter-Chip Hamming Distances)", save_path=None, save_format="png"):
    """
    Plots a histogram of inter-chip Hamming distances to visualize uniqueness using seaborn.
    If save_path is provided, saves the figure instead of showing it.
    """
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.histplot(hamming_distances, bins=np.arange(0, 1.1, 0.05), kde=True)
    plt.title(title, fontsize=16)
    plt.xlabel("Normalized Hamming Distance", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    if save_path:
        plt.savefig(f"{save_path}.{save_format}", format=save_format, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_bit_aliasing_bar_graph(bit_aliasing_data, title="Bit-Aliasing Frequency", save_path=None, save_format="png"):
    """
    Plots a bar graph of bit-aliasing frequencies using seaborn.
    If save_path is provided, saves the figure instead of showing it.
    """
    if not bit_aliasing_data:
        print("No bit aliasing data to plot.")
        return

    bit_positions = list(bit_aliasing_data.keys())
    aliasing_frequencies = list(bit_aliasing_data.values())

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.barplot(x=[str(pos) for pos in bit_positions], y=aliasing_frequencies, palette="viridis")
    plt.title(title, fontsize=16)
    plt.xlabel("Bit Position", fontsize=12)
    plt.ylabel("Aliasing Frequency", fontsize=12)
    plt.ylim(0, 1.0)
    if save_path:
        plt.savefig(f"{save_path}.{save_format}", format=save_format, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_bit_aliasing_distribution(bit_aliasing_data, title="Bit-Aliasing Distribution", save_path=None, save_format="png"):
    """
    Plots a boxplot of the bit-aliasing distribution to show bias.
    bit_aliasing_data is expected to be a dictionary like {bit_position: [aliasing_frequencies]}.
    """
    if not bit_aliasing_data:
        print("No bit aliasing data to plot.")
        return

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # The data is expected to be a list of frequencies for each bit position
    # For a single-bit response PUF, we'll have one boxplot.
    all_frequencies = []
    labels = []
    for pos, freqs in bit_aliasing_data.items():
        all_frequencies.extend(freqs)
        labels.extend([str(pos)] * len(freqs))

    sns.boxplot(x=labels, y=all_frequencies, palette="pastel")
    plt.title(title, fontsize=16)
    plt.xlabel("Bit Position", fontsize=12)
    plt.ylabel("Aliasing Frequency", fontsize=12)
    plt.ylim(0, 1.05)
    
    if save_path:
        plt.savefig(f"{save_path}.{save_format}", format=save_format, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_reliability_line_graph(noise_levels, reliability_scores, title="Reliability vs. Noise Level", save_path=None, save_format="png"):
    """
    Plots a line graph of reliability scores against increasing noise levels using seaborn.
    If save_path is provided, saves the figure instead of showing it.
    """
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.lineplot(x=noise_levels, y=reliability_scores, marker='o', color='b')
    plt.title(title, fontsize=16)
    plt.xlabel("Noise Level", fontsize=12)
    plt.ylabel("Reliability Score", fontsize=12)
    plt.ylim(0, 1.05)
    plt.grid(True)
    if save_path:
        plt.savefig(f"{save_path}.{save_format}", format=save_format, bbox_inches='tight')
        plt.close()
    else:
        plt.show()