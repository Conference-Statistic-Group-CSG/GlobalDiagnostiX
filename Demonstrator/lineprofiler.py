def lineprofile(inputimage, debug=False):
    """
    Function to draw a line profile from a selection in the image.
    Comes in handy to look at the resolution phantom in x-ray images shot with
    the iAi electronics prototype in the x-ray lab.
    Based on http://stackoverflow.com/a/7880726/323100
    """

    # suppress pep8 warning about potentially unreferenced variables
    global x1, x0, y1, y0

    import numpy
    import scipy.ndimage
    import matplotlib.pyplot as plt

    # Debug
    if debug:
        inputimage = scipy.misc.lena()

    # Prepare image
    plt.figure(0, figsize=(16, 16))
    if debug:
        plt.ion()
    plt.imshow(inputimage, cmap='bone', vmin=numpy.min(inputimage),
               vmax=numpy.mean(inputimage) + 3 * numpy.std(inputimage))
    plt.title('Please select the end-points for the line-profile')

    # Let the user select a line to plot the profile from
    pts = []
    while len(pts) < 2:
        pts = numpy.asarray(plt.ginput(2, timeout=-1))
        x0 = pts[1, 0]
        x1 = pts[0, 0]
        y0 = pts[1, 1]
        y1 = pts[0, 1]

    # Interpolate a line between x0, y0 and x1, y1 with double the length of
    # the line
    length = 2 * int(numpy.hypot(x1 - x0, y1 - y0))
    x, y = numpy.linspace(x0, x1, length), numpy.linspace(y0, y1, length)

    # Extract the values along the line, using cubic interpolation
    profileinterpolated = scipy.ndimage.map_coordinates(numpy.transpose(
        inputimage), numpy.vstack((x, y)))
    # Just do nearest-neighbour value extraction
    profilenn = numpy.transpose(inputimage)[x.astype(numpy.int),
                                            y.astype(numpy.int)]

    # Draw the image and line profile again
    plt.subplot(211)
    plt.imshow(inputimage, cmap='bone', vmin=numpy.min(inputimage),
               vmax=numpy.mean(inputimage) + 3 * numpy.std(inputimage))
    plt.plot((x0, x1), (y0, y1), 'r')
    plt.plot(x0, y0, 'yo')
    plt.plot(x1, y1, 'ko')
    plt.axis('image')
    plt.draw()

    plt.subplot(212)
    plt.plot(profileinterpolated, 'red',  label='interpolated')
    plt.plot(profilenn, 'orange', label='nearest neighbour')
    plt.plot(0, profilenn[0], 'yo', markersize=25, alpha=0.309)
    plt.plot(len(profilenn)-1, profilenn[-1], 'ko', markersize=25, alpha=0.309)
    plt.xlim([0, len(profilenn)-1])
    plt.legend(loc='best')
    plt.draw()
    plt.ioff()
    if debug:
        plt.show()
    return pts, profileinterpolated
