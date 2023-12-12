import os
import random

from collections import deque
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.optimizers import Adam
import numpy as np

from src.poker.enums.betting_move import BettingMove

class QValuesCallback(Callback):
    def __init__(self, model, state):
        self.model = model
        self.state = state
        
    def on_epoch_end(self, epoch, logs=None):
        updated_q_values = self.model.predict(self.state)
        #print("Updated Q-values:", updated_q_values)

class DeepQLearning:
    def __init__(self, game_state):
        #print(f"AGENT DEEP Q CONSTRUCTOR")
        self.game_state = game_state
        self.action_size = 4 # may change
        self.model_backup = "model_backup.h5"
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.actions = [BettingMove.CALLED, BettingMove.RAISED, BettingMove.FOLDED, BettingMove.CALLED]

    def choose_action(self):
        #print(f"AGENT DEEP Q choose_action")
        # Example pseudocode:
        current_state = self._build_features_vector()
        print(f"INPUT: {current_state}")
        action = self.act(current_state)
        #print(f"Choosing... {action}")
        return self.index_to_action(action) #BettingMove.CALLED # need to convert

    def act(self, state):
        #print(f"AGENT DEEP Q act")
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action index
    def remember(self, state, action, reward, next_state, done):
        #print(f"AGENT DEEP Q remember")
        feature_state = state.make_features()
        feature_state_numpy = np.array(feature_state)# for f in feature_state]
        feature_next_state = next_state.make_features()
        feature_next_state_numpy = np.array(feature_next_state) #[np.array(f) for f in feature_next_state]
        feature_action = self.action_to_index(action)

        self.memory.append((feature_state_numpy, feature_action, reward, feature_next_state_numpy, done))

    def index_to_action(self, index):
        return self.actions[index % len(self.actions)]

    def action_to_index(self, action):
        index = self.actions.index(action)
        return 0 if index == -1 else index

    def update_state(self, start_state, action, new_state):
        #print(f"AGENT DEEP Q update_state to {new_state}")
        self.game_state = new_state
        if new_state.game.check_game_over():
            reward = new_state.game.table.pots[0][0]
            done = True
        else:
            reward = 0
            done = False

        self.remember(start_state, action, reward, new_state, done)

    def update_model_q_values(self, batch_size):
        #self.model.summary()
        #print(f"AGENT DEEP Q update_model_q_values")
        if len(self.memory) < batch_size:
            batch_size = len(self.memory)
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                prediction = self.model.predict(next_state)
                amax = np.amax(prediction[0])
                target = reward + self.gamma * amax
            target_f = self.model.predict(state)
            #self.model.summary()
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0, callbacks=[QValuesCallback(self.model, state)])
            #self.model.summary()
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def _build_features_vector(self):
        #print(f"AGENT DEEP Q _build_features_vector")
        return self.game_state.make_features()

    def _build_model(self):
        #print(f"AGENT DEEP Q _build_model")
        model = Sequential()

        model.add(Dense(24, input_dim=1, activation='relu'))
        # input_n = Input(shape=(16,), name="input")
        # x = Dense(24, activation='relu')(input_n)
        model.add(Dense(self.action_size, activation='linear'))
        #out = Dense(2)(x)

        # model = Model(inputs=[input_n], outputs=out)
        #model.compile(optimizer='adam', loss='mse')
        optimizer = Adam(learning_rate=self.learning_rate)
        model.compile(loss='mse', optimizer=optimizer)

        # Check for compilation success
        #print("Model successfully compiled.")

        # Access compilation information
        # print("Optimizer:", model.optimizer)
        # print("Loss function:", model.loss)
        # print("Metrics:", model.metrics_names)
        #
        # # Print model summary
        # model.summary()

        # if os.path.isfile(self.model_backup):
        #     model.load_weights(self.model_backup)
        #     self.epsilon = self.epsilon_min
        return model

    def save_model(self):
        #print(f"AGENT DEEP Q save_model")
        self.model.save(self.model_backup, clear_optimizer=True)


"""
import random
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from src.poker.enums.betting_move import BettingMove
from src.poker.enums.computer_playing_style import ComputerPlayingStyle
from src.poker.players.player import Player
from src.poker.players.computer import Computer

class DeepQLearningAgent(Computer):
    def __init__(self, name, state_size, action_size):
        super().__init__(name, ComputerPlayingStyle.DEEP_Q_LEARNING)
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model.
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def choose_next_move(self, table_raise_amount: int, times_table_raised: int, last_table_bet: int) -> BettingMove:
        # Here you'll need to define how the agent decides its next move.
        # This will involve converting the game state to the input format expected by the model,
        # and then choosing an action based on the model's output.
        
        # Example pseudocode:
        # current_state = <convert current game state to neural network input format>
        # action = self.act(current_state)
        # return <convert action to a BettingMove>
        return

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action index

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_state_and_learn(self, state, action, reward, next_state, done):
        self.remember(state, action, reward, next_state, done)
        batch_size = 32  # You might want to adjust this value
        if len(self.memory) > batch_size:
            self.replay(batch_size)

    # Add any additional methods or overrides needed for the Deep Q-Learning agent
"""