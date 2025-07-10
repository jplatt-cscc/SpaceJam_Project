from panda3d.core import PandaNode, Loader, NodePath, CollisionNode, CollisionCapsule, CollisionSphere, CollisionInvSphere, Vec3


class PlacedObject(PandaNode):
    """ . """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
        self.modelNode: NodePath = loader.loadModel(modelPath)
        
        # Error checking
        if not isinstance(self.modelNode, NodePath):
            raise AssertionError('PlacedObject loader.loadModel(' + modelPath + ') did not return a proper PandaNode!')
        
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)


class CollidableObject(PlacedObject):
    """ . """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
        super(CollidableObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        self.collisionNode.show()


class InverseSphereCollider(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(InverseSphereCollider, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(CollisionInvSphere(colPositionVec, colRadius))
        self.collisionNode.show()


class CapsuleCollider(CollidableObject):
    # 'a' represents the top coordinate of the collider & 'b' represents the bottom coordinate
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, ax: float, ay: float, az: float, bx: float, by: float, bz: float, r: float):
        super(CapsuleCollider, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(CollisionCapsule(ax, ay, az, bx, by, bz, r))
        self.collisionNode.show()


class SphereCollider(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(SphereCollider, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(CollisionSphere(colPositionVec, colRadius))
        self.collisionNode.show()