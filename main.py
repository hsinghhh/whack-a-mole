import pygame
import random
import time

pygame.init()
pygame.display.set_caption("Whack-A-Mole")
screen = pygame.display.set_mode((500, 500))

bgColor = [50, 36, 20]
textColor = [255, 255, 255]

running = True
score = 0
timeLimit = 20
cooldown = False
cooldownTime = 0.5

moleImage = pygame.image.load("sprite.png")
squashedImage = pygame.image.load("squashed.png")
moleW, moleH = 150, 180
mole = pygame.transform.scale(moleImage, (moleW, moleH))
squashed = pygame.transform.scale(squashedImage, (150, 140))

cursorImage = pygame.image.load("cursor.png").convert_alpha()
cursorImage = pygame.transform.scale(cursorImage, (75, 105))
pygame.mouse.set_visible(False)

def molePos():
    x = random.randint(0, 350)
    y = random.randint(60, 320)
    return x, y

def moleInText(moleRect, textRects):
    for rect in textRects:
        if moleRect.colliderect(rect):
            return True
    return False

def saveHighScore(score):
    try:
        with open('highScores.txt', 'r') as file:
            highScores = []
            for line in file:
                highScores.append(int(line.strip()))
    except FileNotFoundError:
        highScores = []
        
    highScores.append(score)
    highScores.sort(reverse=True)
    highScores = highScores[:5]
    
    with open('highScores.txt', 'w') as file:
        for score in highScores:
            file.write(f"{score}\n")

def loadHighScores():
    try:
        with open('highScores.txt', 'r') as file:
            highScores = []
            for line in file:
                highScores.append(int(line.strip()))
    except FileNotFoundError:
        highScores = []
        
    return highScores

moleX, moleY = molePos()
moleRect = pygame.Rect(moleX, moleY, moleW, moleH)
startTime = time.time()
hitTime = None

while running:
    currentTime = time.time()
    elapsedTime = currentTime - startTime
    remainingTime = max(0, timeLimit - elapsedTime)
    
    if remainingTime <= 0:
        running = False
        continue
    
    screen.fill(bgColor)

    titleFont = pygame.font.Font('mightysouly.ttf', 40)
    scoreFont = pygame.font.Font('saira.ttf', 15)
    otherFont = pygame.font.Font('mightysouly.ttf', 25)
    titleText = titleFont.render("WHACK-A-MOLE!", True, textColor)
    titleTextRect = titleText.get_rect(center=(250, 30))
    scoreText = scoreFont.render("Score: ", True, textColor)
    scoreTextRect = scoreText.get_rect(center=(250, 480))
    scoreNum = otherFont.render(str(score), True, textColor)
    scoreNumRect = scoreText.get_rect(center=(300, 475))
    timeText = scoreFont.render("Time Left: ", True, textColor)
    timeTextRect = timeText.get_rect(center=(250, 450))
    timeLeftText = otherFont.render(str(int(remainingTime)), True, textColor)
    timeLeftTextRect = scoreText.get_rect(center=(310, 445))


    textRects = [scoreTextRect, titleTextRect, timeTextRect, timeLeftTextRect, scoreNumRect]
    
    screen.blit(scoreText, scoreTextRect)
    screen.blit(scoreNum, scoreNumRect)
    screen.blit(titleText, titleTextRect)
    screen.blit(timeLeftText, timeLeftTextRect)
    screen.blit(timeText, timeTextRect)
    
    if cooldown:
        screen.blit(squashed, (moleX, moleY))
        if currentTime - hitTime > cooldownTime:
            cooldown = False
            moleX, moleY = molePos()
            moleRect.topleft = (moleX, moleY)
            while moleInText(moleRect, textRects):
                moleX, moleY = molePos()
                moleRect.topleft = (moleX, moleY)
    else:
        while moleInText(moleRect, textRects):
            moleX, moleY = molePos()
            moleRect.topleft = (moleX, moleY)
        screen.blit(mole, (moleX, moleY))
    
    mouseX, mouseY = pygame.mouse.get_pos()
    screen.blit(cursorImage, (mouseX, mouseY))
    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not cooldown:
            mousePos = pygame.mouse.get_pos()
            if moleRect.collidepoint(mousePos):
                score += 1
                hitTime = currentTime
                cooldown = True

saveHighScore(score)
highScores = loadHighScores()

screen.fill(bgColor)
endFont = pygame.font.Font('mightysouly.ttf', 25)
finalFont = pygame.font.Font('saira.ttf', 15)
gameOverText = endFont.render("Game Over!", True, textColor)
gameOverTextRect = gameOverText.get_rect(center=(250, 50))
finalScoreText = endFont.render("Your Score: " + str(score), True, textColor)
finalScoreTextRect = finalScoreText.get_rect(center=(250, 100))

screen.blit(gameOverText, gameOverTextRect)
screen.blit(finalScoreText, finalScoreTextRect)

highScoreY = 150
if highScores:
    highScoreTitle = endFont.render("High Scores:", True, textColor)
    highScoreTitleRect = highScoreTitle.get_rect(center=(250, highScoreY))
    screen.blit(highScoreTitle, highScoreTitleRect)
    
    highScoreY += 30
    for score in highScores:
        highScoreText = finalFont.render(str(score), True, textColor)
        highScoreRect = highScoreText.get_rect(center=(250, highScoreY))
        screen.blit(highScoreText, highScoreRect)
        highScoreY += 30

pygame.display.update()
pygame.time.wait(15000)
pygame.quit()
