import itertools
import matplotlib.pyplot as plt
from util import City, read_cities, write_cities_and_return_them, generate_cities, path_cost
import time

def solve_tsp_dynamic(cities):
    distance_matrix = [[x.distance(y) for y in cities] for x in cities]
    cities_a = {(frozenset([0, idx + 1]), idx + 1): (dist, [0, idx + 1]) for idx, dist in
                enumerate(distance_matrix[0][1:])}
    for m in range(2, len(cities)):
        cities_b = {}
        for cities_set in [frozenset(C) | {0} for C in itertools.combinations(range(1, len(cities)), m)]:
            for j in cities_set - {0}:
                cities_b[(cities_set, j)] = min([(cities_a[(cities_set - {j}, k)][0] + distance_matrix[k][j],
                                                  cities_a[(cities_set - {j}, k)][1] + [j])
                                                 for k in cities_set if k != 0 and k != j])
        cities_a = cities_b
    res = min([(cities_a[d][0] + distance_matrix[0][d[1]], cities_a[d][1]) for d in iter(cities_a)])
    return res[1]

if __name__ == "__main__":
    cities = read_cities(20)

    start_time = time.time()
    g = solve_tsp_dynamic(cities)
    computation_end_time = time.time()
    sol = [cities[gi] for gi in g]
    print(f"Minimum path cost: {path_cost(sol)}")
    print(f"Time taken for computation: {computation_end_time - start_time} seconds")

    plt.figure(figsize=(10, 10))
    x, y = zip(*[(city.x, city.y) for city in sol + [sol[0]]])
    plt.plot(x, y, 'o-')
    plt.title("Dynamic Programming TSP Solution")
    plt.show(block=True)