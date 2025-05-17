import heapq
import time
from collections import defaultdict

class DynamicGraph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.nodes = set()

    def add_node(self, u):
        self.nodes.add(u)

    def add_edge(self, u, v, w):
        if u in self.nodes and v in self.nodes:
            self.graph[u].append((v, w))
            self.graph[v].append((u, w))

    def dijkstra(self, start, end):
        if start not in self.nodes or end not in self.nodes:
            return float('inf')

        dist = {node: float('inf') for node in self.nodes}
        dist[start] = 0
        heap = [(0, start)]

        while heap:
            d, u = heapq.heappop(heap)
            if u == end:
                return d
            if d > dist[u]:
                continue
            for v, w in self.graph[u]:
                if dist[v] > d + w:
                    dist[v] = d + w
                    heapq.heappush(heap, (dist[v], v))
        return float('inf')


def run_queries(n, m, s, t, edges, queries, output_file):
    graph = DynamicGraph()

    for i in range(n):
        graph.add_node(i)

    for u, v, w in edges:
        graph.add_edge(u, v, w)

    with open(output_file, "w") as out:
        for query in queries:
            parts = query.strip().split()
            if not parts:
                continue
            start_time = time.time()

            if parts[0] == '1':
                u = int(parts[1])
                graph.add_node(u)

            elif parts[0] == '2':
                u, v, w = map(int, parts[1:])
                graph.add_edge(u, v, w)

            elif parts[0] == '3':
                s_query, t_query = map(int, parts[1:])
                distance = graph.dijkstra(s_query, t_query)
                result = f"Shortest path from {s_query} to {t_query}: {distance if distance != float('inf') else 'No path'}\n"
                out.write(result)

            end_time = time.time()
            out.write(f"Query time: {end_time - start_time:.6f} seconds\n")

def main():
    input_file = "medium_input.txt"
    output_file = "output.txt"

    with open(input_file, "r") as f:
        lines = f.readlines()

    n, m, s, t = map(int, lines[0].strip().split())

    edges = []
    for i in range(1, m + 1):
        u, v, w = map(int, lines[i].strip().split())
        edges.append((u, v, w))

    queries = []
    for line in lines[m + 1:]:
        if line.strip() == "END":
            break
        queries.append(line)

    run_queries(n, m, s, t, edges, queries, output_file)


if __name__ == "__main__":
    main()
