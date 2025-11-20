"""
 * Author: Stjepan Glavina, chilli
 * Date: 2019-05-05
 * License: Unlicense
 * Source: https://github.com/stjepang/snippets/blob/master/convex_hull.cpp
 * Description: Returns a list of the points of the convex hull in counter-clockwise order.
 * Points on the edge of the hull between two other points are not considered part of the hull.
 * Time: O(n \log n)
 * Status: stress-tested, tested with kattis:convexhull
"""

def convexHull(pts):
    if len(pts) <= 1:
        return pts[:]
    pts = sorted(pts)
    h = [None] * (len(pts) + 1)
    s = 0
    t = 0
    for it in range(2):
        for p in pts:
            while t >= s + 2 and h[t-2].cross2(h[t-1], p) <= 0:
                t -= 1
            h[t] = p
            t += 1
        t -= 1
        s = t
        pts = pts[::-1]
    
    result = h[:t]
    # Remove duplicate if only 2 points and they're the same
    if t == 2 and h[0] == h[1]:
        result = h[:1]
    return result
