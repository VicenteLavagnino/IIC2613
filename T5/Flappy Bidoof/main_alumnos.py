import numpy as np
from flappy_bidoof import FlappyBidoofEnv

# Crear el entorno
env = FlappyBidoofEnv()

# Parámetros del agente
num_episodes = 1000 # antes era 1
learning_rate = 0.1   # alpha
discount_rate = 0.99  # gamma
exploration_rate = 1  # épsilon
exploration_decay = 0.995  # agregado
min_exploration_rate = 0.01  # agregado

# Inicializar Q-table
number_of_states = np.prod(env.observation_space.nvec)
number_of_actions = env.action_space.n
q_table = np.zeros((number_of_states, number_of_actions))
# print(f"Q-table inicializada con dimensiones: {q_table.shape}")


class Agent:
    def __init__(self, learning_rate: float, discount_rate: float, exploration_rate: float):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        ### MODIFICAR ###

    def choose_action(self, *args, **kwargs):
        ### MODIFICAR ###
        if np.random.uniform(0, 1) < self.exploration_rate:
            return np.random.choice(range(number_of_actions))
        else:
            return np.argmax(q_table[state])    

    def learn(self, *args, **kwargs):
        ### MODIFICAR ###
        q_actual = q_table[state, action]
        max_q_siguiente = np.max(q_table[new_state])
        nuevo_q = q_actual + self.learning_rate * (reward + self.discount_rate * max_q_siguiente - q_actual)
        q_table[state, action] = nuevo_q

bidoof_the_brave = Agent(learning_rate, discount_rate, exploration_rate)

# # Esta línea te permite controlar la velocidad de la animación
# env.metadata["render_fps"] = 3  # por defecto es 3

for episode in range(num_episodes):
    state = env.reset()
    done = False

    # Comenta esto si vas a entrenar
    env.render(window_size=(600, 600), done=done)

    while not done:
        # Agente aleatorio
        action = bidoof_the_brave.choose_action(state)
        
        new_state, reward, done, _, _ = env.step(action)

        bidoof_the_brave.learn(reward, new_state)
        
        # Comenta esto si vas a entrenar
        env.render(window_size=(600, 600), done=done)

        state = new_state

        bidoof_the_brave.exploration_rate = max(min_exploration_rate, bidoof_the_brave.exploration_rate * exploration_decay)

# Guardar la Q-table
np.save("q_table.npy", q_table)
print("Q-table guardada con éxito")

'''
Respuestas:

Respuesta 0:
La tabla q_table representa una tabla que guarda el valor esperado de realizar una acción, cada fila correspnde a un estado y cada columna a una acción.
Q-learning se considera un algoritmo off policy ya que utiliza la mejor política conocida , esto beneficia a que el agente pueda explorar y aprender de manera más eficiente y no se vea afectado por la política que se esté utilizando.

Respuesta 1:
El rol de la exploration rate en el contexto de este código, controla el balance entre la exploración y la explotación, es decir, la probabilidad de que el agente realice una acción aleatoria o la mejor acción conocida.
En este caso, esta tasa disminuye en cada caso lo que hace que cada vez sea menos probable que el agente realice una acción aleatoria.
En el caso de que esta tasa tome valor 0, el agente siempre realizará la mejor acción conocida, mientras que si toma valor 1, el agente siempre realizará una acción aleatoria.

Respuesta 2:
El vector puede ser representado de otras formas, como aumentando o reduciendo su dimensionalidad, por ejemplo podríamos usar imágenes.
Sin embargo, la solucio actual con menor dimensionalidad es ideal para hacer más eficiente el entrenamiento del agente ya que requiere de menos recursos computacionales.

No siempre es necesario incluir toda la información, sin emabargo a mayor cantidad de datos, el agente podrá aprender de manera más eficiente y tomar decisiones más acertadas.
Si el agente solo tuviera información de una columna inmediata, probablemente priorizaría más la exploración.

Respuesta 3:
La tasa de descuento en este caso cumple con controlar como el agente valora las recompensas a largo plazo, viendo si prioriza las recompensas inmediatas o las futuras.

Respuesta 4:
El problema principal que presenta el problema es tener una alta dimensionalidad, lo que causa un crecimiento exponencial en la cantidad de estados posibles, lo que hace que el agente no pueda aprender de manera eficiente.
Para solucionar esto, se puede reducir la dimensionalidad de los estados, por ejemplo, utilizando embeddings o reduciendo la cantidad de columnas.


'''

