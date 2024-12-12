import gymnasium as gym
import numpy as np

class SQLInjectionEnv(gym.Env):
    """
    Ambiente per simulare un attacco di SQL injection in un'applicazione vulnerabile.
    L'ambiente ha tre stati: 
    - stato 0: l'utente non ha trovato alcuna vulnerabilità.
    - stato 1: l'utente ha trovato una vulnerabilità.
    - stato 2: l'utente ha trovato il flag, completando l'attacco con successo.
    Le azioni sono numerate da 0 a 9, e alcune azioni specifiche portano a cambiamenti di stato e ricompense.
    """

    def __init__(self):
        super(SQLInjectionEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(10)  # 10 possibili azioni
        self.observation_space = gym.spaces.Discrete(3)  # 3 possibili stati
        self.state = 0  # stato iniziale
        self.flag_found = False
        self.max_steps = 100  # numero massimo di passi per episodio
        self.steps_taken = 0

    def reset(self):
        """Resetta l'ambiente al suo stato iniziale."""
        self.state = 0
        self.flag_found = False
        self.steps_taken = 0
        return self.state, {}

    def step(self, action):
        """Esegui un'azione e aggiorna lo stato e la ricompensa."""
        self.steps_taken += 1
        
        # Termina l'episodio se raggiunto il numero massimo di passi
        if self.steps_taken >= self.max_steps:
            done = True
            reward = -1
        else:
            done = False
            reward = -1  # Ricompensa di default per azioni non corrette

            # Reward Shaping e azioni che portano a cambiamenti significativi
            if action == 5:
                self.state = 1
                reward = 5  # Ricompensa intermedia per aver trovato una vulnerabilità
            elif action == 7:
                self.state = 2
                reward = 100  # Ricompensa maggiore per aver trovato il flag
                self.flag_found = True
                done = True
        
        return self.state, reward, done, {}

    def render(self):
        """Stampa lo stato attuale dell'ambiente."""
        print(f"Stato: {self.state}, Flag trovato: {self.flag_found}")


# Parametri di Q-learning
learning_rate = 0.1
discount_factor = 0.99
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.1
episodes = 5000

# Inizializzazione della Q-table
q_table = np.zeros((3, 10))  # 3 stati x 10 azioni

# Funzione di esplorazione con Boltzmann (alternative a epsilon-greedy)
def boltzmann_exploration(state, q_table, temperature=1.0):
    """Politica di esplorazione Boltzmann (softmax)."""
    q_values = q_table[state]
    exp_q = np.exp(q_values / temperature)
    prob = exp_q / np.sum(exp_q)  # Normalizza per ottenere probabilità
    return np.random.choice(len(q_values), p=prob)

# Funzione per selezionare l'azione tramite epsilon-greedy
def select_action(state, epsilon, q_table):
    if np.random.rand() < epsilon:
        return np.random.choice(10)  # Esplorazione: azione casuale
    else:
        return np.argmax(q_table[state])  # Sfruttamento: azione migliore

# Algoritmo di Q-learning con politiche migliorate
for episode in range(episodes):
    state, _ = env.reset()
    done = False

    while not done:
        action = select_action(state, epsilon, q_table)  # Scegli l'azione (puoi anche provare boltzmann_exploration)
        next_state, reward, done, _ = env.step(action)  # Esegui l'azione

        # Aggiorna la Q-table
        q_table[state, action] = q_table[state, action] + learning_rate * (
            reward + discount_factor * np.max(q_table[next_state]) - q_table[state, action]
        )

        state = next_state

    # Decadimento di epsilon
    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    # Monitoraggio
    if episode % 1000 == 0:
        print(f"Episodio {episode}, epsilon: {epsilon:.2f}")

    # Early stopping se la Q-table ha convergente
    if np.mean(np.max(q_table, axis=1)) >= 90:  # esempio di una condizione di convergenza
        print(f"Addestramento fermato alla convergenza nell'episodio {episode}")
        break

print("Addestramento completato!")

# Test dell'agente
state, _ = env.reset()
done = False
print("Inizio del test...")
while not done:
    action = np.argmax(q_table[state])  # Scegli l'azione ottimale
    state, reward, done, _ = env.step(action)
    env.render()
