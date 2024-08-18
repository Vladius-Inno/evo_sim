import math
import pygame
import random
# import matplotlib.pyplot as plt
# import numpy as np


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
        self.organisms = []

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
        energy = random.uniform(20, 40)  # Energy value between 10 and 30
        self.food_positions.append((x, y))
        self.food_energy[(x, y)] = energy

    def add_organism(self, organism):
        """Add an organism to be displayed."""
        self.organisms.append(organism)

    def get_food_positions(self):
        return self.food_positions

    def get_food_energy(self, position):
        """Return the energy value of food at a given position."""
        return self.food_energy.get(position, 0)

    def remove_food(self, position):
        """Remove food from a specific location after it's consumed."""
        if position in self.food_positions:
            self.food_positions.remove(position)
            try:
                del self.food_energy[position]
            except KeyError as e:
                print(f'Food removal error at {position}')

    def get_organisms(self):
        return self.organisms

    def get_organism_at(self, position):
        for organism in self.organisms:
            if math.hypot(organism.x - position[0], organism.y - position[1]) < organism.size:
                return organism
        return None

    def remove_organism(self, organism):
        if organism in self.organisms:
            self.organisms.remove(organism)


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
            'metabolism_rate': random.uniform(0.2, 1.3),
            # 'skin_color': random.choice(['red', 'blue']),
            'food_types': random.choices(['plant', 'prey'], weights=[90, 10])[0],
            'aggressiveness': random.uniform(0.0, 1.0),
            'social_behavior': random.choice([True, False]),
            'food_sense_distance': random.uniform(25.0, 35.0),
            'activeness': random.uniform(0.4, 1.0),  # Add activeness gene with a range between 0.1 and 1.0
            'max_age': random.randint(1000, 1200),  # Add max_age gene with random lifespan between 100 and 1000 ticks
            # 'speed_modifier': random.uniform(1.0, 1.5)
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
                # elif gene == 'skin_color':
                #     mutated_genes[gene] = random.choice(['red', 'blue', 'green', 'yellow'])
                # elif gene == 'food_required_to_grow':
                #     mutated_genes[gene] *= random.uniform(0.9, 1.1)
                # elif gene == 'food_required_to_be_fertile':
                #     mutated_genes[gene] *= random.uniform(0.9, 1.1)
                elif gene == 'food_sense_distance':
                    mutated_genes[gene] *= random.uniform(0.9, 1.1)
                elif gene == 'food_types':
                    mutated_genes[gene] = random.choice(['plant', 'prey'])
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
    def __init__(self, dna):
        self.dna = dna
        # self.traits = self.decode_dna()

    @staticmethod
    def decode_dna(dna):
        traits = {}
        genes = dna.genes

        # Decode each gene type
        traits['size'] = genes.get('initial_size', 3.0)

        # calculated traits
        traits['speed'] = genes.get('metabolism_rate') / traits['size'] * 50
        traits['food_sense_distance'] = genes.get('food_sense_distance', 50.0) if genes.get('food_types') == 'plant' \
            else genes.get('food_sense_distance', 50.0) * 1.2
        traits['skin_color'] = 'blue' if genes.get('food_types') == 'plant' else 'red'
        traits['reproduction_rate'] = genes.get('metabolism_rate') * 5 if genes.get('food_types') == 'plant' \
            else genes.get('metabolism_rate') * 2
        traits['max_energy'] = genes.get('metabolism_rate') * 1000

        return traits

    @staticmethod
    def calculate_speed(dna, organism):
        return dna.get_gene('metabolism_rate') / organism.size * 50

    @staticmethod
    def calculate_size(dna, organism):
        if (organism.max_age / 2 - organism.age) > 0:
            if organism.dna.get_gene('food_types') == 'prey':
                return dna.get_gene('initial_size') * 1.8 / (organism.max_age - organism.age) * (organism.max_age / 2)
            else:
                return dna.get_gene('initial_size') * 1.4 / (organism.max_age - organism.age) * (organism.max_age / 2)
        else:
            return organism.size


class SetupScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.metabolism_low = 0.05
        self.metabolism_high = 0.1
        self.food_amount = "Medium"
        self.initial_organisms = 20

        # Create UI elements like sliders, buttons, etc.
        self.create_ui_elements()

    def create_ui_elements(self):
        # Create sliders and buttons
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen
        # Draw sliders, buttons, and other UI elements
        pygame.display.flip()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle slider and button interactions
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Start the simulation with selected settings
                return self.start_simulation()

    def start_simulation(self):
        # Pass the settings to the simulation initialization
        settings = {
            'metabolism_low': self.metabolism_low,
            'metabolism_high': self.metabolism_high,
            'food_amount': self.food_amount,
            'initial_organisms': self.initial_organisms
        }
        return settings


class Visualizer:
    def __init__(self, environment, screen_width, screen_height):
        pygame.init()
        self.env = environment
        pygame.display.set_caption('Evolution Simulator')
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_x = 0
        self.camera_y = 0
        self.zoom_factor = 1.0
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.organisms = environment.organisms  # List to hold organisms for visualization
        self.ticks = 0  # Track simulation ticks
        self.skip_ticks = 1
        self.paused = False  # Track whether the simulation is paused
        self.font = pygame.font.SysFont(None, 24)
        self.graph_surface = pygame.Surface((self.screen_width, 200), pygame.SRCALPHA)  # Transparent surface for graphs
        self.pop_graph_surface = pygame.Surface((self.screen_height, 100), pygame.SRCALPHA)  # Transparent surface for population graph
        # self.metabolism_bins = [i * 0.05 for i in range(21)]  # Bins for metabolism rate distribution
        self.population_history = []

    # def add_organism(self, organism):
    #     """Add an organism to be displayed."""
    #     self.organisms.append(organism)

    def pan_camera(self, dx, dy):
        # Calculate the maximum pan limits
        max_pan_x = max(0, self.env.width * self.zoom_factor - self.screen_width)
        max_pan_y = max(0, self.env.height * self.zoom_factor - self.screen_height)

        # Update the camera position, respecting the pan limits
        self.camera_x = min(max(self.camera_x + dx, 0), max_pan_x)
        self.camera_y = min(max(self.camera_y + dy, 0), max_pan_y)

    def zoom_in(self):
        self.zoom_factor *= 1.1  # Increase zoom
        self.update_surface()

    def zoom_out(self):
        self.zoom_factor /= 1.1  # Decrease zoom
        self.update_surface()

    def handle_zoom(self, zoom_in):
        previous_zoom_factor = self.zoom_factor

        if zoom_in:
            self.zoom_factor *= 1.1  # Zoom in
        else:
            self.zoom_factor *= 0.9  # Zoom out

        # Limit zoom-out and zoom-in factors
        self.zoom_factor = min(max(self.zoom_factor, 0.5), 2.0)  # Min zoom 50%, max zoom 200%

        # Adjust camera position to ensure it stays within bounds
        self.camera_x = min(max(self.camera_x * (self.zoom_factor / previous_zoom_factor), 0),
                            max(0, self.env.width * self.zoom_factor - self.screen_width))
        self.camera_y = min(max(self.camera_y * (self.zoom_factor / previous_zoom_factor), 0),
                            max(0, self.env.height * self.zoom_factor - self.screen_height))

        # Scale the environment surface only when zoom changes
        self.scaled_env_surface = pygame.transform.scale(
            self.env_surface,
            (int(self.env.width * self.zoom_factor), int(self.env.height * self.zoom_factor))
        )

    def update_surface(self):
        """Update the precomputed environment surface to match the current zoom level."""
        new_width = int(self.env.width * self.zoom_factor)
        new_height = int(self.env.height * self.zoom_factor)
        self.env_surface = pygame.transform.smoothscale(self.env_surface, (new_width, new_height))

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
        # Blit the precomputed and scaled environment surface
        # self.screen.blit(self.scaled_env_surface, (-self.camera_x, -self.camera_y))

        # Zoomed and panned blitting
        zoomed_env_surface = pygame.transform.scale(self.env_surface,
                                                    (int(self.env.width * self.zoom_factor),
                                                     int(self.env.height * self.zoom_factor)))

        """Blit the precomputed environment surface to the screen."""
        self.screen.blit(zoomed_env_surface, (-self.camera_x , -self.camera_y))

        # Draw food
        for food_position in self.env.get_food_positions():
            screen_x = (food_position[0] - self.camera_x) * self.zoom_factor
            screen_y = (food_position[1] - self.camera_y) * self.zoom_factor
            # Draw food if within the current view
            if 0 <= screen_x <= self.screen_width and 0 <= screen_y <= self.screen_height:
                pygame.draw.circle(self.screen, (0, 255, 0), (int(screen_x), int(screen_y)), int(3 * self.zoom_factor))

    def draw_organism(self, organism):
        """Draw an organism on the screen using its size and color."""
        color = pygame.Color(organism.color)  # Convert organism color to pygame.Color
        screen_x = (organism.x - self.camera_x) * self.zoom_factor
        screen_y = (organism.y - self.camera_y) * self.zoom_factor

        # Draw organism if within the current view
        if 0 <= screen_x <= self.screen_width and 0 <= screen_y <= self.screen_height:
            pygame.draw.circle(self.screen, organism.color, (int(screen_x), int(screen_y)), int(organism.size * self.zoom_factor))

    def update_population_history(self):
        predators = sum(1 for organism in self.organisms if 'prey' in organism.dna.genes['food_types'])
        non_predators = len(self.organisms) - predators
        self.population_history.append((predators, non_predators))

    def draw_population_graph(self):
        self.pop_graph_surface.fill((0, 0, 0, 0))  # Clear the population graph surface

        # Get the latest 1000 history entries or less if history is shorter
        history_length = min(1200, len(self.population_history))
        recent_history = self.population_history[-history_length:]

        # Calculate the dynamic scaling factor based on the current population values
        max_population = max(sum(p) for p in recent_history) if recent_history else 1

        # Adjust scaling factor to provide better graph representation
        scaling_factor = max_population * 1.2  # Allow room above the highest value

        for i, (predators, non_predators) in enumerate(recent_history):
            total_population = predators + non_predators

            # Calculate the heights for each population group with dynamic scaling
            predator_height = int((predators / scaling_factor) * 100)
            non_predator_height = int((non_predators / scaling_factor) * 100)

            # Draw predators (red) at the bottom
            pygame.draw.line(self.pop_graph_surface, (255, 0, 0, 100),  # Transparent red
                             (i, self.pop_graph_surface.get_height()),
                             (i, self.pop_graph_surface.get_height() - predator_height), 2)

            # Draw non-predators (white) above the predators
            pygame.draw.line(self.pop_graph_surface, (255, 255, 255, 100),  # Transparent white
                             (i, self.pop_graph_surface.get_height() - predator_height),
                             (i, self.pop_graph_surface.get_height() - predator_height - non_predator_height), 2)

        # Draw vertical label
        label = self.font.render('Population', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (0, self.env.height - 110))

        self.screen.blit(self.pop_graph_surface, (10, self.env.height - 100))  # Adjust position as needed

    def draw_metabolism_graph(self):
        self.font = pygame.font.SysFont(None, 16)
        bin_size = 0.1
        metabolism_rates = [organism.dna.get_gene('metabolism_rate') for organism in self.organisms]
        max_rate = max(metabolism_rates)
        # min_rate = min(metabolism_rates)
        bins_count = int(max_rate / bin_size) + 1
        metabolism_bins = [0] * bins_count

        for metabolism_rate in metabolism_rates:
            bin_index = int(metabolism_rate*10)
            metabolism_bins[bin_index] += 1

        self.graph_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        max_value = max(metabolism_bins) if metabolism_bins else 1

        index = 1
        for i, count in enumerate(metabolism_bins):
            if count > 0:
                # Only draw and label bins that have organisms in them
                index += 1
                bar_height = int((count / max_value) * 100)
                pygame.draw.rect(self.graph_surface, (255, 255, 255, 100), (index * 20 - 2, 100 - bar_height, 18, bar_height))
                label = self.font.render(f'{i / 10:.1f}', True, (255, 255, 255))
                self.graph_surface.blit(label, (index * 20, 110))

        # Draw vertical label
        self.font = pygame.font.SysFont(None, 24)
        label = self.font.render('Metabolism', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (0, 10))
        self.screen.blit(self.graph_surface, (10, 10))

    def draw_food_sense_graph(self):

        self.font = pygame.font.SysFont(None, 16)
        bin_size = 10
        sense_rates = [organism.dna.get_gene('food_sense_distance') for organism in self.organisms]
        max_rate = max(sense_rates)
        bins_count = int(max_rate / bin_size) + 1
        sense_bins = [0] * bins_count

        for sense_rate in sense_rates:
            bin_index = int(sense_rate / 10)
            sense_bins[bin_index] += 1

        self.graph_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        max_value = max(sense_bins) if sense_bins else 1

        index = 1
        for i, count in enumerate(sense_bins):
            if count > 0:
                # Only draw and label bins that have organisms in them
                index += 1
                bar_height = int((count / max_value) * 100)
                pygame.draw.rect(self.graph_surface, (255, 255, 255, 100),
                                 (300 + index * 20 - 2, 100 - bar_height, 18, bar_height))
                label = self.font.render(f'{i * 10}', True, (255, 255, 255))
                self.graph_surface.blit(label, (300 + index * 20, 110))

        # Draw vertical label
        self.font = pygame.font.SysFont(None, 24)
        label = self.font.render('Sense Distance', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (300, 10))
        self.screen.blit(self.graph_surface, (10, 10))

    def draw_activeness_graph(self):

        self.font = pygame.font.SysFont(None, 16)
        bin_size = 0.1
        activness_rates = [organism.dna.get_gene('activeness') for organism in self.organisms]
        max_rate = max(activness_rates)
        # min_rate = min(metabolism_rates)
        bins_count = int(max_rate / bin_size) + 1
        activeness_bins = [0] * bins_count

        for activness_rate in activness_rates:
            bin_index = int(activness_rate * 10)
            activeness_bins[bin_index] += 1

        self.graph_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        max_value = max(activeness_bins) if activeness_bins else 1

        index = 1
        for i, count in enumerate(activeness_bins):
            if count > 0:
                # Only draw and label bins that have organisms in them
                index += 1
                bar_height = int((count / max_value) * 100)
                pygame.draw.rect(self.graph_surface, (255, 255, 255, 100),
                                 (600 + index * 20 - 2, 100 - bar_height, 18, bar_height))
                label = self.font.render(f'{i / 10:.1f}', True, (255, 255, 255))
                self.graph_surface.blit(label, (600 + index * 20, 110))

        # Draw vertical label
        self.font = pygame.font.SysFont(None, 24)
        label = self.font.render('Activeness', True, (255, 255, 255))
        label = pygame.transform.rotate(label, 90)
        self.screen.blit(label, (600, 10))
        self.screen.blit(self.graph_surface, (10, 10))

    def run(self):
        """Run the visualization loop."""
        self.precompute_environment()  # Precompute the environment initially
        generation = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused  # Toggle the paused state when spacebar is pressed
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.zoom_in()
                    elif event.key == pygame.K_MINUS:
                        self.zoom_out()
                    elif event.key == pygame.K_LEFT:
                        self.pan_camera(-10, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pan_camera(10, 0)
                    elif event.key == pygame.K_UP:
                        self.pan_camera(0, -10)
                    elif event.key == pygame.K_DOWN:
                        self.pan_camera(0, 10)

            self.zoom_factor = max(self.zoom_factor, 1200 / self.env.width)  # Minimum zoom-out to 50%

            if not self.paused:
                self.ticks += 1
                generation += 1

                keys = pygame.key.get_pressed()

                # Panning with arrow keys
                # if keys[pygame.K_LEFT]:
                #     self.pan_camera(-10, 0)
                # if keys[pygame.K_RIGHT]:
                #     self.pan_camera(10, 0)
                # if keys[pygame.K_UP]:
                #     self.pan_camera(0, -10)
                # if keys[pygame.K_DOWN]:
                #     self.pan_camera(0, 10)

                # Add food every 5 ticks
                if self.ticks % 5 == 0:
                    self.env.add_food()

                self.draw_environment()  # Draw the precomputed environment

                # Update organism positions
                for organism in self.organisms:
                    if organism.is_alive():
                        organism.update(self.env)
                        screen_x = organism.x - self.camera_x
                        screen_y = organism.y - self.camera_y
                        # Draw organism if within the current view
                        if 0 <= screen_x <= self.screen_width and 0 <= screen_y <= self.screen_height:
                            self.draw_organism(organism)
                    else:
                        self.organisms.remove(organism)

                # Display the organism count
                organisms_count = len(self.organisms)

                self.draw_text(f"Organisms: {organisms_count}", (1000, 10))
                self.draw_text(f"Ticks: {self.ticks}", (1000, 30))
                avg_speed = sum(organism.speed for organism in self.organisms) / organisms_count
                self.draw_text(f"Average speed: {avg_speed:.1f}", (1000, 50))
                avg_size = sum(organism.size for organism in self.organisms) / organisms_count
                self.draw_text(f"Average size: {avg_size:.1f}", (1000, 70))
                max_age = max(organism.age for organism in self.organisms)
                self.draw_text(f"Maximum age: {max_age}", (1000, 90))
                max_energy = max(organism.energy for organism in self.organisms)
                self.draw_text(f"Maximum energy: {max_energy:.1f}", (1000, 110))

                self.update_population_history()
                self.draw_metabolism_graph()
                self.draw_food_sense_graph()
                self.draw_population_graph()
                self.draw_activeness_graph()

                pygame.display.flip()  # Update the display

                self.clock.tick(60)  # Cap the frame rate at 60 FPS


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

        self.energy += prey.energy # Gain energy from prey
        # print('consumed energy', prey.energy)

    def metabolize(self, moved):
        """Reduce energy over time based on metabolism rate."""
        if moved:
            self.energy -= self.metabolism_rate / 2  # * self.speed_modifier / 10
        else:
            self.energy -= self.metabolism_rate / 10

    # Add methods for movement, behavior, etc.


def create_organism(x, y, env):
    # Create DNA and Traits for the organism
    dna = DNA.create_initial_dna()  # Generates random DNA
    # Initialize organism with traits
    return Organism(dna, x=x, y=y, energy=30, environment=env)


def main():

    # pygame.init()
    # screen = pygame.display.set_mode((800, 600))
    # setup_screen = SetupScreen(screen)
    #
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             return
    #         setup_screen.handle_events(event)
    #
    #     setup_screen.draw()

    # Create environment
    env = Environment(width=2000, height=1550)

    # Create visualizer
    visualizer = Visualizer(environment=env, screen_width=1200, screen_height=750)

    # Create and add organisms
    num_organisms = 20
    for i in range(num_organisms):

        # Generate positions in a grid-like pattern for simplicity
        x = (i * (env.width // num_organisms)) % env.width
        y = (i * (env.height // num_organisms)) % env.height

        org = create_organism(x, y, env)

        # Add organism to the visualizer
        env.add_organism(org)

    # Run the simulation
    visualizer.run()


if __name__ == "__main__":

    main()

