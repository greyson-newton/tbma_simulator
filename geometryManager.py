class geometryManager:
    # 3X3 MATRIX INITIALIZED WITH ALL 0's
    #https://developer.rhino3d.com/guides/rhinopython/python-rhinoscriptsyntax-introduction/
    from math import sin, cos, radians
    class Mat3:
        # 3X3 MATRIX INITIALIZED WITH ALL 0's
        def __init__(self):
            self.matrix = [[0 for i in range(3)],
                        [0 for i in range(3)],
                        [0 for i in range(3)]]

    class Vec2:
        # 2D VECTOR
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Vec3:
        #  3D VECTOR
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z
        def __add__(a, b):
            return Vec3(a.x+b.x, a.y+b.y, a.z+b.z)

    def multVecMatrix(vec3, mat3):
        # MULTIPLIES A Vec3 OBJECT WITH Mat3 OBJECT AND RETURNS A NEW Vec3 
        x = vec3.x * mat3.matrix[0][0] + vec3.y * mat3.matrix[0][1] + vec3.z * mat3.matrix[0][2]
        y = vec3.x * mat3.matrix[1][0] + vec3.y * mat3.matrix[1][1] + vec3.z * mat3.matrix[1][2]
        z = vec3.x * mat3.matrix[2][0] + vec3.y * mat3.matrix[2][1] + vec3.z * mat3.matrix[2][2]
        return Vec3(x, y, z)

    class Transform:
        # IT TRANSFORMS THE X AND Y FROM NORMALIZED SPACE TO SCREEN SPACE WITH PROJECTION APPLIED
        def worldSpaceTransform(self, vec3, w, h):
            if vec3.z == 0:
                vec3.z = 0.001
            zInverse = 1/ vec3.z
            xTransformed = ((vec3.x * zInverse) + 1) * (w/2)
            yTransformed = ((-vec3.y * zInverse) + 1) * (h/2)
            xTransformed = str(xTransformed)[:6]
            yTransformed = str(yTransformed)[:6]
            return Vec2(float(xTransformed), float(yTransformed))

    class Rotation:
        def rotateX(self, theta):
            # ROTATION MATRIX IN X AXIS
            sinTheta = sin(theta)
            cosTheta = cos(theta)
            m = Mat3()
            m.matrix = [[1, 0,         0],
                        [0, cosTheta,  sinTheta],
                        [0, -sinTheta, cosTheta]]
            return m

        def rotate(self, vec3, theta, axis=None):
            # ROTATES A Vec3 BY GIVEN THETA AND AXIS
            if axis == "x":
                return multVecMatrix(vec3, self.rotateX(theta))
            if axis == "y":
                return multVecMatrix(vec3, self.rotateY(theta))
            if axis == "z":
                return multVecMatrix(vec3, self.rotateZ(theta))