class StrassenMul:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        if len(a) != len(b) != len(a[0]) != len(b[0]):
            raise ValueError("invalid dimensions")

    @staticmethod
    def _split_array(a):
        l = len(a)
        lh = l//2
        return [[[a[i][s: e] for i in range(x, y)] for s, e in ((0, lh), (lh, l))] for x, y in
                ((0, lh), (lh, l))]

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
        """
        Multiplication using the Strassen algorithm.

        :param a: first matrix in multiplication
        :param b: second matrix in multiplication
        :return:
        """

        w = len(a)

        if w > 2 and w % 2 == 0:

            # split a and b into quarters
            a_split = StrassenMul._split_array(a)
            b_split = StrassenMul._split_array(b)

            # needed in next step
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

            # calculating the
            m1 = StrassenMul.mul(a11_plus_a22, b11_plus_b22)
            m2 = StrassenMul.mul(a21_plus_a22, b_split[0][0])
            m3 = StrassenMul.mul(a_split[0][0], b12_minus_b22)
            m4 = StrassenMul.mul(a_split[1][1], b21_minus_b11)
            m5 = StrassenMul.mul(a11_plus_a12, b_split[1][1])
            m6 = StrassenMul.mul(a21_minus_a11, b11_plus_b12)
            m7 = StrassenMul.mul(a12_minus_a22, b21_plus_b22)

            # construct quarters of resulting matrix
            c11 = StrassenMul._matrix_add(m1, StrassenMul._matrix_add(m4, StrassenMul._matrix_sub(m7,m5)))
            c12 = StrassenMul._matrix_add(m3, m5)
            c21 = StrassenMul._matrix_add(m2, m4)
            c22 = StrassenMul._matrix_add(m1, StrassenMul._matrix_add(m3, StrassenMul._matrix_sub(m6, m2)))

            # putting smaller matrices together to resulting matrix
            upper = [c11[i] + c12[i] for i in range(len(c11))]
            lower = [c21[i] + c22[i] for i in range(len(c21))]

            return upper + lower

        else:
            return StrassenMul._mul_naive(a, b)

    def mul_normal_2x2(self):
        """
        Naive for 2x2...
        :return:
        """
        oc11 = self.a[0][0] * self.b[0][0] + self.a[0][1] * self.b[1][0]
        oc12 = self.a[0][0] * self.b[0][1] + self.a[0][1] * self.b[1][1]
        oc21 = self.a[1][0] * self.b[0][0] + self.a[1][1] * self.b[1][0]
        oc22 = self.a[1][0] * self.b[0][1] + self.a[1][1] * self.b[1][1]

        print([[oc11, oc12], [oc21, oc22]])

    def mul_naive(self):
        """
        Run _mul_naive for a and b of self
        :return:
        """

        return StrassenMul._mul_naive(self.a, self.b)

    @staticmethod
    def _mul_naive(a, b):
        """
        complexity: O(n^3)

        ->->->...
            /
          --
         /
        ->->->...
        ...

        :param a: first matrix in multiplication
        :param b: second matrix in multiplication
        :return:
        """

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


# code for trying the functionality:

def small_matrix():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    sm = StrassenMul(a, b)

    print("s:", sm.mul_s())
    print("n:", sm.mul_naive())


def four_x_four_matrix():
    a = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    b = [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]]
    sm = StrassenMul(a, b)

    print(StrassenMul._split_array(a))

    print("4x4:")
    print("s:",sm.mul_s())
    print("n:", sm.mul_naive())


if __name__ == '__main__':
    small_matrix()
    four_x_four_matrix()
