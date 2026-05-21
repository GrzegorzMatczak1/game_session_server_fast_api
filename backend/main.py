from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Player, Enemy, Match
from typing import List
import json
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Match_Handler:
    def __init__(self):
        self.current_player: Player
        self.current_enemy: Enemy
        self.current_match: Match
        self.turn: int = 1
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

    def save_enemy_data(self):
        temp_enemy_list = []

        for e in self.enemy_list:
            temp_enemy_list.append(e.model_dump())

        with open("json_files/enemies.json", "w") as filee:
            
            json.dump(temp_enemy_list, filee, indent=4)

    def save_match_data(self):
        with open("json_files/match_info.json", "w") as filem:
            json.dump(self.current_match.model_dump(), filem, indent=4)
    
    def save_all_data(self):
        enemy_list_temp = []

        with open("json_files/player.json", "w") as filep:
            
            json.dump(self.current_player.model_dump(), filep, indent=4)
        
        print("Saved player data")


        with open("json_files/enemies.json", "w") as filee:
            for e in self.enemy_list:
                enemy_list_temp.append(e.model_dump())
            
            json.dump(enemy_list_temp, filee, indent=4)

        print("Saved enemy data")

        with open("json_files/match_info.json", "w") as filem:
            json.dump(self.current_match.model_dump(), filem, indent=4)

        print("Saved match data")

        

    def load_data(self):
        try:
            with open("json_files/player.json", "r") as filep:
                player_content = json.load(filep)
                player = Player(**player_content)
                self.current_player = player

            with open("json_files/enemies.json", "r") as filee:
                enemy_content = json.load(filee)
                self.enemy_list = []
                for enemy_data in enemy_content:
                    enemy = Enemy(**enemy_data)
                    self.enemy_list.append(enemy)

            with open("json_files/match_info.json", "r") as filem:
                match_content = json.load(filem)
                match = Match(**match_content)
                self.current_match = match

            self.current_enemy = next(
                (e for e in self.enemy_list if e.enemy_id == self.current_match.enemy_id),
                self.enemy_list[0]
            )

        except FileNotFoundError:
            print("Certain files werent found!")
        except Exception as e:
            print(f"Error loading data: {e}")

    def reset_player_stats(self):
        self.current_player.Player_current_hp = 10
        self.current_player.player_base_hp = 10
        self.current_player.player_attack = 1
        self.current_player.mana = 0

    def reset_match_data(self):
        self.current_match.current_round = 1
        self.generate_new_enemy()
        self.reset_player_stats()

    def verify_reset_username(self, given_username: str):
        temp_name = self.current_player.username
        return temp_name == given_username
            


    def generate_new_enemy(self):
        self.current_enemy = self.enemy_list[random.randint(0, len(self.enemy_list) - 1)]
        self.current_enemy.enemy_current_hp = self.current_enemy.enemy_base_hp
        self.current_match.enemy_id = self.current_enemy.enemy_id

    def update_player_health(self, ammount):
        self.current_player.Player_current_hp += ammount
        if(self.current_player.Player_current_hp >= self.current_player.player_base_hp):
            self.current_player.Player_current_hp = self.current_player.player_base_hp

    def handle_player_attack(self):
        self.current_enemy.enemy_current_hp -= self.current_player.player_attack
        if(self.current_enemy.enemy_current_hp <= 0):
            return True
        return False
    
    def handle_enemy_attack(self):
        self.current_player.Player_current_hp -= self.current_enemy.enemy_attack
        if(self.current_player.Player_current_hp <= 0):
            return True
        return False
        
    def upgrade_health(self):
        if(self.current_player.mana >= 2):
            self.current_player.Player_current_hp += 1
            self.current_player.player_base_hp += 1
            self.current_player.mana -= 2
            return "Player health succesfuly upgraded"
        
        return "Not enough mana!"

    def upgrade_attack(self):
        if(self.current_player.mana >= 3):
            self.current_player.player_attack += 1
            self.current_player.mana -= 3
            return "Player attack succesfuly upgraded"
    
        return "Not enough mana!"
        


#set up Match_Handler object
match_handle_object = Match_Handler()
match_handle_object.load_data()

# a test endpoint to check whether the fast api server is running properly
@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/round/get")
async def app_get_current_round():
    return match_handle_object.current_match.current_round

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

@app.get("/enemy/get")
async def app_get_whole_enemy():
    return match_handle_object.current_enemy.model_dump()

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

# start match
@app.post("/match/start")
async def app_start_match(logged_username: str):

    match_handle_object.load_data()
    match_handle_object.current_enemy.enemy_current_hp = match_handle_object.current_enemy.enemy_base_hp

    if not match_handle_object.verify_reset_username(logged_username):
            match_handle_object.reset_match_data()
            match_handle_object.reset_player_stats()
            match_handle_object.current_player.username = logged_username
            match_handle_object.save_all_data()
    
    return match_handle_object.current_player.model_dump()
# progres round / generates new enemy, resets turns, saves game data, resets player save state when he lost

@app.get("/match/save")
async def app_match_save():
    match_handle_object.save_all_data()
    return "Saved!"

@app.get("/round/progres")
async def app_round_progres():

    match_handle_object.turn = 0

    if(match_handle_object.current_player.Player_current_hp <= 0):

        match_handle_object.reset_player_stats()
        match_handle_object.generate_new_enemy()
        match_handle_object.current_match.current_round = 1
        match_handle_object.save_all_data()

        return True #Has ended
    
    match_handle_object.current_match.current_round += 1
    match_handle_object.generate_new_enemy()
    match_handle_object.update_player_health(5)
    match_handle_object.current_player.mana += 1
    match_handle_object.save_all_data()

    return False #Match continues

# proges turn(player_attacked: bool) / 1 apply player damage, 2 check if enemy can attack if yes attack the player, apply player mana and or regenerate hp

@app.post("/turn/progres")
async def app_turn_progres(player_attacked: bool):
    match_handle_object.turn += 1
    if(player_attacked):
        if(match_handle_object.handle_player_attack()):
            return await app_round_progres()
    if(match_handle_object.turn % 5 == 0):
        if(match_handle_object.handle_enemy_attack()):
            return await app_round_progres()
    else:
        match_handle_object.update_player_health(1)
    
    match_handle_object.current_player.mana += 1
    
    return False #Match continues




# upgrade player stats(stat_index: int) / stat_index = 1 -> hp++ && current_hp++, stat_index = 2 -> attack++ / player chose to upgrade these stats

@app.post("/player/upgrade")
async def app_upgrade_player_stats(stat_index: int):
    if(stat_index == 1):
        return match_handle_object.upgrade_health()
    if(stat_index == 2):
        return match_handle_object.upgrade_attack()
    else:
        return False
