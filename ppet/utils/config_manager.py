import yaml
import os

def load_config(config_path='config.yaml'):
    """
    Loads configuration from a YAML file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

if __name__ == '__main__':
    # Example usage:
    try:
        config = load_config()
        print("Configuration loaded successfully:")
        print(config)
        print(f"Number of PUFs: {config['simulation']['num_pufs']}")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")