import numpy as np

class MazeMDP:

    # up, right, down, left
    _direction_deltas = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ]
    _num_actions = 4
    def __init__(self,
                 reward_grid,
                 terminal_flag,
                 obstacle_flag,
                 action_probabilities,
                 no_action_probability):

        
        self._terminal_flag = terminal_flag
        self._obstacle_flag = obstacle_flag
        self._reward_grid = reward_grid
        self._T = self._calculate_transition_matrix(
            action_probabilities,
            no_action_probability,
            obstacle_flag
        )
        
    @property
    def reward_grid(self):
        return self._reward_grid
    
    @property
    def shape(self):
        return self._reward_grid.shape

    @property
    def size(self):
        return self._reward_grid.size

 

   
    def _policy_iteration(self, *, utility_grid,
                          policy_grid, discount=1.0):
        # policy iteration algorthim
        r, c = self.from_indices_to_coordinates()

        M, N = self.shape

        utility_grid = (
            self._reward_grid +
            discount * ((utility_grid.reshape((1, 1, 1, M, N)) * self._T)
                        .sum(axis=-1).sum(axis=-1))[r, c, policy_grid.flatten()]
            .reshape(self.shape)
        )

        utility_grid[self._terminal_flag] = self._reward_grid[self._terminal_flag]

        return self.optimal_policy(utility_grid), utility_grid
    
    def policy_evalution(self, discount=1.0,
                              iterations=10):
        # perform policy evalution multiple times
        utility_grids, policy_grids = self._init_ans(iterations)

        policy_grid = np.random.randint(0, self._num_actions,
                                        self.shape)
        utility_grid = self._reward_grid.copy()

        for i in range(iterations):
            policy_grid, utility_grid = self._policy_iteration(
                policy_grid=policy_grid,
                utility_grid=utility_grid
            )
            policy_grids[:, :, i] = policy_grid
            utility_grids[:, :, i] = utility_grid
        return policy_grids, utility_grids


    def from_indices_to_coordinates(self, indices=None):
        if indices is None:
            indices = np.arange(self.size)
        return np.unravel_index(indices, self.shape)
    
    def _value_iteration(self, utility_grid, discount=1.0):
        # value iteration algorthim
        out = np.zeros_like(utility_grid)
        M, N = self.shape
        for i in range(M):
            for j in range(N):
                out[i, j] = self._calculate_utility((i, j),
                                                    discount,
                                                    utility_grid)
        return out
    
    def value_evalution(self, discount=1.0,
                             iterations=10):
        # perform value iteration multiple times
           utility_grids, policy_grids = self._init_ans(iterations)
    
           utility_grid = np.zeros_like(self._reward_grid)
           for i in range(iterations):
               utility_grid = self._value_iteration(utility_grid=utility_grid)
               policy_grids[:, :, i] = self.optimal_policy(utility_grid)
               utility_grids[:, :, i] = utility_grid
           return policy_grids, utility_grids
       
        
    def optimal_policy(self, utility_grid):
        # compute the best policy by maximizing utility
        M, N = self.shape
        return np.argmax((utility_grid.reshape((1, 1, 1, M, N)) * self._T)
                         .sum(axis=-1).sum(axis=-1), axis=2)

    def _init_ans(self, depth):
        #intialize utitlty and policy grids
        M, N = self.shape
        utility_grids = np.zeros((M, N, depth))
        policy_grids = np.zeros_like(utility_grids)
        return utility_grids, policy_grids

    def _calculate_transition_matrix(self,
                                  action_probabilities,
                                  no_action_probability,
                                  obstacle_flag):
        ## compute transition matrix
        M, N = self.shape

        T = np.zeros((M, N, self._num_actions, M, N))

        r0, c0 = self.from_indices_to_coordinates()

        T[r0, c0, :, r0, c0] += no_action_probability

        for action in range(self._num_actions):
            for offset, P in action_probabilities:
                direction = (action + offset) % self._num_actions

                dr, dc = self._direction_deltas[direction]
                r1 = np.clip(r0 + dr, 0, M - 1)
                c1 = np.clip(c0 + dc, 0, N - 1)

                temp_flag = obstacle_flag[r1, c1].flatten()
                r1[temp_flag] = r0[temp_flag]
                c1[temp_flag] = c0[temp_flag]

                T[r0, c0, action, r1, c1] += P

        terminal_locs = np.where(self._terminal_flag.flatten())[0]
        T[r0[terminal_locs], c0[terminal_locs], :, :, :] = 0
        return T

    def _calculate_utility(self, loc, discount, utility_grid):
        if self._terminal_flag[loc]:
            return self._reward_grid[loc]
        row, col = loc
        return np.max(
            discount * np.sum(
                np.sum(self._T[row, col, :, :, :] * utility_grid,
                       axis=-1),
                axis=-1)
        ) + self._reward_grid[loc]