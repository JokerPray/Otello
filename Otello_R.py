import random
import sys

WIDTH = 8
HEIGHT = 8


def drawBoard(board):
    # Вывести игровое поле, переданное этой функции. Ничего не возвращать.
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' % (y + 1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y + 1))
    print(' +--------+')
    print('  12345678')


def getNewBoard():
    # Создать структуру данных нового чистого игрового поля.
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board


# Вернуть False, если ход игрока в клетку с координатами xstart, ystart — недопустимый.
# Если это допустимый ход, вернуть список клеток, которые "присвоил" бы игрок, если бы сделал туда ход.
def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        while isOnBoard(x, y) and board[x][y] == otherTile:
            # Продолжать двигаться в этом направлении x и y
            x += xdirection
            y += ydirection
            if isOnBoard(x, y) and board[x][y] == tile:
                # Есть фишки, которые можно перевернуть. Двигаться в обратном направлении до достижения исходной клетки, отмечая все фишки на этом пути
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def isOnBoard(x, y):
    return 0 <= x <= WIDTH - 1 and 0 <= y <= HEIGHT - 1


def getBoardWithValidMoves(board, tile):
    # Вернуть новое поле с точками, обозначающими допустимые ходы, которые может сделать игрок.
    boardCopy = getBoardCopy(board)
    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy


def getValidMoves(board, tile):
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    # Определить количество очков, подсчитав фишки. Вернуть словарь с ключами 'Х' и 'О'.
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}


def enterPlayerTile():
    # Позволить игроку ввести выбранную фишку.
    # Возвращает список с фишкой игрока в качестве первого элемента и фишкой компьютера в качестве второго.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Вы играете за Х или О ?')
        tile = input().upper()
    # Первый элемент в списке — фишка игрока, второй элемент — фишка компьютера.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Случайно выбрать, кто ходит первым.
    if random.randint(0, 1) == 0:
        return 'Компьютер'
    else:
        return 'Человек'


def makeMove(board, tile, xstart, ystart):
    # Поместить фишку на игровое поле в позицию xstart, ystart и перевернуть какую-либо фишку противника.
    # Вернуть False, если это недопустимый ход; вернуть True, если допустимый
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):
    # Сделать копию списка board и вернуть ее.
    boardCopy = getNewBoard()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]
    return boardCopy

def getRandomMove(board, tile):
    possibleMoves = getValidMoves(board, tile)
    return random.choice(possibleMoves)

def isOnCorner(x, y):
    # Вернуть True, если указанная позиция находится в одном из четырех углов.
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)


def getPlayerMove(board, playerTile):
    # Позволить игроку ввести свой ход.
    # Вернуть ход в виде [x, y] (или вернуть строки 'подсказка' или 'выход').
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Укажите ход, текст "выход" для завершения игры или "подсказка" для вывода подсказки.')
        move = input().lower()
        if move == 'выход' or move == 'подсказка':
            return move
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('Это недопустимый ход. Введите номер столбца (1-8) и номер ряда (1-8).')
            print('К примеру, значение 81 перемещает в верхний правый угол.')
    return [x, y]


def getComputerMove(board, computerTile):
    # Учитывая данное игровое поле и данную фишку компьютера, определить,
    # куда сделать ход, и вернуть этот ход в виде списка [x, y].
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)  # Cделать случайным порядок ходов
    # Всегда делать ход в угол, если это возможно.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Найти ход с наибольшим возможным количеством очков.
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print('Ваш счет: %s. Счет компьтера: %s ' % (scores[playerTile], scores[computerTile]))


def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print(turn + ' ходит первым.')
    # Очистить игровое поле и выставить стартовые фишки
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)
        if playerValidMoves == [] and computerValidMoves == []:
            return board  # Ходов нет ни у кого, так что окончить игру.
        elif turn == 'Человек':  # Ход человека
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board, playerTile, computerTile)

                move = getPlayerMove(board, playerTile)
                if move == 'выход':
                    print('Благодарим за игру !')
                    sys.exit()
                elif move == 'подсказка':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            turn = 'Компьютер'

        elif turn == 'Компьютер':
            if computerValidMoves != []:
                drawBoard(board)
                printScore(board, playerTile, computerTile)

                input('Нажмите клавишу Enter для просмотра хода компьютера.')
                move = getRandomMove(board, computerTile)
                makeMove(board, computerTile, move[0], move[1])
            turn = 'Человек'


print('Приветствуем в игре "Реверси"!')
playerTile, computerTile = enterPlayerTile()
while True:
    finalBoard = playGame(playerTile, computerTile)

    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('X набрал %s очков.O набрал %s очков.' % (scores['X'], scores['O']))
    if scores[playerTile] > scores[computerTile]:
        print('Вы победили компьютер, обогнав его на %s очков! Поздравления!' % (
                scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('Вы проиграли. Компьютер победил вас, обогнав на %s очков.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('Ничья!')

        print('Хотите сыграть еще раз? (да или нет)')
        if not input().lower().startswith('д'):
            break