from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define los vértices del cubo
vertices = [
    [-1, -1, -1],
    [ 1, -1, -1],
    [ 1,  1, -1],
    [-1,  1, -1],
    [-1, -1,  1],
    [ 1, -1,  1],
    [ 1,  1,  1],
    [-1,  1,  1]
]

# Define las caras del cubo (con índices de los vértices)
caras = [
    [0, 1, 2, 3],  # Cara trasera
    [4, 5, 6, 7],  # Cara delantera
    [0, 3, 7, 4],  # Cara izquierda
    [1, 2, 6, 5],  # Cara derecha
    [3, 2, 6, 7],  # Cara superior
    [0, 1, 5, 4]   # Cara inferior
]

# Colores para cada cara
colores = [
    [1, 0, 0],  # Rojo
    [0, 1, 0],  # Verde
    [0, 0, 1],  # Azul
    [1, 1, 0],  # Amarillo
    [1, 0, 1],  # Magenta
    [0, 1, 1]   # Cyan
]

# Función para dibujar el cubo
def dibujarCubo():
    glBegin(GL_QUADS)
    for i, cara in enumerate(caras):
        glColor3fv(colores[i])  # Aplica color a cada cara
        for vertice in cara:
            glVertex3fv(vertices[vertice])  # Dibuja los vértices
    glEnd()

# Configuración inicial de OpenGL
def inicializar():
    glClearColor(0, 0, 0, 1)  # Fondo negro
    glEnable(GL_DEPTH_TEST)   # Activa el test de profundidad

# Bucle principal de renderizado
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(3, 4, 5, 0, 0, 0, 0, 1, 0)  # Posición de la cámara
    dibujarCubo()
    glutSwapBuffers()

# Configurar perspectiva de la ventana
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# Inicialización de GLUT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Renderizado de Cubo en PyOpenGL")
inicializar()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMainLoop()

