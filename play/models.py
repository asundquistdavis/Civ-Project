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
        elif self.current_game.phase == Game.Phases.pregame:
            return self.current_game
        else:
            return None

    def overwrite_game(self, gameid=None):
        if Game.objects.filter(id=gameid):
            game = Game.objects.get(id=gameid)
        else:
            game = Game()
            game.save()
        self.current_game = game
        self.save()
        return self.current_game

        
class Game(models.Model):
    start_time = models.DateTimeField(default=timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M:%S'))
    turn = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='current_turn', default=None, null=True)

    class Phases(models.TextChoices):
        pregame = 'PG', gtl('pre game')
        newgame = 'NG', gtl('start of game')
        census = 'CE', gtl('census')
        movement = 'MO', gtl('movement')

    phase = models.CharField(max_length=2, choices=Phases.choices, default=Phases.pregame)

    def __str__(self) -> str:
        return f'Game number {self.id} started on {self.start_time}'

    def start(self):
        print(f'starting game: {self}')
        self.phase = 'new_game'
        self.save()
        print(f'starting new phase: {self.phase}')
        sleep(20)
        self.phase = 'census'
        self.save()
        print(f'starting new phase: {self.phase}')
        return self
    
    def get_phase(self):
        return Game.Phases[self.phase]

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()