import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
from engine.SkyBox import SkyBox
from engine.Camera import Camera
from engine.Texture import Texture
from Planet import Planet
import numpy
import pyrr
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

xPosPrev = 0
yPosPrev = 0
firstCursorCallback = True
sensitivity = 0.05

def cursorCallback(window, xPos, yPos):
	global firstCursorCallback
	global sensitivity
	global xPosPrev, yPosPrev
	if firstCursorCallback:
		firstCursorCallback = False	
	else:
		xDiff = xPos - xPosPrev
		yDiff = yPosPrev - yPos
		camera.rotateUpDown(yDiff * sensitivity)
		camera.rotateRightLeft(xDiff * sensitivity)

	xPosPrev = xPos
	yPosPrev = yPos

if not glfw.init():
	raise Exception("glfw init hiba")
	
window = glfw.create_window(1280, 720, "Solar System Simulation", None, None)
glfw.set_window_pos(window, 0, 0)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_cursor_pos_callback(window, cursorCallback)	
glfw.make_context_current(window)
glEnable(GL_DEPTH_TEST)
glViewport(0, 0, 1280, 720)

### Framebuffer
frameBuffer = glGenFramebuffers(1)
glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer)

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)

glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1280, 720, 0, GL_RGB, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glBindTexture(GL_TEXTURE_2D, 0)

glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture, 0)

rbo = glGenRenderbuffers(1)
glBindRenderbuffer(GL_RENDERBUFFER, rbo)
glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, 1280, 720) 
glBindRenderbuffer(GL_RENDERBUFFER, 0)

glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo)

glBindFramebuffer(GL_FRAMEBUFFER, 0)

with open("./shaders/screen.vert") as f:
	vertex_shader = f.read()

with open("./shaders/screen.frag") as f:
	fragment_shader = f.read()

screen_shader = compileProgram(
	compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

glUseProgram(0)

vertices = [
	-1,  1, 0, 0,
	 1,  1, 1, 0,
	 1, -1, 1, 1,
	-1, -1, 0, 1
]

vertices = numpy.array(vertices, dtype=numpy.float32)
screen = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, screen)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, 0)

camera = Camera(0, 10, 70)

with open("./shaders/texture.vert") as f:
	vertex_shader = f.read()
with open("./shaders/texture.frag") as f:
	fragment_shader = f.read()

shader = compileProgram(
	compileShader(vertex_shader, GL_VERTEX_SHADER),
	compileShader(fragment_shader, GL_FRAGMENT_SHADER),
	validate=False
)

exitProgram = False

skyBox = SkyBox(
	"./cubemap/right.jpg", 
	"./cubemap/left.jpg", 
	"./cubemap/top.jpg", 
	"./cubemap/bottom.jpg", 
	"./cubemap/front.jpg", 
	"./cubemap/back.jpg"
)

perspMat = pyrr.matrix44.create_perspective_projection_matrix(45.0, 1280.0 / 720.0, 0.1, 100.0)

glUseProgram(shader)

lightX = 0.0
lightY = 0.0
lightZ = 0.0
lightPos_loc = glGetUniformLocation(shader, 'lightPos');
viewPos_loc = glGetUniformLocation(shader, 'viewPos');

glUniform3f(lightPos_loc, lightX, lightY, lightZ)
glUniform3f(viewPos_loc, camera.x, camera.y, camera.z )

materialAmbientColor_loc = glGetUniformLocation(shader, "materialAmbientColor")
materialDiffuseColor_loc = glGetUniformLocation(shader, "materialDiffuseColor")
materialSpecularColor_loc = glGetUniformLocation(shader, "materialSpecularColor")
materialEmissionColor_loc = glGetUniformLocation(shader, "materialEmissionColor")
materialShine_loc = glGetUniformLocation(shader, "materialShine")

lightAmbientColor_loc = glGetUniformLocation(shader, "lightAmbientColor")
lightDiffuseColor_loc = glGetUniformLocation(shader, "lightDiffuseColor")
lightSpecularColor_loc = glGetUniformLocation(shader, "lightSpecularColor")

glUniform3f(lightAmbientColor_loc, 1.0, 1.0, 1.0)
glUniform3f(lightDiffuseColor_loc, 1.0, 1.0, 1.0)
glUniform3f(lightSpecularColor_loc, 1.0, 1.0, 1.0)

glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
glUniform3f(materialDiffuseColor_loc, 0.0, 0.0, 0.0)
glUniform3f(materialSpecularColor_loc, 0.0, 0.0, 0.0)
glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
glUniform1f(materialShine_loc, 10)	

perspectiveLocation = glGetUniformLocation(shader, "projection")
worldLocation = glGetUniformLocation(shader, "world")
viewLocation = glGetUniformLocation(shader, "view")
viewWorldLocation = glGetUniformLocation(shader, "viewWorld")

perspMat = pyrr.matrix44.create_perspective_projection_matrix(45.0, 1280.0 / 720.0, 0.1, 1000.0)
glUniformMatrix4fv(perspectiveLocation, 1, GL_FALSE, perspMat)

sun = Planet("sun", 7, 0)
mercury = Planet("mercury", 0.4, 21.0)
venus = Planet("venus", 0.95, 32.0)
earth = Planet("earth", 1, 42.0)
mars = Planet("mars", 0.53, 53.0)
jupiter = Planet("jupiter", 5, 77.0)
saturn = Planet("saturn", 4.5, 112.0)
uranus = Planet("uranus", 2.8, 137.0)
neptune = Planet("neptune", 2.7, 167.0)

for planet in [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]:
	planet.setLightPos(lightX, lightY, lightZ)

viewMat = pyrr.matrix44.create_look_at([0.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0])
screenTexture = Texture("./assets/screen.jpg")
startTime = 0

while not glfw.window_should_close(window) and not exitProgram:
	# startTime = glfw.get_time()
	glfw.poll_events()

	if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
		exitProgram = True

	directionTry = 0
	directionReal = 0
	if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
		directionTry = -30*elapsedTime
		directionReal = -15*elapsedTime
	if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
		directionTry = 30*elapsedTime
		directionReal = 15*elapsedTime
	camera.move(directionTry)

	glClearDepth(1.0)
	glClearColor(0, 0.1, 0.1, 1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

	skyBox.render(perspMat, camera.getMatrixForCubemap())

	for planet in [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]:
		planet.render(camera, perspMat)

	if earth.revolution <= 360:
		mercury.rotation += 0.17
		mercury.revolution += 0.4
		venus.rotation += 0.09
		venus.revolution += 0.16
		earth.rotation += 10.0
		earth.revolution += 0.1
		mars.rotation += 10.0
		mars.revolution += 0.05
		jupiter.rotation += 27.0
		jupiter.revolution += 0.008
		saturn.rotation += 24.0
		saturn.revolution += 0.003
		uranus.rotation += 14.0
		uranus.revolution += 0.001
		neptune.rotation += 15.0
		neptune.revolution += 0.0006

		glUseProgram(shader)
		glUniform3f(viewPos_loc, camera.x, camera.y, camera.z )	
		skyBox.activateCubeMap(shader, 1)
	else:
		glClearDepth(1.0)
		glClearColor(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		glDisable(GL_DEPTH_TEST)

		glUseProgram(screen_shader)

		Texture.enableTexturing()
		screenTexture.activate()

		glBindBuffer(GL_ARRAY_BUFFER, screen)
        
		position_loc = glGetAttribLocation(screen_shader, 'in_position')
		glEnableVertexAttribArray(position_loc)
		glVertexAttribPointer(position_loc, 2, GL_FLOAT, False, vertices.itemsize * 4, ctypes.c_void_p(0))

		texture_loc = glGetAttribLocation(screen_shader, 'in_texCoord')
		glEnableVertexAttribArray(texture_loc)
		glVertexAttribPointer(texture_loc, 2, GL_FLOAT, False, vertices.itemsize * 4, ctypes.c_void_p(8))

		glBindBuffer(GL_ARRAY_BUFFER, 0)	
		glDrawArrays(GL_QUADS, 0, 4)

	glfw.swap_buffers(window)
	
	endTime = glfw.get_time()
	elapsedTime = endTime - startTime

	if elapsedTime > 36:
		exitProgram = True

glfw.terminate()