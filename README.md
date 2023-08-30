# Automated Flappy Bird AI

Flappy Bird AI is a sophisticated solution that employs a Neural Network trained through the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to master the Flappy Bird game. Designed to continually evolve, this AI endeavors to play flawlessly without losing.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Features:
- **AI Learning**: Progressive learning from each gameplay to enhance precision.
- **Consistent Mastery**: Strives to perfect the gameplay and never lose.
- **Real-time Visualization**: Witness the AI's gameplay and admire its evolving skills.

## Prerequisites

- Python 3.x
- Pygame
- neat-python

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MazenTayseer/Automated_Flappy_Bird.git
```

2. Navigate to the cloned repository:
```bash
cd Automated_Flappy_Bird
```

3. Install the necessary packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main script:
```bash
python main.py
```

2. Enjoy watching the AI adeptly navigate the challenges of Flappy Bird!

## How it Works

### NEAT Algorithm

The NEAT algorithm empowers the AI to evolve its neural network, adapting to the intricacies of the Flappy Bird game. By evolving and refining the network topology over time, NEAT ensures the AI's consistent improvement in the game.

### Game Mechanics

The AI assimilates vital game data such as its current vertical position, the upcoming gap's vertical placement, and its vertical velocity. Based on these inputs, it judiciously decides when to make the bird jump.

## Contributing

Contributions are warmly welcomed! Feel free to fork this project, make enhancements, and submit pull requests. If you discover any bugs or have suggestions for improvements, please open an issue.

## License

This project is under the MIT License. See the [LICENSE](LICENSE) file for complete details.
