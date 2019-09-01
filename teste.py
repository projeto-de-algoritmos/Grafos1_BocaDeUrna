from mygraph import MyGraph

if __name__ == '__main__':
    graph = MyGraph(graph_type='graph', dpi=300)
    frames = []

    for i, (src, dst) in enumerate(((1, 2), (3, 4), (2, 4), (4, 8), (9, 10), (10, 8))):
        graph.add_nodes(src, dst)
        graph.link(src, dst)

        if i > 1:
            graph.mark_node(src)

        frames.append(graph.get_image(300, 300))

    frames[0].save(
        'graph.gif',
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=len(frames) * 100,
        loop=0
    )
