class StrassenMul:

    def __init__(self, a, b):
        self.a = a
        self.b = b

        if len(a) != len(b) != len(a[0]) != len(b[0]):
            raise ValueError("invalid dimensions")

    @staticmethod
    def _split_array(a):
        l = len(a)
        return [[[a[i][s: e] for i in range(x, y)] for s, e in ((0, l // 2), (l // 2, l))] for x, y in
                ((0, l // 2), (l // 2, l))]

    @staticmethod
    def _matrix_add(a, b):
        return [[a[y][x] + b[y][x] for x in range(len(a))] for y in range(len(a))]

    @staticmethod
    def _matrix_sub(a, b):
        return [[a[y][x] - b[y][x] for x in range(len(a))] for y in range(len(a))]

    def mul_s(self):
        return StrassenMul.mul(self.a, self.b)

    @staticmethod
    def mul(a, b):

        w = len(a)

        if w > 2:

            a_split = StrassenMul._split_array(a)
            b_split = StrassenMul._split_array(b)

            a11_plus_a22 = StrassenMul._matrix_add(a_split[0][0], a_split[1][1])
            a21_plus_a22 = StrassenMul._matrix_add(a_split[1][0], a_split[1][1])
            a11_plus_a12 = StrassenMul._matrix_add(a_split[0][0], a_split[0][1])
            a21_minus_a11 = StrassenMul._matrix_sub(a_split[1][0], a_split[0][0])
            a12_minus_a22 = StrassenMul._matrix_sub(a_split[0][1], a_split[1][1])

            b11_plus_b22 = StrassenMul._matrix_add(b_split[0][0], b_split[1][1])
            b12_minus_b22 = StrassenMul._matrix_sub(b_split[0][1], b_split[1][1])
            b21_minus_b11 = StrassenMul._matrix_sub(b_split[1][0], b_split[0][0])
            b11_plus_b12 = StrassenMul._matrix_add(b_split[0][0], b_split[0][1])
            b21_plus_b22 = StrassenMul._matrix_add(b_split[1][0], b_split[1][1])

            m1 = StrassenMul.mul(a11_plus_a22, b11_plus_b22)
            m2 = StrassenMul.mul(a21_plus_a22, b_split[0][0])
            m3 = StrassenMul.mul(a_split[0][0], b12_minus_b22)
            m4 = StrassenMul.mul(a_split[1][1], b21_minus_b11)
            m5 = StrassenMul.mul(a11_plus_a12, b_split[1][1])
            m6 = StrassenMul.mul(a21_minus_a11, b11_plus_b12)
            m7 = StrassenMul.mul(a12_minus_a22, b21_plus_b22)

            c11 = StrassenMul._matrix_add(m1, StrassenMul._matrix_add(m4, StrassenMul._matrix_sub(m7,m5)))
            c12 = StrassenMul._matrix_add(m3, m5)
            c21 = StrassenMul._matrix_add(m2, m4)
            c22 = StrassenMul._matrix_add(m1, StrassenMul._matrix_add(m3, StrassenMul._matrix_sub(m6, m2)))

            upper = [c11[i] + c12[i] for i in range(len(c11))]
            lower = [c21[i] + c22[i] for i in range(len(c11))]

            return upper + lower

        else:

            m1 = (a[0][0] + a[1][1]) * (b[0][0] + b[1][1])
            m2 = (a[1][0] + a[1][1]) * b[0][0]
            m3 = a[0][0] * (b[0][1] - b[1][1])
            m4 = a[1][1] * (b[1][0] - b[0][0])
            m5 = (a[0][0] + a[0][1]) * b[1][1]
            m6 = (a[1][0] - a[0][0]) * (b[0][0] + b[0][1])
            m7 = (a[0][1] - a[1][1]) * (b[1][0] + b[1][1])

            c11 = m1 + m4 - m5 + m7
            c12 = m3 + m5
            c21 = m2 + m4
            c22 = m1 - m2 + m3 + m6

            return [[c11, c12], [c21, c22]]

    def mul_normal_2x2(self):
        oc11 = self.a[0][0] * self.b[0][0] + self.a[0][1] * self.b[1][0]
        oc12 = self.a[0][0] * self.b[0][1] + self.a[0][1] * self.b[1][1]
        oc21 = self.a[1][0] * self.b[0][0] + self.a[1][1] * self.b[1][0]
        oc22 = self.a[1][0] * self.b[0][1] + self.a[1][1] * self.b[1][1]

        print([[oc11, oc12], [oc21, oc22]])

    def mul_normal(self):
        """

        complexity: O(n^3)

        ->->->...
            /
          --
         /
        ->->->...
        ...

        :return:
        """

        a = self.a
        b = self.b

        print("a:",a)
        print("b:",b)

        matrix_len = len(a)

        c = [[0 for x in range(matrix_len)] for y in range(matrix_len)]

        for y in range(matrix_len):
            for x in range(matrix_len):

                s = 0

                a_row = a[y]  # Row in A
                for pos in range(matrix_len):
                    axy = a_row[pos]
                    bxy = b[pos][x]
                    s += axy * bxy

                c[y][x] = s

        return c


def small_matrix():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    sm = StrassenMul(a, b)

    print("s:", sm.mul_s())
    print("n:",sm.mul_normal())


def four_x_four_matrix():
    a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    b = [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]]
    sm = StrassenMul(a, b)

    print(StrassenMul._split_array(a))

    print("4x4:")
    print("s:",sm.mul_s())
    print("n:",sm.mul_normal())


if __name__ == '__main__':
    small_matrix()
    four_x_four_matrix()
