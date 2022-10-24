import random
import math

def cordsGen(n,choice):
    cords = []
    if choice == 1:
        for i in range(n):
            temp = input().split()
            temp[0] = int(temp[0])
            temp[1] = int(temp[1])
            cords.append(temp)
    elif choice == 0:
        print("Podaj zakres rozmieszczenia punktow - od a do b")
        print("Podaj a")
        a = int(input())
        print("Podaj b")
        b = int(input())
        for i in range(n):
            temp = [random.randint(a, b), random.randint(a, b)]
            cords.append(temp)
    return cords


def distanceMatrix(n, cords):
    matrix = []
    for i in range(n):
        matrix.append([0 for j in range(n)])
    for i in range(n):
        x1 = cords[i][0]
        y1 = cords[i][1]
        for j in range(n):
            if i != j:
                x2 = cords[j][0]
                y2 = cords[j][1]
                matrix[i][j] = math.sqrt( ( (x2-x1)*(x2-x1) ) + ( (y2-y1)*(y2-y1) ) )
    return matrix


def TSP(x, n, vis, cnt):
    print(x, end=", ")
    vis[x] = 1
    cnt += 1
    if cnt == n:
        return
    shortest = 99999
    newx = 0
    for i in range(n):
        if i != x and distance[x][i] < shortest and vis[i] == 0:
            shortest=distance[x][i]
            newx = i
    TSP(newx, n, vis, cnt)


print("Podaj ilosc wierzcholkow: ")
n = int(input())
print("0 - jesli program ma sam generowac wspolrzedne")
print("1 - jesli chcesz je sam wpisac")
choice = int(input())

cords = cordsGen(n, choice)
distance = distanceMatrix(n, cords)
visited = [0 for i in range(n)]

print(cords)
print(distance)

TSP(0, n, visited, 0)
print(0)

