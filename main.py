from fastapi import FastAPI
from models import Player, Enemy, Match
from typing import List
import json


app = FastAPI()

class Match_Handler:
    def __init__(self):
        self.current_player: Player
        self.current_enemy: Enemy
        self.current_match: Match
        self.turn: int
        self.enemy_list: List[Enemy] = []
        

    def add_player(self, new_player: Player):
        self.current_player = new_player
        self.save_player_data()

    def add_enemy(self, new_enemy: Enemy):
        self.enemy_list.append(new_enemy)
        self.save_enemy_data()

    def add_match(self, new_match: Match):
        self.current_match = new_match
        self.save_match_data()

    def save_player_data(self):
        with open("json_files/player.json", "w") as filep:
            
            json.dump(self.current_player.model_dump(), filep, indent=4)

        filep.close()
    
    def save_enemy_data(self):
        temp_enemy_list = []

        for e in self.enemy_list:
            temp_enemy_list.append(e.model_dump())

        with open("json_files/enemies.json", "w") as filee:
            
            json.dump(temp_enemy_list, filee, indent=4)

        filee.close()

    def save_match_data(self):
        with open("json_files/match_info.json", "w") as filem:
            json.dump(self.current_match.model_dump(), filem, indent=4)

        filem.close()
    
    def save_all_data(self):
        enemy_list_temp = []

        with open("json_files/player.json", "w") as filep:
            
            json.dump(self.current_player, filep, indent=4)

        filep.close()

        with open("json_files/enemies.json", "w") as filee:
            for e in self.enemy_list:
                enemy_list_temp.append(e.model_dump())
            
            json.dump(enemy_list_temp, filee, indent=4)

        filee.close()

        with open("json_files/match_info.json", "w") as filem:
            json.dump(self.current_match.model_dump(), filem, indent=4)

        filem.close()

    def load_data(self):
        try:
            with open("json_files/player.json", "r") as filep:
                player_content = json.load(filep)
                player = Player(**player_content)
                self.current_player = player

            filep.close()

            with open("json_files/enemies.json", "r") as filee:
                enemy_content = json.load(filee)

                for enemy_data in enemy_content:
                    enemy = Enemy(**enemy_data)
                    self.enemy_list.append(enemy)
            
            filee.close()

            with open("json_files/match_info.json", "r") as filem:
                match_content = json.load(filem)
                match = Match(**match_content)
                self.current_match = match

            filem.close()
        except FileNotFoundError:
            print("Certain files werent found!")
        except Exception as e:
            print(f"Error loading data: {e}")

#set up Match_Handler object
match_handle_object = Match_Handler()
match_handle_object.load_data()


#these are test endpoints. They are used to check the fast api app connection with the json database
@app.post("/player/add")
async def app_add_player(player: Player):
    match_handle_object.add_player(player)
    return player

@app.get("/player/get/")
async def app_get_player():
    return match_handle_object.current_player.model_dump()

@app.post("/enemy/add")
async def app_add_enemy(enemy: Enemy):
    match_handle_object.add_enemy(enemy)
    return enemy

@app.get("/enemy/getall")
async def app_get_all_enemies():
    enemy_dump_list = []
    for element in match_handle_object.enemy_list:
        enemy_dump_list.append(element.model_dump())
    return enemy_dump_list

@app.post("/match/add")
async def app_add_match(match: Match):
    match_handle_object.add_match(match)
    return match

@app.post("/match/get")
async def app_get_match():
    return match_handle_object.current_match.model_dump()

# endpoints to do

# progres round / generates new enemy, resets turns, saves game data, resets player save state when he lost

# proges turn(player_attacked: bool) / 1 apply player damage, 2 check if enemy can attack if yes attack the player, apply player mana and or regenerate hp

# upgrade player stats(stat_index: int) / stat_index = 1 -> hp++ && current_hp++, stat_index = 2 -> attack++ / player chose to upgrade these stats

# update player state(stat_index: int, ammount: int) / stat_index = 1 -> current_hp + ammount...