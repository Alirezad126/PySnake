import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random

# Define the Q-network
class QNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 256)
        self.fc3 = nn.Linear(256, 256)
        self.fc4 = nn.Linear(256, 128)
        self.fc5 = nn.Linear(128, action_size)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = F.relu(self.fc4(x))
        return self.fc5(x)

# Define the replay memory
class ReplayMemory():
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, transition):
        self.memory.append(transition)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

# Define the DQN agent
class DQNAgent():
    def __init__(self, capacity, state_size, action_size, batch_size, gamma,tau):
        self.state_size = state_size
        self.action_size = action_size
        self.batch_size = batch_size
        self.gamma = gamma
        self.tau = tau
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.q_network = QNetwork(state_size, action_size).to(self.device)
        self.target_network = QNetwork(state_size, action_size).to(self.device)
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)

        self.replay_memory = ReplayMemory(capacity)

    def act(self, state, epsilon, exploration=True):
        if not exploration:
            state = torch.tensor(state, dtype=torch.float).unsqueeze(0).to(self.device)
            with torch.no_grad():
                action_values = self.q_network(state)
            action = np.argmax(action_values.cpu().data.numpy())
        else:
            if random.random() > epsilon:
                state = torch.tensor(state, dtype=torch.float).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    action_values = self.q_network(state)
                action = np.argmax(action_values.cpu().data.numpy())
            else:
                action = random.randint(0, self.action_size - 1)
        return action


    def train(self):
        if len(self.replay_memory) < self.batch_size:
            return

        transitions = self.replay_memory.sample(self.batch_size)
        batch = list(zip(*transitions))

        state_batch = torch.tensor(batch[0], dtype=torch.float).to(self.device)
        action_batch = torch.tensor(batch[1], dtype=torch.long).unsqueeze(1).to(self.device)
        reward_batch = torch.tensor(batch[2], dtype=torch.float).unsqueeze(1).to(self.device)
        next_state_batch = torch.tensor(batch[3], dtype=torch.float).to(self.device)
        done_batch = torch.tensor(batch[4], dtype=torch.float).unsqueeze(1).to(self.device)

        current_q_values = self.q_network(state_batch).gather(1, action_batch)
        next_q_values = self.target_network(next_state_batch).detach().max(1)[0].unsqueeze(1)
        expected_q_values = reward_batch + (1 - done_batch) * self.gamma * next_q_values

        loss = F.mse_loss(current_q_values, expected_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.update_target_network()

    def update_target_network(self):
        q_network_params = self.q_network.named_parameters()
        target_network_params = self.target_network.named_parameters()

        updated_params = dict(target_network_params)
        for name, param in q_network_params:
            if name in updated_params:
                updated_params[name].data.copy_(
                    self.tau * param.data + (1 - self.tau) * updated_params[name].data
                )

        self.target_network.load_state_dict(updated_params)

    def save_policy(self, directory, filename):
        # Create the full path for the policy file
        policy_path = directory + '/' + filename

        # Save the agent's policy file
        torch.save(self.q_network.state_dict(), policy_path)
        print("Policy saved as:", policy_path)

