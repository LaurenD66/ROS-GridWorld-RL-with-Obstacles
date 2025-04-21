import numpy as np
import os
import yaml

class QLearningAgent:
    def __init__(self, env):
        self.env = env
        self.q_table = np.zeros((env.grid_size, env.grid_size, env.action_space.n))
        self.alpha = 0.1
        self.gamma = 0.95
        self.epsilon = 0.2
        self.rewards_per_episode = []

    def train(self, episodes=20000):
        for ep in range(episodes):
            obs, _ = self.env.reset()
            done = False
            total_reward = 0
            pos = self.env.agent_pos

            while not done:
                x, y = pos
                if np.random.rand() < self.epsilon:
                    action = self.env.action_space.sample()
                else:
                    action = np.argmax(self.q_table[x, y])

                _, reward, done, _, info = self.env.step(action)
                new_x, new_y = self.env.agent_pos

                if info.get("moved", True):
                    best_future = np.max(self.q_table[new_x, new_y])
                    self.q_table[x, y, action] = (1 - self.alpha) * self.q_table[x, y, action] + self.alpha * (reward + self.gamma * best_future)
                    pos = [new_x, new_y]

                total_reward += reward

            self.rewards_per_episode.append(total_reward)

    def evaluate(self, num_episodes=1, gif_name="evaluation.gif"):
        self.env.render_mode = "human"
        all_positions = []
        for _ in range(num_episodes):
            self.env.reset()
            done = False
            path = []

            while not done:
                x, y = self.env.agent_pos
                action = np.argmax(self.q_table[x, y])
                _, _, done, _, _ = self.env.step(action)
                path.append((x, y))
                self.env.render()

            all_positions.append(path)

        # Save GIF from frames
        if hasattr(self.env, "frames") and self.env.frames:
            gif_path = os.path.join("images", gif_name)
            imageio.mimsave(gif_name, self.env.frames, fps=5)
            print(f"GIF saved to {gif_path}")

        return all_positions

    def load(self, path="q_table.yaml"):
        self.q_table = load_q_table_from_yaml(path)

def save_q_table_to_yaml(q_table, filename="q_table.yaml"):
    with open(filename, "w") as f:
        yaml.dump(q_table.tolist(), f)

def load_q_table_from_yaml(filename="q_table.yaml"):
    with open(filename, "r") as f:
        data = yaml.safe_load(f)
    return np.array(data)

