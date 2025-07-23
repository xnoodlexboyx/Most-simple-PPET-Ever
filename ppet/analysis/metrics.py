import numpy as np

def hamming_distance(response1, response2):
    """
    Calculates the Hamming distance between two binary strings/arrays.
    """
    if len(response1) != len(response2):
        raise ValueError("Responses must have the same length.")
    return np.sum(np.array(response1) != np.array(response2))

def calculate_uniqueness(puf_instances, num_challenges, challenge_length):
    """
    Calculates the uniqueness metric for a set of PUF instances using vectorized operations.
    Uniqueness is measured by the average inter-chip Hamming distance.
    """
    num_pufs = len(puf_instances)
    if num_pufs < 2:
        return 0.0  # Not enough PUFs to compare

    # Generate all challenges at once
    all_challenges = np.random.randint(0, 2, size=(num_challenges, challenge_length))

    # Generate responses for all PUFs and all challenges
    # Response matrix shape: (num_pufs, num_challenges)
    all_puf_responses = np.array(
        [[puf.generate_response(c) for c in all_challenges] for puf in puf_instances]
    )

    # Calculate pairwise Hamming distances in a vectorized way
    total_hd = 0
    num_pairs = 0
    for i in range(num_pufs):
        for j in range(i + 1, num_pufs):
            # XORing the responses and summing the result gives the Hamming distance
            hd = np.sum(all_puf_responses[i, :] != all_puf_responses[j, :])
            total_hd += hd
            num_pairs += 1

    # The average Hamming distance is normalized by the number of challenges
    # and the number of PUF pairs.
    if num_pairs == 0:
        return 0.0

    # The average inter-chip HD is the total HD divided by (num_pairs * num_challenges)
    # However, since we summed the HD over all challenges, we just need to divide by num_challenges
    # and then average over all pairs.
    # A simpler way: total_hd is the sum of all pairwise distances over all challenges.
    # The number of comparisons is num_pairs * num_challenges.
    average_hd = total_hd / (num_pairs * num_challenges)
    
    return average_hd


def calculate_reliability(puf_instance, challenge, num_readings, temperature=25.0, voltage=1.0, noise_level=0.0):
    """
    Calculates the reliability metric for a single PUF instance under environmental stress.
    Reliability is measured by comparing responses under stress to a golden response at nominal conditions.
    """
    # Generate the "golden" response at nominal conditions (e.g., 25°C, 1.0V)
    golden_response = puf_instance.generate_response(challenge, temperature=25.0, voltage=1.0)
    
    error_counts = []
    for _ in range(num_readings):
        # Generate a "noisy" response under the specified environmental conditions
        noisy_response = puf_instance.generate_response(challenge, temperature=temperature, voltage=voltage)
        
        # Add a simple bit-flip noise model on top of the environmental stress
        if np.random.rand() < noise_level:
            noisy_response = 1 - noisy_response

        # Ensure responses are numpy arrays for comparison
        golden_response_arr = np.array(golden_response).flatten()
        noisy_response_arr = np.array(noisy_response).flatten()

        error_counts.append(hamming_distance(golden_response_arr, noisy_response_arr))
            
    # Reliability is 1 - average bit error rate
    # The total number of bits is num_readings * number of bits in response
    total_bits = num_readings * len(np.array(golden_response).flatten())
    if total_bits == 0:
        return 1.0 # Perfect reliability if no bits to compare

    average_bit_error_rate = np.sum(error_counts) / total_bits
    return 1 - average_bit_error_rate

def calculate_bit_aliasing(puf_instances, num_challenges, challenge_length):
    """
    Calculates bit aliasing for a set of PUF instances.
    Bit aliasing measures how often a specific bit position in a response matches
    across multiple PUF instances for the same challenge.
    Returns a dictionary where keys are bit positions and values are the
    aliasing frequency (0 to 1).
    """
    all_challenges = [np.random.randint(0, 2, challenge_length) for _ in range(num_challenges)]
    
    # Collect responses for all PUFs and all challenges
    all_puf_responses = []
    for puf in puf_instances:
        puf_responses_for_challenges = [puf.generate_response(c) for c in all_challenges]
        all_puf_responses.append(puf_responses_for_challenges)

    num_pufs = len(puf_instances)
    
    # Initialize counts for 0s and 1s for each bit position
    # This assumes a single bit response from generate_response
    # If generate_response returns a bit array, this logic needs adjustment.
    # For XORArbiterPUF, it returns a single bit.
    
    # We need to collect all responses for each challenge and then analyze bit positions.
    # Since XORArbiterPUF returns a single bit, we'll analyze the "bit position" of that single bit.
    # This interpretation might need refinement if PUFs return multi-bit responses.

    # To align with the proposal's "Heatmaps: Visualize bit-aliasing across multiple challenges and instances.
    # Each cell represents the frequency of a bit being "0" or "1" at a given position."
    # and "Bar Graphs: Show the aliasing frequency for specific bit positions."
    # This implies multi-bit responses or a different interpretation of "bit position".

    # Given our current simple XORArbiterPUF returns a single bit,
    # "bit position" refers to the single output bit.
    # We'll calculate the frequency of this bit being 0 or 1 across instances for each challenge.

    bit_aliasing_data = {0: []} # For the single output bit position

    for k in range(num_challenges):
        responses_for_this_challenge = [all_puf_responses[i][k] for i in range(num_pufs)]
        
        # Count frequency of 0s and 1s for this "bit position" (the single response bit)
        count_zeros = responses_for_this_challenge.count(0)
        count_ones = responses_for_this_challenge.count(1)
        
        # Aliasing frequency can be defined as the maximum of (count_zeros/total, count_ones/total)
        # Or, more simply, the frequency of the most common bit.
        if num_pufs > 0:
            aliasing_freq = max(count_zeros, count_ones) / num_pufs
            bit_aliasing_data[0].append(aliasing_freq)
        else:
            bit_aliasing_data[0].append(0.0) # No PUFs

    # Return the full distribution of aliasing frequencies for each bit position
    return bit_aliasing_data

def calculate_attack_accuracy(attack, puf, num_train_crps, num_test_crps):
    """
    Trains an attack model and evaluates its accuracy.

    :param attack: An instance of an Attack class.
    :param puf: The PUF instance to be attacked.
    :param num_train_crps: The number of CRPs to use for training the attack.
    :param num_test_crps: The number of CRPs to use for testing the attack's accuracy.
    :return: The prediction accuracy of the attack (float between 0 and 1).
    """
    # Train the attack model
    attack.train(puf, num_train_crps)

    # Evaluate the attack model
    accuracy = attack.evaluate(puf, num_test_crps)
    
    return accuracy