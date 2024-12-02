# Example Python Code
class Animal:
    def __init__(self, species):
        self.species = species

    def make_sound(self):
        return f"{self.species} makes a sound."


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__("Dog")
        self.name = name
        self.breed = breed

    def make_sound(self):
        return "Woof!"

    def fetch(self, item):
        return f"{self.name} fetches the {item}."


def main():
    my_dog = Dog("Buddy", "Golden Retriever")
    print(my_dog.make_sound())
    print(my_dog.fetch("ball"))
