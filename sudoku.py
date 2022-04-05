"""
    Sudoku'yu çözen tüm fonksiyonlar burada.
    Bu tarafa girdi olarak gorüntü işlemeden çıkan 2 boyutlu liste verilecek.
    Boş olan kutular '0' olacak şeklinde formatlanmalı !
    Örnek girdi : sudoku_list = [[6, 0, 4, 7, 0, 0, 2, 0, 0],
                                [0, 0, 7, 0, 2, 0, 0, 4, 0],
                                [8, 0, 0, 0, 6, 4, 9, 0, 1],
                                [0, 0, 9, 8, 0, 0, 3, 0, 6],
                                [7, 0, 0, 5, 0, 6, 0, 0, 8],
                                [1, 0, 6, 0, 0, 9, 7, 0, 0],
                                [4, 0, 3, 6, 9, 0, 0, 0, 7],
                                [0, 6, 0, 0, 7, 0, 4, 0, 0],
                                [0, 0, 1, 0, 0, 3, 5, 0, 2]]
"""
class Solver:

    def show(self, matrix):
        #To show sudoku in fragmented

        for i in range(9):
            for j in range(9):
                if j % 3 == 2:
                    print(matrix[i][j], end='')
                    print(' | ', end='')
                    if j == 8 and i % 3 == 2:
                        print('\n- - - - - - - - - - - - ')
                    elif j == 8:
                        print()
                else:
                    print(matrix[i][j], end=' ')

    def findEmpty(self, matrix):
        #To find first blank cell
        for x in range(9):
            for y in range(9):
                if matrix[x][y] == 0:
                    return x, y
        return None, None

    def control(self, sudo, x, y, number):
        #To control assigned numbers are proper or not

        for i in range(9):
            if sudo[x][i] == number:
                return False

        for j in range(9):
            if sudo[j][y] == number:
                return False

        box_X = x // 3
        box_Y = y // 3

        for m in range(box_X * 3, box_X * 3 + 3):
            for n in range(box_Y * 3, box_Y * 3 + 3):
                if sudo[m][n] == number:
                    return False

        return True

    def solve(self, sudo):
        #Backtracking algorithm

        x, y = self.findEmpty(sudo)

        if x == None:#No blanks in the sudoku
            return True
        else:
            for i in range(1, 10):# i is the value to be assigned

                if self.control(sudo, x, y, i):
                    sudo[x][y] = i

                    # self.show(Sudo) # To see step by step
                    # print("\n\n")

                    if self.solve(sudo): #Go down to next depth
                        return sudo

                    sudo[x][y] = 0

        return False #Backtrack

    def puzzleIndexer(self, matrix):
        #Given numbers reminder
        index_list=[]
        for i in range(0,9):
            for j in range(0, 9):

                if (matrix[i][j] != 0):
                    index_list.append((i,j))
        return index_list