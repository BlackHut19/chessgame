from sys import maxsize
from tkinter import *
from PIL import Image, ImageTk
import threading
import random
import time

class chess_game:
    def __init__(self,color,piece):
        self.color = color
        self.piece = piece


    def move_print(self, from_position, to_position):
        print(self.color,self.piece," from ",from_position," to ",to_position)


    #Needs a change to valid_move inside this function/// doesn't work!!!
    def king_check(self,king_position):
        if self.color == 'white':
            enemy_piece_coord_list = black_piece_coord_list
        else:
            enemy_piece_coord_list = white_piece_coord_list

        for place_list in range(len(enemy_piece_coord_list)):
            enemy_coord = enemy_piece_coord_list[place_list]
            enemy_coord_column, enemy_coord_row = list(enemy_coord)
            enemy_coord_row = int(enemy_coord_row) - 1
            enemy_coord_column = letter_to_cijfer[enemy_coord_column]
            enemy_piece = board[enemy_coord_row][enemy_coord_column]
            enemy_coord_temp_check = enemy_piece.valid_move(enemy_coord)
            if king_position in enemy_coord_temp_check:
                return True
            

    def revert(self,coord_x,coord_y):
        revert_x = cijfer_to_letter[coord_x]
        revert_y = int(coord_y) + 1
        position_xy = ("".join([str(revert_x),str(revert_y)]))
        return position_xy


    def promotion_pawn(self,coord_to_pawn):
        to_column_pawn,to_row_pawn = list(coord_to_pawn)
        to_row_pawn = int(to_row_pawn) -1
        to_column_pawn = letter_to_cijfer[to_column_pawn]
        if self.piece == 'pawn':
            if self.color == 'white':
                if to_row_pawn == 7:
                    board[to_row_pawn][to_column_pawn] = wQueen
            if self.color == 'black':
                if to_row_pawn == 0:
                    board[to_row_pawn][to_column_pawn] = bQueen
        

    def valid_move(self, coord_from_position):
        from_column, from_row = list(coord_from_position)
        from_row = int(from_row) - 1
        from_column = letter_to_cijfer[from_column]
        if self.color == 'white':
            enemy_color = 'black'
        if self.color == 'black':
            enemy_color = 'white'

        possible_moves = []
        #En Passant nog programmeren
        if self.piece == 'pawn':
            if self.color == 'white':
                if from_row != 7:
                    temp = board[from_row +1][from_column]
                    if temp == niets:
                        possible_moves.append(self.revert(from_column,from_row +1))
                        if from_row == 1:
                            temp = board[from_row +2][from_column]
                            if temp == niets:
                                possible_moves.append(self.revert(from_column,from_row +2))

                if from_row != 7 and from_column != 0:
                    temp = board[from_row +1][from_column -1]
                    if temp.color == 'black':
                        possible_moves.append(self.revert(from_column -1,from_row +1))
                    
                if from_row != 7 and from_column != 7:
                    temp = board[from_row +1][from_column +1]
                    if temp.color == 'black':
                        possible_moves.append(self.revert(from_column +1,from_row +1))

                if len(moves_list_piece) > 0:
                    if moves_list_piece[-1] == 'blackpawn':
                        from_column_enpassant,from_row_enpassant = list(moves_list_from[-1])
                        to_column_enpassant,to_row_enpassant = list(moves_list_to[-1])
                        if int(from_row_enpassant) == 7 and int(to_row_enpassant) == 5:
                            global enpassant_white
                            if from_row == 4 and from_column == int(letter_to_cijfer[to_column_enpassant]) -1:
                                possible_moves.append(self.revert(from_column +1,from_row +1))
                                enpassant_white = True
                            if from_row == 4 and from_column == int(letter_to_cijfer[to_column_enpassant]) +1:
                                possible_moves.append(self.revert(from_column -1,from_row +1))
                                enpassant_white = True

            if self.color == 'black':
                if from_row != 0:
                    temp = board[from_row -1][from_column]
                    if temp == niets:    
                        possible_moves.append(self.revert(from_column,from_row -1))
                        if from_row == 6:
                            temp = board[from_row -2][from_column]
                            if temp == niets:
                                possible_moves.append(self.revert(from_column,from_row -2))

                if from_row != 0 and from_column != 0:
                    temp = board[from_row -1][from_column -1]
                    if temp.color == 'white':
                        possible_moves.append(self.revert(from_column -1,from_row -1))
                if from_row != 0 and from_column != 7:
                    temp = board[from_row -1][from_column +1]
                    if temp.color == 'white':
                        possible_moves.append(self.revert(from_column +1,from_row -1))

                if len(moves_list_piece) > 0:
                    if moves_list_piece[-1] == 'whitepawn':
                        from_column_enpassant,from_row_enpassant = list(moves_list_from[-1])
                        to_column_enpassant,to_row_enpassant = list(moves_list_to[-1])
                        if int(from_row_enpassant) == 2 and int(to_row_enpassant) == 4:
                            global enpassant_black
                            if from_row == 3 and from_column == int(letter_to_cijfer[to_column_enpassant]) -1:
                                possible_moves.append(self.revert(from_column +1,from_row -1))
                                enpassant_black = True
                            if from_row == 3 and from_column == int(letter_to_cijfer[to_column_enpassant]) +1:
                                possible_moves.append(self.revert(from_column -1,from_row -1))
                                enpassant_black = True

        if self.piece == 'knight':
            knight_list_temp = []
            try:
                temp = board[from_row +1][from_column -2]
                if temp.color != self.color:
                    knight_list_temp.append([from_column -2,from_row +1])
            except:
                pass
            try:
                temp = board[from_row +1][from_column +2]
                if temp.color != self.color:
                    knight_list_temp.append([from_column +2,from_row +1])
            except:
                pass
            try:
                temp = board[from_row -1][from_column -2]
                if temp.color != self.color:
                    knight_list_temp.append([from_column -2,from_row -1])
            except:
                pass
            try:
                temp = board[from_row -1][from_column +2]
                if temp.color != self.color:
                    knight_list_temp.append([from_column +2,from_row -1])
            except:
                pass
            try:
                temp = board[from_row +2][from_column -1]
                if temp.color != self.color:
                    knight_list_temp.append([from_column -1,from_row +2])
            except:
                pass
            try:
                temp = board[from_row +2][from_column +1]
                if temp.color != self.color:
                    knight_list_temp.append([from_column +1,from_row +2])
            except:
                pass
            try:
                temp = board[from_row -2][from_column -1]
                if temp.color != self.color:
                    knight_list_temp.append([from_column -1,from_row -2])
            except:
                pass
            try:
                temp = board[from_row -2][from_column +1]
                if temp.color != self.color:
                    knight_list_temp.append([from_column +1,from_row -2])
            except:
                pass

            temp = [i for i in knight_list_temp if i[0] >= 0 and i[1] >= 0]
            possible_moves = ["".join([cijfer_to_letter[i[0]], str(i[1] + 1)]) for i in temp]

        if self.piece == 'rook':
            for i in range(1,from_row):
                temp = board[from_row -i][from_column]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column,from_row -1))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column,from_row -1))
                    break
            
            for i in range(1,8-from_row):
                temp = board[from_row +i][from_column]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column,from_row +i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column,from_row +i))
                    break

            for i in range(1,from_column):
                temp = board[from_row][from_column -i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column -i,from_row))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column -i,from_row))
                    break
            
            for i in range(1,8- from_column):
                temp = board[from_row][from_column +i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column +i,from_row))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column +i,from_row))
                    break

        if self.piece == 'bishop':
            for i in range(1,min(from_column+1,from_row+1)):
                temp = board[from_row -i][from_column -i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column -i,from_row -i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column -i,from_row -i))
                    break

            for i in range(1,min(8-from_row,8-from_column)):
                temp = board[from_row +i][from_column +i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column +i,from_row +i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column +i,from_row +i))
                    break
                
            for i in range(1,min(8-from_row,from_column +1)):
                temp = board[from_row +i][from_column -i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column -i,from_row +i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column -i,from_row +i))
                    break
                
            for i in range(1,min(from_row +1,8-from_column)):
                temp = board[from_row -i][from_column +i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column +i,from_row -i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column +i,from_row -i))
                    break

        if self.piece == 'queen':
            for i in range(1,min(from_column+1,from_row+1)):
                temp = board[from_row -i][from_column -i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column -i,from_row -i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column -i,from_row -i))
                    break

            for i in range(1,min(8-from_row,8-from_column)):
                temp = board[from_row +i][from_column +i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column +i,from_row +i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column +i,from_row +i))
                    break
                
            for i in range(1,min(8-from_row,from_column+1)):
                temp = board[from_row +i][from_column -i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column -i,from_row +i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column -i,from_row +i))
                    break
                
            for i in range(1,min(from_row +1,8-from_column)):
                temp = board[from_row -i][from_column +i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column +i,from_row -i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column +i,from_row -i))
                    break

            for i in range(1,from_row):
                temp = board[from_row -i][from_column]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column,from_row -1))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column,from_row -1))
                    break
            
            for i in range(1,8-from_row):
                temp = board[from_row +i][from_column]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column,from_row +i))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column,from_row +i))
                    break

            for i in range(1,from_column):
                temp = board[from_row][from_column -i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column -i,from_row))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column -i,from_row))
                    break
            
            for i in range(1,8- from_column):
                temp = board[from_row][from_column +i]
                if temp.color == self.color:
                    break
                if temp == niets:
                    possible_moves.append(self.revert(from_column +i,from_row))
                if temp.color != self.color and temp != niets:
                    possible_moves.append(self.revert(from_column +i,from_row))
                    break

        if self.piece == 'king':
            king_list_temp = []
            try:
                temp = board[from_row -1][from_column -1]
                if temp.color != self.color:
                    king_list_temp.append([from_column-1,from_row-1])
            except:
                pass
            try:
                temp = board[from_row][from_column -1]
                if temp.color != self.color:
                    king_list_temp.append([from_column-1,from_row])
            except:
                pass
            try:
                temp = board[from_row +1][from_column -1]
                if temp.color != self.color:
                    king_list_temp.append([from_column-1,from_row+1])
            except:
                pass
            try:
                temp = board[from_row -1][from_column]
                if temp.color != self.color:
                    king_list_temp.append([from_column,from_row-1])
            except:
                pass
            try:
                temp = board[from_row +1][from_column]
                if temp.color != self.color:
                    king_list_temp.append([from_column,from_row+1])
            except:
                pass
            try:
                temp = board[from_row -1][from_column +1]
                if temp.color != self.color:
                    king_list_temp.append([from_column+1,from_row-1])
            except:
                pass
            try:
                temp = board[from_row][from_column +1]
                if temp.color != self.color:
                    king_list_temp.append([from_column+1,from_row])
            except:
                pass
            try:
                temp = board[from_row +1][from_column +1]
                if temp.color != self.color:
                    king_list_temp.append([from_column+1,from_row+1])
            except:
                pass

            temp = [i for i in king_list_temp if i[0] >= 0 and i[1] >= 0]
            possible_moves = ["".join([cijfer_to_letter[i[0]], str(i[1] + 1)]) for i in temp]

        return possible_moves


wKing = chess_game('white', 'king')
wQueen = chess_game('white', 'queen')
wBishop = chess_game('white', 'bishop')
wKnight = chess_game('white', 'knight')
wRook = chess_game('white', 'rook')
wPawn = chess_game('white', 'pawn')
bKing = chess_game('black', 'king')
bQueen = chess_game('black', 'queen')
bBishop = chess_game('black', 'bishop')
bKnight = chess_game('black', 'knight')
bRook = chess_game('black', 'rook')
bPawn = chess_game('black', 'pawn')
niets = chess_game('nocolor','nopiece')            

board = [[niets] * 8 for i in range(8)]
board[0][0] = wRook
board[0][1] = wKnight
board[0][2] = wBishop
board[0][3] = wKing
board[0][4] = wQueen
board[0][5] = wBishop
board[0][6] = wKnight
board[0][7] = wRook
for x in range(8):
    board[1][x] = wPawn
for x in range(8):
    board[6][x] = bPawn
board[7][0] = bRook
board[7][1] = bKnight
board[7][2] = bBishop
board[7][3] = bKing
board[7][4] = bQueen
board[7][5] = bBishop
board[7][6] = bKnight
board[7][7] = bRook

def search_list(board, piece):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == piece:
                search_piece_row = int(i) +1
                search_piece_column = cijfer_to_letter[j]
                search_piece_coord = ("".join([str(search_piece_column) , str(search_piece_row)]))
                return search_piece_coord


#Tkinter init program
window = Tk()
w = Canvas(window, width=610, height=610, bg='Black')
w.pack()
window.title("Nuub Chess")

WhiteKingImg =  ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\King_White_TP.png'))
WhiteQueenImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Queen_White_TP.png'))
WhiteLoperImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Loper_White_TP.png'))
WhitePaardImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Paard_White_TP.png'))
WhiteTorenImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Toren_White_TP.png'))
WhitePionImg =  ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Pion_White_TP.png'))
BlackKingImg =  ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\King_Black_TP.png'))
BlackQueenImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Queen_Black_TP.png'))
BlackLoperImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Loper_Black_TP.png'))
BlackPaardImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Paard_Black_TP.png'))
BlackTorenImg = ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Toren_Black_TP.png'))
BlackPionImg =  ImageTk.PhotoImage(Image.open('C:\Saba\Python\Chess\Pion_Black_TP.png'))

def initBoard():
    w.create_rectangle(25, 25, 585 , 585, fill='lightgrey', width=0)
    number_list = ['1','2','3','4','5','6','7','8']
    text_list = ['A','B','C','D','E','F','G','H']
    for x in range(8):
        w.create_text(x*70+60,12.5,fill="White",text=text_list[x])
        w.create_text(x*70+60,597.5,fill="White",text=text_list[x])
        w.create_text(12.5,x*70+60,fill="White",text=number_list[x])
        w.create_text(597.5,x*70+60,fill="White",text=number_list[x])
    for c in range(8):
        for r in range(8):
            if c&1 ^ r&1:
                w.create_rectangle(r*70+25, c*70+25, (r*70+25)+70 , (c*70+25)+70, fill='grey', width=0)
                
def initPieces():
    for x,j in enumerate(white_piece_list):
        if j == ('wRook'):
            c_show, r_show = list(white_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=WhiteTorenImg)
        if j == ('wKnight'):
            c_show, r_show = list(white_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=WhitePaardImg)
        if j == ('wBishop'):
            c_show, r_show = list(white_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=WhiteLoperImg)
        if j == ('wQueen'):
            c_show, r_show = list(white_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=WhiteQueenImg)
        if j == ('wKing'):
            c_show, r_show = list(white_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=WhiteKingImg)
        if j == ('wPawn'):
            c_show, r_show = list(white_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=WhitePionImg)

    for x,j in enumerate(black_piece_list):
        if j == ('bRook'):
            c_show, r_show = list(black_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=BlackTorenImg)
        if j == ('bKnight'):
            c_show, r_show = list(black_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=BlackPaardImg)
        if j == ('bBishop'):
            c_show, r_show = list(black_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=BlackLoperImg)
        if j == ('bQueen'):
            c_show, r_show = list(black_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=BlackQueenImg)
        if j == ('bKing'):
            c_show, r_show = list(black_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=BlackKingImg)
        if j == ('bPawn'):
            c_show, r_show = list(black_piece_coord_list[x])
            w.create_image(letter_to_cijfer[c_show]*70+25,(int(r_show)-1)*70+25, anchor=NW, image=BlackPionImg)

            
player_A = True
player_B = False

letter_to_cijfer = {"a" : 0,"b" : 1,"c" : 2,"d" : 3,"e" : 4,"f" : 5,"g" : 6,"h" : 7}
cijfer_to_letter = {0: "a",1: "b",2: "c",3: "d",4: "e",5: "f",6: "g",7: "h"}
letter_list = ['a','b','c','d','e','f','g','h']
cijfer_list = ['1','2','3','4','5','6','7','8']
white_piece_coord_list = ['a1','b1','c1','d1','e1','f1','g1','h1','a2','b2','c2','d2','e2','f2','g2','h2']
black_piece_coord_list = ['a7','b7','c7','d7','e7','f7','g7','h7','a8','b8','c8','d8','e8','f8','g8','h8']
moves_list_from = []
moves_list_to = []
moves_list_piece = []
white_piece_list = ['wRook','wKnight','wBishop','wQueen','wKing','wBishop','wKnight','wRook','wPawn','wPawn','wPawn','wPawn','wPawn','wPawn','wPawn','wPawn']
black_piece_list = ['bPawn','bPawn','bPawn','bPawn','bPawn','bPawn','bPawn','bPawn','bRook','bKnight','bBishop','bQueen','bKing','bBishop','bKnight','bRook']


while True:
    w.delete("all")
    initBoard()
    initPieces()
    window.update()    
    enpassant_white = False
    enpassant_black = False

    if player_A == True:
        my_piece_list = white_piece_list
        my_piece_coord_list = white_piece_coord_list
        enemy_piece_list = black_piece_list
        enemy_piece_coord_list = black_piece_coord_list
        print("WHITE's MOVES")
        input_from = input("from: ")

    if player_B == True:
        my_piece_list = black_piece_list
        my_piece_coord_list = black_piece_coord_list
        enemy_piece_list = white_piece_list
        enemy_piece_coord_list = white_piece_coord_list
        print("BLACK's MOVES")    
        input_from = random.choice(my_piece_coord_list)
        print("from :",input_from)

    input_from = input_from.strip().lower()
    
    if input_from in my_piece_coord_list:
        from_column_input, from_row_input = list(input_from)
        from_row_input = int(from_row_input) -1
        from_column_input = letter_to_cijfer[from_column_input]
        from_piece_input = board[from_row_input][from_column_input]
        possible_move_list = from_piece_input.valid_move(input_from)
        print(possible_move_list)
        if player_A == True:
            if len(possible_move_list) > 0:
                input_to = input("to: ")
            else:
                continue
                
        if player_B == True:
            if len(possible_move_list) > 0:
                input_to = random.choice(possible_move_list)
            else:
                continue
            
        input_to = input_to.strip().lower()
        to_column_input, to_row_input = list(input_to)
        to_row_input = int(to_row_input) -1
        to_column_input = letter_to_cijfer[to_column_input]
        to_piece_input = board[to_row_input][to_column_input]

        if from_piece_input.color == 'white':
            check_king = wKing
            king_position = search_list(board,wKing)
        else:
            check_king = bKing
            king_position = search_list(board,bKing)

        if input_to in possible_move_list:
            board[to_row_input][to_column_input] = from_piece_input
            board[from_row_input][from_column_input] = niets

            if check_king.king_check(king_position) != True:
                if input_to in enemy_piece_coord_list:
                    piece_place_list = enemy_piece_coord_list.index(input_to)
                    del enemy_piece_list[piece_place_list]
                    del enemy_piece_coord_list[piece_place_list]

                if input_from in my_piece_coord_list:
                    coord_place_list = my_piece_coord_list.index(input_from)
                    my_piece_coord_list[coord_place_list] = str(input_to)

                if enpassant_white == True:
                    piece_enpassant = board[to_row_input -1][to_column_input]
                    enpassant_place_list = my_piece_coord_list.index
                    board[to_row_input -1][to_column_input] = niets
                if enpassant_black == True:
                    board[to_row_input +1][to_column_input] = niets

                from_piece_input.promotion_pawn(input_to)
                from_piece_input.move_print(input_from, input_to)
                moves_list_from.append(input_from)
                moves_list_to.append(input_to)
                from_pieceColorPiece = "".join([str(from_piece_input.color),str(from_piece_input.piece)])
                moves_list_piece.append(from_pieceColorPiece)

                if 'wKing' not in white_piece_list:
                    w.configure(background='Grey')
                    w.create_rectangle(25, 25, 585 , 585, fill='Black', width=0)
                    w.create_text(305,240,font=("Verdana",100),fill="White",text="BLACK")
                    w.create_text(305,360,font=("Verdana",100),fill="White",text="WIN")
                    break
                if 'bKing' not in black_piece_list:
                    w.configure(background='Grey')
                    w.create_rectangle(25, 25, 585 , 585, fill='White', width=0)
                    w.create_text(305,240,font=("Verdana",100),fill="Black",text="WHITE")
                    w.create_text(305,360,font=("Verdana",100),fill="Black",text="WIN")
                    break
                if player_A == True:
                    player_A = False
                    player_B = True
                else:
                    player_A = True
                    player_B = False

            if check_king.king_check(king_position) == True:
                print(from_piece_input.color, from_piece_input.piece,"is in check, please protect your king!")
                board[to_row_input][to_column_input] = to_piece_input
                board[from_row_input][from_column_input] = from_piece_input
