import pygame
import pygame_gui


class Visualizer:
    def __init__(self, environment, screen_width, screen_height):
        pygame.init()
        pygame.display.set_caption('Evolution Simulator')
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera_x = 0
        self.camera_y = 0
        self.zoom_factor = 0.5
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        # GUI block
        self.controls_surface = pygame.Surface((200, self.screen_height),
                                               pygame.SRCALPHA)  # Transparent surface for population graph

        self.manager = pygame_gui.UIManager((screen_width, screen_height))
        # Information Box
        self.info_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((950, 50), (220, 150)),
                                                      starting_height=1,
                                                      manager=self.manager)
        # Create labels for displaying information
        self.tick_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 5), (-1, 20)),
            text="Ticks: 0",
            manager=self.manager,
            container=self.info_panel
        )

        self.organism_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 30), (-1, 20)),
            text="Organisms: 0",
            manager=self.manager,
            container=self.info_panel
        )

        self.avg_speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 55), (-1, 20)),
            text="Average speed: 0",
            manager=self.manager,
            container=self.info_panel
        )

        self.avg_size_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((15, 80), (-1, 20)),
            text="Average: size",
            manager=self.manager,
            container=self.info_panel
        )
        # Control Panel
        self.control_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((950, 220), (220, 200)),
                                                         starting_height=0,
                                                         manager=self.manager)

        self.start_pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                                                               text='Start',
                                                               manager=self.manager,
                                                               container=self.control_panel)
        self.food_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 90), (200, 25)),
                                                                  start_value=5,
                                                                  value_range=(0, 10),
                                                                  click_increment=1,
                                                                  manager=self.manager,
                                                                  container=self.control_panel)
        # Create the label for the slider
        self.food_slider_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 65), (-1, 25)),
                                                             text=f"Food Amount: {int(self.food_slider.get_current_value())}",
                                                             manager=self.manager,
                                                             container=self.control_panel)
        # self.food_slider.disable()
        self.tick_skip_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((10, 140), (200, 25)),
                                                                       start_value=1,
                                                                       value_range=(1, 10),
                                                                       manager=self.manager,
                                                                       container=self.control_panel)
        # Create the label for the slider
        self.tick_skip_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 115), (-1, 25)),
                                                           text=f"Ticks to skip: {int(self.tick_skip_slider.get_current_value())}",
                                                           manager=self.manager,
                                                           container=self.control_panel)
        # self.tick_skip_slider.disable()
        # Display Panel
        self.display_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((950, 440), (220, 150)),
                                                         starting_height=1,
                                                         manager=self.manager)

        self.predators_checkbox = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((10, 10), (200, 66)),
                                                                      item_list=['Predators', 'Energy', 'Natural'],
                                                                      manager=self.manager,
                                                                      default_selection='Natural',
                                                                      container=self.display_panel)
        # self.energy_checkbox = pygame_gui.elements.UISelectionList(relative_rect=pygame.Rect((10, 50), (200, 75)),
        #                                                            item_list=['Energy'],
        #                                                            manager=self.manager,
        #                                                            container=self.display_panel)
        # self.natural_colors_checkbox = pygame_gui.elements.UISelectionList(
        #     relative_rect=pygame.Rect((10, 90), (200, 75)),
        #     item_list=['Natural Colors'],
        #     manager=self.manager,
        #     container=self.display_panel)

        self.env = environment
        """Precompute the environment drawing and store it as a surface."""
        self.env_surface = pygame.Surface((self.env.width, self.env.height))

        self.organisms = environment.get_organisms()  # List to hold organisms for visualization

        self.font = pygame.font.SysFont(None, 24)
        self.graph_surface = pygame.Surface((self.screen_width, 200), pygame.SRCALPHA)  # Transparent surface for graphs
        self.pop_graph_surface = pygame.Surface((self.screen_width - 10, 100),
                                                pygame.SRCALPHA)  # Transparent surface for population graph
        self.population_history = []

    def pan_camera(self, dx, dy):
        # Calculate the maximum pan limits
        max_pan_x = max(0, self.env.width * self.zoom_factor - self.screen_width)
        max_pan_y = max(0, self.env.height * self.zoom_factor - self.screen_height)

        # Update the camera position, respecting the pan limits
        self.camera_x = min(max(self.camera_x + dx, 0), max_pan_x)
        self.camera_y = min(max(self.camera_y + dy, 0), max_pan_y)

    def zoom_in(self):
        self.handle_zoom(self.zoom_factor * 1.1)

    def zoom_out(self):
        self.handle_zoom(self.zoom_factor / 1.1)

    # def update_surface(self):
    #     """Update the precomputed environment surface to match the current zoom level."""
    #     new_width = int(self.env.width * self.zoom_factor)
    #     new_height = int(self.env.height * self.zoom_factor)
    #     self.env_surface = pygame.transform.smoothscale(self.env_surface, (new_width, new_height))

    def handle_zoom(self, zoom_in):
        previous_zoom_factor = self.zoom_factor

        self.zoom_factor = zoom_in

        # Limit zoom-out and zoom-in factors
        self.zoom_factor = min(max(self.zoom_factor, 0.5), 1.7)  # Min zoom 50%, max zoom 200%

        # Adjust camera position to ensure it stays within bounds
        self.camera_x = min(max(self.camera_x * (self.zoom_factor / previous_zoom_factor), 0),
                            max(0, self.env.width * self.zoom_factor - self.screen_width))
        self.camera_y = min(max(self.camera_y * (self.zoom_factor / previous_zoom_factor), 0),
                            max(0, self.env.height * self.zoom_factor - self.screen_height))

        # Scale the environment surface only when zoom changes
        self.env_surface = pygame.transform.scale(
            self.env_surface,
            (int(self.env.width * self.zoom_factor), int(self.env.height * self.zoom_factor))
        )

    def update_labels(self, ticks, organism_count, avg_speed, avg_size):
        # Update label texts based on current state
        self.tick_label.set_text(f"Ticks: {ticks}")
        self.organism_label.set_text(f"Organisms: {organism_count}")
        self.avg_speed_label.set_text(f"Average speed: {avg_speed:.2f}")
        self.avg_size_label.set_text(f"Average size: {avg_size:.2f}")

    def precompute_environment(self):
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

        # # Zoomed and panned blitting
        # zoomed_env_surface = pygame.transform.scale(self.env_surface,
        #                                             (int(self.env.width * self.zoom_factor),
        #                                              int(self.env.height * self.zoom_factor)))

        """Blit the precomputed environment surface to the screen."""
        self.screen.blit(self.env_surface, (-self.camera_x, -self.camera_y))

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
            pygame.draw.circle(self.screen, organism.color, (int(screen_x), int(screen_y)),
                               int(organism.size * self.zoom_factor))

    def update_population_history(self):
        predators = sum(1 for organism in self.organisms if 'prey' in organism.dna.genes['food_types'])
        non_predators = len(self.organisms) - predators
        self.population_history.append((predators, non_predators))

    def draw_population_graph(self):
        self.pop_graph_surface.fill((0, 0, 0, 0))  # Clear the population graph surface

        # Get the latest 1000 history entries or less if history is shorter
        history_length = min(self.screen_width, len(self.population_history))
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
        self.screen.blit(label, (0, self.screen_height - 110))

        self.screen.blit(self.pop_graph_surface, (10, self.screen_height - 100))  # Adjust position as needed

    def draw_metabolism_graph(self):
        self.font = pygame.font.SysFont(None, 16)
        bin_size = 0.1
        metabolism_rates = [organism.dna.get_gene('metabolism_rate') for organism in self.organisms]
        max_rate = max(metabolism_rates)
        # min_rate = min(metabolism_rates)
        bins_count = int(max_rate / bin_size) + 1
        metabolism_bins = [0] * bins_count

        for metabolism_rate in metabolism_rates:
            bin_index = int(metabolism_rate * 10)
            metabolism_bins[bin_index] += 1

        self.graph_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        max_value = max(metabolism_bins) if metabolism_bins else 1

        index = 1
        for i, count in enumerate(metabolism_bins):
            if count > 0:
                # Only draw and label bins that have organisms in them
                index += 1
                bar_height = int((count / max_value) * 100)
                pygame.draw.rect(self.graph_surface, (255, 255, 255, 100),
                                 (index * 20 - 2, 100 - bar_height, 18, bar_height))
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

    def draw_ui(self, ticks, organisms_count, avg_speed, avg_size):
        self.manager.draw_ui(self.screen)
        # Update the GUI labels with new data
        self.update_labels(ticks, organisms_count, avg_speed, avg_size)
        # self.controls_surface.fill((0, 0, 0, 0))  # Clear the graph surface
        # Fill part of the overlay surface with semi-transparent color
        # self.controls_surface.fill((0, 0, 0, 128), (1000, 50, 250, 150))  # Semi-transparent black for the info panel
        # self.screen.blit(self.controls_surface, (1000, 50))
