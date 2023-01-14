from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from time import sleep

class Game(models.Model):
    start_time = models.DateTimeField(default=timezone.localtime(timezone.now()).strftime('%Y-%m-%dT%H:%M:%S'))
    phase = models.CharField(max_length=15, default='pre_game')

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

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.user}'

    def getoradd_pre_game(self):
        if not self.game:
            game = Game()
            game.save()
            game.player_set.add(self)
            self.user.save()
            return self.game
        elif self.game.phase == 'pre_game':
            return self.game
        else:
            return None

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()