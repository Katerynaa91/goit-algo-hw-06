"""Завдання 1. Cтворіть граф за допомогою бібліотеки networkX для моделювання певної реальної мережі 
(наприклад, транспортної мережі міста, соціальної мережі, інтернет-топології).
Реальну мережу можна вибрати на свій розсуд, якщо немає можливості придумати свою мережу, наближену до реальності.
Візуалізуйте створений граф, проведіть аналіз основних характеристик 
(наприклад, кількість вершин та ребер, ступінь вершин).
"""

#print(nx.shortest_path(G)) to check if my Дейкстра алгоритм правильный

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from task1_geos import geodata, data


def set_pos(geos:dict, G: nx, m, langt_index=1, lon_index=0) -> dict:
    pos = {}
    for key in geos:
        x,y = m(geos[key][langt_index], geos[key][lon_index])
        G.add_node(key)
        pos[key]=(x,y)
    return pos

def max_value(G):
    return max(G.degree, key=lambda x: x[1])

def sorted_degrees(G):
    return sorted(G.degree, key=lambda x: x[1], reverse=True)

def count_degress(lst):
    d = {}
    counter = 0
    for i in lst:
        if d.get(i[1]) is None:
            d[i[1]] = counter
        d[i[1]]+=1
    return d


if __name__=='__main__':
    
    G = nx.Graph()
    G.add_edges_from(data)

    m = Basemap(lat_0=20.1578888, lon_0=57.5056055)

    """Параметри графа"""

    print(f"Кількість вершин: {G.number_of_nodes()}")
    print(f"Кількість ребер: {G.number_of_edges()}")
    print(f"Вершина з найбільшої кількістю ребер: {max_value(G)}")
    print(f"Список вершин та відповідної їм кількості ребер, відсортований за спаданням: {sorted_degrees(G)}")
    print(f"Словник частот вершин відповідно до кількості ребер: {count_degress(sorted_degrees(G))}")

    
    #VISUALIZATION

    plt.figure(figsize =(9, 6), label="Flights Map") 
    node_color = [G.degree(v) for v in G]
    node_size = [40*G.degree(v) for v in G]
    nx.draw(G, with_labels=True, font_size='5', node_color = node_color, alpha=1.0,
            pos=set_pos(geodata, G, m), node_size =node_size, edge_color='#83879c', width = 0.5,
            cmap = plt.cm.tab10)
    # # plt.savefig('graph1')
    # plt.show()
    
