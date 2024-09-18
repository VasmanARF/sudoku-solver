
import numpy as np

def sudoku_solver(sudoku):
    
    def find_empty(board):
        
        emptyCells = []
        #Loop through each spcae in our board and keep track of all positions with value 0 (Empty)
        for j in range(9):
            for i in range(9):
                if board[i][j] == 0:
                    emptyCells.append((i,j))         
                    
                     
        #This variable is 100, to make anything that is compared to it smaller to start our comparing process to find the smallest possible values.
        minimumSol = 100 
        #This list will hold the elements with the least solutions 
        minimumSolCoords = []
        
        
        #We loop through all empty coords and apply PossibleValues function to each empty cell and return smallest values
        for elements in emptyCells:           
            temp = len(PossibleValues(board,elements))
            if temp < minimumSol:
                #Updating with new coordinates which have the least possible values
                minimumSol = temp 
                minimumSolCoords = elements
        return(minimumSolCoords)

    def PossibleValues(board, pos):        
        row, col = pos #We break the tuple (coordinates of empty cell) into its row,col
        #We create a set of the whole row which has our empty cell so as to keep track of already used numbers in that row
        rowSet = set(board[row]) 
        #We create a set of the whole column which has our empty cell so as to keep track of already used numbers in that column
        colSet = set(board[:, col]) 
        #We calculate the starting row and column for the specific 3x3 grid
        startRow, startCol = 3 * (row // 3), 3 * (col // 3)
        #We create a set with the already existing numbers in the 3x3 grid
        boxSet = set()
        #The +3 is used to iterate all through each element in a 3x3 grid
        for i in range(startRow, startRow + 3): 
            for j in range(startCol, startCol + 3):
                boxSet.add(board[i][j]) #Adding to our set
        
        #Create a set of all possible numbers a cell could be without taking any rule violations into consideration
        allNumbers = set(range(1,10)) 
        
        #Return set with all elements of startRow, StartCol and boSet subtracted from set will all posibble numbers
        return(allNumbers - rowSet -colSet - boxSet) 
    
    #Function used to check if a value in a certain position is legal to be placed
    def ValidNum(board, num, pos):
        #Check if any number in the positions row is the same as num we want to place
        for i in range(9):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        #Check if any number in the position column is the same as the num we want to place
        for i in range(9):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        #Check if any number in the positions box is the same as the num we want to place
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        #Placement of num in pos is valid
        return True 

    #Loops through each index of the board to see if there are any mistakes with the initial board
    def ValidBoard(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0 and not ValidNum(board, board[i][j], (i, j)):
                    return False
        return True


    #Function used to format paramaters for function that will check for hidden singles
    def HiddenSingles(board):
        
        #While Loop with run serves as a means of searching for hidden singles untill nothing is found
        run = True
        while run:
            run = False

            for unit in range(9):
                #Give each space each possible number
                for num in range(1, 10):
                    
                    #Creating a list with coordinates of current row that unit is set to 
                    rowCoords = [(unit,col) for col in range(9)]
                    #Check to see whether num is a hidden single that exists in the rowCoords
                    if CheckHiddenSingles(board, num, rowCoords):
                        run = True

                    #Same process as the rows is then repeated beloww for columns and boxes
                    
                    colCoords = [(row, unit) for row in range(9)]
                    if CheckHiddenSingles(board, num, colCoords):
                        run = True

                    # Check for hidden single in block
                    startRow, startCol = 3 * (unit // 3), 3 * (unit % 3)
                    boxCoords = []
                    for i in range(startRow, startRow + 3):
                        for j in range(startCol, startCol + 3):
                            boxCoords.append((i, j))
                    if CheckHiddenSingles(board, num, boxCoords):
                        run = True

        return board

        
    def CheckHiddenSingles(board, num, cells): 
        #Possibilities will store how many times num was an option in the current list of coords passed to the function
        possibilities = []
        #Loop through all coordinates in the passed paramater and if they are empty on our board will check to see if num is a possible solution for that empty cell
        for cell in cells:
            if board[cell[0]][cell[1]] == 0:
                possible = PossibleValues(board, cell)
                if num in possible:
                    possibilities.append(cell)
        
        #If only one of the empty cells had num as solution, this means we have found a hidden cell thus we can update our board/
        if len(possibilities) == 1:
            board[possibilities[0][0]][possibilities[0][1]] = num
            return True
        #False means nothing was found in the row 
        return False


    #Function used to fill in any hidden singles that are found on our initial board
    def NakedSingles(board):
        
        #While loop with condition run is used to keep iterating through every empty cell whenever a change is made to the board
        run = True 
        while run:
            run = False
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        possibilities = PossibleValues(board, (i, j))
                        if len(possibilities) == 1:
                            board[i][j] = possibilities.pop()
                            run = True
        return board
    
    
    def Solve(board):
        #Find will now contain a list of coordinates in the specific order they should be handled
        find = find_empty(board) 
        #If there is no empty cells on the board, it means our puzzle has been solved
        if not find: 
            return True
        #Else we take the coordinates returned by find_empty function
        else:
            row, col = find
        
        
        #Use of recusrion to assign empty space to all available values untill a solution is found, if a dead end is hit, we make the current cell 0 and backtrack to the previous cell and change its value
        for num in PossibleValues(board, (row, col)):
            
            board[row][col] = num
            if Solve(board):
                return True


            board[row][col] = 0
        
        #If every possibility has been ran through and board has not been solved, we return false
        return False
   
    
    
    if not ValidBoard(sudoku):
        #return board with filled with -1 if starting board contains a rule violation
        
        return np.full_like(sudoku, -1) 
    
    #Creating a copy which we will pass through all our heurstiscs and solvers
    copySudoku = sudoku.copy()
    
    solvedSudoku = NakedSingles(copySudoku)
    solvedSudoku = HiddenSingles(solvedSudoku)
    
    #At this point all the hiiden and naked singles have been filled out on our board
    if Solve(solvedSudoku):
        return solvedSudoku #Soluitions was found
    else:
        return np.full_like(sudoku, -1) #Solution was not found
    

    


