import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import impasse

def load_and_draw_model(filename):
    # Load the model using impasse
    scene = impasse.load(filename)

    # This example only draws the first mesh in the first node; more complex models require recursive traversal
    if scene.meshes and scene.root_node.children:
        mesh = scene.meshes[0]
        for face in mesh.faces:
            GL.glBegin(GL.GL_POLYGON)
            for index in face:
                vertex = mesh.vertices[index]
                GL.glVertex3fv(vertex)
            GL.glEnd()

def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glLoadIdentity()
    GL.glTranslatef(0.0, 0.0, -5)

    load_and_draw_model('02773838/1b9ef45fefefa35ed13f430b2941481/models/model_normalized.obj')  # Update this path to your model file

    GLUT.glutSwapBuffers()

def main():
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(800, 600)
    GLUT.glutCreateWindow(b'3D Model with Assimp and OpenGL')

    GL.glClearColor(0.0, 0.0, 0.0, 1)
    GL.glEnable(GL.GL_DEPTH_TEST)

    GLUT.glutDisplayFunc(display)
    GLUT.glutMainLoop()

if __name__ == '__main__':
    main()
