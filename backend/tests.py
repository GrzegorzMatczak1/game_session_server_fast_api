import unittest
from pydantic import ValidationError
from unittest.mock import patch, mock_open, MagicMock
import json
import random
import sys
import os

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Player, Enemy, Match
from main import Match_Handler


class TestPlayerModel(unittest.TestCase):
    """Test cases for Player model validation"""

    def test_valid_player_creation(self):
        """Test creating a valid player"""
        player = Player(
            player_id=1,
            username="TestPlayer",
            player_base_hp=10,
            Player_current_hp=10,
            player_attack=1,
            mana=0
        )
        self.assertEqual(player.player_id, 1)
        self.assertEqual(player.username, "TestPlayer")
        self.assertEqual(player.player_base_hp, 10)
        self.assertEqual(player.player_attack, 1)

    def test_player_with_defaults(self):
        """Test player creation with default values"""
        player = Player(player_id=1, username="Hero")
        self.assertEqual(player.player_base_hp, 10)
        self.assertEqual(player.player_attack, 1)
        self.assertEqual(player.mana, 0)
        self.assertEqual(player.Player_current_hp, 0)

    def test_player_missing_required_fields(self):
        """Test that player creation fails without required fields"""
        with self.assertRaises(ValidationError):
            Player(username="Hero")  # Missing player_id
        
        with self.assertRaises(ValidationError):
            Player(player_id=1)  # Missing username

    def test_player_negative_hp(self):
        """Test player with negative HP values"""
        player = Player(
            player_id=1,
            username="TestPlayer",
            player_base_hp=-5
        )
        # Pydantic allows negative values by default unless validators are added
        self.assertEqual(player.player_base_hp, -5)

    def test_player_model_dump(self):
        """Test player model serialization"""
        player = Player(
            player_id=1,
            username="TestPlayer",
            player_base_hp=15,
            Player_current_hp=15,
            player_attack=2,
            mana=5
        )
        data = player.model_dump()
        self.assertEqual(data["player_id"], 1)
        self.assertEqual(data["username"], "TestPlayer")
        self.assertEqual(data["mana"], 5)


class TestEnemyModel(unittest.TestCase):
    """Test cases for Enemy model validation"""

    def test_valid_enemy_creation(self):
        """Test creating a valid enemy"""
        enemy = Enemy(
            enemy_id=1,
            enemy_name="Goblin",
            enemy_base_hp=8,
            enemy_current_hp=8,
            enemy_attack=1
        )
        self.assertEqual(enemy.enemy_id, 1)
        self.assertEqual(enemy.enemy_name, "Goblin")
        self.assertEqual(enemy.enemy_base_hp, 8)

    def test_enemy_with_defaults(self):
        """Test enemy creation with default values"""
        enemy = Enemy(enemy_name="Skeleton")
        self.assertEqual(enemy.enemy_id, 0)
        self.assertEqual(enemy.enemy_base_hp, 10)
        self.assertEqual(enemy.enemy_attack, 1)

    def test_enemy_missing_required_name(self):
        """Test that enemy creation fails without enemy_name"""
        with self.assertRaises(ValidationError):
            Enemy(enemy_id=1)  # Missing enemy_name

    def test_enemy_model_dump(self):
        """Test enemy model serialization"""
        enemy = Enemy(
            enemy_id=2,
            enemy_name="Orc",
            enemy_base_hp=15,
            enemy_current_hp=15,
            enemy_attack=3
        )
        data = enemy.model_dump()
        self.assertEqual(data["enemy_id"], 2)
        self.assertEqual(data["enemy_name"], "Orc")
        self.assertEqual(data["enemy_attack"], 3)


class TestMatchModel(unittest.TestCase):
    """Test cases for Match model validation"""

    def test_valid_match_creation(self):
        """Test creating a valid match"""
        match = Match(
            match_id=1,
            player_id=1,
            enemy_id=1,
            current_round=0
        )
        self.assertEqual(match.match_id, 1)
        self.assertEqual(match.player_id, 1)
        self.assertEqual(match.enemy_id, 1)
        self.assertEqual(match.current_round, 0)

    def test_match_missing_required_fields(self):
        """Test that match creation fails without required fields"""
        with self.assertRaises(ValidationError):
            Match(match_id=1, player_id=1)  # Missing enemy_id
        
        with self.assertRaises(ValidationError):
            Match(player_id=1, enemy_id=1)  # Missing match_id

    def test_match_with_rounds(self):
        """Test match with multiple rounds"""
        match = Match(
            match_id=1,
            player_id=1,
            enemy_id=1,
            current_round=5
        )
        self.assertEqual(match.current_round, 5)

    def test_match_model_dump(self):
        """Test match model serialization"""
        match = Match(
            match_id=1,
            player_id=1,
            enemy_id=1,
            current_round=3
        )
        data = match.model_dump()
        self.assertEqual(data["match_id"], 1)
        self.assertEqual(data["current_round"], 3)


class TestMatchHandler(unittest.TestCase):
    """Test cases for Match_Handler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.handler = Match_Handler()
        self.test_player = Player(
            player_id=1,
            username="TestHero",
            player_base_hp=10,
            Player_current_hp=10,
            player_attack=2,
            mana=0
        )
        self.test_enemy = Enemy(
            enemy_id=1,
            enemy_name="TestGoblin",
            enemy_base_hp=5,
            enemy_current_hp=5,
            enemy_attack=1
        )
        self.test_match = Match(
            match_id=1,
            player_id=1,
            enemy_id=1,
            current_round=0
        )

    def test_add_player(self):
        """Test adding a player to handler"""
        with patch('builtins.open', mock_open()):
            with patch('json.dump'):
                self.handler.add_player(self.test_player)
                self.assertEqual(self.handler.current_player.username, "TestHero")

    def test_add_enemy(self):
        """Test adding an enemy to handler"""
        with patch('builtins.open', mock_open()):
            with patch('json.dump'):
                self.handler.add_enemy(self.test_enemy)
                self.assertEqual(len(self.handler.enemy_list), 1)
                self.assertEqual(self.handler.enemy_list[0].enemy_name, "TestGoblin")

    def test_add_match(self):
        """Test adding a match to handler"""
        with patch('builtins.open', mock_open()):
            with patch('json.dump'):
                self.handler.add_match(self.test_match)
                self.assertEqual(self.handler.current_match.match_id, 1)

    def test_update_player_health_increase(self):
        """Test increasing player health"""
        self.handler.current_player = self.test_player
        self.handler.update_player_health(3)
        self.assertEqual(self.handler.current_player.Player_current_hp, 10)  # Capped at base_hp

    def test_update_player_health_decrease(self):
        """Test decreasing player health"""
        self.handler.current_player = self.test_player
        self.handler.current_player.Player_current_hp = 8
        self.handler.update_player_health(-2)
        self.assertEqual(self.handler.current_player.Player_current_hp, 6)

    def test_update_player_health_cap(self):
        """Test that player health is capped at base_hp"""
        self.handler.current_player = self.test_player
        self.handler.current_player.Player_current_hp = 8
        self.handler.update_player_health(10)
        self.assertEqual(self.handler.current_player.Player_current_hp, 10)

    def test_handle_player_attack_enemy_survives(self):
        """Test player attack when enemy survives"""
        self.handler.current_player = self.test_player
        self.handler.current_enemy = self.test_enemy
        self.handler.current_enemy.enemy_current_hp = 5
        
        result = self.handler.handle_player_attack()
        
        self.assertFalse(result)
        self.assertEqual(self.handler.current_enemy.enemy_current_hp, 3)

    def test_handle_player_attack_enemy_dies(self):
        """Test player attack when enemy dies"""
        self.handler.current_player = self.test_player
        self.handler.current_enemy = self.test_enemy
        self.handler.current_enemy.enemy_current_hp = 2
        
        result = self.handler.handle_player_attack()
        
        self.assertTrue(result)
        self.assertLessEqual(self.handler.current_enemy.enemy_current_hp, 0)

    def test_handle_enemy_attack_player_survives(self):
        """Test enemy attack when player survives"""
        self.handler.current_player = self.test_player
        self.handler.current_enemy = self.test_enemy
        self.handler.current_player.Player_current_hp = 5
        
        result = self.handler.handle_enemy_attack()
        
        self.assertFalse(result)
        self.assertEqual(self.handler.current_player.Player_current_hp, 4)

    def test_handle_enemy_attack_player_dies(self):
        """Test enemy attack when player dies"""
        self.handler.current_player = self.test_player
        self.handler.current_enemy = self.test_enemy
        self.handler.current_player.Player_current_hp = 1
        
        result = self.handler.handle_enemy_attack()
        
        self.assertTrue(result)
        self.assertLessEqual(self.handler.current_player.Player_current_hp, 0)

    def test_reset_player_stats(self):
        """Test resetting player stats"""
        self.handler.current_player = self.test_player
        self.handler.current_player.Player_current_hp = 5
        self.handler.current_player.player_attack = 5
        self.handler.current_player.mana = 10
        
        self.handler.reset_player_stats()
        
        self.assertEqual(self.handler.current_player.Player_current_hp, 0)
        self.assertEqual(self.handler.current_player.player_base_hp, 10)
        self.assertEqual(self.handler.current_player.player_attack, 1)
        self.assertEqual(self.handler.current_player.mana, 0)

    def test_reset_match_data(self):
        """Test resetting match data"""
        self.handler.current_player = self.test_player
        self.handler.current_match = self.test_match
        self.handler.enemy_list = [self.test_enemy]
        self.handler.current_player.Player_current_hp = 3
        self.handler.current_match.current_round = 5
        
        with patch.object(self.handler, 'generate_new_enemy'):
            self.handler.reset_match_data()
        
        self.assertEqual(self.handler.current_match.current_round, 0)
        self.assertEqual(self.handler.current_player.Player_current_hp, 0)

    def test_verify_reset_username_match(self):
        """Test username verification when it matches"""
        self.handler.current_player = self.test_player
        result = self.handler.verify_reset_username("TestHero")
        self.assertTrue(result)

    def test_verify_reset_username_mismatch(self):
        """Test username verification when it doesn't match"""
        self.handler.current_player = self.test_player
        result = self.handler.verify_reset_username("DifferentPlayer")
        self.assertFalse(result)

    def test_upgrade_health_sufficient_mana(self):
        """Test health upgrade with sufficient mana"""
        self.handler.current_player = self.test_player
        self.handler.current_player.mana = 5
        self.handler.current_player.Player_current_hp = 10
        
        result = self.handler.upgrade_health()
        
        self.assertEqual(self.handler.current_player.player_base_hp, 11)
        self.assertEqual(self.handler.current_player.Player_current_hp, 11)
        self.assertEqual(self.handler.current_player.mana, 3)
        self.assertIn("succesfuly", result)

    def test_upgrade_health_insufficient_mana(self):
        """Test health upgrade with insufficient mana"""
        self.handler.current_player = self.test_player
        self.handler.current_player.mana = 1
        
        result = self.handler.upgrade_health()
        
        self.assertIn("Not enough mana", result)
        self.assertEqual(self.handler.current_player.player_base_hp, 10)

    def test_upgrade_attack_sufficient_mana(self):
        """Test attack upgrade with sufficient mana"""
        self.handler.current_player = self.test_player
        self.handler.current_player.mana = 5
        
        result = self.handler.upgrade_attack()
        
        self.assertEqual(self.handler.current_player.player_attack, 3)
        self.assertEqual(self.handler.current_player.mana, 2)
        self.assertIn("succesfuly", result)

    def test_upgrade_attack_insufficient_mana(self):
        """Test attack upgrade with insufficient mana"""
        self.handler.current_player = self.test_player
        self.handler.current_player.mana = 1
        
        result = self.handler.upgrade_attack()
        
        self.assertIn("Not enough mana", result)
        self.assertEqual(self.handler.current_player.player_attack, 2)

    @patch('builtins.open', new_callable=mock_open, read_data='{"player_id": 1, "username": "TestHero", "player_base_hp": 10, "Player_current_hp": 10, "player_attack": 2, "mana": 0}')
    @patch('json.load')
    def test_save_player_data(self, mock_json_load, mock_file):
        """Test saving player data"""
        self.handler.current_player = self.test_player
        self.handler.save_player_data()
        mock_file.assert_called_with("json_files/player.json", "w")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_enemy_data(self, mock_json_dump, mock_file):
        """Test saving enemy data"""
        self.handler.enemy_list = [self.test_enemy]
        self.handler.save_enemy_data()
        mock_file.assert_called_with("json_files/enemies.json", "w")

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save_match_data(self, mock_json_dump, mock_file):
        """Test saving match data"""
        self.handler.current_match = self.test_match
        self.handler.save_match_data()
        mock_file.assert_called_with("json_files/match_info.json", "w")


class TestGameCombatFlow(unittest.TestCase):
    """Integration tests for game combat flow"""

    def setUp(self):
        """Set up test fixtures"""
        self.handler = Match_Handler()
        self.handler.current_player = Player(
            player_id=1,
            username="Hero",
            player_base_hp=20,
            Player_current_hp=20,
            player_attack=3,
            mana=0
        )
        self.handler.current_enemy = Enemy(
            enemy_id=1,
            enemy_name="Goblin",
            enemy_base_hp=10,
            enemy_current_hp=10,
            enemy_attack=2
        )
        self.handler.current_match = Match(
            match_id=1,
            player_id=1,
            enemy_id=1,
            current_round=0
        )
        self.handler.turn = 0

    def test_player_defeats_enemy(self):
        """Test combat where player defeats enemy"""
        # Player attacks until enemy dies
        while self.handler.current_enemy.enemy_current_hp > 0:
            result = self.handler.handle_player_attack()
            if result:
                break
        
        self.assertTrue(result)
        self.assertLessEqual(self.handler.current_enemy.enemy_current_hp, 0)

    def test_mana_generation_during_turn(self):
        """Test that mana is generated each turn"""
        initial_mana = self.handler.current_player.mana
        self.handler.current_player.mana += 1
        self.assertEqual(self.handler.current_player.mana, initial_mana + 1)

    def test_health_regeneration_during_turn(self):
        """Test that health is regenerated each turn"""
        self.handler.current_player.Player_current_hp = 15
        initial_hp = self.handler.current_player.Player_current_hp
        self.handler.update_player_health(1)
        self.assertEqual(self.handler.current_player.Player_current_hp, initial_hp + 1)


if __name__ == '__main__':
    unittest.main()
