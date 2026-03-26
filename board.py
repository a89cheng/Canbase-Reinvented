
def draw_board():
    import turtle

    t = turtle.Turtle()
    t.speed(0)

    square_size = 75
    start_x = -300
    start_y = 300

    for row in range(8):
        for col in range(8):
            t.penup()
            t.goto(start_x + col * square_size, start_y - row * square_size)
            t.pendown()

            if (row + col) % 2 == 0:
                t.fillcolor("white")
            else:
                t.fillcolor("black")

            t.begin_fill()
            for _ in range(4):
                t.forward(square_size)
                t.right(90)
            t.end_fill()

        turtle.done()

moves = """1. e4 Nf6 2. e5 Nd5 3. d4 d6 4. Nf3 Bg4 5. Be2 e6 6. O-O Be7 7. c4 Nb6 8. Nc3 O-O 9. Be3 Nc6 
10. exd6 cxd6 11. d5 exd5 12. cxd5 Bxf3 13. gxf3 Ne5 14. f4 Ned7 15. Rc1 Rc8 16. b3 Nf6 17. Kh1 a6 18. Rg1 Re8 19. Bd4 Bf8 
20. Bd3 Nbd7 21. Bf5 g6 22. Bxf6 Nxf6 23. Bxc8 Qxc8 24. Ne4 Qf5 25. Nxf6+ Qxf6 26. Qf3 Bh6 27. Rc3 Bxf4 28. Rc4 Be5 29. Qxf6 Bxf6 
30. Rc2 Bd4 31. Rg4 Re1+ 32. Kg2 Bc5 33. b4 Bb6 34. Rc8+ Kg7 35. Rb8 Re7 36. Rf4 f5 37. Rf3 Kf6 38. Kf1 Ke5 39. Rd3 Kf4 
40. a3 Ke4 41. Rd2 Kf3 42. Rc8 f4 43. h3 1-0"""

pieces = {}


# The sequences goes: move number, white move, black move and then next move
# Use .lower() = true? to test whether it's a pawn move, and or else

def breakdown(moves):
    actions = moves.split(" ")
    for i in range(len(actions)):
        actions[i].strip()
    return actions


def define(actions):
    for i in actions:
        element = actions[i]

        if not element[0].isupper():
            pass
            # It's a pawn

        if element[0] == "0":
            if len(element) == 3:
                # short castling
                pass
            else:
                # long castling
                pass

            pass


def display():
    # could possible set all of them as variables
    board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

    print("  a   b   c   d   e   f   g   h")
    print("---------------------------------")
    for i in range(8):
        print("| ", end="")
        for j in range(7):
            print(board[i][j], end="")
            print(" | ", end="")
        print(board[i][7], end="")
        print(" |")
        print("---------------------------------")


if __name__ in "__main__":
    display()
    breakdown(moves)