from pydotplus import Dot, Edge, Node
from io import BytesIO
from PIL import Image


class MyGraph(Dot):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

        self._marked = set()

    def get_first_node(self, name):
        return self.get_node(str(name))[0]

    def add_nodes(self, *nodes_names):
        for name in nodes_names:
            node = Node(name, style='filled')
            self.add_node(node)

    def link(self, src, dst):
        src = self.get_first_node(src)
        dst = self.get_first_node(dst)

        self.add_edge(Edge(src, dst))

    def mark_node(self, name):
        node = self.get_first_node(name)

        node.set_style('radial')
        node.set_fillcolor('firebrick')
        node.set_fontcolor('white')

        self._marked.add(name)

    def get_image(self, width, height):
        img = self.create_png()
        stream = BytesIO(img)
        img = Image.open(stream)

        return img.resize((width, height))

    def is_node_marked(self, name):
        return name in self_marked
