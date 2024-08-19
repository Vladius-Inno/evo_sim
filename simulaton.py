import pygame
import pygame_gui


class Simulation:
    def __init__(self, environment, visualizer):
        self.env = environment
        self.viz = visualizer
        self.clock = pygame.time.Clock()
        self.ticks = 0  # Track simulation ticks
        self.skip_ticks = 1
        self.paused = True  # Track whether the simulation is paused
        self.overlay_is_on = True
        self.controls_are_on = True

    def overlay_draw(self, organisms_count):

        # self.viz.draw_text(f"Organisms: {organisms_count}", (1000, 10))
        # self.viz.draw_text(f"Ticks: {self.ticks}", (1000, 30))
        # self.viz.draw_text(f"Average speed: {avg_speed:.1f}", (1000, 50))
        # self.viz.draw_text(f"Average size: {avg_size:.1f}", (1000, 70))
        # max_age = max(organism.age for organism in self.env.organisms) if organisms_count else 0
        # self.viz.draw_text(f"Maximum age: {max_age}", (1000, 90))
        # max_energy = max(organism.energy for organism in self.env.organisms) if organisms_count else 0
        # self.viz.draw_text(f"Maximum energy: {max_energy:.1f}", (1000, 110))

        if organisms_count:
            self.viz.draw_metabolism_graph()
            self.viz.draw_food_sense_graph()
            self.viz.draw_population_graph()
            self.viz.draw_activeness_graph()

    def proceed_organisms(self):
        # Update organism positions
        for organism in self.env.organisms:
            if organism.is_alive():
                organism.update(self.env)
            else:
                self.env.organisms.remove(organism)

    def draw_organisms(self):
        for organism in self.env.organisms:
            # screen_x = organism.x - self.viz.camera_x
            # screen_y = organism.y - self.viz.camera_y
            # if 0 <= screen_x <= self.viz.screen_width and 0 <= screen_y <= self.viz.screen_height:
            self.viz.draw_organism(organism)

    def run(self):
        """Run the visualization loop."""

        self.viz.precompute_environment()
        self.viz.handle_zoom(0.5)

        time_delta = self.clock.tick(60)  # Cap the frame rate at 60 FPS

        generation = 0

        organisms_count = len(self.env.organisms)
        avg_speed = sum(
            organism.speed for organism in self.env.organisms) / organisms_count if organisms_count else 0
        avg_size = sum(organism.size for organism in self.env.organisms) / organisms_count if organisms_count else 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused  # Toggle the paused state when spacebar is pressed
                        if self.paused:
                            self.viz.start_pause_button.set_text('Start')
                        else:
                            self.viz.start_pause_button.set_text('Pause')
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.viz.zoom_in()
                    elif event.key == pygame.K_MINUS:
                        self.viz.zoom_out()
                    elif event.key == pygame.K_g:
                        self.overlay_is_on = not self.overlay_is_on
                    elif event.key == pygame.K_c:
                        self.controls_are_on = not self.controls_are_on
                self.viz.manager.process_events(event)

                # Handle Start Button Click
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.viz.start_pause_button:
                        self.paused = not self.paused
                        if self.paused:
                            self.viz.start_pause_button.set_text('Start')
                        else:
                            self.viz.start_pause_button.set_text('Pause')

            self.viz.manager.update(time_delta)

            keys = pygame.key.get_pressed()
            # Panning with arrow keys
            if keys[pygame.K_LEFT]:
                self.viz.pan_camera(-10, 0)
            if keys[pygame.K_RIGHT]:
                self.viz.pan_camera(10, 0)
            if keys[pygame.K_UP]:
                self.viz.pan_camera(0, -10)
            if keys[pygame.K_DOWN]:
                self.viz.pan_camera(0, 10)

            if not self.paused:
                self.ticks += 1
                generation += 1

                # Add food every 5 ticks
                if self.ticks % 5 == 0:
                    self.env.add_food()
                self.proceed_organisms()
                organisms_count = len(self.env.organisms)
                self.viz.update_population_history()
                avg_speed = sum(
                    organism.speed for organism in self.env.organisms) / organisms_count if organisms_count else 0
                avg_size = sum(
                    organism.size for organism in self.env.organisms) / organisms_count if organisms_count else 0

            self.viz.draw_environment()  # Draw the precomputed environment

            self.draw_organisms()

            if self.overlay_is_on:
                self.overlay_draw(organisms_count)

            if self.controls_are_on:
                self.viz.draw_ui(self.ticks, organisms_count, avg_speed, avg_size)

            pygame.display.flip()  # Update the display
