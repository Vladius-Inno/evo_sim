import random
import math


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
        self.grid_size = 50
        self.grid_width = width // self.grid_size
        self.grid_height = height // self.grid_size
        self.grid = {}

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
        grid_x = int(organism.x // self.grid_size)
        grid_y = int(organism.y // self.grid_size)
        cell = (grid_x, grid_y)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(organism)

    def update_grid_position(self, organism, new_x, new_y):
        """Update the organism's position in the grid after moving."""
        old_grid_x = int(organism.x // self.grid_size)
        old_grid_y = int(organism.y // self.grid_size)
        new_grid_x = int(new_x // self.grid_size)
        new_grid_y = int(new_y // self.grid_size)

        # Only update if the organism moved to a new grid cell
        if (old_grid_x, old_grid_y) != (new_grid_x, new_grid_y):
            # Remove from old cell
            old_cell = (old_grid_x, old_grid_y)
            if old_cell in self.grid and organism in self.grid[old_cell]:
                self.grid[old_cell].remove(organism)
                if not self.grid[old_cell]:  # If the cell is empty, remove it
                    del self.grid[old_cell]

            # Add to new cell
            new_cell = (new_grid_x, new_grid_y)
            if new_cell not in self.grid:
                self.grid[new_cell] = []
            self.grid[new_cell].append(organism)

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