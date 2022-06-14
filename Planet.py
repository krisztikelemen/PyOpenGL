from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL.shaders
from engine.Texture import Texture
from Sphere import *
from pygame import Vector3
import numpy
import pyrr

class Planet:
	def __init__(self, name, radius, distance):
		self.radius = radius
		self.distance = distance
		self.vertSlices = 50
		self.horizSlices = 50
		self.zTranslate = -100
		self.revolution = 0.0
		self.rotation = 0.0
		
		vertices = createSphere(radius, 50, 50)
		self.sphereVertCount = int(len(vertices) / 6)
		vertices = numpy.array(vertices, dtype=numpy.float32)

		self.Buffer = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)
		glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
		glBindBuffer(GL_ARRAY_BUFFER, 0)

		with open("./shaders/planet.vert") as f:
			vertex_shader = f.read()
		with open("./shaders/planet.frag") as f:
			fragment_shader = f.read()

		self.shader = OpenGL.GL.shaders.compileProgram(
			OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
    		OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
		)

		self.Texture = Texture("./assets/" + str(name) + ".jpg")
	
	def setLightPos(self, x, y, z):
		self.lightX = x
		self.lightY = y
		self.lightZ = z

	def render(self, camera, projectionMatrix):

		glUseProgram(self.shader)

		materialAmbientColor_loc = glGetUniformLocation(self.shader, "materialAmbientColor")
		materialDiffuseColor_loc = glGetUniformLocation(self.shader, "materialDiffuseColor")
		materialSpecularColor_loc = glGetUniformLocation(self.shader, "materialSpecularColor")
		materialEmissionColor_loc = glGetUniformLocation(self.shader, "materialEmissionColor")
		materialShine_loc = glGetUniformLocation(self.shader, "materialShine")
		glUniform3f(materialAmbientColor_loc, 0.25, 0.25, 0.25)
		glUniform3f(materialDiffuseColor_loc, 0.4, 0.4, 0.4)
		glUniform3f(materialSpecularColor_loc, 0.774597, 0.774597, 0.774597)
		glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
		glUniform1f(materialShine_loc, 76.8)

		lightAmbientColor_loc = glGetUniformLocation(self.shader, "lightAmbientColor")
		lightDiffuseColor_loc = glGetUniformLocation(self.shader, "lightDiffuseColor")
		lightSpecularColor_loc = glGetUniformLocation(self.shader, "lightSpecularColor")

		glUniform3f(lightAmbientColor_loc, 1.0, 1.0, 1.0)
		glUniform3f(lightDiffuseColor_loc, 1.0, 1.0, 1.0)
		glUniform3f(lightSpecularColor_loc, 1.0, 1.0, 1.0)

		lightPos_loc = glGetUniformLocation(self.shader, 'lightPos')
		viewPos_loc = glGetUniformLocation(self.shader, 'viewPos')
		glUniform3f(lightPos_loc, self.lightX, self.lightY, self.lightZ)
		glUniform3f(viewPos_loc, camera.x, camera.y, camera.z)

		proj_loc = glGetUniformLocation(self.shader, 'projection')
		view_loc = glGetUniformLocation(self.shader, 'view')
		world_loc = glGetUniformLocation(self.shader, 'world')
		glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projectionMatrix)
		glUniformMatrix4fv(view_loc, 1, GL_FALSE, camera.getMatrix())

		Texture.enableTexturing()

		glBindBuffer(GL_ARRAY_BUFFER, self.Buffer)

		position_loc = glGetAttribLocation(self.shader, 'in_position')
		glEnableVertexAttribArray(position_loc)
		glVertexAttribPointer(position_loc, 3, GL_FLOAT, False, 4 * 8, ctypes.c_void_p(0))

		normal_loc = glGetAttribLocation(self.shader, 'in_normal')
		glEnableVertexAttribArray(normal_loc)
		glVertexAttribPointer(normal_loc, 3, GL_FLOAT, False, 4 * 8, ctypes.c_void_p(12))

		texture_loc = glGetAttribLocation(self.shader, 'in_texture')
		glEnableVertexAttribArray(texture_loc)
		glVertexAttribPointer(texture_loc, 2, GL_FLOAT, False, 4 * 8, ctypes.c_void_p(24))

		self.Texture.activate()
		
		# transMat = pyrr.matrix44.create_from_translation(pyrr.Vector3([self.distance, 0, self.zTranslate]))
		# rotMat = pyrr.matrix44.create_from_y_rotation(math.radians(self.angle))
		# worldMat = pyrr.matrix44.multiply(rotMat, transMat)
		# glUniformMatrix4fv(world_loc, 1, GL_FALSE, worldMat)

		transMat = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
		rotMat = pyrr.matrix44.create_from_y_rotation(math.radians(self.revolution))
		worldMat = pyrr.matrix44.multiply(rotMat, transMat)
		glUniformMatrix4fv(world_loc, 1, GL_FALSE, worldMat)

		transMat2 = pyrr.matrix44.create_from_translation(pyrr.Vector3([self.distance, 0, 0]))
		worldMat2 = pyrr.matrix44.multiply(transMat2, worldMat)
		glUniformMatrix4fv(world_loc, 1, GL_FALSE, worldMat2)

		rotMat2 = pyrr.matrix44.create_from_y_rotation(math.radians(self.rotation))
		worldMat3 = pyrr.matrix44.multiply(rotMat2, worldMat2)
		glUniformMatrix4fv(world_loc, 1, GL_FALSE, worldMat3)

		glDrawArrays(GL_QUADS, 0, self.sphereVertCount)

		glUseProgram(0)