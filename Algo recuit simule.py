import random
import math

# Matrice des distances
dist = [
    [0, 2, 2, 7, 15, 2, 5, 7, 6, 5],
    [2, 0, 10, 4, 7, 3, 7, 15, 8, 2],
    [2, 10, 0, 1, 4, 3, 3, 4, 2, 3],
    [7, 4, 1, 0, 2, 15, 7, 7, 5, 4],
    [7, 10, 4, 2, 0, 7, 3, 2, 2, 7],
    [2, 3, 3, 7, 7, 0, 1, 7, 2, 10],
    [5, 7, 3, 7, 3, 1, 0, 2, 1, 3],
    [7, 7, 4, 7, 2, 7, 2, 0, 1, 10],
    [6, 8, 2, 5, 2, 2, 1, 1, 0, 15],
    [5, 2, 3, 4, 7, 10, 3, 10, 15, 0]
]


def calc_dist(route):
    """Calcule la distance totale"""
    total = sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))
    return total + dist[route[-1]][route[0]]


def get_neighbor(route):
    """Génère un voisin par échange"""
    new = route[:]
    i, j = random.sample(range(len(route)), 2)
    new[i], new[j] = new[j], new[i]
    return new


def simulated_annealing(T_start=1000, T_end=0.01, alpha=0.95):
    """Recuit simulé simplifié"""
    n = len(dist)

    # Solution initiale
    current = list(range(n))
    random.shuffle(current)
    best = current[:]

    current_dist = calc_dist(current)
    best_dist = current_dist

    T = T_start
    iteration = 0

    print("━" * 50)
    print(f"Démarrage - T={T}, Distance={best_dist}")
    print("━" * 50)

    while T > T_end:
        for _ in range(100):
            # Générer voisin
            neighbor = get_neighbor(current)
            neighbor_dist = calc_dist(neighbor)

            diff = neighbor_dist - current_dist

            # Acceptation
            if diff < 0:
                current = neighbor
                current_dist = neighbor_dist

                if current_dist < best_dist:
                    best = current[:]
                    best_dist = current_dist
                    print(f"Iter {iteration}: Amélioration → {best_dist:.2f}")

            elif random.random() < math.exp(-diff / T):
                current = neighbor
                current_dist = neighbor_dist

            iteration += 1

        # Refroidissement
        T *= alpha

        if iteration % 1000 == 0:
            print(f"Iter {iteration}: T={T:.2f}, Meilleure={best_dist:.2f}")

    print("━" * 50)
    print(f"Solution finale: {best}")
    print(f"Distance: {best_dist:.2f}")
    print("━" * 50)

    return best, best_dist


# Exécution
solution, distance = simulated_annealing()