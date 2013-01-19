#pythonDefender Beta 0.1
#Copyright (c) 2012, RevertedSoft
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pygame, sys, random, os
from pygame.locals import *

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        if gameLoop == 1:
            drawText('Press SPACE to continue . . .', font, windowSurface, round((WINDOWWIDTH / 3)) + 20, round((WINDOWHEIGHT / 2)), GREEN)
            pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return

            if event.type == KEYUP:
                if event.key == K_ESCAPE or event.key == ord('q'):
                    terminate()

                if event.key == K_i:
                    instructions()
                    return

def instructions():
    windowSurface.fill(BLACK)
    instructionsOn = True
    while instructionsOn:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
                
        drawText('INSTRUCTIONS', font, windowSurface, round(WINDOWWIDTH/2) - 40, 5, GREEN)
        drawText('Use the <left> and <right> arrow keys to maneuver your ship.', font, windowSurface, 1, 21, GREEN)
        drawText('Use the <spacebar> to fire your cannons.', font, windowSurface, 1, 36, GREEN)
        drawText('Press the <s> key at any time to open the shop.', font, windowSurface, 1, 51, GREEN)
        drawText('Purchase upgrades with the mouse.', font, windowSurface, 1, 66, GREEN)
        drawText('Press space to continue. . .', font, windowSurface, 1, 81, GREEN)
        pygame.display.update()

        waitForPlayerToPressKey()


        return
            

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 400
WINDOWHEIGHT = 800
pygame.display.set_icon(pygame.image.load('Images' + os.sep + 'playerShip.png'))
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('pythonDefender')

# set up the background and sprites
backgroundImage = pygame.image.load('Images' + os.sep + 'pythonDefenderBackground.jpg')
backgroundRect = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))

enemyImage = pygame.image.load('Images' + os.sep + 'enemyDrone.png')
enemyImageFlipped = pygame.transform.flip(enemyImage, False, True)

playerBulletImage = pygame.image.load('Images' + os.sep + 'Bullet.png')

playerShipImage = pygame.image.load('Images' + os.sep + 'playerShip.png')

enemyBulletImage = pygame.image.load('Images' + os.sep + 'enemyBullet.png')

# setup speed variables
playerSpeed = 10
compSpeed = 6

# setup movement variables
RIGHT = 6
LEFT = 4

# set up the colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
DARKGREY = (52,52,52)
RED = (255,0,0)
GREEN = (0,255,0)
LIGHTBLUE = (0,255,255)
TURQUOISE = (0,255,126)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,126,0)
PURPLE = (255,0,255)
DEEPPURPLE = (128,0,128)

# set up the font
font = pygame.font.SysFont(None, 18)
smallFont = pygame.font.SysFont(None, 14)


#-----------------------------------DEFENDER-----------------------------------#


# Run the game loops
while True:

    gameLoop = 0

    # Welcome loop

    # display the welcome screen
    windowSurface.fill(BLACK)
    drawText('pythonDefender', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 2), GREEN)
    drawText('Press space to start, or ESCAPE to exit.', font, windowSurface, ((WINDOWWIDTH / 4) - 20), (WINDOWHEIGHT / 2) + 30, GREEN)
    drawText('Press <i> for instructions.', font, windowSurface, ((WINDOWWIDTH / 4) - 20), (WINDOWHEIGHT / 2) + 45, GREEN)
    pygame.display.update()

    # wait for player to press key to continue
    waitForPlayerToPressKey()

    while True:

        # Setup loop

        # setup player ship, computer ships, and bullets
        playerAlive = True
        playerShopOpen = False
        dashBoard = pygame.Rect(0, (WINDOWHEIGHT - 45), WINDOWWIDTH, 45)
        playerScore = 0
        playerCredits = 0
        playerWidth = 12
        playerHeight = 16
        shieldSpaceSide = (playerWidth)
        shieldSpaceTop = (playerHeight / 2)
        shieldRadius = (float(playerHeight) * 1.5)
        playerSpeed = 10        
        playerBulletSpeed = 15
        playerShip = {'rect':pygame.Rect((WINDOWWIDTH / 2) - (playerWidth / 2), (dashBoard.top - playerHeight - shieldSpaceTop - 10), playerWidth, playerHeight),
                      'speed':playerSpeed,
                      'surface':pygame.transform.scale(playerShipImage, ((playerWidth*2), (playerHeight*2)))}
        playerShield = pygame.Rect((playerShip['rect'].left - shieldSpaceSide), (playerShip['rect'].top - shieldSpaceTop), ((playerWidth + shieldSpaceSide * 2)), ((playerHeight + shieldSpaceTop * 2)))
        shieldImage = pygame.image.load('Images\\shieldSprite.png')
        shieldRect = pygame.transform.scale(shieldImage, ((int(shieldRadius*2)), (int(shieldRadius*2))))
        playerShieldHealth = 2
        playerShieldRegenRate = 0
        playerShieldRegenThresh = 400 # number of ticks before 1 point of shield regenerates
        playerShieldMax = 2
        playerBullets = []
        playerBulletWidth = 2
        playerBulletHeight = 4
        # setup players superweapon
        playerLaserWidth = 1
        playerLaserCurrentReload = 0
        playerLaserReload = 500
        playerLaserCurrentDuration = 0
        playerLaserDuration = 0
        playerLaserOwned = False
        playerLaserOn = False
        playerLaserTry = False
        extensionValue = 0
        playerLaserList = []
                
        currentReload = 0
        reload = 20 # number of ticks before a player can fire again, upgrades available to increase speed
        reloadUpgradeCount = 0
        reloadUpgradeMax = 10
        cannonSizeUpgradeCount = 0
        cannonSizeUpgradeMax = 5
        maxShieldUpgradeCount = 0
        maxShieldUpgradeMax = 6
        shieldRegenUpgradeCount = 0
        shieldRegenUpgradeMax = 18
        laserUpgradeCount = 0
        laserUpgradeMax = 5
        
        computerShipWidth = 11
        computerShipHeight = 15
        computerSize = 20
        computerStartPositionX = 1
        computerStartPositionY = 1
        computerSpeed = 4
        computerReload = 33
        computerBulletSpeed = 12
        computerBulletWidth = 1
        computerBulletHeight = 3
        computerShips = []
        addComputerShip = 15
        addComputerIncrement = 100 # number of ticks between enemy ship spawns
        computerBullets = []
        spawnRate = 2000 # number of ticks before the spawn rate is increased, also conected to wave
        bulletInflator = 2 # number of spawn cycles before computer bullet size is increased
        wave = 1
        
        # setup player movement variables
        moveLeft = False
        moveRight = False
        addPlayerBullets = False

        while playerAlive:

            # Game loop

            # variable to prevent crash from two bullets hitting an enemy ship
            bulletHit = False

            # increase difficulty after wave 20
            if wave > 20:
                    computerReload = 10
                    computerBulletSpeed = 15
                    computerSpeed = 7

            # check for the QUIT event
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                # check for keypress events
                if event.type == KEYDOWN:
                    # change keyboard variables
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveLeft = True
                        moveRight = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = True
                        moveLeft = False
                    if event.key == K_SPACE:
                        addPlayerBullets = True
                        playerLaserTry = True #REMOVE
                    if event.key == ord('p'):
                        waitForPlayerToPressKey()
            
                    # check for shop open
                    if event.key == ord('s'):
                        playerShopOpen = True
                    
                if event.type == KEYUP:
                    if event.key == K_ESCAPE or event.key == ord('q'):
                        terminate()
                    if event.key == K_LEFT or event.key == ord('a'):
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == ord('d'):
                        moveRight = False
                    if event.key == K_SPACE:
                        addPlayerBullets = False
                        playerLaserTry = False

            # handle the player shop
            while playerShopOpen:

                # set up player mouse position to handle button clicks
                mousePos = pygame.mouse.get_pos()

                # set up the button column
                buttonX = 175

                # set up the costs and increase value as purchased
                reloadUpgradeCost = ((reloadUpgradeCount * 1500) + 1500)
                cannonSizeUpgradeCost = ((cannonSizeUpgradeCount * 2000) + 2000)
                maxShieldUpgradeCost = ((maxShieldUpgradeCount * 2000) + 2000)
                shieldRegenUpgradeCost = ((shieldRegenUpgradeCount * 500) + 500)
                laserUpgradeCost = ((laserUpgradeCount * 25000) + 25000)

                # check for the QUIT event
                for event in pygame.event.get():
                    if event.type == QUIT:
                        terminate()

                    # check for mouse button events, and handle appropriately if a button is clicked
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if reloadUpgrade.collidepoint(mousePos) and reloadUpgradeCount <= reloadUpgradeMax and playerCredits >= reloadUpgradeCost:
                                reload -= 1
                                playerCredits -= reloadUpgradeCost
                                reloadUpgradeCount += 1
                            if cannonSizeUpgrade.collidepoint(mousePos) and cannonSizeUpgradeCount <= cannonSizeUpgradeMax and playerCredits >= cannonSizeUpgradeCost:
                                playerBulletWidth += 1
                                playerBulletHeight += 1
                                playerCredits -= cannonSizeUpgradeCost
                                cannonSizeUpgradeCount += 1
                            if maxShieldUpgrade.collidepoint(mousePos) and maxShieldUpgradeCount <= maxShieldUpgradeMax and playerCredits >= maxShieldUpgradeCost:
                                playerShieldMax += 1
                                playerCredits -= maxShieldUpgradeCost
                                maxShieldUpgradeCount += 1
                            if shieldRegenUpgrade.collidepoint(mousePos) and shieldRegenUpgradeCount <= shieldRegenUpgradeMax and playerCredits >= shieldRegenUpgradeCost:
                                playerShieldRegenThresh -= 20
                                playerCredits -= shieldRegenUpgradeCost
                                shieldRegenUpgradeCount += 1
                            if laserUpgrade.collidepoint(mousePos) and laserUpgradeCount <= laserUpgradeMax and playerCredits >= laserUpgradeCost:
                                playerLaserWidth += 1
                                playerLaserReload -= 75
                                playerLaserDuration += 20
                                playerLaserCurrentDuration = playerLaserDuration
                                playerCredits -= laserUpgradeCost
                                laserUpgradeCount += 1
                                playerLaserOwned = True
                                                                
                    # handle keypress events
                    if event.type == KEYDOWN:
                        if event.key == ord('s'):
                            playerShopOpen = False
                        if event.key == K_ESCAPE or event.key == ord('q'):
                            terminate()
                
                # draw shop menu to screen    
                windowSurface.fill(BLACK)
                reloadUpgrade = pygame.Rect(buttonX, 1, 10, 10)
                cannonSizeUpgrade = pygame.Rect(buttonX, (reloadUpgrade.bottom + 5), 10, 10)
                maxShieldUpgrade = pygame.Rect(buttonX, (cannonSizeUpgrade.bottom + 5), 10, 10)
                shieldRegenUpgrade = pygame.Rect(buttonX, (maxShieldUpgrade.bottom + 5), 10, 10)
                laserUpgrade = pygame.Rect(buttonX, (shieldRegenUpgrade.bottom + 5), 10, 10)

                # display the players credits
                drawText('Credits: $%s' % playerCredits, font, windowSurface, (WINDOWWIDTH / 2), 1, GREEN)

                # list the upgrades and draw their corresponding buttons
                drawText('Reload speed: $%s %s/%s' % (reloadUpgradeCost, reloadUpgradeCount, reloadUpgradeMax), font, windowSurface, 1, 1, RED)
                pygame.draw.rect(windowSurface, YELLOW, reloadUpgrade)
                drawText('Cannon size: $%s %s/%s' % (cannonSizeUpgradeCost, cannonSizeUpgradeCount, cannonSizeUpgradeMax), font, windowSurface, 1, 16, RED)
                pygame.draw.rect(windowSurface, YELLOW, cannonSizeUpgrade)
                drawText('Max shield: $%s %s/%s' % (maxShieldUpgradeCost, maxShieldUpgradeCount, maxShieldUpgradeMax), font, windowSurface, 1, 31, LIGHTBLUE)
                pygame.draw.rect(windowSurface, YELLOW, maxShieldUpgrade)
                drawText('Shield regen: $%s %s/%s' % (shieldRegenUpgradeCost, shieldRegenUpgradeCount, shieldRegenUpgradeMax), font, windowSurface, 1, 46, LIGHTBLUE)
                pygame.draw.rect(windowSurface, YELLOW, shieldRegenUpgrade)
                drawText('Laser Cannon: $%s %s/%s' % (laserUpgradeCost, laserUpgradeCount, laserUpgradeMax), font, windowSurface, 1, 61, PURPLE)
                pygame.draw.rect(windowSurface, YELLOW, laserUpgrade)
                
                pygame.display.update()

            # back to main game loop

            # add computer ship if ship counter is 0 or less
            if addComputerShip <= 0:
                # add a computer ship to the top left of screen
                newComputer = {'rect':pygame.Rect(computerStartPositionX, computerStartPositionY, computerShipWidth, computerShipHeight),
                               'dir':RIGHT,
                               'speed':computerSpeed,
                               'reload':computerReload,
                               'surface':pygame.transform.scale(enemyImageFlipped, (computerSize, computerSize))}
                computerShips.append(newComputer)
                addComputerShip = addComputerIncrement

            # move the player
            if moveLeft and playerShip['rect'].left > 0:
                playerShip['rect'].left -= playerShip['speed']
                playerShield.left -= playerShip['speed']
            if moveRight and playerShip['rect'].right < WINDOWWIDTH:
                playerShip['rect'].right += playerShip['speed']
                playerShield.right += playerShip['speed']

            # regenerate players shield
            if playerShieldRegenRate >= playerShieldRegenThresh and playerShieldHealth < playerShieldMax:
                playerShieldHealth += 1
                playerShieldRegenRate = 0

            # add player bullets if spacebar is down
            if addPlayerBullets and currentReload <= 0:
                # fire bullets from left and right of ship
                playerBullets.append(pygame.Rect(playerShip['rect'].right,playerShip['rect'].top,playerBulletWidth,playerBulletHeight))
                playerBullets.append(pygame.Rect(playerShip['rect'].left,playerShip['rect'].top,playerBulletWidth,playerBulletHeight))
                # reset the reload counter
                currentReload = reload
                
            # fire laser if upgrade was purchased
            if playerLaserTry or playerLaserOn:
                if playerLaserOwned and playerLaserCurrentReload <= 0 and playerLaserCurrentDuration >= 0:
                    playerLaserOn = True
                    if playerLaserCurrentDuration <= 0:
                        playerLaserCurrentReload = playerLaserReload
                        playerLaserCurrentDuration = playerLaserDuration
                        playerLaserOn = False
                        
            # move the players bullets
            for bullets in playerBullets[:]:
                bullets.top -= playerBulletSpeed

            # check if player laser collided with enemy ships
            for ships in computerShips[:]:
                for lasers in playerLaserList[:]:    
                    if lasers.colliderect(ships['rect']) and bulletHit == False:
                        computerShips.remove(ships)
                        playerScore += ((wave - 1) * 25) + 75
                        playerCredits += ((wave - 1) * 25) + 75
                        bulletHit = True

            # move the computers bullets
            for bullets in computerBullets[:]:
                bullets['rect'].top += computerBulletSpeed

            # move the players lasers
            if playerLaserOn:
                for lasers in playerLaserList[:]:
                    lasers.left = playerShip['rect'].centerx

            # check if any computer ships have been hit by a player bullet
            for ships in computerShips[:]:
                for bullets in playerBullets[:]:
                    if ships['rect'].colliderect(bullets) and bulletHit == False:
                        playerBullets.remove(bullets)
                        computerShips.remove(ships)
                        playerScore += ((wave - 1) * 25) + 75
                        playerCredits += ((wave - 1) * 25) + 75
                        bulletHit = True

            # move the computer ships
            for ships in computerShips[:]:
                if ships['dir'] == RIGHT:
                    ships['rect'].right += ships['speed']
                if ships['dir'] == LEFT:
                    ships['rect'].left -= ships['speed']

            # have the computer ships fire bullets
            for ships in computerShips[:]:
                if ships['reload'] <= 0:
                    computerShipsCannonX = ships['rect'].left
                    computerShipsCannonY = ships['rect'].bottom
                    newComputerBullet = {'rect':pygame.Rect(computerShipsCannonX, (computerShipsCannonY - 2), computerBulletWidth, computerBulletHeight),
                                         'speed':computerBulletSpeed,
                                         'surface':pygame.transform.scale(enemyBulletImage, (((computerBulletWidth*2)+1),(computerBulletHeight*2)))}
                    computerBullets.append(newComputerBullet)
                    ships['reload'] = (computerReload + random.randint(-10, 20))

            # check if the computer ships are trying to move off screen
            for ships in computerShips[:]:
                if ships['rect'].right >= WINDOWWIDTH:
                    ships['rect'].top += (computerShipHeight + 2)
                    ships['dir'] = LEFT
                if ships['rect'].left <= 0:
                    ships['rect'].top += (computerShipHeight + 2)
                    ships['dir'] = RIGHT
            
            # check if the players shields have been hit by computer bullets
            for bullets in computerBullets[:]:
                if playerShield.colliderect(bullets['rect']):
                    if playerShieldHealth > 0:
                        if wave > 10 and playerShieldHealth > 1:
                            playerShieldHealth -= 1
                        if wave > 20 and playerShieldHealth > 2:
                            playerShieldHealth -= 1
                        computerBullets.remove(bullets)
                        playerShieldHealth -= 1

            # check if the players ship has been hit when the shields are down
            for bullets in computerBullets[:]:
                if playerShieldHealth <= 0:
                    if playerShip['rect'].colliderect(bullets['rect']):
                        computerBullets.remove(bullets)
                        playerAlive = False
                        gameLoop = 0
                        
            # check if computer or player bullets are off the screen
            for bullets in computerBullets[:]:
                if bullets['rect'].bottom > (WINDOWHEIGHT + computerBulletHeight):
                    computerBullets.remove(bullets)

            for bullets in playerBullets[:]:
                if bullets.top < -(playerBulletHeight):
                    playerBullets.remove(bullets)
           
            # draw the black background onto the surface
            windowSurface.fill(BLACK)
            windowSurface.blit(backgroundRect, (0,0))
            

            # draw the player ship and shield onto the surface
            #pygame.draw.rect(windowSurface, WHITE, playerShip['rect'])
            windowSurface.blit(playerShip['surface'], ((playerShip['rect'].left - (playerWidth / 2)), (playerShip['rect'].top - (playerHeight / 2))))
            if playerShieldHealth > 0:
                windowSurface.blit(shieldRect, ((playerShield.left - shieldSpaceTop +1), (playerShield.top - shieldSpaceTop)))
                #pygame.draw.circle(windowSurface, LIGHTBLUE, playerShip['rect'].center, int(shieldRadius), playerShieldHealth)
            
            # draw the players bullets onto the surface
            for bullets in playerBullets[:]:
                #pygame.draw.rect(windowSurface, GREEN, bullets)
                playerBulletRect = pygame.transform.scale(playerBulletImage, ((playerBulletHeight*2), (playerBulletHeight*2)))
                windowSurface.blit(playerBulletRect, (bullets.left, bullets.top))

            # draw the players laser onto the surface
            if playerLaserOn:
                playerLaser = pygame.Rect(playerShip['rect'].centerx,(playerShip['rect'].top - 5),playerLaserWidth,-10)
                playerLaserExtension = pygame.Rect(playerShip['rect'].centerx,(playerLaser.top-extensionValue),playerLaserWidth,-10)
                pygame.draw.rect(windowSurface, DEEPPURPLE, playerLaser)
                while playerLaserExtension.top > 0:
                    playerLaserExtension = pygame.Rect(playerShip['rect'].centerx,(playerLaser.top-extensionValue),playerLaserWidth,-10)
                    playerLaserList.append(playerLaserExtension)
                    extensionValue += 10
                
                for lasers in playerLaserList[:]:
                    pygame.draw.rect(windowSurface, PURPLE, lasers)

            if not playerLaserOn:
                extensionValue = 0
                for lasers in playerLaserList[:]:
                    playerLaserList.remove(lasers)
                    
            # draw the computers bullets onto the surface
            for bullets in computerBullets[:]:
                #pygame.draw.rect(windowSurface, RED, bullets['rect'])
                windowSurface.blit(bullets['surface'], (bullets['rect'].left, bullets['rect'].top))

            # draw the computer ships onto the surface
            for ships in computerShips[:]:
                #pygame.draw.rect(windowSurface, GREEN, ships['rect'])
                windowSurface.blit(ships['surface'], ((ships['rect'].left - 4), (ships['rect'].top - 2)))

            # draw the dashboard onto the surface
            pygame.draw.rect(windowSurface, GREY, dashBoard)

            # draw the players shield display onto the surface
            shieldDisplay = pygame.Rect(5, (WINDOWHEIGHT - 20), (playerShieldHealth * 25), 10)
            shieldRegenDisplay = pygame.Rect(shieldDisplay.right, (WINDOWHEIGHT - 20), (playerShieldRegenRate / 8), 10)
            shieldRegenFiller = pygame.Rect(shieldDisplay.right, (WINDOWHEIGHT - 20), (playerShieldRegenThresh / 8), 10)
            pygame.draw.rect(windowSurface, LIGHTBLUE, shieldDisplay)
            pygame.draw.rect(windowSurface, DARKGREY, shieldRegenFiller)
            pygame.draw.rect(windowSurface, YELLOW, shieldRegenDisplay)
            drawText('Shields - Regen', smallFont, windowSurface, shieldDisplay.left, (shieldDisplay.top - 20), BLUE)

            # draw the players reload onto the surface
            reloadDisplay = pygame.Rect((WINDOWWIDTH - 40), (WINDOWHEIGHT - 20), currentReload, 10)
            reloadFiller = pygame.Rect((WINDOWWIDTH - 40), (WINDOWHEIGHT - 20), reload, 10)
            pygame.draw.rect(windowSurface, DARKGREY, reloadFiller)
            pygame.draw.rect(windowSurface, RED, reloadDisplay)
            drawText('Reload', smallFont, windowSurface, reloadDisplay.left, (reloadDisplay.top - 20), RED)

            # draw the players score onto the surface
            drawText('Score: %s' % playerScore, font, windowSurface, 1, 1, RED)

            # draw the wave onto the surface
            drawText('Wave: %s' % wave, font, windowSurface, 1, 15, YELLOW)

            # draw the players credits onto the surface
            drawText('Credits: $%s' % playerCredits, font, windowSurface, 1, 31, GREEN)
            
            # decrement the players reload time
            if currentReload > 0:
                currentReload -= 1
            # if the laser is firing, lower its current duration
            if playerLaserOn:
                playerLaserCurrentDuration -= 1
            if not playerLaserOn and playerLaserCurrentReload > 0 and playerLaserOwned:
                playerLaserCurrentReload -= 1
                
            # decrement all computer ships reload times
            for ships in computerShips[:]:
                if ships['reload'] > 0:
                    ships['reload'] -= 1

            # reduce the time between computer spawns after a period of time
            if spawnRate <= 0:

                wave += 1
                 
                if addComputerIncrement > 30:
                    addComputerIncrement -= 7 # increase the rate at which computer ships are spawned
                if computerReload > 20: # increase the rate at which computer ships fire
                    computerReload -= 1
                if bulletInflator <= 0: # increase the size of computer bullets
                    if computerBulletWidth < 8:
                        computerBulletWidth += 1
                        computerBulletHeight += 1
                        bulletInflator = 2

                if computerBulletWidth < 8:
                    bulletInflator -= 1
               
                spawnRate = 2000 # reset the spawn rate cycle timer
            
            # decrement the computer ship, shield regen and spawn rate counters
            addComputerShip -= random.randint(1, 2) # add a random element to computer ship spawn, potentialy doubling the rate
            spawnRate -= 1
            if playerShieldHealth < playerShieldMax:
                if playerShieldRegenRate <= playerShieldRegenThresh:
                    playerShieldRegenRate += 1
                
            # draw the window onto the screen
            pygame.display.update()
            mainClock.tick(40)

        # handle the player's death
        windowSurface.fill(BLACK)
        drawText('You have died . . . press SPACE to continue', font, windowSurface, ((WINDOWWIDTH / 4) - 20), (WINDOWHEIGHT / 2), GREEN)
        drawText('Your score was: %s' % playerScore, font, windowSurface,(WINDOWWIDTH / 4), ((WINDOWHEIGHT / 2) + 20), GREEN)
        pygame.display.update()
        waitForPlayerToPressKey()
        
