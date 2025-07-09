import numpy as np
import os
from ppet.puf.puf_model import XORArbiterPUF, ArbiterPUF
from ppet.analysis.metrics import calculate_uniqueness, calculate_reliability, calculate_bit_aliasing, calculate_attack_accuracy
from ppet.visualization.plots import plot_uniqueness_histogram, plot_reliability_line_graph, plot_bit_aliasing_bar_graph
from ppet.utils.config_manager import load_config
from ppet.attack.attack_model import LogisticRegressionAttack

import argparse

def run_analysis(config):
    """
    Runs the main PUF analysis based on the provided configuration.
    """
    print("Starting PPET Simulation...")
    sim_params = config['simulation']
    output_settings = config['output']

    # Set random seed for reproducibility
    np.random.seed(sim_params['random_seed'])
    print(f"Random seed set to: {sim_params['random_seed']}")

    # Simulation Parameters from config
    num_pufs = sim_params['num_pufs']
    stages_per_arbiter = sim_params['stages_per_arbiter']
    num_arbiters = sim_params['num_arbiters']
    num_challenges = sim_params['num_challenges']
    num_readings_reliability = sim_params['num_readings_reliability']
    noise_levels = np.array(sim_params['noise_levels'])

    # Ensure output directories exist
    figures_dir = output_settings.get('figures_dir', 'figures')
    results_dir = output_settings.get('results_dir', 'results')
    if output_settings.get('save_figures', False):
        os.makedirs(figures_dir, exist_ok=True)
        print(f"Figures will be saved to: {figures_dir}")
    if output_settings.get('save_metrics', False):
        os.makedirs(results_dir, exist_ok=True)
        print(f"Metrics will be saved to: {results_dir}")


    # 1. Instantiate PUF instances
    print(f"\nCreating {num_pufs} XOR Arbiter PUF instances with {num_arbiters} arbiters and {stages_per_arbiter} stages each...")
    puf_instances = [XORArbiterPUF(num_arbiters, stages_per_arbiter) for _ in range(num_pufs)]
    print("PUF instances created.")

    # 2. Uniqueness Analysis
    print("\nPerforming Uniqueness Analysis...")
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
                response_i_k = np.array([all_puf_responses_for_uniqueness[i][k]])
                response_j_k = np.array([all_puf_responses_for_uniqueness[j][k]])
                hd = np.sum(response_i_k != response_j_k)
                inter_chip_hamming_distances_for_plot.append(hd)

    if output_settings.get('save_figures', False):
        save_path = os.path.join(figures_dir, "uniqueness_histogram.png")
        plot_uniqueness_histogram(inter_chip_hamming_distances_for_plot, save_path=save_path)
        print("Uniqueness histogram saved.")
    else:
        plot_uniqueness_histogram(inter_chip_hamming_distances_for_plot)


    # 3. Reliability Analysis
    print("\nPerforming Reliability Analysis...")
    reliability_scores = []
    test_puf = puf_instances[0]
    test_challenge = np.random.randint(0, 2, stages_per_arbiter)

    for noise in noise_levels:
        reliability = calculate_reliability(test_puf, test_challenge, num_readings_reliability, noise_level=noise)
        reliability_scores.append(reliability)
        print(f"  Noise Level: {noise:.2f}, Reliability: {reliability:.4f}")

    if output_settings.get('save_figures', False):
        save_path = os.path.join(figures_dir, "reliability_line_graph.png")
        plot_reliability_line_graph(noise_levels, reliability_scores, save_path=save_path)
        print("Reliability line graph saved.")
    else:
        plot_reliability_line_graph(noise_levels, reliability_scores)


    # 4. Bit-Aliasing Analysis
    print("\nPerforming Bit-Aliasing Analysis...")
    bit_aliasing_results = calculate_bit_aliasing(puf_instances, num_challenges, stages_per_arbiter)
    print(f"Bit-Aliasing Results: {bit_aliasing_results}")
    
    if output_settings.get('save_figures', False):
        save_path = os.path.join(figures_dir, "bit_aliasing_bar_graph.png")
        plot_bit_aliasing_bar_graph(bit_aliasing_results, save_path=save_path)
        print("Bit-Aliasing bar graph saved.")
    else:
        plot_bit_aliasing_bar_graph(bit_aliasing_results)

    # 5. Attack Simulation
    if config.get('attack', {}).get('enabled', False):
        print("\nPerforming Attack Simulation...")
        attack_params = config['attack']
        
        # For now, we'll instantiate a specific PUF for the attack demonstration
        # This part can be made more generic later
        puf_to_attack = ArbiterPUF(stages_per_arbiter)
        
        if attack_params['type'] == 'LogisticRegression':
            attack_model = LogisticRegressionAttack()
            accuracy = calculate_attack_accuracy(
                attack_model,
                puf_to_attack,
                attack_params['num_train_crps'],
                attack_params['num_test_crps']
            )
            print(f"Logistic Regression Attack Accuracy: {accuracy:.4f}")
        else:
            print(f"Warning: Unknown attack type '{attack_params['type']}' specified in config.")


    print("\nPPET Simulation Complete.")


def main():
    parser = argparse.ArgumentParser(description="PPET: A PUF Performance Evaluation Toolkit")
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to the configuration file (default: config.yaml)'
    )
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        run_analysis(config)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()