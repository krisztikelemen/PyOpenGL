import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
from engine.SkyBox import SkyBox
from engine.Camera import Camera
from Planet import Planet
from enum import Enum
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
	
window = glfw.create_window(1280, 720, "OpenGL window", None, None)
glfw.set_window_pos(window, 0, 0)

if not window:
	glfw.terminate()
	raise Exception("glfw window init hiba")

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.set_cursor_pos_callback(window, cursorCallback)	
glfw.make_context_current(window)
glEnable(GL_DEPTH_TEST)
glViewport(0, 0, 1280, 720)

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

class Material(Enum):
	EMERALD = 1,
	JADE = 2,
	OBSIDIAN = 3,
	PEARL = 4,
	RUBY = 5,
	TURQUOISE = 6,
	BRASS = 7,
	BRONZE = 8,
	CHROME = 9,
	COPPER = 10,
	GOLD = 11,
	SILVER = 12,
	BLACK_PLASTIC = 13,
	CYAN_PLASTIC = 14,
	GREEN_PLASTIC = 15,
	RED_PLASTIC = 16,
	WHITE_PLASTIC = 17,
	YELLOW_PLASTIC = 18,
	BLACK_RUBBER = 19,
	CYAN_RUBBER = 20,
	GREEN_RUBBER = 21,
	RED_RUBBER = 22,
	WHITE_RUBBER = 23,
	YELLOW_RUBBER = 24,

materialType = Material.WHITE_RUBBER

if materialType is Material.EMERALD:
	glUniform3f(materialAmbientColor_loc, 0.0215, 0.1745, 0.0215)
	glUniform3f(materialDiffuseColor_loc, 0.07568, 0.61424, 0.07568)
	glUniform3f(materialSpecularColor_loc, 0.633, 0.727811, 0.633)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 76.8)

if materialType is Material.JADE:
	glUniform3f(materialAmbientColor_loc, 0.135,	0.2225,	0.1575)
	glUniform3f(materialDiffuseColor_loc, 0.54, 0.89, 0.63)
	glUniform3f(materialSpecularColor_loc, 0.316228, 0.316228, 0.316228)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 12.8)

if materialType is Material.OBSIDIAN:
	glUniform3f(materialAmbientColor_loc, 0.05375, 0.05, 0.06625)
	glUniform3f(materialDiffuseColor_loc, 0.18275, 0.17, 0.22525)
	glUniform3f(materialSpecularColor_loc, 0.332741, 0.328634, 0.346435)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 38.4)

if materialType is Material.PEARL:
	glUniform3f(materialAmbientColor_loc, 0.25, 0.20725, 0.20725)
	glUniform3f(materialDiffuseColor_loc, 1, 0.829, 0.829)
	glUniform3f(materialSpecularColor_loc, 0.296648, 0.296648, 0.296648)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 11.264)

if materialType is Material.RUBY:
	glUniform3f(materialAmbientColor_loc, 0.1745, 0.01175, 0.01175)
	glUniform3f(materialDiffuseColor_loc, 0.61424, 0.04136, 0.04136)
	glUniform3f(materialSpecularColor_loc, 0.727811, 0.626959, 0.626959)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 76.8)	

if materialType is Material.TURQUOISE:
	glUniform3f(materialAmbientColor_loc, 0.1, 0.18725, 0.1745)
	glUniform3f(materialDiffuseColor_loc, 0.396, 0.74151, 0.69102)
	glUniform3f(materialSpecularColor_loc, 0.297254, 0.30829, 0.306678)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 12.8)

if materialType is Material.BRASS:
	glUniform3f(materialAmbientColor_loc, 0.329412, 0.223529, 0.027451)
	glUniform3f(materialDiffuseColor_loc, 0.780392, 0.568627, 0.113725)
	glUniform3f(materialSpecularColor_loc, 0.992157, 0.941176, 0.807843)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 27.89743616)

if materialType is Material.BRONZE:
	glUniform3f(materialAmbientColor_loc, 0.2125, 0.1275, 0.054)
	glUniform3f(materialDiffuseColor_loc, 0.714, 0.4284, 0.18144)
	glUniform3f(materialSpecularColor_loc, 0.393548, 0.271906, 0.166721)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 25.6)

if materialType is Material.CHROME:
	glUniform3f(materialAmbientColor_loc, 0.25, 0.25, 0.25)
	glUniform3f(materialDiffuseColor_loc, 0.4, 0.4, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.774597, 0.774597, 0.774597)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 76.8)

if materialType is Material.COPPER:
	glUniform3f(materialAmbientColor_loc, 0.19125, 0.0735, 0.0225)
	glUniform3f(materialDiffuseColor_loc, 0.7038, 0.27048, 0.0828)
	glUniform3f(materialSpecularColor_loc, 0.256777, 0.137622, 0.086014)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 12.8)

if materialType is Material.GOLD:
	glUniform3f(materialAmbientColor_loc, 0.24725, 0.1995, 0.0745)
	glUniform3f(materialDiffuseColor_loc, 0.75164, 0.60648, 0.22648)
	glUniform3f(materialSpecularColor_loc, 0.628281, 0.555802, 0.366065)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 51.2)	

if materialType is Material.SILVER:
	glUniform3f(materialAmbientColor_loc, 0.19225, 0.19225, 0.19225)
	glUniform3f(materialDiffuseColor_loc, 0.50754, 0.50754, 0.50754)
	glUniform3f(materialSpecularColor_loc, 0.508273, 0.508273, 0.508273)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 51.2)

if materialType is Material.BLACK_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.01, 0.01, 0.01)
	glUniform3f(materialSpecularColor_loc, 0.5, 0.5, 0.5)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)	

if materialType is Material.CYAN_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.1, 0.06)
	glUniform3f(materialDiffuseColor_loc, 0.00, 0.50980392, 0.50980392)
	glUniform3f(materialSpecularColor_loc, 0.50196078, 0.50196078, 0.50196078)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.GREEN_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.1, 0.35, 0.1)
	glUniform3f(materialSpecularColor_loc, 0.45, 0.55, 0.45)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.RED_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.0, 0.0)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.6, 0.6)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.WHITE_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.55, 0.55, 0.55)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.7, 0.7)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)

if materialType is Material.YELLOW_PLASTIC:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.5, 0.0)
	glUniform3f(materialSpecularColor_loc, 0.6, 0.6, 0.5)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 32)	

if materialType is Material.BLACK_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.02, 0.02, 0.02)
	glUniform3f(materialDiffuseColor_loc, 0.01, 0.01, 0.01)
	glUniform3f(materialSpecularColor_loc, 0.4, 0.4, 0.4)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)	

if materialType is Material.CYAN_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.05, 0.05)
	glUniform3f(materialDiffuseColor_loc, 0.4, 0.5, 0.5)
	glUniform3f(materialSpecularColor_loc, 0.04, 0.7, 0.7)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.GREEN_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.0, 0.5, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.4, 0.5, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.04, 0.7, 0.04)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.RED_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.05, 0.0, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.4, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.04, 0.04)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.WHITE_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.05, 0.05, 0.05)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.5, 0.5)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.7, 0.7)
	glUniform3f(materialEmissionColor_loc, 0.0, 0.0, 0.0)
	glUniform1f(materialShine_loc, 10)

if materialType is Material.YELLOW_RUBBER:
	glUniform3f(materialAmbientColor_loc, 0.05, 0.05, 0.0)
	glUniform3f(materialDiffuseColor_loc, 0.5, 0.5, 0.4)
	glUniform3f(materialSpecularColor_loc, 0.7, 0.7, 0.04)
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
elapsedTime = 0

while not glfw.window_should_close(window) and not exitProgram:
	startTime = glfw.get_time()
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
		mercury.rotation += 0.017
		mercury.revolution += 0.04
		venus.rotation += 0.009
		venus.revolution += 0.016
		earth.rotation += 1.0
		earth.revolution += 0.01
		mars.rotation += 1.0
		mars.revolution += 0.005
		jupiter.rotation += 2.7
		jupiter.revolution += 0.0008
		saturn.rotation += 2.4
		saturn.revolution += 0.0003
		uranus.rotation += 1.4
		uranus.revolution += 0.0001
		neptune.rotation += 1.5
		neptune.revolution += 0.00006

	glUseProgram(shader)
	glUniform3f(viewPos_loc, camera.x, camera.y, camera.z )	

	skyBox.activateCubeMap(shader, 1)
	
	glfw.swap_buffers(window)
	
	endTime = glfw.get_time()
	elapsedTime = endTime - startTime

glfw.terminate()