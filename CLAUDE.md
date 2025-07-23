# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Running the Main Application
```bash
python main.py --config config.yaml
```

### Testing
```bash
pytest tests/
pytest tests/test_metrics.py  # Run specific test file
pytest tests/test_puf_model.py  # Run PUF model tests
```

### Package Installation
```bash
pip install -r requirements.txt
# Or install as package:
pip install -e .
```

## Architecture Overview

PPET (PUF Performance Evaluation Toolkit) is organized into distinct modules:

### Core Components

- **`ppet/puf/`**: PUF model implementations
  - `puf_model.py`: Contains abstract `PUF` base class and concrete implementations:
    - `ArbiterPUF`: Single arbiter PUF with environmental stress modeling
    - `XORArbiterPUF`: Multiple arbiter PUFs with XOR combination
    - `SRAMPUF`: SRAM-based PUF model
    - `RingOscillatorPUF`: Ring oscillator frequency comparison PUF

- **`ppet/analysis/`**: Metrics calculation and evaluation
  - `metrics.py`: Core security metrics including uniqueness, reliability, bit-aliasing, and attack accuracy calculations

- **`ppet/attack/`**: Attack simulation models
  - `attack_model.py`: Abstract `Attack` base class and `LogisticRegressionAttack` implementation for modeling ML-based attacks

- **`ppet/visualization/`**: Plotting and visualization
  - `plots.py`: Matplotlib-based plotting functions for all metrics

- **`ppet/utils/`**: Utility functions
  - `config_manager.py`: YAML configuration file loading

### Main Application Flow

The `main.py` orchestrates the entire analysis pipeline:
1. Load configuration from YAML file
2. Create PUF instances based on simulation parameters
3. Calculate uniqueness metrics across PUF instances
4. Evaluate reliability under different noise/environmental conditions
5. Perform bit-aliasing analysis
6. Execute attack simulations (if enabled)
7. Generate visualizations and save results

### Configuration System

The application uses YAML configuration (`config.yaml`) with these key sections:
- `simulation`: PUF parameters (num_pufs, stages_per_arbiter, num_arbiters, etc.)
- `output`: File saving settings for figures and results
- `attack`: Attack simulation parameters (type, training/test CRP counts)

### Environmental Modeling

PUF models include realistic environmental stress factors:
- Temperature effects on delay variations
- Voltage variations impacting performance
- Thermal noise modeling
- Aging and reliability degradation

This is a defense-oriented framework specifically designed for security evaluation of PUF architectures in military and national security contexts.