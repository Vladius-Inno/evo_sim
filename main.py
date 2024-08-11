import math
import pygame
import random


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
        """Add food at a random location in the environment."""
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        self.food_positions.append((x, y))

    def get_food_positions(self):
        return self.food_positions

    def remove_food(self, position):
        """Remove food from a specific location after it's consumed."""
        if position in self.food_positions:
            self.food_positions.remove(position)


class DNA:
    def __init__(self, genes=None):
        # Initialize with a dictionary of genes
        if genes is None:
            genes = {}
        self.genes = genes

    def get_gene(self, gene_type):
        """Retrieve the value of a specific gene."""
        return self.genes.get(gene_type, None)

    def mutate(self):
        if not self.genes:
            return

        # Choose a random gene to mutate
        gene_type = random.choice(list(self.genes.keys()))
        value = self.genes[gene_type]

        # Apply mutation based on gene type
        if gene_type == 'initial_size':
            self.genes[gene_type] = value + random.uniform(-1, 1)
        elif gene_type == 'metabolism_rate':
            self.genes[gene_type] = value + random.uniform(-0.01, 0.01)
        elif gene_type == 'speed':
            self.genes[gene_type] = value + random.uniform(-0.5, 0.5)
        elif gene_type == 'skin_color':
            self.genes[gene_type] = random.choice(['red', 'blue'])
        elif gene_type == 'food_required_to_grow':
            self.genes[gene_type] = value + random.uniform(-5, 5)
        elif gene_type == 'food_required_to_be_fertile':
            self.genes[gene_type] = value + random.uniform(-5, 5)
        elif gene_type == 'food_sense_distance':
            self.genes[gene_type] = value + random.uniform(-10, 10)
        elif gene_type == 'food_types':
            # Randomly change food type
            self.genes[gene_type] = random.choice([['plant'], ['insect'], ['plant', 'insect']])
        elif gene_type == 'aggressiveness':
            self.genes[gene_type] = random.uniform(0.0, 1.0)
        elif gene_type == 'social_behavior':
            self.genes[gene_type] = not value
        elif gene_type == 'reproduction_rate':
            self.genes[gene_type] = value + random.uniform(-0.1, 0.1)
        elif gene_type == 'temperature_tolerance':
            min_temp, max_temp = self.genes[gene_type]
            if random.choice([True, False]):
                self.genes[gene_type] = (min_temp + random.uniform(-2, 2), max_temp)
            else:
                self.genes[gene_type] = (min_temp, max_temp + random.uniform(-2, 2))

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
    def __init__(self, dna):
        self.dna = dna
        self.traits = self.decode_dna()

    def decode_dna(self):
        traits = {}
        genes = self.dna.genes

        # Decode each gene type
        traits['initial_size'] = genes.get('initial_size', 10.0)
        traits['metabolism_rate'] = genes.get('metabolism_rate', 0.1)
        traits['speed'] = genes.get('speed', 5.0)
        traits['skin_color'] = genes.get('skin_color', 'green')
        traits['food_required_to_grow'] = genes.get('food_required_to_grow', 20.0)
        traits['food_required_to_be_fertile'] = genes.get('food_required_to_be_fertile', 30.0)
        traits['food_sense_distance'] = genes.get('food_sense_distance', 50.0)
        traits['food_types'] = genes.get('food_types', ['plant'])
        traits['aggressiveness'] = genes.get('aggressiveness', 0.5)
        traits['social_behavior'] = genes.get('social_behavior', True)
        traits['reproduction_rate'] = genes.get('reproduction_rate', 1.0)
        traits['temperature_tolerance'] = genes.get('temperature_tolerance', (10.0, 35.0))
        traits['activeness'] = dna.get_gene("activeness")  # Decode activeness gene

        return traits

    def get_trait(self, trait_name):
        return self.traits.get(trait_name)

    def __str__(self):
        return str(self.traits)


def create_initial_dna():
    genes = {
        'initial_size': random.uniform(5.0, 10.0),
        'metabolism_rate': random.uniform(0.05, 0.2),
        'speed': random.uniform(1.0, 10.0),
        'skin_color': random.choice(['red', 'blue']),
        'food_required_to_grow': random.uniform(10.0, 50.0),
        'food_required_to_be_fertile': random.uniform(20.0, 60.0),
        'food_sense_distance': random.uniform(10.0, 100.0),
        'food_types': random.choice([['plant'], ['insect'], ['plant', 'insect']]),
        'aggressiveness': random.uniform(0.0, 1.0),
        'social_behavior': random.choice([True, False]),
        'reproduction_rate': random.uniform(0.1, 1.0),
        'temperature_tolerance': (random.uniform(0.0, 10.0), random.uniform(30.0, 40.0)),
        "activeness": random.uniform(0.1, 1.0)  # Add activeness gene with a range between 0.1 and 1.0
    }
    return DNA(genes)


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

    def run(self):
        """Run the visualization loop."""
        self.precompute_environment()  # Precompute the environment initially
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.ticks += 1
            # self.env.update()  # Update the environment if needed (e.g., food spawn)

            # Add food every 5 ticks
            if self.ticks % 5 == 0:
                self.env.add_food()

            self.draw_environment()  # Draw the precomputed environment

            # Update organism positions
            for organism in self.organisms:
                organism.update(self.env)
                self.draw_organism(organism)

            pygame.display.flip()  # Update the display

            self.clock.tick(60)  # Cap the frame rate at 60 FPS


class Organism:
    def __init__(self, x, y, size, speed, metabolism_rate, color, food_sense_distance, food_types,
                 food_required_to_grow, food_required_to_be_fertile, activeness):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.metabolism_rate = metabolism_rate
        self.color = color
        self.food_sense_distance = food_sense_distance
        self.food_types = food_types
        self.food_required_to_grow = food_required_to_grow
        self.food_required_to_be_fertile = food_required_to_be_fertile
        self.activeness = activeness  # gene for movement activity
        self.direction = (0, 0)  # Initial direction
        self.hunger = 0  # Start with 0 hunger

    def move_towards(self, target_x, target_y):
        """Move the organism towards a target point (target_x, target_y)."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            # Normalize direction and scale by speed
            dx /= distance
            dy /= distance

            self.x += dx * self.speed
            self.y += dy * self.speed

    def update(self, environment):
        """Update the organism's position."""
        closest_food = None
        closest_distance = float('inf')

        for food_x, food_y in environment.get_food_positions():
            distance = math.hypot(food_x - self.x, food_y - self.y)
            if distance < closest_distance and distance <= self.food_sense_distance:
                closest_food = (food_x, food_y)
                closest_distance = distance

        if closest_food:
            self.move_towards(*closest_food)
            if math.hypot(closest_food[0] - self.x, closest_food[1] - self.y) < self.size:
                self.consume_food(environment, closest_food)
        else:
            # Decide whether to move based on activeness
            if random.random() < self.activeness:
                # Random direction change
                if self.direction == (0, 0):  # Initial random direction if stationary
                    self.direction = (random.uniform(-1, 1), random.uniform(-1, 1))
                elif random.random() < 0.1:  # Occasionally adjust direction slightly
                    self.direction = (
                        self.direction[0] + random.uniform(-0.5, 0.5),
                        self.direction[1] + random.uniform(-0.5, 0.5)
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

                # Keep the organism within bounds
                self.x = max(0, min(environment.width - 1, self.x))
                self.y = max(0, min(environment.height - 1, self.y))

    def consume_food(self, environment, food_position):
        """Consume food and decrease hunger."""
        self.hunger -= 50  # Decrease hunger by a fixed amount
        environment.remove_food(food_position)

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
        dna = create_initial_dna()  # Generates random DNA
        traits = Traits(dna)  # Decode DNA into traits

        # Initialize organism with traits
        org = Organism(
            x=x,
            y=y,
            size=traits.get_trait('initial_size'),
            speed=traits.get_trait('speed'),
            metabolism_rate=traits.get_trait('metabolism_rate'),
            color=traits.get_trait('skin_color'),
            food_sense_distance=traits.get_trait('food_sense_distance'),
            food_types=traits.get_trait('food_types'),
            food_required_to_grow=traits.get_trait('food_required_to_grow'),
            food_required_to_be_fertile=traits.get_trait('food_required_to_be_fertile'),
            activeness=traits.get_trait('activeness')
            # activeness=random.uniform(0.1, 1.0)  # Random activeness gene
        )

        # Add organism to the visualizer
        visualizer.add_organism(org)

    # Run the simulation
    visualizer.run()

