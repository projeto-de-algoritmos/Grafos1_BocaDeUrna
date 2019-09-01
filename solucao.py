graph = {}

def make_graph(voters):
    global graph 
    graph = {k : [] for k in range(voters+1)}

def make_edges(Q):
    global graph 
    for r in range(Q):
        a, b = map(int, input('\tInsira dois eleitores relacionados: ').split())
        graph[a].append(b) 
        graph[b].append(a) 

def bfs(v):
    global visited
    global graph

    to_visit = []
    to_visit.append(v)
    visited[v] = True

    while to_visit:
        visiting = to_visit.pop(0)

        for i in graph[visiting]:
            if not visited[i]:
                visited[i] = True
                to_visit.append(i)

def to_be_checked():
    count = 0
    for v in graph.keys():
        if not visited[v]:
            bfs(v)
            count +=1
    return count
    
voters = int(input("Insira o número de eleitores do município: "))
relations = int(input("Insira o número de relações conhecidas: "))
know_votes = int(input("Insira o número de votos apurados: "))

make_graph(voters)
make_edges(relations)

visited = {k : False for k in range(voters+1)}
visited[0] = True

if know_votes:
    E = map(int, input("Insira os eleitores que declararam seus votos: ").split())
    for v in E:
        bfs(v)

print(f"Para ter 100% de acurácia é preciso conhecer os votos de {to_be_checked()} eleitores!")
