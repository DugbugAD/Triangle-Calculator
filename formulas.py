from math import acos, sqrt, sin, radians, degrees, asin, cos


class FORMULAS(object):
    '''
    CASES:
    - Side Side Side
    - Side Side Angle
    - Angle Angle Side
    '''

    def __init__(self):
        pass

    def __new__(self, A=None, B=None, C=None, a=None, b=None, c=None, decimals=3):
        if (a != None) and (b != None) and (c != None):
            self.values = self.side_side_side(
                self, a=a, b=b, c=c, decimals=decimals)

        elif (A != None and B != None) or (A != None and C != None) or (B != None and C != None):
            self.values = self.side_angle_angle(
                self, a=a, b=b, c=c, A=A, B=B, C=C, decimals=decimals)

        elif (a != None and b != None) or (a != None and c != None) or (b != None and c != None):

            if (a != None and A != None) or (b != None and B != None) or (c != None and C != None):
                self.values = self.side_side_angle(
                    self, A=A, B=B, C=C, a=a, b=b, c=c, decimals=decimals)
            else:
                self.values = self.side_side_angle_2(
                    self, A=A, B=B, C=C, a=a, b=b, c=c, decimals=decimals)

        if self.values == None:
            return None

        self.values['area'] = self.area(
            self, a=self.values['a'], b=self.values['b'], c=self.values['c'], decimals=decimals)

        self.values['perimeter'] = self.perimeter(
            self, a=self.values['a'], b=self.values['b'], c=self.values['c'], decimals=decimals)

        self.values['semiperimeter'] = self.semiperimeter(
            self, a=self.values['a'], b=self.values['b'], c=self.values['c'], decimals=decimals)

        self.values['inradius'] = self.inradius(
            self, area=self.values['area'], semiperimeter=self.values['semiperimeter'], decimals=decimals)

        self.values['circumradius'] = self.circumradius(
            self, a=self.values['a'], A=self.values['A'], decimals=decimals)

        self.values['heights'] = self.heights(
            self, a=self.values['a'], b=self.values['b'], c=self.values['c'], decimals=decimals)

        self.values['medians'] = self.medians(
            self, a=self.values['a'], b=self.values['b'], c=self.values['c'], decimals=decimals)

        self.values['type_side'] = self.type_side(
            self, a=self.values['a'], b=self.values['b'], c=self.values['c'])

        self.values['type_angle'] = self.type_angle(
            self, A=self.values['A'], B=self.values['B'], C=self.values['C'])

        ...
        ...
        ...
        if self.triangle_sum_theorem(self, A=self.values['A'], B=self.values['B'], C=self.values['C']) == False:
            return None
        elif self.triangle_inequality_theorem(self, a=self.values['a'], b=self.values['b'], c=self.values['c']) == False:
            return None

        return self.values

    def triangle_sum_theorem(self, A, B, C):
        if sum((A, B, C)) < 180.5 and sum((A, B, C)) > 179.5:
            return True
        else:
            return False

    def triangle_inequality_theorem(self, a, b, c):
        if a + b <= c or a + c <= b or b + c <= a:
            return False
        else:
            return True

    def area(self, a, b, c, decimals):
        s = (a + b + c) / 2
        area = sqrt((s * (s - a) * (s - b) * (s - c)))
        return float(round(area, decimals))

    def perimeter(self, a, b, c, decimals):
        return float(round(sum((a, b, c)), decimals))

    def semiperimeter(self, a, b, c, decimals):
        return float(round(sum((a, b, c)) / 2, decimals))

    def inradius(self, area, semiperimeter, decimals):
        return float(round(area / semiperimeter, decimals))

    def circumradius(self, a, A, decimals):
        return float(round((a / (2 * sin(radians(A)))), decimals))

    def heights(self, a, b, c, decimals):
        height_a = round(
            (2 * self.area(self, a=a, b=b, c=c, decimals=decimals)) / a, decimals)
        height_b = round(
            (2 * self.area(self, a=a, b=b, c=c, decimals=decimals)) / b, decimals)
        height_c = round(
            (2 * self.area(self, a=a, b=b, c=c, decimals=decimals)) / c, decimals)

        return(float(height_a), float(height_b), float(height_c))

    def medians(self, a, b, c, decimals):
        median_a = round(sqrt((2*b**2 + 2*c**2 - a**2)/4), decimals)
        median_b = round(sqrt((2*a**2 + 2*c**2 - b**2)/4), decimals)
        median_c = round(sqrt((2*b**2 + 2*a**2 - c**2)/4), decimals)
        return(median_a, median_b, median_c)

    def type_side(self, a, b, c):
        if a != b and a != c and b != c:
            return 'Scalene'
        elif a == b == c:
            return 'Equilateral'
        else:
            return 'Isosceles'

    def type_angle(self, A, B, C):
        if A > 90 or B > 90 or C > 90:
            return 'Obtuse'
        elif A == 90 or B == 90 or C == 90:
            return 'Right'
        else:
            return 'Acute'

    def side_side_side(self, a, b, c, decimals):
        # Side, Side, Side
        try:
            angleA = degrees(acos((b**2 + c**2 - a**2) / (2 * b * c)))
            angleB = degrees(acos((c**2 + a**2 - b**2) / (2 * c * a)))
            angleC = degrees(acos((a**2 + b**2 - c**2) / (2 * a * b)))

            return {"a": float(round(a, decimals)),
                    "b": float(round(b, decimals)),
                    "c": float(round(c, decimals)),
                    "A": float(round(angleA, decimals)),
                    "B": float(round(angleB, decimals)),
                    "C": float(round(angleC, decimals)),
                    }
        except:
            return None

    def side_angle_angle(self, decimals, A=None, B=None, C=None, a=None, b=None, c=None):
        # Side, Angle, Angle, (Angle)

        try:
            if A == None:
                A = 180 - B - C
            elif B == None:
                B = 180 - A - C
            elif C == None:
                C = 180 - A - B

            if a != None:
                sideA = a
                sideB = (a * sin(radians(B))) / sin(radians(A))
                sideC = (a * sin(radians(C))) / sin(radians(A))

            elif b != None:
                sideB = b
                sideA = (b * sin(radians(A)) / sin(radians(B)))
                sideC = (b * sin(radians(C)) / sin(radians(B)))

            elif c != None:
                sideC = c
                sideA = (c * sin(radians(A)) / sin(radians(C)))
                sideB = (c * sin(radians(B)) / sin(radians(C)))

            return {"a": float(round(sideA, decimals)),
                    "b": float(round(sideB, decimals)),
                    "c": float(round(sideC, decimals)),
                    "A": float(round(A, decimals)),
                    "B": float(round(B, decimals)),
                    "C": float(round(C, decimals)),
                    }
        except:
            return None

    def side_side_angle(self, decimals, A=None, B=None, C=None, a=None, b=None, c=None):
        # Side, Side, Angle
        # Angle is NOT beyween the sides
        try:
            def angles(a, b, A):
                angle_a = A
                angle_b = degrees(asin((b * sin(radians(A))) / a))

                angle_c = 180 - angle_a - angle_b

                return (angle_a, angle_b, angle_c)
            ...
            ...
            if c == None:
                if A != None:
                    angle_a, angle_b, angle_c = angles(a=a, b=b, A=A)
                elif B != None:
                    angle_b, angle_a, angle_c = angles(a=b, b=a, A=B)

                side_a = a
                side_b = b
                side_c = sqrt(
                    ((a**2 + b**2) - (2 * a * b * cos(radians(angle_c)))))

            elif b == None:
                if C != None:
                    angle_c, angle_a, angle_b = angles(a=c, b=a, A=C)
                elif A != None:
                    angle_a, angle_c, angle_b = angles(a=a, b=c, A=A)

                side_a = a
                side_c = c
                side_b = sqrt(
                    ((a**2 + c**2) - (2 * a * c * cos(radians(angle_b)))))

            elif a == None:
                if C != None:
                    angle_c, angle_b, angle_a = angles(a=c, b=b, A=C)
                elif B != None:
                    angle_b, angle_c, angle_a = angles(a=b, b=c, A=B)

                side_b = b
                side_c = c
                side_a = sqrt(
                    ((b**2 + c**2) - (2 * b * c * cos(radians(angle_a)))))

            return {"a": float(round(side_a, decimals)),
                    "b": float(round(side_b, decimals)),
                    "c": float(round(side_c, decimals)),
                    "A": float(round(angle_a, decimals)),
                    "B": float(round(angle_b, decimals)),
                    "C": float(round(angle_c, decimals)),
                    }
        except:
            return None

    def side_side_angle_2(self, decimals, A=None, B=None, C=None, a=None, b=None, c=None):
        try:
            if c == None:
                side_c = sqrt((a**2 + b**2) - ((2 * a * b) * cos(radians(C))))
                return self.side_side_side(self, a=a, b=b, c=side_c, decimals=decimals)

            elif b == None:
                side_b = sqrt((a**2 + c**2) - ((2 * a * c) * cos(radians(B))))
                return self.side_side_side(self, a=a, b=side_b, C=c, decimals=decimals)

            elif a == None:
                side_a = sqrt((c**2 + b**2) - ((2 * c * b) * cos(radians(A))))
                return self.side_side_side(self, a=side_a, b=b, c=c, decimals=decimals)
        except:
            return None
