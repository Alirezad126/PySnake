# PySnake RL Game

Welcome to the PySnake RL Game repository! This repository contains code for a reinforcement learning (RL) environment and a Pygame-based game where players can play the game themselves.

## Repository Structure

The repository is organized into the following folders:

- `envs`: This folder contains the RL environment for the PySnake game. It provides an interface for training and evaluating RL agents using the game environment.

- `agent`: The `agent` folder contains code for DQN agent that can learn to play the PySnake game. It includes evaulation file for evaluating the agent's performance and creating a GIF file.

- `pygame`: The `pygame` folder contains the game interface for human players. Players can run the game and play it themselves using the Pygame-based graphical interface.


## Getting Started

To get started with the PySnake RL Game, follow these steps:

1. Clone the repository to your local machine.
    ```shell
   git clone https://github.com/Alirezad126/PySnake.git

2. Set up the required dependencies. Ensure that you have Python 3 installed and install the necessary packages by running:

   ```shell
   pip install -r requirements.txt

## Train the agent

To train the agent, use Run.ipynb notebook

## Play Yourself

To train the agent, use Run.ipynb notebook

1. Change directory to pygame:

    ```shell
   cd Pygame

2. Run the game

    ```shell
   python3 run.py

![Alt Text](results/score_61.gif)
   

