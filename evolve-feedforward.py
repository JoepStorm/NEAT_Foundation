"""
Feed-forward neural network beam_moments modified from Single-pole balancing experiment.
"""

from __future__ import print_function

import os
import pickle
import beam_moments
import neat
import visualize

runs_per_net = 5
simulation_steps = 500.0    # 500 steps at 50fps = 10 sec


# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        sim = beam_moments.BeamMoment()

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        while sim.t < simulation_steps:

            inputs = sim.get_scaled_state()
            action = net.activate(inputs)

            # Apply action to the simulated cart-pole
            '''For now use simple scalefactor to scale instead of: force = cart_pole.discrete_actuator_force(action) 
            sim.step(force)'''
            sim.step(action)

            # Run the simulation 'simulation_steps' amount of times
            # the fitness is the difference in moments scaled to: worst score 0 and best score 1
            result = sim.get_scaled_state()             # The optimal result returns [1, 1]
            fitness = sum(result)
            # print('fitness = ', fitness)

        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    # print(min(fitnesses))
    return min(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(4, eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    node_names = {-1: 'M1', -2: 'M2', -3: 'M3', 0: 'x1', 1: 'x2'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled.gv", show_disabled=False)
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)


if __name__ == '__main__':
    run()
