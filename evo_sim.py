from environment import Environment
from visualizer import Visualizer
from simulaton import Simulation
from dna import DNA
from organism import Organism


def create_organism(x, y, env):
    # Create DNA for the organism
    dna = DNA.create_initial_dna()  # Generates random DNA
    return Organism(dna, x=x, y=y, energy=30, environment=env)


def main():
    # Create environment
    env = Environment(width=2400, height=1500)

    # Create visualizer
    visualizer = Visualizer(environment=env, screen_width=1200, screen_height=750)

    num_organisms = 50
    for i in range(num_organisms):
        # Generate positions in a grid-like pattern for simplicity
        x = (i * (env.width // num_organisms)) % env.width
        y = (i * (env.height // num_organisms)) % env.height

        org = create_organism(x, y, env)

        # Add organism to the visualizer
        env.add_organism(org)

    # Run the simulation
    sim = Simulation(env, visualizer)
    sim.run()


if __name__ == "__main__":
    main()
