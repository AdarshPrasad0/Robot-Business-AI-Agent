import random
import pytest

# --- Ground truth policy ---
GROUND_TRUTH_POLICY = {
    ("DOCKED", "CALM"): "START_MOWING",
    ("DOCKED", "WINDY"): "DOCK",
    ("MOWING", "CALM"): "PAUSE",
    ("MOWING", "WINDY"): "RETURN_TO_DOCK",
    ("PAUSED", "CALM"): "RESUME",
    ("PAUSED", "WINDY"): "DOCK",
    ("RETURNING", "CALM"): "DOCK",
    ("RETURNING", "WINDY"): "DOCK",
    ("ERROR", "CALM"): "CLEAR_ERROR",
    ("ERROR", "WINDY"): "CLEAR_ERROR",
}

ACTIONS = list(set(GROUND_TRUTH_POLICY.values()))
STATES = list(GROUND_TRUTH_POLICY.keys())


# --- RL Agent ---
class RLAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.2):
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


# --- Environment ---
class MowerEnv:
    def step(self, state, action):
        correct_action = GROUND_TRUTH_POLICY[state]
        reward = 1 if action == correct_action else -1
        # For simplicity, stay in same state (episodic)
        return state, reward


# --- Training loop ---
def train_agent(episodes=5000):
    env = MowerEnv()
    agent = RLAgent()
    for _ in range(episodes):
        state = random.choice(STATES)
        action = agent.choose_action(state)
        next_state, reward = env.step(state, action)
        agent.update(state, action, reward, next_state)
    return agent


# --- Pytest tests ---
def test_agent_learns_ground_truth():
    agent = train_agent(episodes=2000)
    for state in STATES:
        learned_action = agent.choose_action(state)
        assert learned_action == GROUND_TRUTH_POLICY[state]