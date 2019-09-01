from mygraph import MyGraph

def get_graph(voters):
    graph = MyGraph(graph_type='graph', dpi=300)

    for v in range(1,voters+1):
        graph.add_nodes(v)

    return graph

voters = int(input("Insira o número de eleitores do município: "))
relations = int(input("Insira o número de relações conhecidas: "))

graph = get_graph(voters)

for r in range(relations):
        a, b = map(int, input('\tInsira dois eleitores relacionados: ').split())
        graph.link(a, b)


know_votes = int(input("Insira o número de votos apurados: "))

if know_votes:
    E = map(int, input("Insira os eleitores que declararam seus votos: ").split())
    for v in E:
        graph.bfs(v)

print(f"Para ter 100% de acurácia é preciso conhecer os votos de {graph.count_not_checked_components()} eleitores!")

img = graph.get_image(300, 300)
img.show()
