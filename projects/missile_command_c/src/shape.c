#!/usr/bin/python3.9


class Shape:

    # https://stackoverflow.com/questions/1201200/fast-algorithm-for-drawing-filled-circles
    def filled_circle(x,y,r, putPixel):
        r2 = r * r
        area = r2 << 2
        rr = r << 1

        for i in range(area):
            tx = (i % rr) - r
            ty = (i / rr) - r
            if tx * tx + ty * ty <= r2:
                putPixel(int(x + tx), int(y + ty))


    def circle(x0, y0, radius, putPixel):
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        putPixel(x0, y0 + radius)
        putPixel(x0, y0 - radius)
        putPixel(x0 + radius, y0)
        putPixel(x0 - radius, y0)

        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            putPixel(x0 + x, y0 + y)
            putPixel(x0 - x, y0 + y)
            putPixel(x0 + x, y0 - y)
            putPixel(x0 - x, y0 - y)
            putPixel(x0 + y, y0 + x)
            putPixel(x0 - y, y0 + x)
            putPixel(x0 + y, y0 - x)
            putPixel(x0 - y, y0 - x)


    def line(x0, y0, x1, y1, putPixel):

        #make integer
        x0 = int(x0+0.5)
        y0 = int(y0+0.5)
        x1 = int(x1+0.5)
        y1 = int(y1+0.5)

        # Bresenham's algorithm

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        err = dx - dy

        while True:
            putPixel (x, y)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    # https://6502disassembly.com/va-missile-command/
    def filled_octogon(centerx,centery,radius, slope_dx,slope_dy, putPixel):
        width       = radius * 2
        height      = radius * 2
        lines = Shape._get_octogon_lines(width,height,slope_dx,slope_dy)
        for y, (start_x,end_x) in enumerate(lines):
            py = centery + y - radius
            for x in range(start_x,end_x):
                px = centerx + x - radius
                putPixel(px,py)


    def _get_octogon_lines(width,height,slope_dx,slope_dy):

        cornerx,cornery = Shape._find_octogon_corner(width//2,height//2,slope_dx,slope_dy)
        points = []
        Shape.line(width//2, 0, cornerx,cornery,lambda x,y:points.append((x,y)) )
        Shape.line(cornerx,cornery, 0,height//2,lambda x,y:points.append((x,y)) )

        lines = height * [(-1,-1)]
        for x,y in points:
            lines[y] = (x, width-x)
            lines[height-y-1] = (x, width-x)

        return lines


    def _find_octogon_corner(half_width,half_height,slope_dx,slope_dy):

        if slope_dx == slope_dy:
            return (half_width//2,half_height//2)


        A1 = [0,0]
        B1 = [half_width,half_height]
        slope_A = slope_dy / slope_dx
        slope_B = slope_dx / slope_dy
        y_int_A = Math.y_intercept(A1, slope_A)
        y_int_B = Math.y_intercept(B1, slope_B)
        x, y = Math.line_intersect(slope_A, y_int_A, slope_B, y_int_B)
        #flip y
        y = half_height - y
        return x,y


class Math:

    # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
    def slope(P1, P2):
        # dy/dx
        # (y2 - y1) / (x2 - x1)
        return(P2[1] - P1[1]) / (P2[0] - P1[0])

    def y_intercept(P1, slope):
        # y = mx + b
        # b = y - mx
        # b = P1[1] - slope * P1[0]
        return P1[1] - slope * P1[0]

    def line_intersect(m1, b1, m2, b2):
        if m1 == m2:
            print ("These lines are parallel!!!")
            return None
        # y = mx + b
        # Set both lines equal to find the intersection point in the x direction
        # m1 * x + b1 = m2 * x + b2
        # m1 * x - m2 * x = b2 - b1
        # x * (m1 - m2) = b2 - b1
        # x = (b2 - b1) / (m1 - m2)
        x = (b2 - b1) / (m1 - m2)
        # Now solve for y -- use either line, because they are equal here
        # y = mx + b
        y = m1 * x + b1
        return x,y

    def line_intersect_test(A1,A2,B1,B2):
        slope_A = slope(A1, A2)
        slope_B = slope(B1, B2)
        y_int_A = y_intercept(A1, slope_A)
        y_int_B = y_intercept(B1, slope_B)
        return line_intersect(slope_A, y_int_A, slope_B, y_int_B)



