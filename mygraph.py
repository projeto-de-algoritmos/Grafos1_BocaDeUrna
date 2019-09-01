from pydotplus import Dot, Edge, Node
from io import BytesIO
from PIL import Image


class MyGraph:

    def __init__(self, *args, **kwargs):
        self._drawing = Dot(*args, **kwargs)
        self._adjs = {}
        self._marked = {}
        self._frames = []
        self._gif_width = 300
        self._gif_height = 300

    def get_node(self, name):
        return self._drawing.get_node(str(name))[0]

    def add_nodes(self, *nodes_names):
        for name in nodes_names:
            node = Node(name, style='filled')
            self._drawing.add_node(node)
            self._frames.append(self.get_image(self._gif_width,self._gif_height))
            self._adjs[name] = []
            self._marked[name] = False

    def link(self, src, dst):
        self._adjs[src].append(dst)
        self._adjs[dst].append(src)

        src = self.get_node(src)
        dst = self.get_node(dst)
        
        self._drawing.add_edge(Edge(src, dst))
        self._frames.append(self.get_image(self._gif_width,self._gif_height))

    def mark_node(self, name):
        node = self.get_node(name)

        node.set_style('radial')
        node.set_fillcolor('firebrick')
        node.set_fontcolor('white')

        self._marked[name] = True
        
        self._frames.append(self.get_image(self._gif_width,self._gif_height))

    def get_image(self, width, height):
        img = self._drawing.create_png()
        stream = BytesIO(img)
        img = Image.open(stream)

        return img.resize((width, height))

    def is_node_marked(self, name):
        return self._marked[name]
    
    def bfs(self, name):
        to_visit = []
        to_visit.append(name)
        self.mark_node(name)

        while to_visit:
            visiting = to_visit.pop(0)

            for v in self._adjs[visiting]:
                if not self.is_node_marked(v):
                    self.mark_node(v)
                    to_visit.append(v)

    def count_not_checked_components(self):
        count = 0
        for v in self._adjs.keys():
            if not self.is_node_marked(v):
                self.bfs(v)
                count +=1
        return count
    
    def save_gif(self, file_name):
        self._frames[0].save(
            file_name + '.gif',
            format="GIF",
            append_images=self._frames[1:],
            save_all=True,
            duration=len(self._frames) * 100,
            loop=0
        )
