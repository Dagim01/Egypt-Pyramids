import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture
from ObjLoader import ObjLoader
from camera import Camera

def getFileContents(filename):
    p = os.path.join(os.getcwd(), "shaders", filename)
    return open(p, 'r').read()


vertexShaderContent = getFileContents("triangle.vertex.shader")
fragmentShaderContent = getFileContents("triangle.fragment.shader")

cam = Camera()
WIDTH, HEIGHT = 1280, 720
position1,position2 = WIDTH/2, HEIGHT/2
first_mouse = True
left, right, forward, backward = False, False, False, False

def mouse_look_clb(window, xpos, ypos):
    global first_mouse,position1, position2

    if first_mouse:
        position1 = xpos
        position2 = ypos
        first_mouse = False

    xoffset = xpos - position1
    yoffset = position2 - ypos

    position1 = xpos
    position2 = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    
    if key == glfw.KEY_W and action == glfw.PRESS:
            forward = True
    elif key == glfw.KEY_W and action == glfw.RELEASE:
        forward = False
    if key == glfw.KEY_S and action == glfw.PRESS:
        backward = True
    elif key == glfw.KEY_S and action == glfw.RELEASE:
        backward = False
    if key == glfw.KEY_A and action == glfw.PRESS:
        left = True
    elif key == glfw.KEY_A and action == glfw.RELEASE:
        left = False
    if key == glfw.KEY_D and action == glfw.PRESS:
        right = True
    elif key == glfw.KEY_D and action == glfw.RELEASE:
        right = False

def do_movement():
    if left:
        cam.process_keyboard("LEFT", 0.03)
    if right:
        cam.process_keyboard("RIGHT", 0.03)
    if forward:
        cam.process_keyboard("FORWARD", 0.03)
    if backward:
        cam.process_keyboard("BACKWARD", 0.03)  


def window_resize_clb(window, width, height):
    glViewport(0, 0, width, height)
    projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(WIDTH, HEIGHT, "My OpenGL window", None, None)
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

glfw.set_window_pos(window, 400, 200)
glfw.set_window_size_callback(window, window_resize_clb)
glfw.set_cursor_pos_callback(window, mouse_look_clb)
glfw.set_key_callback(window, key_input_clb)
glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
glfw.make_context_current(window)

# loading 3d objects here
pyramid1_idx, pyramid_buf = ObjLoader.load_model("meshes/pyramid22.obj")
pyramid2_idx, pyramid2_buf = ObjLoader.load_model("meshes/pyramid11.obj")
floor_indices, floor_buf = ObjLoader.load_model("meshes/floor.obj")

shader = compileProgram(compileShader(vertexShaderContent, GL_VERTEX_SHADER), compileShader(fragmentShaderContent, GL_FRAGMENT_SHADER))

#VAO and VBO
VAO = glGenVertexArrays(3)
VBO = glGenBuffers(3)

glBindVertexArray(VAO[0])
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, pyramid_buf.nbytes, pyramid_buf, GL_STATIC_DRAW)

# pyramid 1 vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, pyramid_buf.itemsize * 8, ctypes.c_void_p(0))
# pyramid 1 textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, pyramid_buf.itemsize * 8, ctypes.c_void_p(12))
# pyramid 1 normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, pyramid_buf.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


glBindVertexArray(VAO[1])
#pyramid 2 Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
glBufferData(GL_ARRAY_BUFFER, pyramid2_buf.nbytes, pyramid2_buf, GL_STATIC_DRAW)

# pyramid 2 vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, pyramid2_buf.itemsize * 8, ctypes.c_void_p(0))
# pyramid 2 textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, pyramid2_buf.itemsize * 8, ctypes.c_void_p(12))
# pyramid 2 normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, pyramid2_buf.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# sand VAO
glBindVertexArray(VAO[2])
# sad Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, floor_buf.nbytes, floor_buf, GL_STATIC_DRAW)

# sand vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buf.itemsize * 8, ctypes.c_void_p(0))
# sand textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buf.itemsize * 8, ctypes.c_void_p(12))
# floor normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buf.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)


textures = glGenTextures(3)
load_texture("meshes/pyramid1.jpg", textures[0])
load_texture("meshes/pyramid2.jpg", textures[1])
load_texture("meshes/floor.jpg", textures[2])

glUseProgram(shader)
glClearColor(0.42, 0.82, 0.92, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, WIDTH / HEIGHT, 0.1, 100)
pyramid1_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([6, 0, 0]))
pyramid2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, -4]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

while not glfw.window_should_close(window):
    glfw.poll_events()
    do_movement()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    # rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())
    model = pyrr.matrix44.multiply(1, pyramid1_pos)

    # drawing 1st pyramid
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawArrays(GL_TRIANGLES, 0, len(pyramid2_idx))

    # drawing 2nd pyramid
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyramid2_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(pyramid2_idx))

    # drawing the floor
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    glfw.swap_buffers(window)


glfw.terminate()
