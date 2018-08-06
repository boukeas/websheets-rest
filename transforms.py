# docutil imports
import docutils.transforms
from docutils import nodes

# before, after and group functions, to be added to the Node class
def before(node):
    index = node.parent.index(node)
    if index:
        return node.parent[index-1]
    else:
        return None

def after(node):
    index = node.parent.index(node)
    if index == len(node.parent)-1:
        return None
    else:
        return node.parent[index+1]

def group(node, cls, include_first=True):
    """
    Iterates over all nodes after this one that are instances of the cls class.
    # cls might eventually be replaced with a more general condition function
    """

    # implementation note: storing the next node before yielding the current
    # one makes it possible to modify the node yielded without affecting
    # the iterable.

    next = node.after()
    if include_first and isinstance(node, cls):
        yield node
    node = next
    if next is not None:
        next = node.after()
        while isinstance(node, cls):
            yield node
            node = next
            if next is not None:
                next = node.after()

# add before, after and group methods to nodes.Node
nodes.Node.before = before
nodes.Node.after = after
nodes.Node.group = group

def test_transform(priority):

    import sys

    class Test(docutils.transforms.Transform):

        default_priority = priority

        def apply(self):
            self.document.reporter.warning('Applying a test transform!')
            sys.stderr.write("[Test] priority: " + str(priority) + "\n")
            sys.stderr.write(str(self.document) + "\n")

    return Test


def group_transform(cls, priority):

    clsname = cls.__name__.lower() + '-group'

    class Group(docutils.transforms.Transform):
        """ Groups consecutive nodes of the cls class under a container."""

        # because the writer_aux.Admonitions transform has a priority of 920
        assert priority < 920
        default_priority = priority

        def is_first_of_group(self, node):
            return isinstance(node, cls) and not isinstance(node.before(), cls)

        def apply(self):
            for first in self.document.traverse(self.is_first_of_group):
                # determine parent of group and where to insert the container
                parent = first.parent
                point = parent.index(first)
                # create container and insert it in parent
                container = nodes.container()
                container['classes'].append(clsname)
                parent.insert(point, container)
                # gather nodes in group and move them into the container
                for node in first.group(cls):
                    parent.remove(node)
                    container.append(node)

    return Group
