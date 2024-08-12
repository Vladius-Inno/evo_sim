import math
import pygame
import random
import matplotlib.pyplot as plt
import numpy as np


class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.center_x = width / 2
        self.center_y = height / 2
        self.temperature_border1 = 20
        self.temperature_border2 = 10
        self.light_radius = min(width, height) / 2  # Radius of light circle
        self.food_positions = []
        self.food_energy = {}  # Map positions to energy levels

    def get_light_level(self, x, y):
        """Calculate the light level at coordinates (x, y)."""
        distance_from_center = math.sqrt((x - self.center_x) ** 2 + (y - self.center_y) ** 2)
        if distance_from_center > self.light_radius:
            return 0
        else:
            return 1 - (distance_from_center / self.light_radius)

    def get_temperature(self, x, y):
        """Calculate the temperature at coordinates (x, y)."""
        # Calculate the temperature range
        temperature_range = self.temperature_border2 - self.temperature_border1

        # Distance from the left border (x = 0) to the current x-coordinate
        distance_from_left_border = x / self.width

        # Calculate temperature based on the position
        return self.temperature_border1 + distance_from_left_border * temperature_range

    def add_food(self):
        """Add food at a random location in the environment with a random energy value."""
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        energy = random.uniform(10, 30)  # Energy value between 10 and 30
        self.food_positions.append((x, y))
        self.food_energy[(x, y)] = energy

    def get_food_positions(self):
        return self.food_positions

    def get_food_energy(self, position):
        """Return the energy value of food at a given position."""
        return self.food_energy.get(position, 0)

    def remove_food(self, position):
        """Remove food from a specific location after it's consumed."""
        if position in self.food_positions:
            self.food_positions.remove(position)
            del self.food_energy[position]


class DNA:
    def __init__(self, genes=None):
        # Initialize with a dictionary of genes
        if genes is None:
            genes = {}
        self.genes = genes

    def get_gene(self, gene_type):
        """Retrieve the value of a specific gene."""
        return self.genes.get(gene_type, None)

    @classmethod
    def create_initial_dna(cls):
        genes = {
            'initial_size': random.uniform(2.0, 4.0),
            'metabolism_rate': random.uniform(0.4, 0.8),
            'skin_color': random.choice(['red', 'blue']),
            'food_types': random.choice([['plant'], ['prey'], ['corpse']]),
            'aggressiveness': random.uniform(0.0, 1.0),
            'social_behavior': random.choice([True, False]),
            #
            # 'food_required_to_grow': random.uniform(40.0, 60.0),
            # 'food_required_to_be_fertile': random.uniform(30.0, 40.0),
            'food_sense_distance': random.uniform(25.0, 35.0),

            # 'reproduction_rate': random.uniform(0.1, 1.0),
            # 'temperature_tolerance': (random.uniform(0.0, 10.0), random.uniform(30.0, 40.0)),
            'activeness': random.uniform(0.4, 1.0),  # Add activeness gene with a range between 0.1 and 1.0
            'max_age': random.randint(1000, 1200),  # Add max_age gene with random lifespan between 100 and 1000 ticks
            'speed_modifier': random.uniform(1.0, 1.5)
        }
        return cls(genes)

    def mutate(self):
        """Create a mutated copy of the DNA."""
        mutated_genes = self.genes.copy()
        mutation_chance = 0.1  # 10% chance for each gene to mutate

        for gene in mutated_genes:
            if random.random() < mutation_chance:
                if gene == 'initial_size':
                    mutated_genes[gene] *= random.uniform(0.9, 1.1)
                elif gene == 'metabolism_rate':
                    mutated_genes[gene] *= random.uniform(0.9, 1.1)
                elif gene == 'skin_color':
                    mutated_genes[gene] = random.choice(['red', 'blue', 'green', 'yellow'])
                # elif gene == 'food_required_to_grow':
                #     mutated_genes[gene] *= random.uniform(0.9, 1.1)
                # elif gene == 'food_required_to_be_fertile':
                #     mutated_genes[gene] *= random.uniform(0.9, 1.1)
                elif gene == 'food_sense_distance':
                    mutated_genes[gene] *= random.uniform(0.9, 1.1)
                # elif gene == 'food_types':
                #     mutated_genes[gene] = random.choice([['plant'], ['insect'], ['plant', 'insect']])
                # elif gene == 'aggressiveness':
                #     mutated_genes[gene] *= random.uniform(0.9, 1.1)
                # elif gene == 'social_behavior':
                #     mutated_genes[gene] = not mutated_genes[gene]
                # elif gene == 'reproduction_rate':
                #     mutated_genes[gene] *= random.uniform(0.9, 1.1)
                # elif gene == 'temperature_tolerance':
                #     mutated_genes[gene] = (
                #         mutated_genes[gene][0] * random.uniform(0.9, 1.1),
                #         mutated_genes[gene][1] * random.uniform(0.9, 1.1)
                #     )
                elif gene == 'activeness':
                    mutated_genes[gene] *= random.uniform(0.9, 1.1)

        return DNA(mutated_genes)

    # def mutate(self):
    #     """Create a mutated copy of the DNA."""
    #     mutated_genes = self.genes.copy()
    #     mutation_chance = 0.1  # 10% chance for each gene to mutate
    #     for gene in mutated_genes:
    #         if random.random() < mutation_chance:
    #             if isinstance(mutated_genes[gene], float):
    #                 mutated_genes[gene] *= random.uniform(0.9, 1.1)
    #             elif isinstance(mutated_genes[gene], list):
    #                 mutated_genes[gene] = random.choice([['plant'], ['insect'], ['plant', 'insect']])
    #             elif isinstance(mutated_genes[gene], bool):
    #                 mutated_genes[gene] = not mutated_genes[gene]
    #     return DNA(mutated_genes)

    def crossover(self, other):
        if not self.genes or not other.genes:
            return DNA(self.genes), DNA(other.genes)

        # Perform crossover
        child1_genes = self.genes.copy()
        child2_genes = other.genes.copy()
        for gene_type in self.genes.keys() & other.genes.keys():
            if random.random() > 0.5:
                child1_genes[gene_type], child2_genes[gene_type] = other.genes[gene_type], self.genes[gene_type]

        return DNA(child1_genes), DNA(child2_genes)

    def __str__(self):
        return str(self.genes)


class Traits:
    def __init__(self, dna, organism=None):
        self.dna = dna
        # self.traits = self.decode_dna()

    @staticmethod
    def decode_dna(dna):
        traits = {}
        genes = dna.genes

        # Decode each gene type
        traits['size'] = genes.get('initial_size', 3.0)
        # traits['aggressiveness'] = genes.get('aggressiveness', 0.5)
        # traits['activeness'] = genes.get("activeness")  # Decode activeness gene
        # traits['social_behavior'] = genes.get('social_behavior', True)

        # traits['reproduction_rate'] = genes.get('reproduction_rate', 1.0)
        # traits['temperature_tolerance'] = genes.get('temperature_tolerance', (10.0, 35.0))
        # traits['max_age'] = genes.get('max_age')
        # traits['speed_modifier'] = genes.get('speed_modifier')

        # calculated traits
        traits['speed'] = genes.get('metabolism_rate') / traits['size'] * 100

        # traits['food_required_to_grow'] = genes.get('food_required_to_grow', 20.0)
        # traits['food_required_to_be_fertile'] = genes.get('food_required_to_be_fertile', 30.0)
        traits['food_sense_distance'] = genes.get('food_sense_distance', 50.0)

        return traits

    # def get_trait(self, trait_name):
    #     return self.traits.get(trait_name)

    # def __str__(self):
    #     return str(self.traits)

    @staticmethod
    def calculate_speed(dna, organism):
        return dna.get_gene('metabolism_rate') / organism.size * 50

    @staticmethod
    def calculate_size(dna, organism):
        if (organism.max_age / 2 - organism.age) > 0:
            return dna.get_gene('initial_size') * 1.4 / (organism.max_age - organism.age) * (organism.max_age / 2)
        else:
            return organism.size


class Visualizer:
    def __init__(self, environment):
        pygame.init()
        self.env = environment
        self.screen = pygame.display.set_mode((environment.width, environment.height))
        pygame.display.set_caption('Evolution Simulator')
        self.clock = pygame.time.Clock()
        self.organisms = []  # List to hold organisms for visualization
        self.ticks = 0  # Track simulation ticks
        self.skip_ticks = 1
        self.paused = False  # Track whether the simulation is paused
        self.font = pygame.font.SysFont(None, 24)
        self.graph_surface = pygame.Surface((environment.width, 200), pygame.SRCALPHA)  # Transparent surface for graphs
        self.pop_graph_surface = pygame.Surface((environment.width, 100), pygame.SRCALPHA)  # Transparent surface for population graph
        self.metabolism_bins = [i * 0.05 for i in range(21)]  # Bins for metabolism rate distribution
        self.population_history = []

    def add_organism(self, organism):
        """Add an organism to be displayed."""
        self.organisms.append(organism)

    def precompute_environment(self):
        """Precompute the environment drawing and store it as a surface."""
        self.env_surface = pygame.Surface((self.env.width, self.env.height))

        # Define the temperature border values
        temp_border1 = self.env.temperature_border1
        temp_border2 = self.env.temperature_border2

        # Define the gradient width
        gradient_width = 10  # Width of the gradient transition zone

        for y in range(self.env.height):
            for x in range(self.env.width):
                light_level = self.env.get_light_level(x, y)
                temperature = self.env.get_temperature(x, y)

                # Define color boundaries
                cold_color = (0, 0, 255)  # Color for colder temperatures
                hot_color = (255, 0, 0)  # Color for hotter temperatures

                # Calculate temperature influence and gradient
                if temperature < temp_border2:
                    color = cold_color
                elif temperature > temp_border1:
                    color = hot_color
                else:
                    # Calculate distance from the nearest border
                    dist_to_border1 = abs(temperature - temp_border1)
                    dist_to_border2 = abs(temperature - temp_border2)

                    # Determine the gradient zone and calculate influence
                    if dist_to_border1 < gradient_width:
                        gradient_influence = 1 - (dist_to_border1 / gradient_width)
                    elif dist_to_border2 < gradient_width:
                        gradient_influence = 1 - (dist_to_border2 / gradient_width)
                    else:
                        gradient_influence = 0

                    # Interpolate between cold_color and hot_color based on gradient influence
                    color = (
                        int((1 - gradient_influence) * cold_color[0] + gradient_influence * hot_color[0]),
                        int((1 - gradient_influence) * cold_color[1] + gradient_influence * hot_color[1]),
                        int((1 - gradient_influence) * cold_color[2] + gradient_influence * hot_color[2])
                    )

                # Apply light level to the color
                color = (
                    int(light_level * color[0]),
                    int(light_level * color[1]),
                    int(light_level * color[2])
                )

                self.env_surface.set_at((x, y), color)

    def draw_text(self, text, position):
        """Render text on the screen."""
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def draw_environment(self):
        """Blit the precomputed environment surface to the screen."""
        self.screen.blit(self.env_surface, (0, 0))

        # Draw food
        for food_position in self.env.get_food_positions():
            pygame.draw.circle(self.screen, (0, 255, 0), food_position, 3)

    def draw_organism(self, organism):
        """Draw an organism on the screen using its size and color."""
        color = pygame.Color(organism.color)  # Convert organism color to pygame.Color
        pygame.draw.circle(
            self.screen,
            color,
            (int(organism.x), int(organism.y)),
            int(organism.size)
        )

    # def update_metabolism_distribution(self):
    #     """Update the metabolism rate distribution."""
    #     metabolism_rates = [org.dna.genes['metabolism_rate'] for org in self.organisms]
    #     distribution, _ = np.histogram(metabolism_rates, bins=self.metabolism_bins)
    #
    #     return distribution

    def draw_population_graph(self):
        self.pop_graph_surface.fill((0, 0, 0, 0))  # Clear the population graph surface
        max_population = max(self.population_history) if self.population_history else 1

        for i, population in enumerate(self.population_history[-1000:]):  # Limit history to last 400 ticks
            height = int((population / max_population) * 100)
            pygame.draw.line(self.pop_graph_surface, (255, 255, 255, 100),  # Transparent white
                             (i, self.pop_graph_surface.get_height()),
                             (i, self.pop_graph_surface.get_height() - height), 2)
            # pygame.draw.rect(self.pop_graph_surface, (255, 255, 255), (i, 100 - bar_height, 1, bar_height))

        # Draw vertical label
        label = self.font.render('Population', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (0, self.env.height - 110))

        self.screen.blit(self.pop_graph_surface, (10, 700))

    def draw_metabolism_graph(self):
        metabolism_bins = [0] * 10
        for organism in self.organisms:
            bin_index = min(int(organism.dna.genes['metabolism_rate'] * 10), 9)
            metabolism_bins[bin_index] += 1

        self.graph_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        max_value = max(metabolism_bins) if metabolism_bins else 1

        for i, count in enumerate(metabolism_bins):
            bar_height = int((count / max_value) * 100)
            pygame.draw.rect(self.graph_surface, (255, 255, 255, 100), (i * 40, 100 - bar_height, 35, bar_height))

            # Only label bins that have organisms in them
            if count > 0:
                label = self.font.render(f'{i / 10:.1f}', True, (255, 255, 255))
                self.graph_surface.blit(label, (i * 40, 110))

        # Draw vertical label
        label = self.font.render('Metabolism', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (0, 10))

        self.screen.blit(self.graph_surface, (10, 10))

    def draw_food_sense_graph(self):
        sense_bins = [0] * 10
        for organism in self.organisms:
            bin_index = min(int(organism.dna.genes['food_sense_distance'] / 10), 9)
            sense_bins[bin_index] += 1

        self.graph_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        max_value = max(sense_bins) if sense_bins else 1

        for i, count in enumerate(sense_bins):
            bar_height = int((count / max_value) * 100)
            pygame.draw.rect(self.graph_surface, (255, 255, 255, 100), (i * 40, 100 - bar_height, 35, bar_height))

            # Only label bins that have organisms in them
            if count > 0:
                label = self.font.render(f'{i * 10}', True, (255, 255, 255))
                self.graph_surface.blit(label, (i * 40, 110))

        # Draw vertical label
        label = self.font.render('Food Sense', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (420, 10))

        self.screen.blit(self.graph_surface, (430, 10))

    def draw_activeness_graph(self):
        activeness_bins = [0] * 10
        for organism in self.organisms:
            bin_index = min(int(organism.dna.genes['activeness'] * 10), 9)
            activeness_bins[bin_index] += 1

        self.graph_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        max_value = max(activeness_bins) if activeness_bins else 1

        for i, count in enumerate(activeness_bins):
            bar_height = int((count / max_value) * 100)
            pygame.draw.rect(self.graph_surface, (255, 255, 255, 100), (i * 40, 100 - bar_height, 35, bar_height))

            # Only label bins that have organisms in them
            if count > 0:
                label = self.font.render(f'{i / 10:.1f}', True, (255, 255, 255))
                self.graph_surface.blit(label, (i * 40, 110))

        # Draw vertical label
        label = self.font.render('Activeness', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (100, 150))

        # Place the graph below the others
        self.screen.blit(self.graph_surface, (10, 130))

    def run(self):
        """Run the visualization loop."""
        self.precompute_environment()  # Precompute the environment initially
        generation = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.paused = not self.paused  # Toggle the paused state when spacebar is pressed

            if not self.paused:
                self.ticks += 1
                generation += 1

                # self.env.update()  # Update the environment if needed (e.g., food spawn)

                # Add food every 5 ticks
                if self.ticks % 10 == 0:
                    self.env.add_food()

                self.draw_environment()  # Draw the precomputed environment

                # Update organism positions
                for organism in self.organisms:
                    if organism.is_alive():
                        organism.update(self.env)
                        self.draw_organism(organism)
                    else:
                        self.organisms.remove(organism)

                # Display the organism count
                organisms_count = len(self.organisms)
                self.draw_text(f"Organisms: {organisms_count}", (800, 10))
                self.draw_text(f"Ticks: {self.ticks}", (800, 30))
                avg_speed = sum(organism.speed for organism in self.organisms) / organisms_count
                self.draw_text(f"Average speed: {avg_speed:.1f}", (800, 50))
                avg_size = sum(organism.size for organism in self.organisms) / organisms_count
                self.draw_text(f"Average size: {avg_size:.1f}", (800, 70))

                self.population_history.append(len(self.organisms))
                self.draw_metabolism_graph()
                self.draw_food_sense_graph()
                self.draw_population_graph()
                self.draw_activeness_graph()


                pygame.display.flip()  # Update the display

                self.clock.tick(60)  # Cap the frame rate at 60 FPS


class Organism:
    def __init__(self, dna, traits, x, y, energy):
        self.x = x
        self.y = y
        self.dna = dna
        # self.size = traits.get_trait('size')
        self.size = traits.get('size')
        self.speed = traits.get('speed')
        self.metabolism_rate = dna.genes.get('metabolism_rate')
        self.color = dna.genes.get('skin_color')
        self.food_sense_distance = dna.genes.get('food_sense_distance')
        self.food_types = dna.genes.get('food_types')
        # self.food_required_to_grow = traits.get('food_required_to_grow')
        # self.food_required_to_be_fertile = traits.get('food_required_to_be_fertile')
        self.activeness = dna.genes.get('activeness')  # gene for movement activity
        self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))  # Initial random direction
        self.hunger = 50  # Start with 50 hunger
        self.age = 0  # Initialize age to 0
        self.max_age = dna.genes.get('max_age')  # Maximum age determined by DNA
        self.alive = True  # State to check if organism is alive
        self.energy = energy  # New energy attribute
        self.speed_modifier = dna.genes.get('speed_modifier')

    def move_towards(self, target_x, target_y):
        """Move the organism towards a target point (target_x, target_y)."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            # Normalize direction and scale by speed
            dx /= distance
            dy /= distance

            self.x += dx * self.speed * self.speed_modifier
            self.y += dy * self.speed * self.speed_modifier

    def update(self, environment):
        """Update the organism's state."""
        if not self.is_alive():
            return

        self.age += 1  # Increment age each tick

        # Check for death probability
        if self.age > self.max_age * 0.5:  # Start considering death after 50% of max age
            death_probability = (self.age - self.max_age * 0.5) / (self.max_age * 0.5)
            if random.random() < death_probability:
                self.alive = False
                return

        closest_food = None
        closest_distance = float('inf')
        moved = False

        for food_x, food_y in environment.get_food_positions():
            distance = math.hypot(food_x - self.x, food_y - self.y)
            if distance < closest_distance and distance <= self.food_sense_distance:
                closest_food = (food_x, food_y)
                closest_distance = distance

        if closest_food:
            self.move_towards(*closest_food)
            moved = True
            if math.hypot(closest_food[0] - self.x, closest_food[1] - self.y) < self.size:
                food_energy = environment.get_food_energy(closest_food)
                self.consume_food(environment, closest_food, food_energy)
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

        self.speed = Traits.calculate_speed(dna, self)
        self.size = Traits.calculate_size(dna, self)

        if self.age > self.max_age * 0.1 and self.energy >= 50:
            self.reproduce(self.dna)

    def reproduce(self, dna):
        """Attempt to reproduce if conditions are met."""
        child_dna = dna.mutate()  # Mutate the DNA slightly
        child_x = self.x + random.uniform(-5, 5)
        child_y = self.y + random.uniform(-5, 5)
        child_energy = 30  # Transfer energy to the child
        self.energy -= 30  # Deduct energy from the parent
        child_traits = Traits.decode_dna(child_dna) # Decode DNA into traits
        child = Organism(child_dna, child_traits, child_x, child_y, child_energy)
        visualizer.add_organism(child)

    def is_alive(self):
        if self.energy <= 0:
            self.alive = False
        return self.alive

    def consume_food(self, environment, food_position, food_energy):
        """Consume food and decrease hunger."""
        self.hunger -= food_energy  # Decrease hunger by a fixed amount
        environment.remove_food(food_position)
        self.energy += food_energy

    def metabolize(self, moved):
        """Reduce energy over time based on metabolism rate."""
        if moved:
            self.energy -= self.metabolism_rate * self.speed_modifier / 10
        else:
            self.energy -= self.metabolism_rate / 10

    # Add methods for movement, behavior, etc.


if __name__ == "__main__":
    # Create environment
    env = Environment(width=1000, height=800)

    # Create visualizer
    visualizer = Visualizer(environment=env)

    # Create and add organisms
    num_organisms = 10
    for i in range(num_organisms):

        # Generate positions in a grid-like pattern for simplicity
        x = (i * (env.width // num_organisms)) % env.width
        y = (i * (env.height // num_organisms)) % env.height

        # Create DNA and Traits for the organism
        dna = DNA.create_initial_dna()  # Generates random DNA
        traits = Traits.decode_dna(dna) # Decode DNA into traits

        # Initialize organism with traits
        org = Organism(dna, traits, x=x, y=y, energy=30)

        # Add organism to the visualizer
        visualizer.add_organism(org)

    # Run the simulation
    visualizer.run()

