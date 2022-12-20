import random
import math
import time
import sys

sys.setrecursionlimit(10**6)

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
            tmp[1] = int(tmp[1])
            tmp[2] = int(tmp[2])
            if tmp not in coords:
                coords.append([tmp[1], tmp[2]])
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


def TSP(cost, n, vis, curr_point, cnt):
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
    TSP(cost, n, vis, new_point, cnt)


def tspColony(n, vis, curr_point, cnt, localPath, phero):
    #print(curr_point, end=", ")
    localPath.append(curr_point)
    vis[curr_point] = 1
    cnt += 1
    if cnt == n:
        localPath.append(localPath[0])
        cost.append(distances[curr_point][localPath[0]])
        # print("Sciezka to: ",localPath)
        return

    new_point = ant(distances, phero, curr_point, vis)
    # print(new_point)
    cost.append(distances[curr_point][new_point])
    tspColony(n, vis, new_point, cnt, localPath, phero)


def ant(dist, phero, position, vis):
    chances = []
    cumulative_sum = []
    points = []
    denominator = 0
    for j in range(len(dist)):
        if j == position or vis[j]:
            pass
        else:
            denominator += ((phero[position][j] * (1 / dist[position][j])))

    for i in range(len(dist)):
        if i == position or vis[i]:
            pass
        else:
            nominator = (phero[position][i] * (1 / dist[position][i]))
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
        elif i == len(cumulative_sum)-2 and cumulative_sum[i] >= choose and cumulative_sum[i + 1] <= choose:
            return points[i]

def updatePheromones(phero, evapo, path, cost):

    for i in range(len(phero)):
        for j in range(len(phero)):
                phero[i][j] *= (1-evapo)
        
    for i in range(1, len(path)):
        phero[path[i]][path[i-1]] += 1/cost
        phero[path[i-1]][path[i]] += 1/cost


     
    # for i in range(len(path)-1):
    #     for j in range(len(phero)):
    #         for k in range(len(phero)):
    #             if path[i] == j and path[i+1] == k:
    #                 phero[j][k] = (phero[j][k]*(1-evapo)) + 1/cost
    #                 phero[k][j] = (phero[k][j]*(1-evapo)) + 1/cost
    #             elif path[i] == j and path[i+1] != k:
    #                 phero[j][k] *= (1-evapo)
    #                 phero[k][j] *= (1-evapo)


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
TSP(cost, len(coords), visited, 0, 0)
end = time.time()
print(f"Koszt przejscia: {sum(cost)}")
print(f"Czas egzekucji algorytmu zachlannego: {(end - start)}")

i = 1
ants = 1000
evapo = 0.05
start = time.time()
final_costs = []
prev_cost = 0
exit_cnt = 0
while True:
    starting_points = []
    final_paths = []
    while len(starting_points) < 15:
        starting_point = random.randint(0, n-1)
        if starting_point not in starting_points:
            starting_points.append(starting_point)

    # print(f'i: {i}, feromony: {pheromones}')
    # print(starting_points)
    for s in starting_points:
        cost = []
        path = []
        ant_path = []
        visited = [0 for _ in range(len(coords))]
        tspColony(len(coords), visited, s, 0, ant_path, pheromones)
        #print(ant_path, cost)
        final_paths.append([ant_path, sum(cost)])
    
    # print(f'przed posortowaniem: {final_paths}')
    final_paths = sorted(final_paths, key=lambda x: x[1])
    # print(f'po posortowaniu: {final_paths}')

    final_costs.append(final_paths[0][1])
    updatePheromones(pheromones, evapo, final_paths[0][0], final_paths[0][1])
    print(f'przejscie nr: {i}, koszt: {final_paths[0][1]}')
    if abs(final_paths[0][1]-prev_cost) < 0.00001:
        exit_cnt += 1
        if exit_cnt == 10:
            break
    else:
        exit_cnt = 0
    prev_cost = final_paths[0][1]
    
    #if final_paths[0][1] <= 7600:
        #print(f"Sciezka przejscia nr {i}: {sorted(final_paths[0][0])}")
        #print(f"Dlugosc setu: {len(set(final_paths[0][0]))}")
        
    
    # print("Sciezka heurystyczna to : ", ant_path)
    # print()
    i += 1
# print(ant(distances,pheromones,0,visited))
end = time.time()
print(f"Koszt przejscia: {min(final_costs)}")
print(f"Czas egzekucji algorytmu mrowkowego: {(end - start)}")


# for x in distances:
#     print(*x)
#
# for x in pheromones:
#     print(*x)