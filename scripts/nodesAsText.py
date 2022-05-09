import hou
from pprint import pprint


def getItemDict(node, recursive=True):
    """From a Houdini item, get the contents

    :param node: Node to get a content dict from
    :type node: hou.Node()
    :param recursive: In recursive mode, this will recurse on all sub-children items
    :type recursive: bool
    :return: A dictionary containing information on the node's contents
    :rtype: dict
    """
    item = dict()
    nodeTypeName = node.type().name()
    item['__node_type_name__'] = nodeTypeName
    item['__node_position_x__'] = node.position().x()
    item['__node_position_y__'] = node.position().y()
    item['__node_color_rgb__'] = node.color().rgb()
    item['__inputs__'] = [i.name() for i in node.inputs()]

    for parm in node.parms():
        item[parm.name()] = '{}'.format(parm.evalAsString())

    if nodeTypeName == 'subnet' and recursive:
        item['__subnet_contents__'] = dict()
        for child in node.allSubChildren():
            childName = child.name()
            item['__subnet_contents__'][childName] = getItemDict(child)

    return item


def copySelectionAsText():
    """This will copy all selected nodes to clipboard as text. This is especially useful when working remotely"""
    # TODO : support for all items, not just nodes
    items = dict()

    for node in hou.selectedNodes():
        nName = node.name()
        items[nName] = getItemDict(node)

    hou.ui.copyTextToClipboard(str(items))

    return items


copySelectionAsText()
