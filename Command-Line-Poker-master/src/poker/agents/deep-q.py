
class DeepQLearning:
    def __init__(self, game_state):
        self.game_state = game_state
        pass

    def choose_action(self):
        pass


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