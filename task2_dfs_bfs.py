"""Завдання 2. 
Напишіть програму, яка використовує алгоритми DFS і BFS для знаходження шляхів у графі, 
який було розроблено у першому завданні.
Далі порівняйте результати виконання обох алгоритмів для цього графа, висвітліть різницю в отриманих шляхах. 
Поясніть, чому шляхи для алгоритмів саме такі.
Висновки оформлено у вигляді файлу readme.md домашнього завдання.
"""

import queue
import networkx as nx
import matplotlib.pyplot as plt
from random import choices, choice
from mpl_toolkits.basemap import Basemap as Basemap
from task1_network_graph import set_pos
from task1_geos import geodata, data


def bfs(graph, start_node, target= None):
    """Функція для алгоритму bfs. Має параметр target, який дозволяє обрати кінцеву точку обходу графа"""
    visited = set()
    q = queue.Queue()
    q.put(start_node)
    order = []

    while not q.empty():
        vertex = q.get()
        
        if vertex not in visited:
            order.append(vertex)
            visited.add(vertex)
            for node in graph[vertex]:
                if node!=target and node not in visited:
                    q.put(node)
                else:
                    if node == target:
                        order.append(node)
                        return order

    return order


def dfs(graph, start_node, visited=None):
    """Базова функція для алгоритму dfs для повного обходу графа"""
    if not visited:
        visited = []
    visited.append(start_node)

    for node in graph[start_node]:
        if node not in visited:
            dfs(graph, node, visited)
    return visited


def dfs_target(graph, start_node, target, visited):  
    """Функція для обходу графа за алгоритмом dfs. Має обов'язковий параметр для кінцевої точки обходу"""
    if start_node not in visited:
        visited.append(start_node)

        if start_node == target:
            return True
        
        for node in graph[start_node]:
            if dfs_target(graph, node, target, visited):
                return visited
    return False


def compare_algos(cities, bfs_func, dfs_func, start_cities, results):
    """Функція для порівняння кількості вершин, яку проходять алгоритми при досягненні вершини призначення.
    Повертає словник, де ключем є початкова вершина обходу, значенням - словник з ключами-вершинами призначення
    та значеннями - списком з результату для bfs та dfs алгоритмів"""
    for start in start_cities:
        for city in cities:
            if city == start:
                continue
            else:
                visited = []
                bfs_route = bfs_func(G, start, city)
                if not results.get(start):
                    results[start] = {city: [len(bfs_route)]}

                    dfs_route = dfs_func(G, start, city, visited)
                    results[start][city].append(len(dfs_route))
                else: 
                    results[start].update({city: [len(bfs_route)]})
                    dfs_route = dfs_func(G, start, city, visited)
                    results[start][city].append(len(dfs_route))
        
    return results

def show_destination(gfunc, G, start, destination, title, visited=None):
    """Функція для візуалізації обходу графа з використаннями алгоритмів bfs або dfs до певної зазначеної вершини"""
    if visited is None:
        l = gfunc(G, start, destination)
    else:
        l = gfunc(G, start, destination, visited)
    node_colors = ["red" if n == destination else "green" for n in G.nodes]
    edge_colors = ["red" if edge[0] in l and edge[1] else "black" for edge in G.edges()]
    plt.figure(title, figsize=(10, 8))

    nx.draw(G, with_labels=True, font_size='8', font_family='serif', font_weight='100', node_color = node_colors, alpha=0.6,
        pos=pos, node_size =150, edge_color=edge_colors, width = 0.7)

    plt.show()

def draw_graph(gfunc, G, start_node, title, pos, c='r'):
    """Функція для візуалізації повного обходу графа з використаннями алгоритмів bfs або dfs"""
    l = []
    plt.figure(figsize=(10, 8), label=title)
    for node in gfunc(G, start_node):
        l.append(node)
        plt.clf
        nx.draw(G, with_labels=True, font_size='8', font_family='serif', font_weight='100', node_color = ['r' if n==node else "gainsboro" for n in G.nodes], alpha=0.6,
            pos=pos, node_size =100, edge_color=[c if v[0] in l and v[1] in l else "gainsboro" for v in G.edges], width = 0.7)
        plt.pause(0.3)
    plt.show()


if __name__ == "__main__":

    m = Basemap(lat_0=20.1578888, lon_0=57.5056055)

    G = nx.Graph()
    G.add_edges_from(data)
    pos = set_pos(geodata, G, m)


    """ПОРІВНЯННЯ BFS ТА DFS """

    cities_to_visit = ['London', 'Mumbai', 'Miami', 'Shanghai', 'Tokyo', 'Frankfurt']
    START_CITY = ["Fairbanks"]
    data1 = {}

    """Порівняння довжин (=кількість відвіданих вершин на шляху до цілі) шляхів обходу алгоритмів
    з однаковою початковою вершиною ("Fairbanks", найвища ліва вершина) та різними вершинами призначення"""

    print(compare_algos(cities_to_visit, bfs, dfs_target, START_CITY, data1))
  
    """Візуалізація шляху обходу до вершини 'Miami' (обране саме це місто, оскільки відповідно до даного
    графа немає прямого шляху перельоту від іншого міста США до даного міста, і потрібно летіти через інші країни.
    Також вершина має лише одне ребро. Подивимось на шляхи, обрані обома алгоритмами"""

    destination_city = 'Miami'

    # show_destination(bfs, G, START_CITY, destination_city, 'Miami BFS')
    # show_destination(dfs_target, G, START_CITY, destination_city, 'Miami DFS', visited = [])


    """Порівняння довжин (=кількість відвіданих вершин на шляху до цілі) шляхів обходу алгоритмів
    з різними початковими вершинами та різними вершинами призначення.
    Для генерації списку випадкових вершин використано модуль random.choices до списку вершин графа"""
    # print(choices(list(G.nodes), k=5))

    destination_cities = ['Jakarta', 'Lahore', 'Shanghai', 'Frankfurt']
    start_cities = ['San Francisco', 'Santiago', 'Houston', 'Cape Town']
    data = {}

    print(compare_algos(destination_cities, bfs, dfs_target, start_cities, data))
 

    """Розраховуємо кількість випадків, коли шлях, обраний кожним з алгоритмів, був коротший за інший"""

    cities_from, dest = [n for n in G.nodes], [n for n in G.nodes]
    
    stats = {}
    bf_win = 0
    df_win = 0
    same_res = 0

    for record in compare_algos(dest, bfs, dfs_target, cities_from, stats).values():
        for key in record:
            if record[key][0]-record[key][1]<0:
                bf_win+=1
            elif record[key][0]-record[key][1]>0:
                df_win+=1
            else: same_res +=1

    print(f"BFS was faster: {bf_win} times, DFS is faster: {df_win} time, same result: {same_res} ")
    


    """Послідовність вершин, за яким здійснюється повний обход графа кожним з алгоритмів BFS та DFS"""
    print('BFS', bfs(G, START_CITY[0]))
    print('DFS',dfs(G, START_CITY[0]))  


    """Візуалізація повного обходу графа алгоритмами BFS та DFS"""
    # draw_graph(bfs, G, 'Fairbanks', 'BFS Algorithm', pos)
    # #     plt.savefig('bfs')
    # draw_graph(dfs, G, 'Fairbanks', 'DFS Algorithm', pos, c='#90D5FF')
    # # # plt.savefig('dfs')
   

