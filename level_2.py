import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, min as min_


class DynamicGraphSpark:
    def __init__(self, spark):
        self.spark = spark
        self.edges = spark.createDataFrame([], "src INT, dst INT, weight FLOAT")
        self.nodes = spark.createDataFrame([], "id INT")

    def add_node(self, u):
        new_node_df = self.spark.createDataFrame([(u,)], ["id"])
        self.nodes = self.nodes.union(new_node_df).dropDuplicates(["id"])

    def node_exists(self, u):
        return not self.nodes.filter(col("id") == u).isEmpty()

    def add_edge(self, u, v, w):
        if self.node_exists(u) and self.node_exists(v):
            new_edges = self.spark.createDataFrame([(u, v, w), (v, u, w)], ["src", "dst", "weight"])
            self.edges = self.edges.union(new_edges)

    def shortest_path(self, start, end, max_iter=30):
        if not self.node_exists(start) or not self.node_exists(end):
            return float("inf"), "INVALID"

        distances = self.nodes.withColumn(
            "distance", when(col("id") == start, 0.0).otherwise(float("inf"))
        ).withColumnRenamed("id", "node")

        for _ in range(max_iter):
            joined = self.edges.join(distances, self.edges.src == distances.node, "inner") \
                .select(col("dst").alias("node"), (col("distance") + col("weight")).alias("new_distance"))

            min_dist = joined.groupBy("node").agg(min_("new_distance").alias("distance"))
            distances = distances.union(min_dist).groupBy("node").agg(min_("distance").alias("distance"))

        result = distances.filter(col("node") == end).collect()
        if result:
            return result[0]["distance"], "OK"
        return float("inf"), "NO_RESULT"


def run_queries(n, m, s, t, edges, queries, output_file, spark):
    graph = DynamicGraphSpark(spark)

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
            query_text = query.strip()

            if parts[0] == "1":
                u = int(parts[1])
                graph.add_node(u)

            elif parts[0] == "2":
                u, v, w = map(int, parts[1:])
                graph.add_edge(u, v, w)

            elif parts[0] == "3":
                s_query, t_query = map(int, parts[1:])
                distance, status = graph.shortest_path(s_query, t_query)
                if status == "OK":
                    msg = f"Shortest path from {s_query} to {t_query}: {distance:.2f}\n"
                elif status == "INVALID":
                    msg = f"Shortest path from {s_query} to {t_query}: INVALID NODE(S)\n"
                else:
                    msg = f"Shortest path from {s_query} to {t_query}: No path\n"
                out.write(msg)

            end_time = time.time()
            elapsed = end_time - start_time
            out.write(f"[Query: {query_text}] Time: {elapsed:.6f} seconds\n")


def main():
    input_file = "large_input.txt"
    output_file = "output.txt"

    spark = SparkSession.builder \
        .appName("SparkGraphQueries") \
        .config("spark.driver.memory", "8g") \
        .config("spark.executor.memory", "16g") \
        .getOrCreate()

    with open(input_file, "r") as f:
        lines = f.readlines()

    n, m, s, t = map(int, lines[0].strip().split())

    edges = [tuple(map(int, line.strip().split())) for line in lines[1:m + 1]]
    queries = [line.strip() for line in lines[m + 1:] if line.strip() and line.strip() != "END"]

    run_queries(n, m, s, t, edges, queries, output_file, spark)


if __name__ == "__main__":
    main()
