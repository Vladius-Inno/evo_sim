from environment import Environment
from visualizer import Visualizer
from simulaton import Simulation


def main():
    # Create environment
    env = Environment(width=2400, height=1500)

    # Create visualizer
    visualizer = Visualizer(environment=env, screen_width=1200, screen_height=750)

    # Run the simulation
    sim = Simulation(env, visualizer)
    sim.run()


if __name__ == "__main__":

    main()
