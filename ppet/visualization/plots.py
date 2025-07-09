import matplotlib.pyplot as plt
import numpy as np

def plot_uniqueness_histogram(hamming_distances, title="Uniqueness Histogram (Inter-Chip Hamming Distances)"):
    """
    Plots a histogram of inter-chip Hamming distances to visualize uniqueness.
    """
    plt.figure(figsize=(8, 6))
    plt.hist(hamming_distances, bins=np.arange(0, 2, 0.1), edgecolor='black')
    plt.title(title)
    plt.xlabel("Hamming Distance")
    plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.75)
    plt.show()

def plot_reliability_line_graph(noise_levels, reliability_scores, title="Reliability vs. Noise Level"):
    """
    Plots a line graph of reliability scores against increasing noise levels.
    """
    plt.figure(figsize=(8, 6))
    plt.plot(noise_levels, reliability_scores, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel("Noise Level")
    plt.ylabel("Reliability Score")
    plt.grid(True)
    plt.ylim(0, 1.1) # Reliability is between 0 and 1
    plt.show()