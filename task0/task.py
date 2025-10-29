import csv

def read_graph_from_csv(filename):
    edges = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2:
                edges.append((int(row[0]), int(row[1])))
    return edges


def build_adjacency_matrix(edges):
    max_vertex = max(max(u, v) for u, v in edges)
    matrix = [[0] * max_vertex for _ in range(max_vertex)]

    for u, v in edges:
        matrix[u - 1][v - 1] = 1
        matrix[v - 1][u - 1] = 1
    return matrix


def main():
    filename = "task2.csv"
    edges = read_graph_from_csv(filename)
    matrix = build_adjacency_matrix(edges)

    for row in matrix:
        print(row)

    return matrix


if __name__ == "__main__":
    main()