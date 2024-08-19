from traits import Traits
import random
import math


class Organism:

    next_id = 0

    def __init__(self, dna, x, y, energy, environment):
        self.traits = Traits.decode_dna(dna)  # Decode DNA into traits
        self.x = x
        self.y = y
        self.dna = dna
        self.id = Organism.next_id
        Organism.next_id += 1
        self.environment = environment
        # self.size = traits.get_trait('size')
        self.size = self.traits.get('size')
        self.speed = self.traits.get('speed')
        self.metabolism_rate = dna.get_gene('metabolism_rate')
        self.color = self.traits.get('skin_color')
        self.food_sense_distance = dna.get_gene('food_sense_distance')
        self.food_types = dna.get_gene('food_types')
        # self.food_required_to_grow = traits.get('food_required_to_grow')
        # self.food_required_to_be_fertile = traits.get('food_required_to_be_fertile')
        self.activeness = dna.get_gene('activeness')  # gene for movement activity
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))  # Initial random direction
        self.hunger = 50  # Start with 50 hunger
        self.age = 0  # Initialize age to 0
        self.max_age = dna.get_gene('max_age')  # Maximum age determined by DNA
        self.alive = True  # State to check if organism is alive
        self.energy = energy  # New energy attribute
        self.max_energy = self.traits.get('max_energy')
        self.reproduction_rate = self.traits.get('reproduction_rate')
        self.fertile_development = 0

    def move_towards(self, target_x, target_y):
        """Move the organism towards a target point (target_x, target_y)."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            # Normalize direction and scale by speed
            dx /= distance
            dy /= distance

            self.x += dx * self.speed  # * self.speed_modifier
            self.y += dy * self.speed  # * self.speed_modifier

    @staticmethod
    def calculate_death_probability(age, max_age):
        if age < 0.6 * max_age:
            return 0  # No death probability before 60% of max age
        k = 2  # Steepness constant, adjust as needed
        death_probability = 1 - math.exp(-((age - 0.6 * max_age) / (0.4 * max_age)) * k)
        return death_probability

    def update(self, environment):
        """Update the organism's state."""
        if not self.is_alive():
            return

        self.age += 1  # Increment age each tick

        # Check for death probability
        if random.random() < self.calculate_death_probability(self.age, self.max_age):
            self.alive = False
            return

        closest_food = None
        closest_distance = float('inf')
        moved = False

        if 'plant' in self.food_types:
            for food_x, food_y in environment.get_food_positions():
                distance = math.hypot(food_x - self.x, food_y - self.y)
                if distance < closest_distance and distance <= self.food_sense_distance:
                    closest_food = (food_x, food_y)
                    closest_distance = distance

        if 'prey' in self.food_types:
            for prey in environment.get_organisms():
                if prey != self and prey.dna.get_gene('food_types') != 'prey' and prey.is_alive():
                    distance = math.hypot(prey.x - self.x, prey.y - self.y)
                    if distance < closest_distance and distance <= self.food_sense_distance:
                        closest_food = (prey.x, prey.y)
                        closest_distance = distance

        if closest_food:
            self.move_towards(*closest_food)
            moved = True

            if math.hypot(closest_food[0] - self.x, closest_food[1] - self.y) < self.size:
                if 'plant' in self.food_types:
                    food_energy = environment.get_food_energy(closest_food)
                    self.consume_food(environment, closest_food, food_energy)
                elif 'prey' in self.food_types:
                    prey = environment.get_organism_at(closest_food)
                    if prey:
                        self.consume_prey(environment, prey)

        else:
            # Decide whether to move based on activeness
            if random.random() < self.activeness:
                moved = True
                # Add small random perturbations to direction more frequently
                self.direction = (
                    self.direction[0] + random.uniform(-0.3, 0.3),
                    self.direction[1] + random.uniform(-0.3, 0.3)
                )

                # Normalize direction
                direction_magnitude = math.hypot(self.direction[0], self.direction[1])
                if direction_magnitude > 0:
                    self.direction = (
                        self.direction[0] / direction_magnitude,
                        self.direction[1] / direction_magnitude
                    )

                # Move according to the direction
                self.x += self.direction[0] * self.speed
                self.y += self.direction[1] * self.speed

                # Handle border collisions by bouncing off the edges
                if self.x <= 0 or self.x >= environment.width - 1:
                    self.direction = (-self.direction[0], self.direction[1])  # Reverse X direction
                    self.x = max(0, min(environment.width - 1, self.x))  # Keep within bounds

                if self.y <= 0 or self.y >= environment.height - 1:
                    self.direction = (self.direction[0], -self.direction[1])  # Reverse Y direction
                    self.y = max(0, min(environment.height - 1, self.y))  # Keep within bounds

        self.metabolize(moved)

        self.speed = Traits.calculate_speed(self.dna, self)
        self.size = Traits.calculate_size(self.dna, self)

        if (self.age > self.max_age * 0.1) and self.energy >= 31:
            self.fertile_development += 1
            self.energy -= 1

        if (self.age > self.max_age * 0.1) and self.fertile_development >= 30:
            self.reproduce(self.dna)

    def reproduce(self, dna):
        """Attempt to reproduce if conditions are met."""
        child_dna = dna.mutate()  # Mutate the DNA slightly
        child_x = self.x + random.uniform(-5, 5)
        child_y = self.y + random.uniform(-5, 5)
        child_energy = 30  # Transfer energy to the child
        self.fertile_development -= 30  # Deduct energy from the parent
        child = Organism(child_dna, child_x, child_y, child_energy, self.environment)
        self.environment.add_organism(child)
        # print(f'{self.id}, energy {self.energy} reproduced {child.id}')

    def is_alive(self):
        if self.energy <= 0:
            self.alive = False
        return self.alive

    def consume_food(self, environment, food_position, food_energy):
        """Consume food and decrease hunger."""
        self.hunger -= food_energy  # Decrease hunger by a fixed amount
        environment.remove_food(food_position)
        # print(f' {self.id}, energy {self.energy} consumed plant for {food_energy}')
        self.energy += food_energy

    def consume_prey(self, environment, prey):
        """Consume another organism."""
        self.hunger -= prey.size  # Decrease hunger by prey size or energy
        prey.alive = False  # Kill the prey
        # print(f' {self.id}, energy {self.energy} consumed prey {prey.id} for {prey.energy}')

        self.energy += prey.energy  # Gain energy from prey
        # print('consumed energy', prey.energy)

    def metabolize(self, moved):
        """Reduce energy over time based on metabolism rate."""
        if moved:
            self.energy -= self.metabolism_rate / 2  # * self.speed_modifier / 10
        else:
            self.energy -= self.metabolism_rate / 10
