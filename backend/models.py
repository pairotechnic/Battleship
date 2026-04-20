'''
    These are the Pydantic models that define the shape of data going in and out of your API,
    and the WebSocket message types that the server and client will exchange.
'''
# Standard Library Imports

# Third-Party Library Imports
from pydantic import BaseModel

# Local Application Imports
from game_manager import GameMode

# --------- HTTP Request/Response models ---------------- 

class CreateGameRequest(BaseModel):
    mode: GameMode
    player_id: str

class CreateGameResponse(BaseModel):
    game_id: str
    mode: GameMode

class JoinGameRequest(BaseModel):
    game_id: str
    player_id: str

# ---------- WebSocket Message Models --------------

class PlaceShipMessage(BaseModel):
    type: str = "place_ship"
    row: int
    col: int
    length: int
    orientation: str    # "horizontal" | "vertical"

class ShotMessage(BaseModel):
    type: str = "shot"
    row: int
    col: int

class GameStateMessage(BaseModel):
    type: str = "game_state"
    phase: str  # "placing" | "playing" | "finished"
    turn: str | None # player_id of whose turn it is
    result: str | None # "miss" | "hit" | "sink" | None
    winner: str | None

class ErrorMessage(BaseModel):
    type: str = "error"
    message: str

class PlayerJoinedMessage(BaseModel):
    type: str = "player_joined"
    player_id: str
