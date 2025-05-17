#include <iostream>
#include <fstream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <queue>
#include <limits>
#include <chrono>

using namespace std;
using namespace std::chrono;

const long long INF = numeric_limits<long long>::max();

class Graph
{
public:
    unordered_map<int, vector<pair<int, int>>> adj;
    unordered_set<int> nodes;

    void add_node(int u)
    {
        nodes.insert(u);
    }

    void add_edge(int u, int v, int w, ofstream &out, int query_id)
    {
        if (nodes.count(u) && nodes.count(v))
        {
            adj[u].emplace_back(v, w);
            adj[v].emplace_back(u, w);
        }
        else
        {
            out << "[Query " << query_id << "] Edge (" << u << ", " << v << ") not added: One or both vertices not in graph.\n";
        }
    }

    long long dijkstra(int s, int t)
    {
        if (!nodes.count(s) || !nodes.count(t))
            return INF;

        unordered_map<int, long long> dist;
        for (int node : nodes)
            dist[node] = INF;

        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<>> pq;
        dist[s] = 0;
        pq.emplace(0, s);

        while (!pq.empty())
        {
            auto [d, u] = pq.top();
            pq.pop();
            if (d > dist[u])
                continue;
            if (u == t)
                return d;

            for (auto &[v, w] : adj[u])
            {
                if (dist[v] > d + w)
                {
                    dist[v] = d + w;
                    pq.emplace(dist[v], v);
                }
            }
        }
        return INF;
    }
};

int main()
{
    ifstream in("large_input.txt");
    ofstream out("output.txt");

    if (!in || !out)
    {
        cerr << "Cannot open input/output file.\n";
        return 1;
    }

    int n, m, s, t;
    in >> n >> m >> s >> t;

    Graph g;
    for (int i = 0; i < n; ++i)
    {
        g.add_node(i);
    }

    for (int i = 0; i < m; ++i)
    {
        int u, v, w;
        in >> u >> v >> w;
        g.add_edge(u, v, w, out, -1);
    }

    string cmd;
    int query_id = 1;

    while (in >> cmd && cmd != "END")
    {
        auto start = high_resolution_clock::now();

        if (cmd == "1")
        {
            int u;
            in >> u;
            g.add_node(u);
            out << "[Query " << query_id << "] Add node: " << u << "\n";
        }
        else if (cmd == "2")
        {
            int u, v, w;
            in >> u >> v >> w;
            g.add_edge(u, v, w, out, query_id);
            out << "[Query " << query_id << "] Add edge: " << u << " " << v << " weight " << w << "\n";
        }
        else if (cmd == "3")
        {
            int u, v;
            in >> u >> v;
            long long dist = g.dijkstra(u, v);
            if (dist == INF)
            {
                out << "[Query " << query_id << "] Shortest path " << u << " -> " << v << ": No path or invalid nodes\n";
            }
            else
            {
                out << "[Query " << query_id << "] Shortest path " << u << " -> " << v << ": " << dist << "\n";
            }
        }
        else
        {
            out << "[Query " << query_id << "] Unknown command\n";
        }

        auto stop = high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::duration<double>>(stop - start).count();
        out << "[Query " << query_id << "] Time: " << duration << " seconds\n\n";

        query_id++;
    }

    in.close();
    out.close();
    return 0;
}
