import gizeh as gz
import moviepy.editor as mpy
import random

momenten = [0, 0, 0]
coords = [0, 0]


def make_movie(duration_seconds, output_filename):

    w, h = 500, 100
    scale = 50
    beamwidth = 8  # beam width in m
    beamheight = 0.2
    coords[0] = 0  # Start position of first pole relative to start of beam
    coords[1] = 8  # random position of 2nd pole relative to start of beam

    # TODO: Change like in testfile, start at 0,0, change coords in make_frame file. Also add 1 general textfile that you change
    # Standard support
    # To use, translate support in make_frame, it will create a copy
    support = gz.rectangle(scale * .2, scale * 0.25, xy=[0, 0], stroke_width=1, fill=(0, 1, 0))

    # Beam at center of screen
    beam = gz.rectangle(scale * beamwidth, scale * beamheight, xy=[w / 2, h / 2], stroke_width=1, fill=(1, 1, 0))

    # Standard text at 0, 0
    text = gz.text(str('placeholder'), fontfamily="Impact", fontsize=14, fill=(0, 0, 1),
                    xy=[0, 0])
    '''
    paal1 = gz.rectangle(scale * .2, scale * 0.25, xy=((coords[0] + 1) * scale, h / 2 + 10), stroke_width=1, fill=(0, 1, 0))
    paal2 = gz.rectangle(scale * .2, scale * 0.25, xy=((coords[1] + 1) * scale, h / 2 + 10), stroke_width=1, fill=(0, 1, 0))
    pole = gz.rectangle(scale * beamwidth, scale * beamheight, xy=(w / 2, h / 2), stroke_width=1, fill=(1, 1, 0))
    '''

    def make_frame(t):
        speed = t * -20
        surface = gz.Surface(w, h, bg_color=(1, 1, 1))

        x0 = (coords[0] + 1) * scale        # change coords with neat
        x1 = (coords[1] + 1) * scale + speed  # change coords with neat and remove +speed
        height_support = h / 2 + beamheight * 50

        support0 = support.translate(xy=[x0, height_support])
        group = gz.Group((support0,))
        group.draw(surface)

        support1 = support.translate(xy=[x1, height_support])
        group = gz.Group((support1,))
        group.draw(surface)

        group = gz.Group((beam,))
        group.draw(surface)


        # Get the moments
        momentenfunction(beamwidth)
        # Draw text
        text1 = gz.text(str(round(momenten[0])), fontfamily="Impact", fontsize=14, fill=(0, 0, 1), xy=[x0, 30])
        text2 = gz.text(str(round(momenten[1])), fontfamily="Impact", fontsize=14, fill=(0, 0, 1), xy=[(x0 + x1) / 2, 80])
        text3 = gz.text(str(round(momenten[2])), fontfamily="Impact", fontsize=14, fill=(0, 0, 1), xy=[x1, 30])

        group = gz.Group((text1, text2, text3))
        group.draw(surface)

        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=duration_seconds)
    clip.write_videofile(output_filename, codec="mpeg4", fps=50)


def momentenfunction(beamwidth):    # TODO: make more general, applicable with multiple poles, multiple load cases, include stiffness
    q = 1000
    momenten[0] = q * coords[0]
    momenten[2] = q * (beamwidth - coords[1])
    momenten[1] = abs((momenten[0] + momenten[2]) / 2 - q * (coords[1] - coords[0])**2 / 8)  # waarde tussen m0 en m2 - 1/8 q l^2

    return


make_movie(10, 'Movie-test2.mp4')



