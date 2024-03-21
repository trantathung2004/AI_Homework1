from node import Node
from copy import deepcopy

class NpuzzleNode(Node):
    """Extends the Node class to solve the 15 puzzle.

    Parameters
    ----------
    parent : Node, optional
        The parent node. It is optional only if the input_str is provided. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this puzzle it is the number of moves to reach this node from the initial configuration.
        It is optional only if the input_str is provided. Default is 0.

    board : list of lists
        The two-dimensional list that describes the state. It is a 4x4 array of values 0, ..., 15.
        It is optional only if the input_str is provided. Default is None.

    input_str : str
        The input string to be parsed to create the board.
        The argument 'board' will be ignored, if input_str is provided.
        Example: input_str = '1 2 3 4\n5 6 7 8\n9 10 0 11\n13 14 15 12' # 0 represents the empty cell

    Examples
    ----------
    Initialization with an input string (Only the first/root construction call should be formatted like this):
    >>> n = NpuzzleNode(input_str=initial_state_str)
    >>> print(n)
      5  1  4  8
      7     2 11
      9  3 14 10
      6 13 15 12

    Generating a child node (All the child construction calls should be formatted like this) ::
    >>> n = NpuzzleNode(parent=p, g=p.g+c, board=updated_board)
    >>> print(n)
      5  1  4  8
      7  2    11
      9  3 14 10
      6 13 15 12

    """

    def __init__(self, parent=None, g=0, board=None, input_str=None):
        # NOTE: You shouldn't modify the constructor
        
        if input_str:
            self.board = []
            for i, line in enumerate(filter(None, input_str.splitlines())):
                self.board.append([int(n) for n in line.split()])
        else:
            self.board = board

        super(NpuzzleNode, self).__init__(parent, g)

    def generate_children(self):
        """Generates children by trying all 4 possible moves of the empty cell.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """
        children = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        x, y = None, None

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    x, y = i, j
                    break
            if x is not None:
                break

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.board) and 0 <= new_y < len(self.board[new_x]):
                new_board = deepcopy(self.board)
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                child = NpuzzleNode(parent=self, g=self.g + 1, board=new_board)
                children.append(child)
        return children
        # TODO: add your code here
        # You should use self.board to produce children. Don't forget to create a new board for each child
        # e.g you can use copy.deepcopy function from the standard library.
        # pass

    def is_goal(self):
        """Decides whether this search state is the final state of the puzzle.

        Returns
        -------
            is_goal : bool
                True if this search state is the goal state, False otherwise.
        """
        # n = 1
        # for i in range(len(self.board)):
        #     for j in range(len(self.board[i])):
        #         if self.board[i][j] != n:
        #             if i != len(self.board)-1 or j != len(self.board[i])-1:
        #                 return False
        #         n += 1

        goal = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 0]
        ]
        return self.board == goal
        # TODO: add your code here
        # You should use self.board to decide.
        # pass

    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of moves
        required to reach the goal state from this node.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
        """
        h = 0
        size = len(self.board)
        for i in range(size):
            for j in range(size):
                current = self.board[i][j]
                if current != 0:
                    goal_x, goal_y = divmod(current-1, size)
                    h += abs(i - goal_x) + abs(j - goal_y)
        return h
        # TODO: add your code here
        # You may want to use self.board here.
        # pass
    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple([n for row in self.board for n in row])

    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = []  # String builder
        for row in self.board:
            for i in row:
                sb.append(' ')
                if i == 0:
                    sb.append('  ')
                else:
                    if i < 10:
                        sb.append(' ')
                    sb.append(str(i))
            sb.append('\n')
        return ''.join(sb)
    
    def __lt__(self, other):
        return self.f < other.f

class NqueensNode(Node):
    """Extends the Node class to solve the Superqueens problem.

    Parameters
    ----------
    parent : Node, optional
        The parent node. Default is None.

    g : int or float, optional
        The cost to reach this node from the start node : g(n).
        In this problem it is the number of pairs of superqueens that can attack each other in this state configuration.
        Default is 1.

    queen_positions : list of pairs
        The list that stores the x and y positions of the queens in this state configuration.
        Example: [(q1_y,q1_x),(q2_y,q2_x)]. Note that the upper left corner is the origin and y increases downward
        Default is the empty list [].
        ------> x
        |
        |
        v
        y

    n : int
        The size of the board (n x n)

    Examples
    ----------
    Initialization with a board size (Only the first/root construction call should be formatted like this):
    >>> n = NqueensNode(n=4)
    >>> print(n)
         .  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    Generating a child node (All the child construction calls should be formatted like this):
    >>> n = NqueensNode(parent=p, g=p.g+c, queen_positions=updated_queen_positions, n=p.n)
    >>> print(n)
         Q  .  .  .
         .  .  .  .
         .  .  .  .
         .  .  .  .

    """

    def __init__(self, parent=None, g=0, queen_positions=[], n=1):
        # NOTE: You shouldn't modify the constructor
        self.queen_positions = queen_positions
        self.n = n
        super(NqueensNode, self).__init__(parent, g)
    
    def addable(self, new_queen_pos):
        queens = self.queen_positions
        for queen in queens:
            if queen[1] == new_queen_pos[1]:
                return False
        return True
    
    def conflict_count(self, new_queen):
        queens = self.queen_positions
        count = 0

        [x, y] = new_queen
        for queen in queens:
            [i, j] = queen
            if (abs(x-i) == abs(y-j)) or abs(x-i) + abs(y-j) == 3:
                count += 1
        return count

    def generate_children(self):
        """Generates children by adding a new queen.

        Returns
        -------
            children : list of Nodes
                The list of child nodes.
        """
        # TODO: add your code here
        # You should use self.queen_positions and self.n to produce children.
        # Don't forget to create a new queen_positions list for each child.
        # You can use copy.deepcopy function from the standard library.
        
        # if self.is_goal():
        #     return []
        # children = []
        # for new_queen_pos in range(self.n):
        #     if not self.is_conflict(new_queen_pos):
        #         new_queen_pos = deepcopy(self.queen_positions)
        #         new_queen_pos.append(new_queen_pos)
        #         children.append(NqueensNode(self, self.g+1, new_queen_pos,self.n))
        # return children

        children = []
        if len(self.queen_positions) >= self.n:
            return []
        
        for i in range(self.n):
            if self.addable((len(self.queen_positions),i)):
                new_queen_pos = deepcopy(self.queen_positions)
                new_queen_pos.append((len(self.queen_positions),i))
                conflicts = self.conflict_count((len(self.queen_positions),i))
                new_node = NqueensNode(self, self.g+conflicts, new_queen_pos, self.n)
                children.append(new_node)
        return children
        pass

    # def is_conflict(self, new_queen_pos):
    #     for i in range(len(self.queen_positions)):
    #         if self.queen_positions[i] == new_queen_pos or \
    #             self.queen_positions[i] - i == new_queen_pos - len(self.queen_positions) or \
    #             self.queen_positions[i] + i == new_queen_pos + len(self.queen_positions):
    #             return True
    #     return False
    
    def is_goal(self):
        """Decides whether all the queens are placed on the board.

        Returns
        -------
            is_goal : bool
                True if all the queens are placed on the board, False otherwise.
        """
        # You should use self.queen_positions and self.n to decide.
        # TODO: add your code here
        return len(self.queen_positions) == self.n
        pass


    def _get_state(self):
        """Returns an hashable representation of this search state.

        Returns
        -------
            state: tuple
                The hashable representation of the search state
        """
        # NOTE: You shouldn't modify this method.
        return tuple(self.queen_positions)


    def evaluate_heuristic(self):
        """Heuristic function h(n) that estimates the minimum number of moves
        required to reach the goal state from this node.

        Returns
        -------
            h : int or float
                The heuristic value for this state.
                
        Note: to get FULL points for this puzzle, your heuristic also needs 
        to discourage the superqueens from attacking eachother (no diagonals 
        and no knight moves that is attacking other queens).
        """

        # TODO: add your code here
        return 0
        pass
    def __str__(self):
        """Returns the string representation of this node.

        Returns
        -------
            state_str : str
                The string representation of the node.
        """
        # NOTE: You shouldn't modify this method.
        sb = [[' . '] * self.n for i in range(self.n)]  # String builder
        for i, j in self.queen_positions:
            sb[i][j] = ' Q '
        return '\n'.join([''.join(row) for row in sb])
    
    def __lt__(self, other):
        return self.f < other.f