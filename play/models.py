from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as gtl
from django.dispatch import receiver
from time import sleep

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_game = models.ForeignKey('Game', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user}'

    def getoradd_game(self):
        if not self.current_game:
            game = Game()
            game.save()
            game.player_set.add(self)
            self.user.save()
            return self.current_game
        elif self.current_game.phase == 'pre game':
            return self.current_game
        else:
            return None

    def overwrite_game(self, gameid=None):
        print('query:', self.current_game.id == gameid)
        game = Game() if not (Game.objects.filter(id=gameid) and self.current_game.id != gameid) else Game.objects.get(id=gameid)
        game.save()
        self.current_game = game
        self.user.save()
        return self.current_game

    def send_data(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
        }

class Game(models.Model):
    start_time = models.DateTimeField(default=timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M:%S'))
    turn = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='current_turn', default=None, null=True)
    PHASES = [
        'pre game',
        'new game',
        'census',
        'movement',
        'trade',
        'purchases',
    ]
    phase = models.CharField(max_length=15, default='pre game')

    def __str__(self) -> str:
        return f'Game number {self.id} started on {self.start_time}'

    def start(self):
        print(f'starting game: {self}')
        self.phase = 'new game'
        self.save()
        print(f'starting new phase: {self.phase}')
        sleep(20)
        self.phase = 'census'
        self.save()
        print(f'starting new phase: {self.phase}')
        return self

    def get_phase(self):
        return self.phase

    def next_phase(self):
        phase = self.PHASES.index(self.phase)
        self.phase = self.PHASES[phase+1]
        return self.phase

    def send_data(self):
        return {
            'palyers': [dict(player) for player in self.player_set_all()],
            'turn': self.turn.user.username,
            'phase': self.phase
        }

class Territory(models.Model):
    name = models.CharField(max_length=30)


class TerritoryOccupation(models.Model):
    pass

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()