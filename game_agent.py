"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

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
    #return moves_combined(game, player, param)
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(0.77 * my_moves + 0.23 * opp_moves)

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

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

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        # no legal moves left
        if legal_moves == []:
            return (-1, -1)
        # Default best move
        best_move = legal_moves[0]
        # Determine the search method
        if self.method == 'minimax':
            search_method = self.minimax
        elif self.method == 'alphabeta':
            search_method = self.alphabeta
        else:
            raise ValueError(
                'Method ' + str(self.method) + ' not supported.')
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if not self.iterative:
                fixed_depth = self.search_depth
                _, best_move = search_method(game, fixed_depth, maximizing_player=True)
            else:
                current_depth = 1
                while True: # continue to do this until we run out of time
                    _, best_move = search_method(game, current_depth, maximizing_player=True)
                    current_depth += 1
        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass
        # Return the best move from the last completed search iteration
        return best_move
    
    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        
        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        # List all legal moves
        legal_moves = game.get_legal_moves()
        if legal_moves == []:
            return self.score(game, self), (-1, -1)
        if depth == 1:
            children = [(self.score(game.forecast_move(m), self), m) for m in legal_moves]
        else:
            children = [(self.minimax(game.forecast_move(m),
                                      depth-1, not maximizing_player)[0], m)
                        for m in legal_moves]
        return max(children) if maximizing_player else min(children)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

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

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
        
        legal_moves = game.get_legal_moves()
        if depth == 0 or legal_moves == []:
            return self.score(game, self), (-1, -1)
        
        # Default values
        best_score = float('-inf') if maximizing_player else float('inf')
        best_move = legal_moves[0]
        
        for move in legal_moves:
            score, _ = self.alphabeta(game.forecast_move(move),
                                      depth-1,
                                      alpha=alpha,
                                      beta=beta,
                                      maximizing_player=not maximizing_player)
            if (maximizing_player and score > best_score) or \
                (not maximizing_player and score < best_score):
                best_move, best_score = move, score
                # only checking for pruning if best_score is updated
                if self.__prune__(alpha, beta, best_score, maximizing_player):
                    break
                alpha, beta = self.__update_limit__(alpha, beta, best_score, maximizing_player)
                
        return best_score, best_move
    
    def __prune__(self, old_alpha, old_beta, score, maximizing_player):
        """ Helper Function for alphabeta method
        Decide if we can prune the rest of the child nodes on the current branch
        Returns a boolean value
        """
        return (maximizing_player and old_beta <= score) or \
            (not maximizing_player and old_alpha >= score)
                    
    def __update_limit__(self, old_alpha, old_beta, score, maximizing_player):
        """ Helper Function for alphabeta method
        Update the alpha beta limit based on the score of a child node
        Return (new-alpha, new-beta) tuple
        """
        if maximizing_player:
            return score, old_beta
        else:
            return old_alpha, score    

                
                                              
                                              
                                                                
                                                      
            
            
            
