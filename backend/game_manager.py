import uuid
from enum import Enum
from core.board import create_ocean_grid, create_ship_info

class GameMode(str, Enum):
    AI = "ai"
    FRIEND = "friend"
    RANDOM = "random"

class GamePhase(str, Enum):
    PLACING = "placing"
    PLAYING = "playing"
    FINISHED = "finished"

class Player:
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.ocean_grid = create_ocean_grid()
        self.ship_info = create_ship_info()
        self.ships_placed = 0
        self.websocket = None

class Game:
    def __init__(self, game_id: str, mode: GameMode):
        self.game_id = game_id
        self.mode = mode
        self.phase = GamePhase.PLACING
        self.players: dict[str, Player] = {}    # player_id -> Player
        self.turn: str | None = None            # player_id of whose turn it is
        self.winner: str | None = None

    def add_player(self, player_id: str) -> Player:
        player = Player(player_id)
        self.players[player_id] = player
        return player
    
    def is_full(self) -> bool:
        return len(self.players) >= 2
    
    def both_players_placed(self) -> bool:
        return all(p.ships_placed == 5 for p in self.players.values())
    
class GameManager:
    def __init__(self):
        self.games: dict[str, Game] = {}    # game_id -> Game
        self._waiting_game_id: str | None = None # for random matchmaking

    def create_game(self, mode: GameMode) -> Game:
        game_id = str(uuid.uuid4())
        game = Game(game_id, mode)
        self._games[game_id] = game
        return game
    
    def get_game(self, game_id: str) -> Game | None:
        return self._games.get(game_id)
    
    def join_or_create_random(self) -> tuple[Game, bool]:
        """Returns (game, is_new). Joins waiting game if one exists, else creates one."""
        if self._waiting_game_id:
            game = self._games[self._waiting_game_id]
            self._waiting_game_id = None
            return game, False
        
        game = self.create_game(GameMode.RANDOM)
        self._waiting_game_id = game.game_id
        return game, True
    
    def remove_game(self, game_id: str):
        self._games.pop(game_id, None)
        if self._waiting_game_id == game_id:
            self._waiting_game_id = None

game_manager = GameManager()
