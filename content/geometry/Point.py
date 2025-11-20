"""
 * Author: Ulf Lundstrom
 * Date: 2009-02-26
 * License: CC0
 * Source: My head with inspiration from tinyKACTL
 * Description: Class to handle points in the plane.
 * T can be e.g. float or int. (Avoid int for division operations.)
 * Status: Works fine, used a lot
"""

import math

def sgn(x):
    return (x > 0) - (x < 0)

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __lt__(self, p):
        return (self.x, self.y) < (p.x, p.y)
    
    def __eq__(self, p):
        return (self.x, self.y) == (p.x, p.y)
    
    def __add__(self, p):
        return Point(self.x + p.x, self.y + p.y)
    
    def __sub__(self, p):
        return Point(self.x - p.x, self.y - p.y)
    
    def __mul__(self, d):
        return Point(self.x * d, self.y * d)
    
    def __truediv__(self, d):
        return Point(self.x / d, self.y / d)
    
    def dot(self, p):
        return self.x * p.x + self.y * p.y
    
    def cross(self, p):
        return self.x * p.y - self.y * p.x
    
    def cross2(self, a, b):
        # cross product of (a - self) and (b - self)
        return (a - self).cross(b - self)
    
    def dist2(self):
        return self.x * self.x + self.y * self.y
    
    def dist(self):
        return math.sqrt(self.dist2())
    
    def angle(self):
        # angle to x-axis in interval [-pi, pi]
        return math.atan2(self.y, self.x)
    
    def unit(self):
        # makes dist()=1
        return self / self.dist()
    
    def perp(self):
        # rotates +90 degrees
        return Point(-self.y, self.x)
    
    def normal(self):
        return self.perp().unit()
    
    def rotate(self, a):
        # returns point rotated 'a' radians ccw around the origin
        return Point(self.x * math.cos(a) - self.y * math.sin(a),
                    self.x * math.sin(a) + self.y * math.cos(a))
    
    def __repr__(self):
        return f"({self.x},{self.y})"
