from server.monopoly.PlayerData import PlayerData

__author__ = 'mateusz'

import unittest


class PlayerDataTestSimpleMove(unittest.TestCase):
    def setUp(self):
        self.player_data = PlayerData(0, 1500)

    def test_move_player_simple(self):
        self.player_data.movePlayer(10)
        self.assertEqual(self.player_data.fieldPosition, 10, 'incorrect player position')
        self.assertEqual(self.player_data.singleMoveChanges, [10], 'incorrect move change')

    def test_move_player_with_overflow(self):
        self.player_data.movePlayer(60)
        self.assertEqual(self.player_data.fieldPosition, 20, 'incorrect player position')
        self.assertEqual(self.player_data.singleMoveChanges, [60], 'incorrect move change')

    def test_move_player_full_round(self):
        self.player_data.movePlayer(40)
        self.assertEqual(self.player_data.fieldPosition, 0, 'incorrect player position')
        self.assertEqual(self.player_data.singleMoveChanges, [40], 'incorrect move change')


class PlayerDataTestToPosition(unittest.TestCase):
    def setUp(self):
        self.player_data = PlayerData(13, 1500)

    def test_move_player_to_position(self):
        self.player_data.movePlayerToField(25)
        self.assertEqual(self.player_data.fieldPosition, 25, 'incorrect player position')
        self.assertEqual(self.player_data.singleMoveChanges, [12], 'incorrect move change')

    def test_move_player_to_position_back(self):
        self.player_data.movePlayerToField(25, forward=False)
        self.assertEqual(self.player_data.fieldPosition, 25, 'incorrect player position')
        self.assertEqual(self.player_data.singleMoveChanges, [-28], 'incorrect move change')

    def test_move_player_to_the_same_position(self):
        self.player_data.movePlayerToField(13, forward=True)
        self.assertEqual(self.player_data.fieldPosition, 13, 'incorrect player position')
        self.assertEqual(self.player_data.singleMoveChanges, [], 'incorrect move change')

    def test_move_player_to_the_same_position_back(self):
        self.player_data.movePlayerToField(13, forward=False)
        self.assertEqual(self.player_data.fieldPosition, 13, 'incorrect player position')
        self.assertEqual(self.player_data.singleMoveChanges, [], 'incorrect move change')

class PlayerDataStartPassesTest(unittest.TestCase):
    def setUp(self):
        self.player_data = PlayerData(13, 1500)

    def test_move_player_no_start_pass(self):
        self.player_data.movePlayerToField(25)
        self.assertEqual(self.player_data.calculateStartPasses(), 0, 'incorrect start passes number')

    def test_move_player_no_start_pass_relative(self):
        self.player_data.movePlayer(25)
        self.assertEqual(self.player_data.calculateStartPasses(), 0, 'incorrect start passes number')

    def test_move_player_single_start_pass_border(self):
        self.player_data.movePlayerToField(40)
        self.assertEqual(self.player_data.calculateStartPasses(), 1, 'incorrect start passes number')

    def test_move_player_single_start_pass_border_relative(self):
        self.player_data.movePlayer(27)
        self.assertEqual(self.player_data.calculateStartPasses(), 1, 'incorrect start passes number')

    def test_move_player_potential_pass_backward(self):
        self.player_data.movePlayerToField(3, forward=False)
        self.assertEqual(self.player_data.calculateStartPasses(), 0, 'incorrect start passes number')

    def test_move_player_potential_pass_backward_relative(self):
        self.player_data.movePlayer(-10)
        self.assertEqual(self.player_data.calculateStartPasses(), 0, 'incorrect start passes number')

    def test_move_player_backward_pass_relative(self):
        self.player_data.movePlayer(-20)
        self.assertEqual(self.player_data.calculateStartPasses(), 0, 'incorrect start passes number')

    def test_move_player_backward_pass(self):
        self.player_data.movePlayerToField(35, forward=False)
        self.assertEqual(self.player_data.calculateStartPasses(), 0, 'incorrect start passes number')

    def test_move_player_backward_pass_end_on_zero(self):
        self.player_data.movePlayer(-13)
        self.assertEqual(self.player_data.calculateStartPasses(), 0, 'incorrect start passes number')

    def test_move_player_multiple_passes(self):
        self.player_data.movePlayerToField(35)
        self.player_data.movePlayer(17)
        self.player_data.movePlayerToField(10, forward=True)
        self.assertEqual(self.player_data.calculateStartPasses(), 2, 'incorrect start passes number')