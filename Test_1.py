import gymnasium as gym
from gymnasium import spaces
import numpy as np

class SQLInjectionEnv(gym.Env):
    """
    Ambiente di esempio per simulare un attacco di SQL injection
    """

    def __init__(self):
        super(SQLInjectionEnv, self).__init__()
        # Definizione dello spazio delle azioni (10 azioni possibili, es. tentativi di iniezioni)
        self.action_space = spaces.Discrete(10)
        
        # Definizione dello spazio di osservazione (stato del server)
        # 3 stati possibili: 0 - Inizio, 1 - Vulnerabilità trovata, 2 - Flag trovato
        self.observation_space = spaces.Discrete(3)

        self.state = 0  # Stato iniziale
        self.flag_found = False
        self.max_steps = 100  # Numero massimo di passi per episodio
        self.steps_taken = 0  # Passi già eseguiti

    def reset(self):
        """
        Reset dell'ambiente. Restituisce lo stato iniziale.
        """
        self.state = 0  # Inizio, il flag non è ancora trovato
        self.flag_found = False
        self.steps_taken = 0
        return self.state, {}

    def step(self, action):
        """
        Azione eseguita dall'agente (tentativo di attacco)
        """
        self.steps_taken += 1

        if self.steps_taken >= self.max_steps:
            done = True
            reward = -1  # Penalizzazione per non aver trovato il flag
        else:
            done = False
            reward = -1  # Default penalty

            if action == 5:  # Azione specifica per la SQL injection
                self.state = 1  # Vulnerabilità trovata
                reward = 10  # Ricompensa per aver trovato la vulnerabilità
            elif action == 7:  # Azione per eseguire un'iniezione corretta
                self.state = 2  # Flag trovato
                reward = 100  # Ricompensa per il flag trovato
                self.flag_found = True
                done = True  # Termina l'episodio

        return self.state, reward, done, {}

    def render(self):
        """
        Visualizza lo stato attuale dell'ambiente.
        """
        print(f"Stato: {self.state}, Flag trovato: {self.flag_found}")

# Creazione dell'ambiente
env = SQLInjectionEnv()

# Test dell'ambiente con un agente che esegue azioni casuali
state, _ = env.reset()
for _ in range(100):
    action = env.action_space.sample()  # Seleziona un'azione casuale
    state, reward, done, _ = env.step(action)
    env.render()
    if done:
        print("Episodio terminato!")
        break

env.close()
