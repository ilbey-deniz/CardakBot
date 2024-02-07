import random


class Royale:
    def __init__(self, *players):
        self.players = list(players)

    def start_royale(self):
        while all(player.is_alive() for player in self.players):
            self.round_royale()

    def round_royale(self):
        for player in self.players:
            player.reduce_immunity_turns()

        for player in self.players:
            if player.is_stunned:
                player.remove_stun()
                continue

            other_players = [p for p in self.players if p != player]

            # Example: 70% chance of regular attack, 30% chance of AoE attack
            if random.random() < 0.7:
                result = player.attack(random.choice(other_players))
            else:
                result = player.aoe_attack(other_players)

            print(result)

            # Example: 20% chance of stunning a random opponent
            if random.random() < 0.2:
                random.choice(other_players).apply_stun()
                print(f"{player.name} stuns a random opponent!")

            # Example: 10% chance of gaining immunity for 1 turn
            if random.random() < 0.1:
                player.apply_immunity(1)
                print(f"{player.name} gains immunity for 1 turn.")