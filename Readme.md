Questo progetto implementa un ambiente personalizzato per simulare attacchi di SQL Injection utilizzando il framework Gymnasium. È incluso un agente di Reinforcement Learning (RL) basato sull'algoritmo Q-Learning.

  

Requisiti

  

Prima di eseguire il progetto, assicurati di avere i seguenti requisiti:

  

Librerie Python necessarie:

Gymnasium: Per l'ambiente RL.

NumPy: Per la gestione delle operazioni matematiche.

Installa le librerie con i seguenti comandi:

  

    pip install gymnasium
    
    pip install numpy

Sistema operativo:

Il codice è compatibile con qualsiasi sistema operativo in cui sia installato Python 3.7 o superiore.

  

Istruzioni per l'Esecuzione

  

Clona o copia il repository: Salva il codice in un file Python, ad esempio sql_injection_rl.py.

Avvia il file Python: Esegui il file dal terminale con il seguente comando:

    python sql_injection_rl.py

Addestramento:

L'agente verrà addestrato per 5000 episodi utilizzando l'algoritmo di Q-learning.

Ogni 1000 episodi, verrà mostrato il progresso dell'addestramento con il valore attuale di epsilon (fattore di esplorazione).

Test dell'agente: Dopo l'addestramento, l'agente sarà testato per verificare la sua capacità di navigare nell'ambiente e identificare il flag.

File principali

  

sql_injection_rl.py: Script principale che implementa l'ambiente di SQL Injection e il Q-Learning.

Moduli inclusi nello script:

**gymnasium: Per la creazione e gestione dell'ambiente.
numpy: Per operazioni matematiche e gestione della Q-table.**

Configurazione dell'algoritmo

  

Il Q-Learning utilizza i seguenti parametri configurabili:

  

learning_rate: Tasso di apprendimento (

α

α), default: 0.1.

discount_factor: Fattore di sconto (

γ

γ), default: 0.99.

epsilon: Probabilità di esplorazione iniziale, default: 1.0.

epsilon_decay: Decadimento di epsilon per ridurre l'esplorazione nel tempo, default: 0.995.

min_epsilon: Valore minimo di epsilon, default: 0.1.

episodes: Numero di episodi per l'addestramento, default: 5000.

Funzionalità

Simulazione di attacchi di SQL Injection con tre stati:

**Stato iniziale (0).
Vulnerabilità trovata (1).
Flag trovato (2).**

Ricompense:

-1 per azioni non utili.

+10 per identificare una vulnerabilità.

+100 per trovare il flag.

Prossimi Passi

Integrare algoritmi più avanzati come Deep Q-Learning per migliorare le prestazioni.

Espandere l'ambiente per includere più stati e azioni legati a scenari di hacking reali.
