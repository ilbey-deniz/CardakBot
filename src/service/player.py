import random

class Player:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.is_stunned = False
        self.immunity_turns = 0

    def attack(self, target):
        if not self.is_stunned and not target.is_immune():
            damage = random.randint(1, 10)
            target.take_damage(damage)
            return f"{self.name} attacks {target.name} for {damage} damage."
        else:
            return f"{self.name} cannot attack due to stun or immunity."

    def aoe_attack(self, targets):
        if not self.is_stunned:
            total_damage = 0
            for target in targets:
                if not target.is_immune():
                    damage = random.randint(1, 5)
                    target.take_damage(damage)
                    total_damage += damage
            return f"{self.name} performs AoE attack, dealing {total_damage} damage to targets."
        else:
            return f"{self.name} cannot perform AoE attack due to stun."

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def apply_stun(self):
        self.is_stunned = True

    def remove_stun(self):
        self.is_stunned = False

    def apply_immunity(self, turns):
        self.immunity_turns = turns

    def is_immune(self):
        return self.immunity_turns > 0

    def reduce_immunity_turns(self):
        if self.immunity_turns > 0:
            self.immunity_turns -= 1