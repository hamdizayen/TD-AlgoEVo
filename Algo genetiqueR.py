import random

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
    """Calcule la distance"""
    total = sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))
    return total + dist[route[-1]][route[0]]


def create_population(size, n_cities):
    """Crée la population initiale"""
    pop = []
    for _ in range(size):
        ind = list(range(n_cities))
        random.shuffle(ind)
        pop.append(ind)
    return pop


def rank_select(pop):
    """Sélection par rang"""
    # Trier par distance (meilleurs en premier)
    sorted_pop = sorted(pop, key=calc_dist)

    # Probabilités basées sur le rang
    n = len(sorted_pop)
    ranks = list(range(1, n + 1))
    total = sum(ranks)

    # Roulette
    r = random.random() * total
    cumul = 0

    for i, rank in enumerate(ranks):
        cumul += rank
        if r <= cumul:
            return sorted_pop[i][:]

    return sorted_pop[-1][:]


def mutate(individual, rate=0.2):
    """Mutation par échange"""
    if random.random() < rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual


def genetic_algorithm(pop_size=100, n_gen=500, mutation_rate=0.2):
    """Algorithme génétique avec sélection par rang"""
    n = len(dist)

    # Population initiale
    pop = create_population(pop_size, n)
    best = min(pop, key=calc_dist)
    best_dist = calc_dist(best)

    print("━" * 50)
    print(f"Algorithme Génétique (Rang)")
    print(f"Population: {pop_size}, Générations: {n_gen}")
    print(f"Distance initiale: {best_dist}")
    print("━" * 50)

    for gen in range(n_gen):
        # Trouver le meilleur
        current_best = min(pop, key=calc_dist)
        current_dist = calc_dist(current_best)

        if current_dist < best_dist:
            best = current_best[:]
            best_dist = current_dist
            print(f"Gen {gen}: Amélioration → {best_dist:.2f}")

        # Nouvelle génération
        new_pop = [current_best[:]]  # Élitisme

        while len(new_pop) < pop_size:
            # Sélection par rang
            parent = rank_select(pop)

            # Mutation
            child = mutate(parent[:], mutation_rate)
            new_pop.append(child)

        pop = new_pop

        if gen % 100 == 0:
            avg = sum(calc_dist(ind) for ind in pop) / pop_size
            print(f"Gen {gen}: Meilleure={best_dist:.2f}, Moyenne={avg:.2f}")

    print("━" * 50)
    print(f"Solution finale: {best}")
    print(f"Distance: {best_dist:.2f}")
    print("━" * 50)

    return best, best_dist


# Exécution
solution, distance = genetic_algorithm()