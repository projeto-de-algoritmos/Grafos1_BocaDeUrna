from pydotplus import Dot, Edge, Node, Cluster
from io import BytesIO
from PIL import Image
from os import path


class MyGraph:

    def __init__(self, *args, **kwargs):
        self._drawing = Dot(*args, **kwargs)
        self._adjs = {}
        self._marked = {}
        self._frames = []
    
    def add_cluster(self, name, label):
        cluster = Cluster(name)
        cluster.set_label(label)
        self._drawing.add_subgraph(cluster)

    def get_node(self, name):
        return self._drawing.get_node(str(name))[0]

    def make_node(self, name):
        return Node(
            name,
            shape='none',
            style='filled',
            color='azure2',
            image='voter.png',
            labelloc='b',
            fontname="Times-Roman:bold",
            fixedsize='true',
            width=1.0,
            height=1.0,
            fontcolor='white',
            fontsize=15,
        )


    def add_nodes(self, *nodes_names):
        this_path = path.dirname(__file__)
        this_path = path.join(this_path, 'images', 'voter.png')

        self._drawing.shape_files = [this_path]
        
        for name in nodes_names:
            node = self.make_node(name)

            self._drawing.add_node(node)
            self._adjs[name] = []
            self._marked[name] = False

    def add_nodes_cluster(self, cluster_name, *nodes_names):
        for name in nodes_names:
            node = self.make_node(name)

            cluster = self._drawing.get_subgraph("cluster_"+cluster_name)
            cluster[0].add_node(node)
            if cluster_name is not "unknows":
                self._frames.append(self.get_image())

    def del_node_cluster(self, cluster_name, node):
            cluster = self._drawing.get_subgraph("cluster_"+cluster_name)
            cluster[0].del_node(str(node))
            self._frames.append(self.get_image())

    def link(self, src, dst):
        self._adjs[src].append(dst)
        self._adjs[dst].append(src)

        src = self.get_node(src)
        dst = self.get_node(dst)
        self._drawing.add_edge(Edge(src, dst))

        self._frames.append(self.get_image())

    def mark_node(self, name, color):
        node = self.get_node(name)

        node.set_style('filled')
        node.set_fillcolor(color)

        self._marked[name] = True

        self._frames.append(self.get_image())

    def get_image(self):
        img = self._drawing.create_png()
        stream = BytesIO(img)
        img = Image.open(stream)

        return img

    def is_node_marked(self, name):
        return self._marked[name]
    
    def bfs(self, name, color, cluster=None):
        to_visit = []
        to_visit.append(name)
        self.mark_node(name, color)
        
        if cluster is not None:
            self.add_nodes_cluster(cluster, name)
            self.del_node_cluster("unknows", name)

        while to_visit:
            visiting = to_visit.pop(0)

            for v in self._adjs[visiting]:
                if not self.is_node_marked(v):
                    self.mark_node(v, color)
                    to_visit.append(v)

                    if cluster is not None:
                        self.add_nodes_cluster(cluster, v)
                        self.del_node_cluster("unknows", v)

    def count_not_checked_components(self, color):
        count = 0
        for v in self._adjs.keys():
            if not self.is_node_marked(v):
                self.add_cluster(f"unknows_{count+1}", f"Grupo #{count+1} de votos com valor desconhecido") 
                self.bfs(v, color, f"unknows_{count+1}")
                count +=1
        return count
    
    def save_gif(self, file_name):
        self._preprocess_frames()

        self._frames[0].save(
            file_name + '.gif',
            format="GIF",
            append_images=self._frames[1:],
            save_all=True,
            duration=len(self._frames) * 10,
            loop=0
        )

    def save_img(self, img_name):
        self._frames[-1].save(
            img_name + '.png',
            format="PNG",
        )

    def _preprocess_frames(self):
        biggest_w = max(i.width for i in self._frames)
        biggest_h = max(i.height for i in self._frames)

        for i, old_frame in enumerate(self._frames):
            frame = Image.new('RGBA', (biggest_w, biggest_h),
                              (255, 255, 255, 255))
            frame.paste(old_frame)
            self._frames[i] = frame
        for i in range(5):
            self._frames.append(self._frames[-1])
