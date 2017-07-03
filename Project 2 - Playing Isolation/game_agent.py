"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def run_away(game, player):
    """Maximize the distance between the player and the opponent, i.e., run
    away from the opponent. Returns the absolute difference between the sum of
    the location vectors, where larger differences equal higher scores. Not
    submitted.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_location = game.get_player_location(game.get_opponent(player))
    if opp_location == None:
        return 0.

    own_location = game.get_player_location(player)
    if own_location == None:
        return 0.

    return float(abs(sum(opp_location) - sum(own_location)))


def custom_score_3(game, player):
    """run_towards
    Minimize the distance between the player and the opponent, i.e., run
    towards from the opponent. Returns the negative of the absolute difference
    between the sum of the location vectors, therefore rewarding smaller
    absolute differences with higher scores. Not submitted.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp_location = game.get_player_location(game.get_opponent(player))
    if opp_location == None:
        return 0.

    own_location = game.get_player_location(player)
    if own_location == None:
        return 0.

    return float(-abs(sum(opp_location) - sum(own_location)))


def custom_score_2(game, player):
    """open_move_walls
    Outputs a score equal to the difference in the number of moves
    available to the two players, while penalizing the moves for the
    maximizing player that are against the wall and rewarding the moves
    for the minimizing player that are against the wall. Not submitted.


    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    own_v_wall = [move for move in own_moves if move[0] == 0
                  or move[0] == (game.height - 1)
                  or move[1] == 0
                  or move[1] == (game.width - 1)]

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_v_wall = [move for move in opp_moves if move[0] == 0
                  or move[0] == (game.height - 1)
                  or move[1] == 0
                  or move[1] == (game.width - 1)]

    # Penalize/reward move count if some moves are against the wall
    return float(len(own_moves) - len(own_v_wall)
                 - len(opp_moves) + len(opp_v_wall))


def custom_score(game, player):
    """Outputs a score equal to the difference in the number of moves
    available to the two players, while penalizing the moves for the
    maximizing player that are in the corner and rewarding the moves for the
    minimizing player that are in the corner. These penalties/rewards are
    elevated near end game through a game state factor. Submitted.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).
    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    game_state_factor = 1
    # Being in a corner in late game (less than 25% of board empty) is bad
    if len(game.get_blank_spaces()) < game.width * game.height / 4.:
        game_state_factor = 4

    # Four corners
    corners = [(0, 0),
               (0, (game.width - 1)),
               ((game.height - 1), 0),
               ((game.height - 1), (game.width - 1))]

    own_moves = game.get_legal_moves(player)
    own_in_corner = [move for move in own_moves if move in corners]
    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_in_corner = [move for move in opp_moves if move in corners]

    # Penalize/reward move count if some moves are in the corner
    return float(len(own_moves) - (game_state_factor * len(own_in_corner))
                 - len(opp_moves) + (game_state_factor * len(opp_in_corner)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        def max_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if depth == 0 or not game.get_legal_moves():
                return self.score(game, self)
            if not game.get_legal_moves():
                return game.utility(self)

            depth -= 1
            v = float("-inf")
            for m in game.get_legal_moves():
                v = max(v, min_value(game.forecast_move(m), depth))
            return v

        def min_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
            if depth == 0:
                return self.score(game, self)
            if not game.get_legal_moves():
                return game.utility(self)

            depth -= 1
            v = float("inf")
            for m in game.get_legal_moves():
                v = min(v, max_value(game.forecast_move(m), depth))
            return v

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if not game.get_legal_moves():
            return game.utility(self)
        if depth == 0:
            return self.score(game, game.active_player)

        main_score = float('-inf')
        best_move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if legal_moves:
            best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        for each_move in legal_moves:
            game_subbranch = game.forecast_move(each_move)
            score = min_value(game_subbranch, depth - 1)
            if score > main_score:
                best_move = each_move
                main_score = score
        return best_move


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        recent_best = best_move

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            s_depth = 1
            while True:
                current_move = self.alphabeta(game, s_depth)
                if current_move != (-1, -1):
                    best_move = current_move
                    recent_best = current_move
                else:
                    best_move = recent_best
                    break
                s_depth += 1

        except SearchTimeout:
            return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout
        if depth == 0:
            return self.score(game, self)
        node_value = float("-inf")
        for move in game.get_legal_moves():
            node_value = max(node_value, self.min_value(game.forecast_move(move), depth-1, alpha, beta))
            if node_value >= beta:
                return node_value
            alpha = max(alpha, node_value)
        return node_value

    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout
        if depth == 0:
            return self.score(game, self)
        node_value = float("inf")
        for move in game.get_legal_moves():
            node_value = min(node_value, self.max_value(game.forecast_move(move), depth-1, alpha, beta))
            if node_value <= alpha:
                return node_value
            beta = min(beta, node_value)
        return node_value

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Get legal moves for active player
        legal_moves = game.get_legal_moves()

        # Game over terminal test
        if not legal_moves:
            # -inf or +inf from point of view of maximizing player
            return game.utility(self)

        # Search depth reached terminal test
        if depth == 0:
            # Heuristic score from point of view of maximizing player
            return self.score(game, self)

        # Best for maximizing player is highest score
        best_move = (-1, -1)
        best_score = float("-inf")

        for move in legal_moves:
            # Forecast_move switches the active player
            val = self.min_value(game.forecast_move(move), depth-1, alpha, beta)
            if val >= best_score:
                best_score = val
                best_move = move
                alpha = best_score
        return best_move