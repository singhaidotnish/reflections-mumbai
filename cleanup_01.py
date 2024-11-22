import maya.cmds as cmds
import math

# defines a value to not delete an edge based on whether the u or v values of two uvs in question are within this threshold
keepTol = 0.0001

# user selects a set of uvs
uvSelection = cmds.ls( selection=True, flatten=True )
# for all uvs in the selection
for uv in uvSelection :
    # set the first uv
    uv1 = uv
    # get the uv value
    uv1Val = cmds.polyEditUV( uv1, query=True )
    # get the adjacent edges
    adjEdges = cmds.polyListComponentConversion( uv1, toEdge=True )
    # get the adjacent uvs
    adjUvs = cmds.polyListComponentConversion( adjEdges, toUV=True )
    # select the uvs
    cmds.select( adjUvs )
    # remove the first uv from the selection
    cmds.select( uv1, deselect=True )
    # set the adjacent uvs
    adjUvs = cmds.ls( selection=True, flatten=True )
    # for the adjacent uvs
    for xy in adjUvs :
        # set the second uv
        uv2 = xy
        # get the uv values
        uv2Val = cmds.polyEditUV( uv2, query=True )
        # if the first and second uvs don't match within a given tolerance
        if abs( uv1Val[0] - uv2Val[0] ) > keepTol and abs( uv1Val[1] - uv2Val[1] ) > keepTol : # proceed to delete the edge between
            # get the vertices
            verts = cmds.polyListComponentConversion( uv1, uv2, toVertex=True )
            # get the edge
            edge = cmds.polyListComponentConversion( verts[0], verts[1], toEdge=True, internal=True )
            # delete the edge
            cmds.polyDelEdge( edge, cv=False )
            # exit the loop
            break
