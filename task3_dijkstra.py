import heapq
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from task1_network_graph import set_pos
from task1_geos import geodata, data


def dijkstra(graph: dict, start: str, end:str) -> dict | list:
    """Функція для знаходження найкоротшого шляху (в даному випадку часу перельоту) від заданими точками початку
    та кінця маршруту"""
    # словник для зберігання часів перельоту для кожної вершини. Початкові значення - безкінечність.
    #стартовій вершині присвоїмо значення 0
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
     
    # використовуємо пріоритетну чергу для зберігання поточних значень часу та відповідних їм вершин
    pq = [(0, start)]
     
    # словник для зберігання міст, що входять до маршруту найкоротшого шляху від старту до міста призначеня
    parents = {}
     
    while pq:
        current_distance, current_node = heapq.heappop(pq)
         
        # якщо найменше значення для певної вершини знайдено, не роглядаємо її, переходимо далі
        if current_distance > distances[current_node]:
            continue
         
        # якщо вершина співпадає з містом призначення, виходимо з циклу
        if current_node == end:
            break
         
        # досліджуємо зв'язки між сусідніми вершинами, заносимо зміни до словника distances, якщо знайдені менші значення
        #при перевірці наступних сусідніх вершин
        for neighbor, distance in graph[current_node].items():
            new_distance = current_distance + distance
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))
                parents[neighbor] = current_node
     
    # список міст, що входять до найкоротшого маршруту від початкового міста до міста призначеня
    path = []
    node = end
    while node != start:
        path.append(node)
        node = parents[node]
    path.append(start)
    path.reverse()
     
    return distances[end], path


if __name__=='__main__':

    m = Basemap(lat_0=20.1578888, lon_0=57.5056055)

    G = nx.Graph()
    G.add_edges_from(data)
    pos = set_pos(geodata, G, m)

    graph = {}
    for node in G.edges(data=True):
        u, v, w = node[0], node[1], node[2]['weight']
        if not graph.get(u):
            graph[u] = {v: w}
        else: graph[u].update({v: w})
        if not graph.get(v):
            graph[v] = {u: w}
        else: graph[v].update({u: w})


    go1, go2, go3, go4, go5 = 'London', 'Ottawa', 'Mexico', 'New York', 'Mumbai'
    dest1, dest2, dest3, dest4, dest5 = 'Tokyo', 'Beijing', 'Cairo', 'Miami', 'Melbourne'

    print(f"From {go1} to {dest1}: {dijkstra(graph, go1, dest1)[0]:.2f} hours via -> {dijkstra(graph, go1, dest1)[1]}")
    print(f"From {go2} to {dest2}: {dijkstra(graph, go2, dest2)[0]:.2f} hours via -> {dijkstra(graph, go2, dest2)[1]}")
    print(f"From {go3} to {dest3}: {dijkstra(graph, go3, dest3)[0]:.2f} hours via -> {dijkstra(graph, go3, dest3)[1]}")
    print(f"From {go4} to {dest4}: {dijkstra(graph, go4, dest4)[0]:.2f} hours via -> {dijkstra(graph, go4, dest4)[1]}")
    print(f"From {go5} to {dest5}: {dijkstra(graph, go5, dest5)[0]:.2f} hours via -> {dijkstra(graph, go5, dest5)[1]}")