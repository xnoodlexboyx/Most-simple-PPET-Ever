import numpy as np
from ppet.puf.puf_model import XORArbiterPUF
from ppet.analysis.metrics import calculate_uniqueness, calculate_reliability, calculate_bit_aliasing
from ppet.visualization.plots import plot_uniqueness_histogram, plot_reliability_line_graph, plot_bit_aliasing_bar_graph

def main():
    print("Starting PPET Simulation...")

    # Simulation Parameters
    num_pufs = 10
    stages_per_arbiter = 64
    num_arbiters = 4
    num_challenges = 100
    num_readings_reliability = 50
    
    # Noise levels for reliability analysis
    noise_levels = np.linspace(0, 0.5, 10)

    # 1. Instantiate PUF instances
    print(f"Creating {num_pufs} XOR Arbiter PUF instances with {num_arbiters} arbiters and {stages_per_arbiter} stages each...")
    puf_instances = [XORArbiterPUF(num_arbiters, stages_per_arbiter) for _ in range(num_pufs)]
    print("PUF instances created.")

    # 2. Uniqueness Analysis
    print("\nPerforming Uniqueness Analysis...")
    # For uniqueness, we really need to generate responses for the same challenges across different PUFs
    # The calculate_uniqueness function handles challenge generation internally for simplicity
    uniqueness_score = calculate_uniqueness(puf_instances, num_challenges, stages_per_arbiter)
    print(f"Average Inter-Chip Hamming Distance (Uniqueness): {uniqueness_score:.4f}")

    # Generate Hamming distances for plotting
    all_challenges_for_uniqueness = [np.random.randint(0, 2, stages_per_arbiter) for _ in range(num_challenges)]
    all_puf_responses_for_uniqueness = []
    for puf in puf_instances:
        puf_responses_for_challenges = [puf.generate_response(c) for c in all_challenges_for_uniqueness]
        all_puf_responses_for_uniqueness.append(puf_responses_for_challenges)

    inter_chip_hamming_distances_for_plot = []
    num_pufs_for_plot = len(puf_instances)
    for i in range(num_pufs_for_plot):
        for j in range(i + 1, num_pufs_for_plot):
            for k in range(num_challenges):
                # Ensure responses are treated as arrays for element-wise comparison
                response_i_k = np.array([all_puf_responses_for_uniqueness[i][k]])
                response_j_k = np.array([all_puf_responses_for_uniqueness[j][k]])
                hd = np.sum(response_i_k != response_j_k)
                inter_chip_hamming_distances_for_plot.append(hd)

    plot_uniqueness_histogram(inter_chip_hamming_distances_for_plot)
    print("Uniqueness histogram plotted.")

    # 3. Reliability Analysis
    print("\nPerforming Reliability Analysis...")
    reliability_scores = []
    # Pick one PUF instance and a fixed challenge for reliability testing
    test_puf = puf_instances[0]
    test_challenge = np.random.randint(0, 2, stages_per_arbiter)

    for noise in noise_levels:
        reliability = calculate_reliability(test_puf, test_challenge, num_readings_reliability, noise_level=noise)
        reliability_scores.append(reliability)
        print(f"  Noise Level: {noise:.2f}, Reliability: {reliability:.4f}")

    plot_reliability_line_graph(noise_levels, reliability_scores)
    print("Reliability line graph plotted.")

    # 4. Bit-Aliasing Analysis
    print("\nPerforming Bit-Aliasing Analysis...")
    bit_aliasing_results = calculate_bit_aliasing(puf_instances, num_challenges, stages_per_arbiter)
    print(f"Bit-Aliasing Results: {bit_aliasing_results}")
    
    # Since our current PUF returns a single bit, we'll plot this single bit's aliasing frequency
    plot_bit_aliasing_bar_graph(bit_aliasing_results)
    print("Bit-Aliasing bar graph plotted.")

    print("\nPPET Simulation Complete.")

if __name__ == "__main__":
    main()