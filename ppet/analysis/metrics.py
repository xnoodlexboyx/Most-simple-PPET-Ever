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
    Calculates the uniqueness metric for a set of PUF instances.
    Uniqueness is typically measured by the average inter-chip Hamming distance.
    """
    all_challenges = [np.random.randint(0, 2, challenge_length) for _ in range(num_challenges)]
    
    all_puf_responses = []
    for puf in puf_instances:
        puf_responses_for_challenges = [puf.generate_response(c) for c in all_challenges]
        all_puf_responses.append(puf_responses_for_challenges)

    inter_chip_hamming_distances = []
    num_pufs = len(puf_instances)
    
    for i in range(num_pufs):
        for j in range(i + 1, num_pufs):
            # Compare responses of PUF i and PUF j for the same challenges
            for k in range(num_challenges):
                # Hamming distance is calculated between single bits (responses)
                hd = hamming_distance([all_puf_responses[i][k]], [all_puf_responses[j][k]])
                inter_chip_hamming_distances.append(hd)
    
    if not inter_chip_hamming_distances:
        return 0.0 # No pairs to compare

    return np.mean(inter_chip_hamming_distances)


def calculate_reliability(puf_instance, challenge, num_readings, noise_level=0.1):
    """
    Calculates the reliability metric for a single PUF instance under simulated noise.
    Reliability is typically measured by the intra-chip Hamming distance (bit error rate).
    """
    original_response = puf_instance.generate_response(challenge)
    
    error_counts = []
    for _ in range(num_readings):
        # Simulate noise by randomly flipping bits in the challenge or response generation
        # For simplicity, we'll simulate noise by re-generating the response with a chance of error
        # A more accurate simulation would involve modifying the PUF's internal state or challenge.
        
        # Here, we'll simulate noise by adding a small random perturbation to the decision boundary
        # or by directly flipping the response bit with a certain probability.
        
        # For a simple Arbiter PUF, we can simulate noise by slightly altering the delays
        # or by introducing a probability of bit flip in the final response.
        
        # Let's use a simple bit-flip probability for now.
        noisy_response = original_response
        if np.random.rand() < noise_level:
            noisy_response = 1 - original_response # Flip the bit
        
        error_counts.append(hamming_distance([original_response], [noisy_response]))
            
    # Reliability is 1 - average bit error rate
    average_bit_error_rate = np.mean(error_counts)
    return 1 - average_bit_error_rate