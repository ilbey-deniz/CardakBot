import random
from service.player import Player


class RoyaleLogic:
    def __init__(self, players):
        self.players = [Player(player) for player in players]


    def start_game(self):
        result = []
        while len(self.players) > 1:
            for player in self.players:
                if player.hp <= 0:
                    self.players.remove(player)
                    result.append(f"{player.name} has been eliminated")
                    continue
                target = random.choice(self.players)
                while target == player:
                    target = random.choice(self.players)
                damage = random.randint(1, 5)
                target.hp -= damage
                result.append(f"{player.name} attacked {target.name} for {damage} damage, {target.name} remaining hp: {target.hp}")
        result.append(f"{self.players[0].name} is the winner!")

        return result