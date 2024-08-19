import random


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
