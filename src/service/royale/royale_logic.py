import random
from service.royale.player import Player
import json
import os 

class RoyaleLogic:
    def __init__(self, players):
        self.players = [Player(player) for player in players]


    def load_config(self):
        with open(os.path.join(os.getcwd(), os.pardir, "config.json"), "r") as file:
            config = file.read()
        return config

    def start_game(self):

        config = self.load_config()
        config_file = json.loads(config)

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
                index = random.randint(0, len(config_file["actions"]) - 1)
                attack = config_file["actions"][index]
                attack_name = attack["name"]
                if attack["type"] == "melee":
                    damage = config_file["actions"][index]["damage"]
                
                if attack["type"] == "ranged":
                    damage = config_file["actions"][index]["damage"]
                target.hp -= damage
                result.append(f"{player.name} {attack_name} {target.name} for {damage} damage, {target.name} remaining hp: {target.hp}")
        result.append(f"{self.players[0].name} is the winner!")

        return result
    
