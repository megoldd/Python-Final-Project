
import pygame
import random


pygame.init()

width = 600
height = 700
margin = 10
tMargin = 100
bMargin = 100
lrMargin = 100

sqSize = (width - 4 * margin - 2 * lrMargin) // 5
huge_font = pygame.font.Font('freesansbold.ttf', sqSize)
small_font = pygame.font.Font('freesansbold.ttf', sqSize//3)

def findUnguessedLetters(guessed):
    guessedLetters = "".join(guesses)
    unguessedLetters = ""
    for letter in alphabet:
        if letter not in guessedLetters:
            unguessedLetters = unguessedLetters + letter
    return unguessedLetters

def determineColor(guess, l):
    letter = guess[l]
    if letter == secret_word[l]:
        return green
    elif letter in secret_word:
        Ntarget = secret_word.count(letter)
        Ncorrect = 0
        Noccurrance = 0
        for i in range(5):
            if guess[i] == letter:
                if i <= l:
                    Noccurrance += 1
                if letter == secret_word[i]:
                    Ncorrect += 1
        if Ntarget - Ncorrect - Noccurrance >= 0:
            return yellow
    else:
        return gray


white = (255, 255, 255)
black = (0, 0, 0)
green = (6, 220, 160)
yellow = (255, 210, 100)
gray = (75, 75, 90)

input = ""
guesses = []
alphabet = "abcdefghijklmnopqrstuvwxyz"
unguessed = alphabet
gameOver = False

#screen setup 
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('Wordle')
font = pygame.font.Font('freesansbold.ttf', 56)

secret_word = random.choice(open('words.txt', 'r').readline().split())
screen = pygame.display.set_mode([width, height])

running = True 
while running:
    screen.fill(white)

    letters = small_font.render(unguessed, False, gray)
    surface = letters.get_rect(center = (width//2, tMargin//2))
    screen.blit(letters, surface)

 

    y = tMargin 
    for i in range(6):
        x = lrMargin
        for l in range(5):
            square = pygame.Rect(x,y,sqSize, sqSize)
            pygame.draw.rect(screen, gray, square, width=2, border_radius=3)

            if i < len(guesses):
                color = determineColor(guesses[i], l)
                pygame.draw.rect(screen, color, square, border_radius=3)
                letter = font.render(guesses[i][l], False, white)
                surface = letter.get_rect(center = (x + sqSize//2, y + sqSize //2))
                screen.blit(letter, surface)

            if i == len(guesses) and l < len(input):
                letter = font.render(input[l], False, gray)
                surface = letter.get_rect(center = (x + sqSize//2, y + sqSize //2))
                screen.blit(letter, surface)


            x += sqSize + margin
        y += sqSize + margin

    if len(guesses) == 6 and guesses[5] != secret_word:
        gameOver = True
        letters = font.render(secret_word, False, gray)
        surface = letters.get_rect(center = (width//2, height - bMargin//2 - margin))
        screen.blit(letters, surface)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_BACKSPACE:
                if len(input) > 0:
                    input = input[:len(input)-1]

            elif event.key == pygame.K_RETURN:
                if len(input) == 5 and input: 
                    guesses.append(input)
                    unguessed = findUnguessedLetters(guesses)
                    gameOver = True if input == secret_word else False
                    input = ""
            
            elif event.key == pygame.K_SPACE:
                gameOver = False
                secret_word = random.choice(open('words.txt', 'r').readline().split())
                print("The word was:\n", secret_word)
                guesses = []
                unguessed = alphabet
                input = ""

            elif len(input) < 5 and not gameOver:
                input = input + event.unicode.lower()