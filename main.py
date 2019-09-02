from mygraph import MyGraph

def get_graph(voters):
    graph = MyGraph(graph_type='graph', size='7,3.9375!', ratio='fill')
    graph.add_cluster("unknows", "Votos a serem apurados")

    for v in range(1,voters+1):
        graph.add_nodes(v)
        graph.add_nodes_cluster("unknows", v)

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
    graph.add_cluster("knows", "Votos com valor conhecido")
    for v in E:
        graph.bfs(v, 'darkolivegreen3', "knows")

print(f"Para ter 100% de acurácia é preciso conhecer os votos de {graph.count_not_checked_components('brown2')} eleitores!")

file_name = input("Escolha um nome para o seu gif: ")

graph.save_gif(file_name)

print(f"Parabéns! Seu gif foi salvo em {file_name}.gif!")
