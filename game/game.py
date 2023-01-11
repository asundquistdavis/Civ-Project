# create new game object
# start server 
# loop
#   game updates turn
#   server serves appropriate pages
#   client post changes
#   server listens for changes and serves changes

class Game():
    def __init__(self) -> None:
        self.players: list[Game.Player] = []
        self.board: Game.Board
        self.turn: int = 0
        self.phase: Game.Phase = Game.Phase(self, 'start_of_game')

    class Board():
        def __init__(self) -> None:
            pass

    class Phase():
        PHASES: 'list[str]' = ['census', 'movement', 'trade cards', 'purhcases' ]

        def __init__(self, game, phase_name) -> None:
            self.game = game
            self.phase_name: str = phase_name

        def next(self):
            self.game.phase = Game.Phase(self)

    class Player():
        def __init__(self) -> None:
            pass