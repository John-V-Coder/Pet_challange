import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
import pygame
import os
import time
from pet import Pet

class PetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Pet")

        self.pet_name = simpledialog.askstring("Pet Name", "What is your pet's name?")
        if not self.pet_name:
            self.pet_name = "Buddy"

        self.pet = Pet.load_from_file(self.pet_name)

        pygame.mixer.init()
        try:
            self.pet_sound = pygame.mixer.Sound("sounds/pet_sound.wav")
        except pygame.error:
            self.pet_sound = None

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack()

        # Load images
        self.images = {
            "happy": ImageTk.PhotoImage(Image.open("images/happy.png").resize((150, 150))),
            "neutral": ImageTk.PhotoImage(Image.open("images/neutral.png").resize((150, 150))),
            "sad": ImageTk.PhotoImage(Image.open("images/sad.png").resize((150, 150)))
        }

        self.pet_image_label = tk.Label(self.frame, image=self.get_mood_image())
        self.pet_image_label.grid(row=0, column=0, columnspan=3)
        self.pet_image_label.bind("<Enter>", self.show_tooltip)
        self.pet_image_label.bind("<Motion>", self.move_tooltip)
        self.pet_image_label.bind("<Leave>", self.hide_tooltip)

        self.tooltip = tk.Label(self.frame, text=f"Hi! I'm {self.pet.name} 🐾", bg="yellow", bd=1, relief="solid")
        self.tooltip.place_forget()

        # Stat bars
        self.hunger_bar = self.create_bar("Hunger", self.pet.hunger, 1)
        self.energy_bar = self.create_bar("Energy", self.pet.energy, 2)
        self.happiness_bar = self.create_bar("Happiness", self.pet.happiness, 3)
        self.xp_bar = self.create_bar("XP", self.pet.xp, 4, max_value=100)

        self.level_label = tk.Label(self.frame, text=f"Level: {self.pet.level}", font=("Arial", 12, "bold"))
        self.level_label.grid(row=5, column=0, columnspan=3, pady=(5, 10))

        # Buttons
        tk.Button(self.frame, text="🍽️ Eat", width=10, command=self.feed_pet).grid(row=6, column=0)
        tk.Button(self.frame, text="😴 Sleep", width=10, command=self.put_pet_to_sleep).grid(row=6, column=1)
        tk.Button(self.frame, text="🎾 Play", width=10, command=self.play_with_pet).grid(row=6, column=2)

        self.update_ui()

    def create_bar(self, label, value, row, max_value=10):
        tk.Label(self.frame, text=label).grid(row=row, column=0, sticky="w")
        bar = ttk.Progressbar(self.frame, length=200, maximum=max_value)
        bar.grid(row=row, column=1, columnspan=2)
        bar["value"] = value
        return bar

    def get_mood_image(self):
        if self.pet.happiness >= 7:
            return self.images["happy"]
        elif self.pet.happiness >= 4:
            return self.images["neutral"]
        else:
            return self.images["sad"]

    def play_sound(self):
        if self.pet_sound:
            self.pet_sound.play()

    def animate_pet(self):
        original = self.pet_image_label["image"]
        self.pet_image_label["image"] = ""
        self.root.update()
        time.sleep(0.1)
        self.pet_image_label["image"] = original

    def feed_pet(self):
        self.pet.eat()
        self.react_to_action()

    def put_pet_to_sleep(self):
        self.pet.sleep()
        self.react_to_action()

    def play_with_pet(self):
        self.pet.play()
        self.react_to_action()

    def react_to_action(self):
        self.play_sound()
        self.animate_pet()
        event = self.pet.random_event()
        if event:
            print(event)
        self.update_ui()
        self.pet.save_to_file()

    def update_ui(self):
        self.hunger_bar["value"] = self.pet.hunger
        self.energy_bar["value"] = self.pet.energy
        self.happiness_bar["value"] = self.pet.happiness
        self.xp_bar["value"] = self.pet.xp
        self.level_label.config(text=f"Level: {self.pet.level}")
        self.pet_image_label["image"] = self.get_mood_image()

    def show_tooltip(self, event):
        self.tooltip.place(x=event.x_root - self.root.winfo_rootx() + 10, y=event.y_root - self.root.winfo_rooty() + 10)

    def move_tooltip(self, event):
        self.tooltip.place(x=event.x_root - self.root.winfo_rootx() + 10, y=event.y_root - self.root.winfo_rooty() + 10)

    def hide_tooltip(self, event):
        self.tooltip.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = PetApp(root)
    root.mainloop()