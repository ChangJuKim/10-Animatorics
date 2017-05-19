import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
  ==================== """

def first_pass( commands ):
    print("First_pass")
    #ensures that you can put frames/etc at the bottom, and won't crash
    num_frames = 0
    basename = "random_anim"
    isFrames = False
    isBasename = False
    isVary = False
    for i in range(len(commands)):
        if commands[i][0] == "frames":
            num_frames = commands[i][1]
            isFrames = True
        if commands[i][0] == "basename":
            basename = commands[i][1]
            isBasename = True
        if commands[i][0] == "vary":
            isVary = True
    if isVary and not isFrames:
        print("vary found, but frames missing. Exiting.")
        exit()
    if isFrames and not isBasename:
        print("Basename not found. Will save as {0} with {1} frames".format(basename, num_frames))
    return [num_frames, basename]

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames ):
    print("Second_pass")
    knobs = [None] * num_frames
    knob_dict = {}
    #loops through number of frames
    for i in range(num_frames):
        knobs[i] = {}
        #loops through the commands in each frame
        for j in range(len(commands)):
            if commands[j][0] == "vary" and commands[j][2] <= i and commands[j][3] > i:
                #vary e.g: vary spinny 0 49 0 1
                #print str(commands[j]) + "  \t{0}".format(i)
                vary = commands[j]
                knobs[i][vary[1]] = vary[4] + ((vary[5] - vary[4]) / float(vary[3] - vary[2]))
    print "second_pass done!"
    knobs[0].keys()[0] = knobs[0][knobs[0].keys()[0]]
    print spinny
    return knobs


def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    num_frames = first_pass(commands)[0]
    basename = first_pass(commands)[1]
    knobs = second_pass(commands, num_frames)

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    if num_frames > 1:
        for i in range(num_frames):
            
            for command in commands:
                c = command[0]
                args = command[1:]

                if c == 'box':
                    add_box(tmp,
                            args[0], args[1], args[2],
                            args[3], args[4], args[5])
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, color)
                    tmp = []
                elif c == 'sphere':
                    add_sphere(tmp,
                               args[0], args[1], args[2], args[3], step)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, color)
                    tmp = []
                elif c == 'torus':
                    add_torus(tmp,
                              args[0], args[1], args[2], args[3], args[4], step)
                    matrix_mult( stack[-1], tmp )
                    draw_polygons(tmp, screen, color)
                    tmp = []
                elif c == 'move':
                    tmp = make_translate(args[0], args[1], args[2])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                elif c == 'scale':
                    tmp = make_scale(args[0], args[1], args[2])
                    matrix_mult(stack[-1], tmp)
                    stack[-1] = [x[:] for x in tmp]
                    tmp = []
                elif c == 'rotate':
                    theta = args[1] * (math.pi/180)
                    if args[0] == 'x':
                        tmp = make_rotX(theta)
                    elif args[0] == 'y':
                        tmp = make_rotY(theta)
                    else:
                        tmp = make_rotZ(theta)
                    matrix_mult( stack[-1], tmp )
                    stack[-1] = [ x[:] for x in tmp]
                    tmp = []
                elif c == 'push':
                    stack.append([x[:] for x in stack[-1]] )
                elif c == 'pop':
                    stack.pop()
                elif c == 'display':
                    display(screen)
                elif c == 'save':
                    save_extension(screen, args[0])
