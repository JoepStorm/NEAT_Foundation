'''
General simplified calculation of the moment of a beam for test purposes
For now only x1 moves and only 1 equally distributed force
'''

import random
from numpy import exp

'''
     10 kN/m                                                                  10 kN/m                  
|---------------|                                                       |---------------|
|               |                           5 kN/m                      |               |
|               |-------------------------------------------------------|               |
|               |                                                       |               |
_________________________________________________________________________________________
                    /\                                              /\
                   /--\                                            /--\
        2 m                                 4 m                                 2 m
|---------------|-------------------------------------------------------|---------------|
        x1
|-------------------|
                                 x2
|--------------------------------------------------------------------|
'''
'''
                  
                                                     
                                          10 kN/m                                     
|-----------------------------------------------------------------------------------------|               
|                                                                                         |
|_________________________________________________________________________________________|
                    /\                                              /\
                   /--\                                            /--\
                                           8 m                                 
|-----------------------------------------------------------------------------------------|
        x1
|-------------------|
                                 x2
|--------------------------------------------------------------------|
'''


class BeamMoment(object):
    length = 8.0    # length
    q = 10.0    # load
    
    
        

    size_scale = 0.2  # scale factor for movement (1 becomes a step of x m)
    step_loss_factor = 500   # factor, the low->steps become smaller very quick, high->steps become smaller slowly

    def __init__(self, x1=None, x2=None, # dx1=1, dx2=None,
                 lim_x_min=0.0, lim_x_max=length):
        self.x_limit_min = lim_x_min    # set limits so x1 and x2 can't be outside the beam.
        self.x_limit_max = lim_x_max

        if x1 is None:   # pick random location for x1 on left side of beam
            x1 = self.x_limit_max / 4 + random.uniform(-self.x_limit_max / 4, self.x_limit_max / 4)

        if x2 is None:   # pick random location for x2 on right side of beam
            x2 = self.x_limit_max / 4 * 3 + random.uniform(-self.x_limit_max / 4, self.x_limit_max / 4)

        # if dx1 is None:   # pick random movement for x1
        #     dx1 = random.uniform(-1.0, 1.0)

        # if dx2 is None:   # pick random movement for x1
        #     dx2 = random.uniform(-1.0, 1.0)
        self.length = lim_x_max
        self.t = 0
        self.x1 = x1
        self.x2 = (self.length - x2)
        # print('start=', x1, x2)
        # self.dx1 = dx1
        # self.dx2 = dx2

        q = self.q
        self.M1 = q/2*self.x1**2
        self.M3 = q/2*self.x2**2
        self.M2 = abs((self.M1+self.M3)/2-q/8*(self.length - self.x1 - self.x2)**2)

    def step(self, force1):  # , force2):
        # print('force=', force1)
        '''
        force1 and force 2 are values between 0 and 1 ????
        Calculate the new x1 and x2 and use these to recalculate the moments in middle and end points.
        '''
        # Locals for readability
        length = self.length
        q = self.q

        scale_factor = self.size_scale * exp(-self.t / self.step_loss_factor)

        # Update positions
        step1 = (force1[0] - 0.5) * scale_factor
        self.x1 += step1   # If force < 0.5 move left, if > 0.5 move right
        if self.x1 < 0 or self.x1 > 8 or self.x1 > (8 - self.x2):     # keep within bounds
            self.x1 -= step1

        step2 = (0.5 - force1[1]) * scale_factor
        self.x2 += step2   # If force < 0.5 move left, if > 0.5 move right
        if self.x2 < 0 or self.x2 > 8 or self.x2 > (8 - self.x1):     # keep within bounds
            self.x2 -= step2

        # Calculate new moments
        self.M1 = q/2*self.x1**2
        self.M3 = q/2*self.x2**2
        self.M2 = (self.M1+self.M3)/2-q/8*(length - self.x1 - self.x2)**2

        self.t += 1

    def get_scaled_state(self):
        '''Get full state, scaled into as a factor of the largest moment. i.e. [1.0, 0.25, 0.50] or [0.5, 1.0, 1.0]'''
        # print(self.M1, self.M2, self.M3)
        Mmax = max(self.M1, abs(self.M2), self.M3)
        return [self.M1 / Mmax,
                self.M2 / -Mmax,
                self.M3 / Mmax]

    def get_x_coords(self):
        return [self.x1, self.x2]




    
    
    











