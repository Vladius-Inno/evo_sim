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
