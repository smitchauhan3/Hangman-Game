import pygame
import random
from tkinter import messagebox
import sys
from button import Button

#----------------------------------------#
#   setting pygame
#----------------------------------------#

pygame.init()
pygame.display.set_caption('Hangman!')

pygame_icon = pygame.image.load('assets\icon.png')

pygame.display.set_icon(pygame_icon)
winHeight = 650
winWidth = 425
win = pygame.display.set_mode((winWidth,winHeight))

BG = pygame.image.load("assets/home bg.png")
BG = pygame.transform.scale(BG,(425,650))

#-----------------------------------------#
# initializing global variables/constants #
#-----------------------------------------#

#global variables
word = ''
buttons = []
guessed = []
lives = 0
levels = 1
prob=0

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)

#fonts
sec_font = pygame.font.SysFont('RooneySans Light', 28)

#Hangman Pics
hangmanPics = [pygame.image.load('assets/h2.png'), pygame.image.load('assets/h3.png'), 
               pygame.image.load('assets/h4.png'), pygame.image.load('assets/h5.png'), 
               pygame.image.load('assets/h6.png'), pygame.image.load('assets/h7.png'),]

# Game sounds
GAME_SOUNDS = {}
GAME_SOUNDS['lose'] = pygame.mixer.Sound('assets/audio/lose.wav')
GAME_SOUNDS['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound('assets/audio/point.wav')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')
GAME_SOUNDS['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')
GAME_SOUNDS['win'] = pygame.mixer.Sound('assets/audio/win.wav')

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

def getword():
    file = open('projectdata.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)
    return f[i][:-1]

#------------------------------------------------------------------------------------------#

def hint(hintword):
    h = hintword[0]
    global hintcategory
    if(h=='#'):
        hintcategory ='Cricketer'
    if(h=='@'):
        hintcategory ='Fruit'
    if(h=='!'):
        hintcategory ='Country'
    if(h=='$'):
        hintcategory ='Animal'
    if(h=='%'):
        hintcategory ='School'
    print("hint :" + hintcategory)
    return hintword[1:]

#------------------------------------------------------------------------------------------#

def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord

#------------------------------------------------------------------------------------------# 

def draw_window():
    global guessed
    global hangmanPics
    global lives

    backPics = pygame.image.load("assets/bg1.png").convert()
    backPics = pygame.transform.scale(backPics,(425,650))
    win.blit(backPics, (0, 0))
    
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, WHITE, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2)
            label = sec_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))
            
    # dash label
    spaced = spacedOut(word, guessed)
    label1 = sec_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    win.blit(label1,(winWidth/2 - length/2, 400))

    # level label
    levellbl = sec_font.render('Winning Streak - '+ str(levels-1), 1, BLACK)
    win.blit(levellbl, (winWidth/2 - (levellbl.get_width()/2),30))

    # guesses label
    totalguesses = 6
    guesslbl = sec_font.render('Guesses : ' + str(lives) + '/' + str(totalguesses), 1, BLACK)
    win.blit(guesslbl, (20, 75))

    #analysis label
    if len(guessed)==0:
        plabel= sec_font.render('Win %: 0%', 1, BLACK)
    else:
        plabel= sec_font.render('Win %: '+str(prob) +'%', 1, BLACK)
    win.blit(plabel, (275, 75))

    # hint
    pygame.draw.rect(win, '#ffffff', pygame.Rect(150, 340, 125, 35),border_radius=12)
    hintlbl = sec_font.render(hintcategory, 1, BLACK)
    win.blit(hintlbl, (winWidth / 2 - hintlbl.get_width() / 2, 348))
    
    # hangman pictures
    pic = hangmanPics[lives]
    win.blit(pic, (winWidth/2 - pic.get_width()/2, 110))

    pygame.display.update()
  
#------------------------------------------------------------------------------------------#

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                GAME_SOUNDS['wing'].play()
                return buttons[i][5]
    
    return None
        
#------------------------------------------------------------------------------------------#

def find_prob():
    li1 = list(set(guessed)&set(word.upper()))
    li2 = list(set(word.upper()))
    prob = len(li1)/((len(li2) + lives)/2 )* 100
    if prob>=100:
        prob = len(li1) / len(li2) * 100
    return int(prob)

#------------------------------------------------------------------------------------------#

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False
 
#------------------------------------------------------------------------------------------#

def quit_redraw_window():
    que = messagebox.askquestion("Question Box", "Are you sure to quit this game ?")
    if que == "yes":
        sys.exit()
    else:
        reset()

#------------------------------------------------------------------------------------------#

def end(winner=False):
    global lives
    global levels
    
    levelTxtcomplete = 'Level - ' + str(levels) + ' completed' 
    levelTxtfailed = 'Level - ' + str(levels) + ' failed' 
    lbl = 'press any key to play again...'
    draw_window()
    win.fill(WHITE)

    if winner == True:
        GAME_SOUNDS['win'].play()
        wPics = pygame.image.load("assets/win.jpg").convert()
        wPics = pygame.transform.scale(wPics,(300,270))
        win.blit(wPics, (60, 280))
        wPics = pygame.image.load("assets/winner.jpg").convert()
        wPics = pygame.transform.scale(wPics,(425,300))
        win.blit(wPics, (0, 0))
        slabel = sec_font.render(lbl, 1, BLACK)
        levellbl = sec_font.render(levelTxtcomplete,1,BLACK)
        levels = levels + 1
    else:
        GAME_SOUNDS['lose'].play()
        lPics = pygame.image.load("assets/loss.jpg").convert()
        lPics = pygame.transform.scale(lPics,(270,270))
        win.blit(lPics, (60, 280))
        lPics = pygame.image.load("assets/looser.jpg").convert()
        lPics = pygame.transform.scale(lPics,(425,300))
        win.blit(lPics, (0, 0))
        slabel = sec_font.render(lbl, 1, BLACK)
        levellbl = sec_font.render(levelTxtfailed,1,BLACK)

    wordTxt = sec_font.render(word.upper(), 1, BLACK)
    wordWas = sec_font.render('correct word is: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 85))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 50))
    win.blit(levellbl, (winWidth / 2 - levellbl.get_width() / 2, 160))
    win.blit(slabel, (winWidth / 2 - slabel.get_width() / 2, 580))

    pygame.display.update()

    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_redraw_window()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()

#------------------------------------------------------------------------------------------#

def reset():
    global lives
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    lives = 0
    guessed = []
    word = getword()
    word = hint(word)

#------------------------------------------------------------------------------------------#

def get_font(size):
    return pygame.font.Font("assets/font4.ttf", size)
      
def main_menu():
    while True:
        win.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/btn2.png"), pos=(win.get_width()/2, 450), 
                            text_input="PLAY", font=get_font(22), base_color="#21252b", hovering_color="#0070b2")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/btn2.png"), pos=(win.get_width()/2, 525), 
                            text_input="QUIT", font=get_font(22), base_color="#21252b", hovering_color="#0070b2")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    GAME_SOUNDS['swoosh'].play()
                    return None
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    GAME_SOUNDS['swoosh'].play()
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

#------------------------------------------------------------------------------------------#
#   MAINLINE
#------------------------------------------------------------------------------------------#

main_menu()

# Setup buttons
increase = round(winWidth / 10)
for i in range(26):
    if i < 9:
        y = 485
        x = 45 + (increase * i)
    elif (i>=9 and i<18):
        x = 45 + (increase * (i - 9))
        y = 535
    elif(i<=26):
        x = increase * (i - 16.2)
        y = 585
    buttons.append([WHITE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word = getword()
word = hint(word)
inPlay = True

while inPlay:
    draw_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_redraw_window()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None and chr(letter) not in guessed:
                guessed.append(chr(letter))
                prob = find_prob()
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if lives != 5:
                        lives += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()

#------------------------------------------------------------------------------------------#
#   END                                                                                    
#------------------------------------------------------------------------------------------#