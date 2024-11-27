import gymnasium as gym
import numpy as np

class SQLInjectionEnv(gym.Env):
    """
    Ambiente di esempio per simulare un attacco di SQL injection
    """

    def __init__(self):
        super(SQLInjectionEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(10)
        self.observation_space = gym.spaces.Discrete(3)
        self.state = 0
        self.flag_found = False
        self.max_steps = 100
        self.steps_taken = 0

    def reset(self):
        self.state = 0
        self.flag_found = False
        self.steps_taken = 0
        return self.state, {}

    def step(self, action):
        self.steps_taken += 1
        if self.steps_taken >= self.max_steps:
            done = True
            reward = -1
        else:
            done = False
            reward = -1
            if action == 5:
                self.state = 1
                reward = 10
            elif action == 7:
                self.state = 2
                reward = 100
                self.flag_found = True
                done = True
        return self.state, reward, done, {}

    def render(self):
        print(f"Stato: {self.state}, Flag trovato: {self.flag_found}")

# Ambiente
env = SQLInjectionEnv()

# Parametri Q-learning
learning_rate = 0.1
discount_factor = 0.99
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.1
episodes = 5000

# Inizializzazione della Q-table
q_table = np.zeros((env.observation_space.n, env.action_space.n))

# Algoritmo di Q-learning
for episode in range(episodes):
    state, _ = env.reset()
    done = False

    while not done:
        # Politica ε-greedy
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Esplorazione
        else:
            action = np.argmax(q_table[state])  # Sfruttamento

        # Esegui l'azione
        next_state, reward, done, _ = env.step(action)

        # Aggiornamento Q-value
        q_table[state, action] = q_table[state, action] + learning_rate * (
            reward + discount_factor * np.max(q_table[next_state]) - q_table[state, action]
        )

        state = next_state

    # Decadimento di epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    # Monitoraggio
    if episode % 1000 == 0:
        print(f"Episodio {episode}, epsilon: {epsilon:.2f}")

print("Addestramento completato!")

# Test dell'agente
state, _ = env.reset()
done = False
print("Inizio del test...")
while not done:
    action = np.argmax(q_table[state])
    state, reward, done, _ = env.step(action)
    env.render()

