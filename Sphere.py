import numpy 
import math

def getPoints(radius, vertIndex, horizIndex, vertSlices, horizSlices):
	# eszaki sark:
	tx = 1.0 - horizIndex / horizSlices
	ty = vertIndex / vertSlices

	if vertIndex == 0:
		return [0.0, radius, 0.0, 0.0, 1.0, 0.0, tx, ty]
	# deli sark:
	if vertIndex == vertSlices - 1:
		return [0.0, -radius, 0.0, 0.0, -1.0, 0.0, tx, ty]
	
	alpha = math.radians(180 * (vertIndex / vertSlices))
	beta = math.radians(360 * (horizIndex / horizSlices))
	x = radius * math.sin(alpha) * math.cos(beta)
	y = radius * math.cos(alpha)
	z = radius * math.sin(alpha) * math.sin(beta)
	l = math.sqrt(x**2 + y**2 + z**2)
	nx = x / l
	ny = y / l
	nz = z / l
	return [x, y, z, nx, ny, nz, tx, ty]

def createSphere(radius, vertSlices, horizSlices):
	vertList = []
	for i in range(vertSlices):
		for j in range(horizSlices):
			vert1 = getPoints(radius, i, j, vertSlices, horizSlices)
			vert2 = getPoints(radius, i + 1, j, vertSlices, horizSlices)
			vert3 = getPoints(radius, i + 1, j + 1, vertSlices, horizSlices)
			vert4 = getPoints(radius, i, j + 1, vertSlices, horizSlices)
			vertList.extend(vert1)
			vertList.extend(vert2)
			vertList.extend(vert3)
			vertList.extend(vert4)
	return vertList

def getVertices(vertices):
	return numpy.array(vertices, dtype=numpy.float32)