# docutil imports
import docutils.transforms
from docutils import nodes
# local imports
from directives import commentary

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

###

'''
class AnonymousHyperlinks(Transform):

    """
    Link anonymous references to targets.  Given::

        <paragraph>
            <reference anonymous="1">
                internal
            <reference anonymous="1">
                external
        <target anonymous="1" ids="id1">
        <target anonymous="1" ids="id2" refuri="http://external">

    Corresponding references are linked via "refid" or resolved via "refuri"::

        <paragraph>
            <reference anonymous="1" refid="id1">
                text
            <reference anonymous="1" refuri="http://external">
                external
        <target anonymous="1" ids="id1">
        <target anonymous="1" ids="id2" refuri="http://external">
    """

    default_priority = 440

    def apply(self):
        anonymous_refs = []
        anonymous_targets = []
        for node in self.document.traverse(nodes.reference):
            if node.get('anonymous'):
                anonymous_refs.append(node)
        for node in self.document.traverse(nodes.target):
            if node.get('anonymous'):
                anonymous_targets.append(node)
        if len(anonymous_refs) \
              != len(anonymous_targets):
            msg = self.document.reporter.error(
                  'Anonymous hyperlink mismatch: %s references but %s '
                  'targets.\nSee "backrefs" attribute for IDs.'
                  % (len(anonymous_refs), len(anonymous_targets)))
            msgid = self.document.set_id(msg)
            for ref in anonymous_refs:
                prb = nodes.problematic(
                      ref.rawsource, ref.rawsource, refid=msgid)
                prbid = self.document.set_id(prb)
                msg.add_backref(prbid)
                ref.replace_self(prb)
            return
        for ref, target in zip(anonymous_refs, anonymous_targets):
            target.referenced = 1
            while True:
                if target.hasattr('refuri'):
                    ref['refuri'] = target['refuri']
                    ref.resolved = 1
                    break
                else:
                    if not target['ids']:
                        # Propagated target.
                        target = self.document.ids[target['refid']]
                        continue
                    ref['refid'] = target['ids'][0]
                    self.document.note_refid(ref)
                    break

'''

class AnonymousCommentaryHyperlinks(docutils.transforms.Transform):

    # docutils.parsers.rst.directives.references.AnonymousHyperlinks at 440
    default_priority = 439
    assert default_priority < 440

    def is_anonymous_reference(self, node):
        return isinstance(node, nodes.reference) and node['anonymous']

    def apply(self):
        # add appropriate error handling (all the else's in the if's...)
        # - every codeblock with anonymous references must be _immediately_
        #   followed by a group of (the same number of) commentaries,
        #   excluding orphan commentaries
        self.document.reporter.warning('Applying anonymous reference transform!')
        for codeblock in self.document.traverse(nodes.literal_block):
            # collect anonymous references
            references = [ref for ref in codeblock.traverse(self.is_anonymous_reference)]
            if references:
                # collect non-orphan commentaries
                next = codeblock.after()
                if next:
                    commentaries = [node for node in next.group(commentary)
                                    if 'orphan' not in node]

                    if len(references) == len(commentaries):
                        for ref, target in zip(references, commentaries):
                            # must unset anonymous attr, otherwise the reference
                            # is also processed by other transforms
                            del ref['anonymous']
                            #
                            if not target['ids']:
                                self.document.set_id(target)
                            ref['refid'] = target['ids'][0]
                            self.document.note_refid(ref)
                            target.referenced = 1

                # TODO:
                # - set refid's
                # - probably remove names from references
