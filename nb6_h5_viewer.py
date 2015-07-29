"""
    NBODY6/NBODY6++ HDF5 data viewer
    COLOR ==> effective temperature; SIZE ==> mass
    Author: Maxwell Xu CAI (NAOC/KIAA) maxwellemail@gmail.com
    Date: Dec 8, 2014
    License: GPL

    Usage: modify the 'self.h5_file_name' line to load the HDF5 file.
           running the code with 'python nb6_h5_viewer.py'.
           use 'n' and 'm' to navigate to the previous frame and next frame, respectively.
"""



import os
import numpy as np

from vispy import gloo
from vispy import app
from vispy.gloo import gl
from vispy.util.transforms import perspective, translate, rotate

import h5py


class Viewer:

    def __init__(self):
        self.h5_file_name = '/Users/maxwell/Works/visnb6/run/data.h5part'
        self.canvas = Canvas(self)
        try:
            self.h5_file = h5py.File(self.h5_file_name, 'r')
            self.nsteps = len(self.h5_file)
            self.ntot = 0 # will be set later
            self.current_step_id = 0
            self.current_step_len = 0
            self.current_step_data = None
        except Exception:
            self.h5_file = None
            self.nsteps = 0
            self.ntot = 0
            self.current_step_id = 0
            self.current_step_len = 0
            self.current_step_data = None

    def show(self):
        # Load the first frame
        self.canvas.set_frame_data(self.load_data_by_step_id(0))
        self.canvas.show()
        app.run()


    def load_next_frame(self):
        data = None
        if self.current_step_id < self.nsteps - 1:
            data = self.load_data_by_step_id(self.current_step_id + 1)
            if data != None and data > 0:
                self.current_step_id += 1
                return data
            else:
                return None


    def load_prev_frame(self):
        data = None
        if self.current_step_id < self.nsteps - 1:
            data = self.load_data_by_step_id(self.current_step_id - 1)
            if data != None and data > 0:
                self.current_step_id -= 1
                return data
            else:
                return None



    def set_h5_file(filename):
        """
        Set the HDF5 file name and open the file.
        """
        if os.path.isfile(filename):
            try:
                self.h5_file_name = filename
                self.h5_file = h5py.File(self.h5_file_name, 'r')
                self.nsteps = len(self.h5_file)
                return 0
            except Exception:
                print 'Error opening the HDF5 file:', filename
                return -1


    def load_data_by_step_id(self, step_id):
        if self.h5_file == None:
            print 'Error: HDF5 file not set!'
            return -1
        if self.nsteps < step_id or step_id < 0:
            print 'Error: invalid step_id (not in range)!'
            return -2

        try:
            h5_step = self.h5_file['Step#' + str(step_id)]
            ntot = h5_step.attrs['TotalN']
            self.current_step_len = len(h5_step['X'])
            n = len(h5_step['X'])
            P = np.zeros((n,3), dtype=np.float32)

            X, Y, Z =  P[:,0],P[:,1],P[:,2]
            X[...] = h5_step['X'][...]
            Y[...] = h5_step['Y'][...]
            Z[...] = h5_step['Z'][...]
            t_eff = h5_step['TEFF'][...]

            # Color determination according to the effective temperature
            color_r = np.zeros(n)
            color_g = np.zeros(n)
            color_b = np.zeros(n)
            i = 0
            for t in t_eff:
                t = t/100
                if t <= 66:
                    color_r[i] = 255
                    color_g[i] = t
                    color_g[i] = 99.4708025861 * np.log(color_g[i]) - 161.1195681661
                    if color_g[i] < 0: color_b[i] = 0
                    if color_g[i] > 255: color_b[i] = 255

                    if t <= 19:
                        color_b[i] = 0
                    else:
                        color_b[i] = t - 10
                        color_b[i] = 138.5177312231 * np.log(color_b[i]) - 305.0447927307
                        if color_b[i] < 0: color_b[i] = 0
                        if color_b[i] > 255: color_b[i] = 255
                else:
                    color_r[i] = t - 60
                    color_r[i] = 329.698727446 * (color_r[i] ** -0.1332047592)
                    if color_r[i] < 0: color_r[i] = 0
                    if color_r[i] > 255: color_r[i] = 255

                    color_g[i] = t - 60
                    color_g[i] = 288.1221695283 * (color_g[i] ** -0.0755148492)
                    if color_g[i] < 0: color_g[i] = 0
                    if color_g[i] > 255: color_g[i] = 255

                    color_b[i] = 255

                i += 1
            color_r = color_r/255
            color_b = color_b/255
            color_g = color_g/255

            # Dot size determination according to the mass
            S = np.zeros(n)
            S[...] = (h5_step['Mass'][...])**(1./3)*50


            # Wrap the data into a package
            data = np.zeros(n, [('a_position', np.float32, 3),
                                ('a_size',     np.float32, 1),
                                ('color_r',     np.float32, 1),
                                ('color_g',     np.float32, 1),
                                ('color_b',     np.float32, 1)])

            data['color_r'] = color_r
            data['color_g'] = color_g
            data['color_b'] = color_b
            data['a_position'] = P
            data['a_size'] = S

            self.current_step_data = data
            self.current_step_id = step_id
            self.current_step_length = n
            self.ntot = ntot
            return data
        except Exception:
            print 'Error loading HDF5 data!'
            return -3




class Canvas(app.Canvas):
    def __init__(self, viewer_helper):

        # ==================================================
        # Define graphics constants
        self.MAX_THETA_SPEED = 1.2
        self.MAX_PHI_SPEED = 1.2

        self.CMAP = np.array([[255, 255,   255], [255, 163,  76],
            [137, 177, 255]], dtype=np.uint8).reshape(1,3,3) # color map


        #OpenGL vertex shader
        self.VERT_SHADER = """
        // Uniforms
        // ------------------------------------
        uniform mat4  u_model;
        uniform mat4  u_view;
        uniform mat4  u_projection;
        uniform float u_size;


        // Attributes
        // ------------------------------------
        attribute vec3  a_position;
        attribute float a_size;
        //attribute float a_dist;
        attribute float color_r;
        attribute float color_g;
        attribute float color_b;

        // Varyings
        // ------------------------------------
        varying float v_size;
        varying float v_dist;
        varying float v_color_r;
        varying float v_color_g;
        varying float v_color_b;

        void main (void) {
            v_size  = a_size*u_size;
            v_color_r = color_r;
            v_color_g = color_g;
            v_color_b = color_b;
            //v_color_r = 0.5;
            //v_color_g = 0.3;
            //v_color_b = 0.9;
            gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
            gl_PointSize = v_size;
        }
        """

        # OpenGl Fragment shader
        self.FRAG_SHADER = """
        // Uniforms
        // ------------------------------------
        //uniform sampler2D u_colormap;

        // Varyings
        // ------------------------------------
        varying float v_size;
        varying float v_dist;
        varying float v_color_r;
        varying float v_color_g;
        varying float v_color_b;

        // Main
        // ------------------------------------
        void main()
        {
            float a = 2*(length(gl_PointCoord.xy - vec2(0.5,0.5)) / sqrt(2.0));
            //vec3 color = texture2D(u_colormap, vec2(v_dist,.5)).rgb;
            //gl_FragColor = vec4(color,(1-a)*.25);
            gl_FragColor = vec4(v_color_r, v_color_g, v_color_b, (1-a)*1.0);
        }
        """

        # ==================================================
        # Instance variables
        self.viewer_helper = viewer_helper
        app.Canvas.__init__(self)
        self.size = 800, 600
        self.title = "NBODY6 HDF5 Viewer"
        self.program = gloo.Program(self.VERT_SHADER, self.FRAG_SHADER)
        self.view = np.eye(4,dtype=np.float32)
        self.model = np.eye(4,dtype=np.float32)
        self.projection = np.eye(4,dtype=np.float32)
        self.theta, self.phi = 0,0

        self.translate = 5
        translate(self.view, 0,0, -self.translate)
        self.program.set_vars(u_size = 5./self.translate,
                              u_model = self.model,
                              u_view = self.view)
        self.timer_dt = 1.0/60
        self.timer_t = 0.0
        self.timer = app.Timer(self.timer_dt)
        self.timer.connect(self.on_timer)

        self.is_dragging = False
        self.is_mouse_pressed = False

        self.prev_phi = 0.0
        self.prev_theta = 0.0
        self.prev_timer_t = 0

        self.rotate_theta_speed = 0.0
        self.rotate_phi_speed = 0.0




    def on_initialize(self, event):
        gl.glClearColor(0,0,0,1)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE) #_MINUS_SRC_ALPHA)
        # Start the timer upon initialization.
        self.timer.start()

    def set_frame_data(self,data):
        self.program.set_vars(gloo.VertexBuffer(data))





    def on_key_press(self,event):
        print event.text
        if event.text == ' ':
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()
        if event.text == 'm':
            d = self.viewer_helper.load_next_frame()
            if d != None:
                self.set_frame_data(d)
        elif event.text == 'n':
            d = self.viewer_helper.load_prev_frame()
            if d != None:
                self.set_frame_data(d)


    def on_timer(self,event):
        self.timer_t += self.timer_dt # keep track on the current time
        self.theta += self.rotate_theta_speed
        self.phi += self.rotate_phi_speed
        self.model = np.eye(4, dtype=np.float32)
        rotate(self.model, self.theta, 0,0,1)
        rotate(self.model, self.phi,   0,1,0)
        self.program['u_model'] = self.model
        self.update()


    def on_resize(self, event):
        width, height = event.size
        gl.glViewport(0, 0, width, height)
        self.projection = perspective( 45.0, width/float(height), 1.0, 1000.0 )
        self.program['u_projection'] = self.projection


    def on_mouse_wheel(self, event):
        self.translate +=event.delta[1]
        self.translate = max(2,self.translate)
        self.view       = np.eye(4,dtype=np.float32)
        translate(self.view, 0,0, -self.translate)
        self.program['u_view'] = self.view
        self.program['u_size'] = 5/self.translate
        self.update()

    def on_mouse_press(self, event):
        self.prev_cursor_x, self.prev_cursor_y = event.pos
        print self.prev_cursor_x, self.prev_cursor_y
        self.dragging_marked = False
        self.is_mouse_pressed = True

    def on_mouse_move(self, event):
        if event.is_dragging:
            self.is_dragging = True
            w, h = self.size
            x, y = event.pos
            dx = x-self.prev_cursor_x
            dy = y-self.prev_cursor_y
            dphi = float(dx)/x*180
            dtheta = float(dy)/y*180
            dt = self.timer_t - self.prev_timer_t
            if dt > 0 or True:
                self.phi += float(dx)/x*180
                self.theta += float(dy)/y*180

                rotate(self.model, self.theta, 0,0,1)
                rotate(self.model, self.phi,   0,1,0)
                self.prev_cursor_x, self.prev_cursor_y = event.pos
                self.prev_timer_t = self.timer_t


    def on_mouse_release(self, event):
        self.is_dragging = False
        self.is_mouse_pressed = False


    def on_paint(self, event):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        self.program.draw(gl.GL_POINTS)

if __name__ == '__main__':
    #c = Canvas()
    #c.show()
    v = Viewer()
    v.show()



