import hou

NODE_COLORS_MAPPING = {
    'null': (1, 0.5, 0),
    'subnet': (.71, .518, .004),
    'filecache': (.98, .275, .275),
    'object_merge': (.145, .667, .557),
    'attribvop': (.475, .812, .204),
    'attribwrangle': (.29, .565, .886),
    'volumewrangle': (.29, .565, .886),
    'timeshift': (.565, .494, .863),
    'groupcreate': (0.094, 0.3, 0.8)
}

PREFIX_COLORS_MAPPING = {
    'TEMP': (.996, .933, 0),
    'VIS': (0.322, 0.259, 0.58),
    'VIEWER': (0.094, 0.369, 0.69),
    'RENDER': (0.322, 0.259, 0.58),
    'USD': (0.996, 0.933, 0)
}


def applyColorCode():
    for n in hou.selectedNodes():
        nodeName = n.name()
        nodeTypeName = n.type().name()

        # Set node color depending on type name
        if nodeTypeName in NODE_COLORS_MAPPING.keys():
            colorRgb = NODE_COLORS_MAPPING.get(nodeTypeName)
            n.setColor(hou.Color(colorRgb))

        # Set node color depending on prefix
        for prefix, colorRgb in PREFIX_COLORS_MAPPING.items():
            if nodeName.startswith(prefix):
                n.setColor(hou.Color(colorRgb))

        if n.type().name() == 'color':
            colorRgb = (
                n.parm('colorr').eval(),
                n.parm('colorg').eval(),
                n.parm('colorb').eval()
            )
            n.setColor(hou.Color(colorRgb))
