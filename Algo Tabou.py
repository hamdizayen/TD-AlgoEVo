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
    """Calcule la distance totale"""
    total = sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))
    return total + dist[route[-1]][route[0]]


def swap_cities(route):
    """Échange deux villes aléatoires"""
    new = route[:]
    i, j = random.sample(range(len(route)), 2)
    new[i], new[j] = new[j], new[i]
    return new, (i, j)


def tabu_search(max_iter=1000, tabu_size=20):
    """Recherche Tabou simplifiée"""
    n = len(dist)

    # Solution initiale
    current = list(range(n))
    random.shuffle(current)
    best = current[:]
    best_dist = calc_dist(best)

    # Liste tabou (mouvements interdits)
    forbidden = []

    print("━" * 50)
    print(f"Démarrage - Distance: {best_dist}")
    print("━" * 50)

    for step in range(max_iter):
        candidates = []

        # Générer des voisins
        for _ in range(30):
            neighbor, move = swap_cities(current)
            d = calc_dist(neighbor)
            candidates.append((neighbor, move, d))

        # Trouver le meilleur non-tabou
        best_neighbor = None
        best_move = None
        best_neighbor_dist = float('inf')

        for neighbor, move, d in candidates:
            if move not in forbidden and d < best_neighbor_dist:
                best_neighbor = neighbor
                best_move = move
                best_neighbor_dist = d

        # Mise à jour
        if best_neighbor:
            current = best_neighbor
            forbidden.append(best_move)

            # Limiter la taille de la liste tabou
            if len(forbidden) > tabu_size:
                forbidden.pop(0)

            # Nouvelle meilleure solution ?
            if best_neighbor_dist < best_dist:
                best = current[:]
                best_dist = best_neighbor_dist
                print(f"Iter {step}: Amélioration → {best_dist}")

        if step % 100 == 0:
            print(f"Iter {step}: Meilleure = {best_dist}")

    print("━" * 50)
    print(f"Solution finale: {best}")
    print(f"Distance: {best_dist}")
    print("━" * 50)

    return best, best_dist


# Exécution
solution, distance = tabu_search()