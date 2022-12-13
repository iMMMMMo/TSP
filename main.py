import random
import math
import time


def generate_coords(choice):
    coords = []
    if choice == 0:
        print("Podaj ilosc wierzcholkow: ", end="")
        n = int(input())
        print("Podaj zakres rozmieszczenia punktow - od a do b wlacznie")
        print("Podaj a: ", end="")
        a = int(input())
        print("Podaj b: ", end="")
        b = int(input())

        for _ in range(n):
            tmp = [random.randint(a, b), random.randint(a, b)]
            if tmp not in coords:
                coords.append(tmp)
    elif choice == 1:
        print("Podaj ilosc wierzcholkow: ", end="")
        n = int(input())

        for _ in range(n):
            tmp = input().split()
            tmp[0] = int(tmp[0])
            tmp[1] = int(tmp[1])
            if tmp not in coords:
                coords.append(tmp)
    elif choice == 2:
        print("Podaj nazwe pliku: ", end="")
        name = input()
        f = open(f"dane/{name}", "r")

        content = f.readlines()
        n = int(content[0])
        for i in range(1, n + 1):
            tmp = content[i].split()
            tmp[0] = int(tmp[0])
            tmp[1] = int(tmp[1])
            if tmp not in coords:
                coords.append(tmp)
    else:
        exit()

    return coords, n


def create_distance_matrix(n, coords):
    matrix = []
    for _ in range(n):
        matrix.append([0 for _ in range(n)])

    for i in range(n):
        x1 = coords[i][0]
        y1 = coords[i][1]
        for j in range(n):
            if i != j:
                x2 = coords[j][0]
                y2 = coords[j][1]
                matrix[i][j] = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    return matrix


def pheromones_graph(matrix):
    new = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix)):
            if i == j:
                temp.append(0)
            else:
                temp.append(1)
        new.append(temp)
    return new


def TSP(n, vis, curr_point, cnt):
    print(curr_point, end=", ")
    vis[curr_point] = 1
    cnt += 1
    if cnt == n:
        print(0)
        cost.append(distances[0][curr_point])
        return

    shortest = float('inf')
    for i in range(n):
        if i != curr_point and distances[curr_point][i] < shortest and vis[i] == 0:
            shortest = distances[curr_point][i]
            new_point = i
    cost.append(shortest)
    TSP(n, vis, new_point, cnt)


def tspColony(n, vis, curr_point, cnt, localPath, phero):
    # print(curr_point, end=", ")
    localPath.append(curr_point)
    vis[curr_point] = 1
    cnt += 1
    if cnt == n:
        path.append(localPath[0])
        cost.append(distances[0][curr_point])
        # print("Sciezka to: ",localPath)
        return

    shortest = float('inf')
    new_point = ant(distances, phero, curr_point, vis)
    # print(new_point)
    shortest = distances[curr_point][new_point]
    cost.append(shortest)
    tspColony(n, vis, new_point, cnt, localPath, phero)


def ant(dist, phero, position, vis):
    chances = []
    cumulative_sum = []
    points = []
    for i in range(len(dist)):
        if i == position or vis[i]:
            pass
        else:
            nominator = (phero[position][i] * (1 / dist[position][i]))
            denominator = 0
            for j in range(len(dist)):
                if j == position or vis[j]:
                    pass
                else:
                    denominator += ((phero[position][j] * (1 / dist[position][j])))
            chances.append(nominator / denominator)
            points.append(i)
            # print(nominator,denominator,nominator/denominator)

    if len(points) == 1:
        return points[0]

    # print("Chances: ", chances)
    # print("Points: ", points)
    cumulative_sum.append(sum(chances))
    for i in range(len(chances) - 1):
        cumulative_sum.append(cumulative_sum[i] - chances[i])

    cumulative_sum.append(0)
    # print("Cumulative sum", cumulative_sum)
    choose = random.uniform(0, cumulative_sum[0])
    # print("Wylosowana wartosc: ", choose)
    for i in range(len(cumulative_sum) - 1):
        # print("i: ", i, "points[i]: ", points[i])
        # print(cumulative_sum[i], cumulative_sum[i+1])
        if cumulative_sum[i] >= choose and cumulative_sum[i + 1] < choose:
            # print("dla ",i," wynik to ",cumulative_sum[len(cumulative_sum)-i-1],choose)
            # print("Nastepny punkt: ", points[i])
            return points[i]
        elif i == len(cumulative_sum) - 2 and cumulative_sum[i] >= choose and cumulative_sum[i + 1] <= choose:
            return points[i]


def updatePheromones(phero, evapo, path, cost):
    for i in range(1, len(path)):
        phero[path[i]][path[i - 1]] += 1 / sum(cost)
        phero[path[i - 1]][path[i]] += 1 / sum(cost)

    for i in range(len(phero)):
        for j in range(len(phero)):
            phero[i][j] *= evapo

    # for i in range(len(path)-1):
    #     for j in range(len(phero)):
    #         for k in range(len(phero)):
    #             if path[i] == j and path[i+1] == k:
    #                 phero[j][k] = (phero[j][k]*evapo) + (1/sum(cost))
    #                 phero[k][j] = (phero[k][j]*evapo) + (1/sum(cost))
    #             elif path[i] == j and path[i+1] != k:
    #                 phero[j][k] *= evapo
    #                 phero[k][j] *= evapo


print("Wybierz jedna z opcji:")
print("0 - jesli program ma sam generowac wspolrzedne")
print("1 - jesli chcesz sam wpisac wspolrzedne")
print("2 - wczytaj wspolrzedne z pliku")
choice = int(input())

coords, n = generate_coords(choice)
# print(coords)
distances = create_distance_matrix(len(coords), coords)
pheromones = pheromones_graph(distances)

path = []
cost = []
visited = [0 for _ in range(len(coords))]
start = time.time()
TSP(len(coords), visited, 0, 0)
end = time.time()
print(f"Koszt przejscia: {sum(cost)}")
print(f"Czas egzekucji algorytmu zachlannego: {(end - start)}")

i = 1
ants = 1000
evapo = 0.1
start = time.time()
while i <= ants:
    starting_point = random.randint(0, n-1)
    cost = []
    path = []
    ant_path = []
    visited = [0 for _ in range(len(coords))]
    # print(f'i: {i}, feromony: {pheromones}')
    tspColony(len(coords), visited, starting_point, 0, ant_path, pheromones)
    updatePheromones(pheromones, evapo, ant_path, cost)
    # print(f'przejscie nr: {i}, koszt: {sum(cost)}')
    # print("Sciezka heurystyczna to : ", ant_path)
    # print()
    i += 1

# print(ant(distances,pheromones,0,visited))
end = time.time()
print(f"Koszt przejscia: {sum(cost)}")
print(f"Czas egzekucji algorytmu mrowkowego: {(end - start)}")

# ant(distances,pheromones,0)

# for x in distances:
#     print(*x)
#
# for x in pheromones:
#     print(*x)