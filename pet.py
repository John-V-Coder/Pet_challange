import json
import os
import random

class Pet:
    def __init__(self, name, hunger=5, energy=5, happiness=5, tricks=None, xp=0, level=1):
        self.name = name
        self.hunger = hunger
        self.energy = energy
        self.happiness = happiness
        self.tricks = tricks if tricks else []
        self.xp = xp
        self.level = level

    def eat(self):
        self.hunger = max(0, self.hunger - 3)
        self.happiness = min(10, self.happiness + 1)
        self.gain_xp(5)

    def sleep(self):
        self.energy = min(10, self.energy + 5)
        self.gain_xp(3)

    def play(self):
        if self.energy >= 2:
            self.energy -= 2
            self.happiness = min(10, self.happiness + 2)
            self.hunger = min(10, self.hunger + 1)
            self.gain_xp(7)
        else:
            print(f"{self.name} is too tired to play. 🥱")

    def train(self, trick):
        self.tricks.append(trick)
        self.happiness = min(10, self.happiness + 1)
        self.gain_xp(10)

    def show_tricks(self):
        if self.tricks:
            print(f"{self.name} knows the following tricks:")
            for trick in self.tricks:
                print(f"  - {trick}")
        else:
            print(f"{self.name} doesn't know any tricks yet.")

    def get_status(self):
        print(f"\n🐾 {self.name}'s Status:")
        print(f"  Hunger: {self.hunger}/10")
        print(f"  Energy: {self.energy}/10")
        print(f"  Happiness: {self.happiness}/10")
        print(f"  XP: {self.xp}")
        print(f"  Level: {self.level}")

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= 100:
            self.level += 1
            self.xp -= 100
            print(f"🎉 {self.name} leveled up to Level {self.level}!")

    def save_to_file(self):
        data = {
            "name": self.name,
            "hunger": self.hunger,
            "energy": self.energy,
            "happiness": self.happiness,
            "tricks": self.tricks,
            "xp": self.xp,
            "level": self.level
        }
        with open(f"{self.name.lower()}_save.json", "w") as f:
            json.dump(data, f)
        print("💾 Game saved!")

    @classmethod
    def load_from_file(cls, name):
        filename = f"{name.lower()}_save.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
            print("📂 Save file found. Loading...")
            return cls(
                name=data["name"],
                hunger=data["hunger"],
                energy=data["energy"],
                happiness=data["happiness"],
                tricks=data.get("tricks", []),
                xp=data.get("xp", 0),
                level=data.get("level", 1)
            )
        else:
            print("📁 No save file found. Starting a new pet.")
            return cls(name)

    def random_event(self):
        events = [
            ("found a snack! 🍖", lambda: (self._change("hunger", -1), self._change("energy", 1))),
            ("found a toy! 🧸", lambda: self._change("happiness", 2)),
            ("got muddy in the rain! 🌧️", lambda: self._change("happiness", -2)),
        ]
        if random.random() < 0.3:
            event, effect = random.choice(events)
            effect()
            return f"{self.name} {event}"
        return None

    def _change(self, attr, amount):
        value = getattr(self, attr)
        value = max(0, min(10, value + amount))
        setattr(self, attr, value)
