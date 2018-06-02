import gizeh as gz
import moviepy.editor as mpy
from beam_moments import BeamMoment


def make_movie(net, duration_seconds, output_filename):
    """

    :param net: The trained network
    :param duration_seconds: The amount of seconds the movie will be
    :param output_filename: The file name
    :return:
    """

    w, h = 500, 100
    scale = 50
    beamwidth = 8  # beam width in m
    beamheight = 0.2
    height_support = h / 2 + beamheight * scale

    sim = BeamMoment()

    # Standard support
    support = gz.rectangle(scale * .2, scale * 0.25, xy=[0, 0], stroke_width=1, fill=(0, 1, 0))
    # Beam at center of screen
    beam = gz.rectangle(scale * beamwidth, scale * beamheight, xy=[w / 2, h / 2], stroke_width=1, fill=(1, 1, 0))

    def make_frame(t):

        inputs = sim.get_scaled_state()
        '''
        if hasattr(net, 'activate'):
            action = net.activate(inputs)
        else:
            action = net.advance(inputs)
        '''
        action = net.activate(inputs)

        sim.step(force1=action)

        surface = gz.Surface(w, h, bg_color=(1, 1, 1))

        support0 = support.translate(xy=[(sim.x1 + 1) * scale, height_support])
        group = gz.Group((support0,))
        group.draw(surface)

        support1 = support.translate(xy=[(beamwidth - sim.x2 + 1) * scale, height_support])
        group = gz.Group((support1,))
        group.draw(surface)

        group = gz.Group((beam,))
        group.draw(surface)

        # Draw text
        text1 = gz.text(str(round(sim.M1, 2)), fontfamily="Impact", fontsize=14, fill=(0, 0, 1), xy=[(sim.x1 + 1) * scale, 30])
        text2 = gz.text(str(round(sim.M2, 2)), fontfamily="Impact", fontsize=14, fill=(0, 0, 1), xy=[((sim.x1 + beamwidth - sim.x2) / 2 + 1) * scale, 80])
        text3 = gz.text(str(round(sim.M3, 2)), fontfamily="Impact", fontsize=14, fill=(0, 0, 1), xy=[(beamwidth - sim.x2 + 1) * scale, 30])

        fitness = sum(sim.get_scaled_state())

        text4 = gz.text('fitness= {}'.format(str(round(fitness, 1))), fontfamily="Impact", fontsize=14, fill=(0, 0, 1),
                        xy=[50, 10])

        text5 = gz.text('force: {},   {}'.format(str(round(action[0], 4)), str(round(action[1], 4))), fontfamily="Impact", fontsize=14, fill=(0, 0, 1),
                        xy=[150, 10])

        group = gz.Group((text1, text2, text3, text4, text5))
        group.draw(surface)
        # print(f't={t}, x1={sim.x1}, x2={sim.x2}')

        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=duration_seconds)
    clip.write_videofile(output_filename, codec="mpeg4", fps=50)
