import maya.cmds as cmd
import maya.OpenMaya as om 

def test_if_inside_mesh(point=(0.0, 0.0, 0.0), dir=(0.0, 0.0, 1.0)):
    sel = om.MSelectionList()
    dag = om.MDagPath()

    #replace torus with arbitrary shape name
    sel.add("pTorusShape1")
    sel.getDagPath(0,dag)

    mesh = om.MFnMesh(dag)

    point = om.MFloatPoint(*point)
    dir = om.MFloatVector(*dir)
    farray = om.MFloatPointArray()

    mesh.allIntersections(
            point, dir,
            None, None,
            False, om.MSpace.kWorld,
            10000, False,
            None, # replace none with a mesh look up accelerator if needed
            False,
            farray,
            None, None,
            None, None,
            None
        ) 
    return farray.length()%2 == 1   

#test
cmd.polyTorus()
print test_if_inside_mesh()
print test_if_inside_mesh((1,0,0))
