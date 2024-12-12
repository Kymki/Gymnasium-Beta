Simulazione di Attacco di SQL Injection con Q-learning

Questa simulazione dimostra come un agente di Q-learning possa essere utilizzato per identificare e sfruttare una vulnerabilità di SQL injection in un'applicazione web vulnerabile. Il codice è composto da due parti principali:

Un server web vulnerabile creato con Flask. (Web_server.py)
Un agente di Q-learning che interagisce con il server per cercare di eseguire l'iniezione SQL.
Prerequisiti:
Python 3.6+ installato con le seguenti librerie:
```
Flask (per il server web vulnerabile)
Gymnasium (per l'ambiente di simulazione di Q-learning)
Requests (per inviare richieste HTTP al server web)
```
Passo 1: Installare le dipendenze

```
pip install -r requirements.txt
```
```
python3 -m venv sql_injection_env
```
Attiva l'ambiente virtuale:

Su Windows:
```
sql_injection_env\Scripts\activate
```
Su macOS/Linux:
```
source sql_injection_env/bin/activate
```
Installa le dipendenze necessarie:
```
pip install flask gymnasium requests numpy
```
Passo 2: Creare il server web vulnerabile

Passo 3: Avviare il server Flask
Avvia il server Flask eseguendo il file Web_server.py:
```
python Web_server.py
```
Il server sarà in esecuzione su http://localhost:5000 e avrà una vulnerabilità di SQL injection nell'endpoint /login.
Passo 4: Creare l'ambiente di Q-learning
Passo 5: Eseguire la simulazione
(è avviato su http://localhost:5000)?
```
python sql_injection_rl.py
```
Durante l'esecuzione, l'agente di Q-learning tenterà di identificare e sfruttare la vulnerabilità SQL injection nel server web. Se l'agente riesce a trovare una SQL injection funzionante, verrà fornita una ricompensa e il test terminerà.

Passo 6: Monitoraggio e risultati

Durante l'esecuzione del codice, progresso su console che indicano il progresso dell'agente durante il processo di addestramento, come ad esempio:
```
Episodio 1000, epsilon: 0.97
Episodio 2000, epsilon: 0.94
Episodio 3000, epsilon: 0.91
```
...
Una volta che l'agente ha completato l'addestramento, il programma eseguirà il test finale, mostrando lo stato attuale dell'ambiente e se l'attacco ha avuto successo.