from pydantic import BaseModel, Field, ConfigDict, field_validator, SerializerFunctionWrapHandler, WrapSerializer
from typing import Annotated, Any, List
from pydantic_core import PydanticCustomError 
import json

def ser_number(value: Any, handler: SerializerFunctionWrapHandler) -> int:
    return handler(value) + 1

class Player(BaseModel):
    player_id: int
    username: str 
    player_base_hp: int = 10
    Player_current_hp: int = 10
    player_attack: int = 1
    mana: int = 0

class Enemy(BaseModel):
    enemy_id: int = 0
    enemy_name: str
    enemy_base_hp: int = 10
    enemy_current_hp: int = 10
    enemy_attack: int = 1

class Match(BaseModel):
    match_id: int
    player_id: int
    enemy_id: int
    current_round: int = 0

