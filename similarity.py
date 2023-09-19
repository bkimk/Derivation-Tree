#############################################################
# USE FOR LATER ONCE MATHML COMPONENTS HAVE BEEN TRANSLATED #
#############################################################

# Debug function that prints pretty Matrix
def printMatrix(Matrix):
    for row in Matrix:
        print(row, '\n')

# Helper function for LongestCommonSubstring that finds max value along with (x,y) coords
def findMax(Matrix):
    max = (0,0,0)
    for i in range(len(Matrix)):
        for j in range(len(Matrix[0])):
            if Matrix[i][j]> max[2]:
                max = (i,j,Matrix[i][j])
    return max

# Helper function for LongestCommonSubstring that eliminates longest common substring in matrix
def addNegOne(Matrix, max):
    for i in range(max[0]-max[2]+1, max[0]+1):
        for j in range(max[1]-max[2]+1, max[1]+1):
            Matrix[i][j] = -1


# DP solution to finding all common substrings (Starting from largest w/o duplicates)
# Taking in 2 equations, will create a matrix showing matching substring

def LongestCommonSubstring(equation1, equation2):

    # Matrix of size length of first equation X length of second equation
    Matrix = [ [0] * len(equation2) for i in range(len(equation1))]

    # Populating Matrix
    for i in range(len(equation1)):
        for j in range(len(equation2)):
            if equation1[i] == equation2[j]:
                if i == 0 or j == 0:
                    Matrix[i][j] = 1
                else:
                    Matrix[i][j] = Matrix[i-1][j-1]+1
            else:
                Matrix[i][j] = 0
    # printMatrix(Matrix)

    # Iterate through matrix and finding total substring matchings
    max = findMax(Matrix)
    totLen = 0
    while max[2] > 2:
        addNegOne(Matrix, max)
        printMatrix(Matrix)
        totLen += max
        max = findMax(Matrix)
        # printMatrix(Matrix)

    # Once Matrix has been iterated, calculate percentage of equation that was shared
    # Change current % after further trials
    if totLen/len(equation1) > 0.25:
        return True
    elif totLen/len(equation2) > 0.25:
        return True
    else:
        return False

LongestCommonSubstring('deskchair', 'chairlemon')