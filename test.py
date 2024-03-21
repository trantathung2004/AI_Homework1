"""A set of example unit tests.
NOTE: Do not rely on these tests as they are just simple examples.
Your code will be tested on some secret instances of the problems!
"""

import unittest
from problems import NpuzzleNode, NqueensNode
from search import Astar,DFS,BFS
from copy import deepcopy
def is_attack_queen(queen1, queen2):
    y1, x1 = queen1
    y2, x2 = queen2
    # Check for queen attacks (same row, column, or diagonal)
    if y1 == y2 or x1 == x2 or abs(y1 - y2) == abs(x1 - x2):
        return True
    return False
def is_attack_knight(queen1, queen2):
    # Check for knight attacks
    y1, x1 = queen1
    y2, x2 = queen2
    knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    for move in knight_moves:
        ny, nx = y1 + move[0], x1 + move[1]
        if (ny, nx) == (y2, x2):
            return True
    return False

def count_attacks(queens):
    attack_count = 0
    n = len(queens)
    for i in range(n):
        attacking=[]
        for j in range(i + 1, n):
            if is_attack_queen(queens[i], queens[j]):
                y1, x1 = queens[i]
                y2, x2 = queens[j]
                valid_attack = True
                if y1-y2>0:
                    vert = range(0,y2-y1,-1)
                else:
                    vert = range(0,y2-y1)
                if x1-x2>0:
                    hort = range(0,y2-y1,-1)
                else:
                    hort = range(0,y2-y1)
                for k,l in list(zip(vert,hort)):
                    shadow_queen = deepcopy(queens[i])
                    shadow_queen =(shadow_queen[0]+k,shadow_queen[1]+l)
                    if shadow_queen in attacking:
                        valid_attack=False
                        break
                if valid_attack:
                    attack_count += 1
                attacking.append(queens[j])
            elif is_attack_knight(queens[i], queens[j]):
                attack_count += 1
    return attack_count

class TestNpuzzle(unittest.TestCase):
    def test_constucting_instances(self):
        """Test that an instance of NpuzzleNode can be created without an error.
        """
        input_str = '1  2  3  4\n5  6  7  8\n9 10  0 11\n13 14 15 12'
        npuzzle_root = NpuzzleNode(input_str=input_str)
        self.assertEqual(str(npuzzle_root), '  1  2  3  4\n  5  6  7  8\n  9 10    11\n 13 14 15 12\n')

    def test_goal_states(self):
        """Test that is_goal returns True when the state is the goal configuration.
        """
        final_str = "1  2  3  4\n5  6  7  8\n9 10 11 12\n13 14 15  0"
        npuzzle_node = NpuzzleNode(input_str=final_str)
        self.assertTrue(npuzzle_node.is_goal())

    def test_node_expansions(self):
        """Test that generate_children returns 4 children when the empty cell is in the middle region.
        """
        input_str = '1  2  3  4\n5  6  7  8\n9 10  0 11\n13 14 15 12'
        npuzzle_root = NpuzzleNode(input_str=input_str)
        children = npuzzle_root.generate_children()
        self.assertTrue(len(children) == 4) 

    def test_a_star_algorithm(self):
        """Test that the length of the solution to a sample initial configuration is correct,
        and the last state is the goal.
        """
        input_str = '1  2  3  4\n5  6  7  8\n9 10  0 11\n13 14 15 12'
        npuzzle_root = NpuzzleNode(input_str=input_str)
        npuzzle_path = Astar(npuzzle_root)
        self.assertEqual(len(npuzzle_path), 3)
        self.assertTrue(npuzzle_path[-1].is_goal())
    
    def test_bfs_algorithm(self):
        """Test that the length of the solution to a sample initial configuration is correct,
        and the last state is the goal.
        """
        input_str = '1  2  3  4\n5  6  7  8\n9 10  11 12\n13 14 0 15'
        npuzzle_root = NpuzzleNode(input_str=input_str)
        npuzzle_path = BFS(npuzzle_root)
        self.assertTrue(npuzzle_path[-1].is_goal())


class TestNQueens(unittest.TestCase):
    def test_constucting_instances(self):
        """Test that an instance of NqueensNode can be created without an error."""
        nqueens_root = NqueensNode(n=7)
        for i, a in enumerate(str(nqueens_root)):
            if i % 22 == 21:
                self.assertEqual(a, '\n')
            elif (i - i // 22) % 3 == 1:
                self.assertEqual(a, '.')
            else:
                self.assertEqual(a, ' ')

    def test_goal_states(self):
        """Test that is_goal returns True when the state is a goal configuration.
        """
        queen_positions = [(0, 0), (1, 3), (2, 4), (3, 6), (4, 1), (5, 2), (6, 5)]
        nqueens_node = NqueensNode(n=7)
        nqueens_node.queen_positions = queen_positions
        self.assertTrue(nqueens_node.is_goal())

    def test_node_expansions(self):
        """Test that generate_children returns without raising an error.
        """
        nqueens_root = NqueensNode(n=7)
        nqueens_root.generate_children()

    def test_a_star_algorithm(self):
        """Test that the length of the solution path is 8 when the board size is 7,
        the last state is the goal state, and there is no queen in the initial state."""
        nqueens_root = NqueensNode(n=7)
        nqueens_path = Astar(nqueens_root)
        self.assertEqual(len(nqueens_path), 8)
        self.assertEqual(len(nqueens_path[0].queen_positions), 0)
        self.assertTrue(nqueens_path[-1].is_goal())
    
    def test_a_star_algorithm(self):
        """Test that the A* solution did minimize the attack pair of nqueens."""
        nqueens_root = NqueensNode(n=7)
        nqueens_path = Astar(nqueens_root)
        self.assertEqual(len(nqueens_path), 8)
        self.assertEqual(len(nqueens_path[0].queen_positions), 0)
        self.assertTrue(nqueens_path[-1].is_goal())
        self.assertLessEqual(count_attacks(nqueens_path[-1].queen_positions),3)
        
    def test_dfs_algorithm(self):
        """Test that the length of the solution to a sample initial configuration is correct,
        and the last state is the goal.
        """
        nqueens_root = NqueensNode(n=7)
        nqueens_path = DFS(nqueens_root)
        self.assertTrue(nqueens_path[-1].is_goal())
if __name__ == '__main__':
    unittest.main()
