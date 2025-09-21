import random
import asyncio

# ---------------- RL Environment ---------------- #
ACTIONS = ["START_MOWING", "RETURN_TO_DOCK", "CHARGE", "WAIT", "SEND_ALERT"]

class SimpleMowerEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.activity = "DOCKED"
        self.battery = 100
        self.weather = random.choice(["SUNNY", "RAINY"])
        self.obstacle = random.choice([True, False])
        self.schedule = random.choice([True, False])
        return self.get_state()

    def get_state(self):
        # Reduced state space: (activity, battery level (high/low), weather, obstacle, schedule)
        battery_level = "HIGH" if self.battery > 30 else "LOW"
        return (self.activity, battery_level, self.weather, self.obstacle, self.schedule)

    async def step(self, action):
        reward = 0

        if action == "START_MOWING":
            if self.weather == "SUNNY" and self.battery > 30 and self.schedule:
                self.activity = "MOWING"
                reward += 10
            else:
                self.activity = "ERROR"
                reward -= 10

        elif action == "RETURN_TO_DOCK":
            self.activity = "DOCKED"
            reward += 2

        elif action == "CHARGE":
            if self.activity == "DOCKED":
                self.battery = min(100, self.battery + 20)
                reward += 5
            else:
                reward -= 2

        elif action == "WAIT":
            reward += 0

        elif action == "SEND_ALERT":
            if self.obstacle:
                reward += 3
            else:
                reward -= 1

        # Environment dynamics
        if self.activity == "MOWING":
            self.battery -= 10
            if self.battery <= 10:
                self.activity = "ERROR"
                reward -= 10

        next_state = self.get_state()
        return next_state, reward


# ---------------- RL Agent ---------------- #
class RLAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.5):
        self.Q = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_Q(self, state, action):
        return self.Q.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(ACTIONS)
        q_values = {a: self.get_Q(state, a) for a in ACTIONS}
        return max(q_values, key=q_values.get)

    def update(self, state, action, reward, next_state):
        old_q = self.get_Q(state, action)
        next_max = max([self.get_Q(next_state, a) for a in ACTIONS], default=0)
        new_q = old_q + self.alpha * (reward + self.gamma * next_max - old_q)
        self.Q[(state, action)] = new_q

    def adjust_epsilon(self, episode_reward):
        # Reduce exploration if reward is improving
        if episode_reward > 0:
            self.epsilon = max(0.05, self.epsilon * 0.99)


# ---------------- Training Loop ---------------- #
async def train(env, agent, episodes=50, verbose=True):
    reward_history = []

    for ep in range(episodes):
        state = env.reset()
        episode_reward = 0
        errors = 0
        successes = 0
        actions_taken = []

        for step in range(500):
            action = agent.choose_action(state)
            next_state, reward = await env.step(action)
            agent.update(state, action, reward, next_state)

            episode_reward += reward
            actions_taken.append(action)

            if reward < 0:
                errors += 1
            if reward > 5:
                successes += 1

            if verbose and ep % 10 == 0 and step < 3:
                print(f"[EP {ep}] STATE={state} ACTION={action} REWARD={reward}")

            state = next_state

        reward_history.append(episode_reward)
        agent.adjust_epsilon(episode_reward)

        if verbose:
            most_common = max(set(actions_taken), key=actions_taken.count)
            print(
                f"EP {ep:03d} | Reward={episode_reward:4d} "
                f"Errors={errors:3d} Successes={successes:3d} "
                f"Top Action={most_common} | Epsilon={agent.epsilon:.2f}"
            )

    return reward_history


# ---------------- Main Function ---------------- #
def main():
    env = SimpleMowerEnv()
    agent = RLAgent()
    rewards = asyncio.run(train(env, agent, episodes=50, verbose=True))

    print("\nTraining complete!")
    print("Final epsilon:", agent.epsilon)
    print("Q-table size:", len(agent.Q))
    print("Reward history (last 10):", rewards[-10:])


if __name__ == "__main__":
    main()
