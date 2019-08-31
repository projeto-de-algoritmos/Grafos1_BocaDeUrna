graph = {}

def make_graph(N):
    global graph 
    graph = {k : [] for k in range(N+1)}

def make_edges(Q):
    global graph 
    for r in range(Q):
        a, b = map(int, input('\tInsira os vértices da relação: ').split())
        graph[a].append(b) 
        graph[b].append(a) 
        print(graph)

N = int(input("Insira o número de habitantes do município: "))

make_graph(N)

Q = int(input("Insira o número de relações conhecidas: "))

make_edges(Q)

print(graph)





