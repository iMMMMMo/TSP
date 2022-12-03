import random
import math
import time

def generate_coords(choice):
    coords = []
    if choice == 0:
        f = open(f"dane/dane20.txt", "w")
        print("Podaj ilosc wierzcholkow: ", end="")
        n = int(input())
        f.write(f"{str(n)}\n")
        print("Podaj zakres rozmieszczenia punktow - od a do b wlacznie")
        print("Podaj a: ", end="")
        a = int(input())
        print("Podaj b: ", end="")
        b = int(input())

        for _ in range(n):
            tmp = [random.randint(a, b), random.randint(a, b)]
            if tmp not in coords:
                coords.append(tmp)
                f.write(f"{str(tmp[0])} {str(tmp[1])}\n")
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
        for i in range(1, n+1):
            tmp = content[i].split()
            tmp[0] = int(tmp[0])
            tmp[1] = int(tmp[1])
            if tmp not in coords:
                coords.append(tmp)
    else:
        exit()
    
    return coords


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
                matrix[i][j] = math.sqrt( ( (x2-x1)**2 ) + ( (y2-y1)**2 ) )
    return matrix


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


print("Wybierz jedna z opcji:")
print("0 - jesli program ma sam generowac wspolrzedne")
print("1 - jesli chcesz sam wpisac wspolrzedne")
print("2 - wczytaj wspolrzedne z pliku")
choice = int(input())

coords = generate_coords(choice)
distances = create_distance_matrix(len(coords), coords)

cost = []
visited = [0 for _ in range(len(coords))]
start = time.time()
TSP(len(coords), visited, 0, 0)
end = time.time()
print(f"Koszt przejscia: {sum(cost)}")
print(f"Czas egzekucji algorytmu zachlannego: {(end-start)}")
