import googlemaps
from itertools import combinations
import random
import pandas as pd
import numpy as np
import os


gmaps = googlemaps.Client(key="YOUR API KEY HERE")

all_waypoints = ['Cheaha State Park Observation Tower, Delta, AL 36258',
                 'Humphreys Summit Trail, Flagstaff, AZ 86001',
                 'Mt Magazine Rd, Paris, AR 72855',
                 'Whitney Portal Rd, Lone Pine, CA 93545',
                 'Trl 110, Twin Lakes, CO',
                 'Mt Frissell Trailhead parking, Salisbury, CT 06068',
                 '2715 Ebright Rd, Wilmington, DE 19810',
                 '4000 Chesapeake St NW, Washington, DC 20016',
                 'Britton Hill, Florida 32433',
                 'GA-180 Spur, Blairsville, GA 30512',
                 'Borah Peak Trailhead, Mackay, ID 83251',
                 'Charles Mound, Scales Mound Township, IL 61075',
                 'Hoozier Hill, Franklin Township, IN 47341',
                 'Hawkeye Pt Rd, Sibley, IA 51249',
                 'Mount Sunflower, Weskan, KS 67762',
                 'Black Mountain Ridge Rd, Partridge, KY 40862',
                 'Driskill Mountain Trailhead, LA-507, Simsboro, LA 71275',
                 'Appalachian National Scenic TrailHead parking, Millinocket, ME 04462',
                 '2428 Seneca Trail, Eglon, WV 26716',
                 'Veterans War Memorial Tower, Mount Greylock State Reservation, Adams, MA 01220',
                 'Skanee, MI 49962',
                 'Eagle Mountain Trailhead, Grand Marais, MN 55604',
                 '105 Woodall Mountain Rd, Iuka, MS 38852',
                 'High Point Trail Head, Ironton, MO 63650',
                 'W Rosebud Lake Rd, Fishtail, MT 59028',
                 'Panorama Point, Bushnell, NE 82082',
                 'Boundary Peak Trailhead, Nevada 89010',
                 '1598 Mt Washington Auto Rd, Sargents Purchase, NH 03589',
                 'Monument Rd, Wantage, NJ 07461',
                 'Taos Ski Valley, NM 87525',
                 'Adirondack Loj Rd, Lake Placid, NY 12946',
                 'Mount Mitchell Summit Trail, Burnsville, NC 28714',
                 'White Butte Trl, Bowman, ND 58623',
                 '2280 OH-540, Bellefontaine, OH 43311',
                 'Black Mesa Trail, Kenton, OK 73946',
                 'Mt. Hood National Forest Timberline Lodge, Government Camp, OR 97028',
                 'Mount Davis Observation Tower, Fort Hill, PA 15540',
                 '250-216 Hartford Pike, Foster, RI 02825',
                 '1391 F Van Clayton Memorial Hwy, Sunset, SC 29685',
                 'Palmer Creek Trailhead, Hill City, SD 57745',
                 'Clingmans Dome Tennessee High Point, Tennessee 37738',
                 'Pine Springs Trailhead, Salt Flat, TX 79847',
                 '85GFWM59+MG, Evanston, UT 84031',
                 'Long Trail, Stowe, VT 05672',
                 'Elk Garden Trailhead, Co Rd 600, Troutdale, VA 24378',
                 'Henry M. Jackson Memorial Visitors Center, Paradise Rd E, Ashford, WA 98304',
                 'Trailhead to Spruce Knob, Forest Rd 274, Riverton, WV 26814',
                 'W3206 Co Rd R R, Ogema, WI 54459',
                 'Trail Lake Trailhead, Dubois, WY 82513']

if not os.path.exists('my-waypoints-dist-dur.tsv'):
    waypoint_distances = {}
    waypoint_durations = {}
    for (waypoint1, waypoint2) in combinations(all_waypoints, 2):
        route = gmaps.distance_matrix(origins=[waypoint1], destinations=[waypoint2], mode="driving",
                                      language="English", units="metric")
        try:
            distance = route["rows"][0]["elements"][0]["distance"]["value"] # in meters
            duration = route["rows"][0]["elements"][0]["duration"]["value"] # in seconds
            waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
            waypoint_durations[frozenset([waypoint1, waypoint2])] = duration
        except Exception as e:
            print(e, route, waypoint1, waypoint2)

    with open("my-waypoints-dist-dur.tsv", "w") as out_file:
        out_file.write("\t".join(["waypoint1", "waypoint2", "distance_m", "duration_s"]))

        for (waypoint1, waypoint2) in waypoint_distances.keys():
            out_file.write("\n" + "\t".join([waypoint1, waypoint2,
                                             str(waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                             str(waypoint_durations[frozenset([waypoint1, waypoint2])])]))
waypoint_distances = {}
waypoint_durations = {}
all_waypoints = set()

waypoint_data = pd.read_csv("my-waypoints-dist-dur.tsv", sep="\t")

print(waypoint_data)

for i, row in waypoint_data.iterrows():
    waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
    waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
    all_waypoints.update([row.waypoint1, row.waypoint2])


def compute_fitness(solution):
    solution_fitness = 0.0
    for index in range(len(solution)):
        waypoint1 = solution[index - 1]
        waypoint2 = solution[index]
        solution_fitness += waypoint_durations[frozenset([waypoint1, waypoint2])]
    return solution_fitness


def generate_random_agent():
    new_random_agent = list(all_waypoints)
    random.shuffle(new_random_agent)
    return tuple(new_random_agent)


def mutate_agent(agent_genome, max_mutations=3):
    agent_genome = list(agent_genome)
    num_mutations = random.randint(1, max_mutations)
    for mutation in range(num_mutations):
        swap_index1 = random.randint(0, len(agent_genome) - 1)
        swap_index2 = swap_index1
        while swap_index1 == swap_index2:
            swap_index2 = random.randint(0, len(agent_genome) - 1)
        agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]
    return tuple(agent_genome)


def shuffle_mutation(agent_genome):
    agent_genome = list(agent_genome)
    start_index = random.randint(0, len(agent_genome) - 1)
    length = random.randint(2, 20)
    genome_subset = agent_genome[start_index:start_index + length]
    agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]
    insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
    agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]
    return tuple(agent_genome)


def generate_random_population(pop_size):
    random_population = []
    for agent in range(pop_size):
        random_population.append(generate_random_agent())
    return random_population


def run_genetic_algorithm(generations=5000, population_size=100):
    population_subset_size = int(population_size / 10.)
    generations_10pct = int(generations / 10.)
    population = generate_random_population(population_size)
    for generation in range(generations):
        population_fitness = {}
        for agent_genome in population:
            if agent_genome in population_fitness:
                continue
            population_fitness[agent_genome] = compute_fitness(agent_genome)
        new_population = []
        for rank, agent_genome in enumerate(sorted(population_fitness,
                                                   key=population_fitness.get)[:population_subset_size]):
            if (generation % generations_10pct == 0 or generation == generations - 1) and rank == 0:
                print("Generation %d best: %d | Unique genomes: %d" % (generation,
                                                                       population_fitness[agent_genome],
                                                                       len(population_fitness)))
                print(agent_genome)
                print("")
            new_population.append(agent_genome)
            for offspring in range(2):
                new_population.append(mutate_agent(agent_genome, 3))
            for offspring in range(7):
                new_population.append(shuffle_mutation(agent_genome))
        for i in range(len(population))[::-1]:
            del population[i]
        population = new_population


if __name__ == '__main__':
    run_genetic_algorithm(generations=20000, population_size=200)

