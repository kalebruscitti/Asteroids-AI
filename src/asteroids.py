#! /usr/bin/env python
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright (C) 2008  Nick Redshaw
#

# TODO
# safe area on new life
# sounds thump

# Notes:
# random.randrange returns an int
# random.uniform returns a float
# p for pause
# o for frame advance whilst paused

import pygame, sys, os, random
import numpy as np
from pygame.locals import *
from util.vectorsprites import *
from ship import *
from stage import *
from badies import *
from shooter import *
from soundManager import *
from ai import *


class Asteroids():

    explodingTtl = 180

    def __init__(self):
        self.stage = Stage('Pythentic Asteroids')
        self.paused = False
        self.frameAdvance = False
        self.gameState = "attract_mode"
        self.rockList = []
        self.createRocks(3)
        self.saucer = None
        self.secondsCount = 1
        self.score = 0
        self.ship = None
        self.lives = 0

    def initialiseGame(self):
        self.gameState = 'playing'
        [self.stage.removeSprite(sprite) for sprite in self.rockList] # clear old rocks
        if self.saucer is not None:
            self.killSaucer()
        self.startLives = 1
        self.createNewShip()
        self.createLivesList()
        self.score = 0
        self.rockList = []
        self.numRocks = 3
        self.nextLife = 10000

        self.createRocks(self.numRocks)
        self.secondsCount = 1

    def createNewShip(self):
        if self.ship:
            [self.stage.spriteList.remove(debris) for debris in self.ship.shipDebrisList]
        self.ship = Ship(self.stage)
        self.stage.addSprite(self.ship.thrustJet)
        self.stage.addSprite(self.ship)

    def createLivesList(self):
        self.lives += 1
        self.livesList = []
        for i in range(1, self.startLives):
            self.addLife(i)

    def addLife(self, lifeNumber):
        self.lives += 1
        ship = Ship(self.stage)
        self.stage.addSprite(ship)
        ship.position.x = self.stage.width - (lifeNumber * ship.boundingRect.width) - 10
        ship.position.y = 0 + ship.boundingRect.height
        self.livesList.append(ship)


    def createRocks(self, numRocks):
        for _ in range(0, numRocks):
            position = Vector2d(random.randrange(-10, 10), random.randrange(-10, 10))

            newRock = Rock(self.stage, position, Rock.largeRockType)
            self.stage.addSprite(newRock)
            self.rockList.append(newRock)


    def playGame(self):

        clock = pygame.time.Clock()

        frameCount = 0.0
        timePassed = 0.0
        self.fps = 0.0
        # Main loop
        self.running = True
        while self.running:

            # fps
            timePassed += clock.tick(600)
            frameCount += 1
            if frameCount % 10 == 0:
                self.fps = (frameCount / (timePassed / 1000.0))
                timePassed = 0
                frameCount = 0

            self.secondsCount += 1

            self.input(pygame.event.get())

            if self.paused and not self.frameAdvance:
                #self.displayPaused()
                continue

            self.stage.screen.fill((0, 0, 0))
            self.stage.moveSprites()
            self.stage.drawSprites()
            self.doSaucerLogic()
            self.displayScore()
            #self.displayFps()
            self.checkScore()

            # Process keys
            if self.gameState == 'playing':
                self.playing()
            elif self.gameState == 'exploding':
                self.exploding()
            else:
                self.displayText()
                self.initialiseGame()
            # Double buffer draw
            pygame.display.flip()


    def playing(self):
        if self.lives == 0:
            self.running = False
            self.gameState = 'attract_mode'
        else:
            self.interfaceWithAI()
            self.checkCollisions()
            if len(self.rockList) == 0:
                self.levelUp()

    def doSaucerLogic(self):
        if self.saucer is not None:
            if self.saucer.laps >= 2:
                self.killSaucer()

        # Create a saucer
        if self.secondsCount % 2000 == 0 and self.saucer is None:
            randVal = random.randrange(0,10)
            if randVal <= 3:
                self.saucer = Saucer(self.stage, Saucer.smallSaucerType, self.ship)
            else:
                self.saucer = Saucer(self.stage, Saucer.largeSaucerType, self.ship)
            self.stage.addSprite(self.saucer)


    def exploding(self):
        self.explodingCount += 1;
        if self.explodingCount > self.explodingTtl:
            self.gameState = 'playing'
            [self.stage.spriteList.remove(debris) for debris in self.ship.shipDebrisList]
            self.ship.shipDebrisList = []

            if self.lives == 0:
                self.ship.visible = False
            else:
                self.createNewShip()

    def levelUp(self):
        self.numRocks += 1
        self.createRocks(self.numRocks)

    # move this kack somewhere else!
    def displayText(self):
        font1 = pygame.font.Font(None, 50)
        titleText = font1.render('Pythentic Asteroids', True, (255, 255, 255))
        titleTextRect = titleText.get_rect(centerx=self.stage.width/2)
        titleTextRect.y = self.stage.height/2 - titleTextRect.height*2
        self.stage.screen.blit(titleText, titleTextRect)

        font2 = pygame.font.Font(None, 30)
        keysText = font2.render('Z left, X right, B fire, N thrust, H hyperspace, Esc to quit', True, (255, 255, 255))
        keysTextRect = keysText.get_rect(centerx=self.stage.width/2)
        keysTextRect.y = self.stage.height/2 - keysTextRect.height/2
        self.stage.screen.blit(keysText, keysTextRect)

        instructionText = font1.render('Press Enter To Play', True, (255, 255, 255))
        instructionTextRect = instructionText.get_rect(centerx=self.stage.width/2)
        instructionTextRect.y = self.stage.height/2 + instructionTextRect.height
        self.stage.screen.blit(instructionText, instructionTextRect)

    def sendScore(self):
        print("Sending Score")
        return self.score

    def displayScore(self):
        font2 = pygame.font.Font(None, 30)
        scoreStr = str("%06d" % self.score)
        scoreText = font2.render(scoreStr, True, (255, 255, 255))
        scoreTextRect = scoreText.get_rect(centerx=40, centery=15)
        self.stage.screen.blit(scoreText, scoreTextRect)

    def displayPaused(self):
        if self.paused:
            font2 = pygame.font.Font(None, 30)
            pausedText = font2.render("Paused", True, (255, 255, 255))
            textRect = pausedText.get_rect(centerx=self.stage.width/2, centery=self.stage.height/2)
            self.stage.screen.blit(pausedText, textRect)
            pygame.display.update()

    # Should move the ship controls into the ship class
    def input(self, events):
        self.frameAdvance = False
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                if self.gameState == 'attract_mode':
                    # Start a new game
                    if event.key == K_RETURN:
                        self.initialiseGame()

                if event.key == K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

                if event.key == K_f:
                    pygame.display.toggle_fullscreen()

                #if event.key == K_k:
                    #self.killShip()
            elif event.type == KEYUP:
               if event.key == K_o:
                   self.frameAdvance = True

    def interfaceWithAI(self):

        #generate information to allow the AI to "see" the screen
        self.baddie_array = np.empty([0,2])
        for rock in self.rockList:
            x = rock.position.x /self.stage.width
            y = rock.position.y /self.stage.height
            position = np.array([[x,y]])
            self.baddie_array = np.append(self.baddie_array, position, axis=0)
        #getting ship position
        self.ship_pos = np.array([self.ship.position.x /self.stage.width, self.ship.position.y /self.stage.height])

    	#Pretty self-explanatory; if the input index is true, do that action.
        input_array = AI.sendInput(self.baddie_array, self.ship.angle, self.ship_pos)
        if input_array[0]:
    		self.ship.increaseThrust()
    		self.ship.thrustJet.accelerating = True
        if not input_array[0]:
    	 	self.ship.thrustJet.accelerating = False
        if input_array[1]:
    		self.ship.rotateLeft()
        if input_array[2]:
    		self.ship.rotateRight()
        if input_array[3]:
    		self.ship.fireBullet()

        def sendScore(self):
            return self.score

    # Check for ship hitting the rocks etc.
    def checkCollisions(self):

        # Ship bullet hit rock?
        newRocks = []
        shipHit, saucerHit = False, False

        # Rocks
        for rock in self.rockList:
            rockHit = False

            if not self.ship.inHyperSpace and rock.collidesWith(self.ship):
                p = rock.checkPolygonCollision(self.ship)
                if p is not None:
                    shipHit = True
                    rockHit = True

            if self.saucer is not None:
                if rock.collidesWith(self.saucer):
                    saucerHit = True
                    rockHit = True

                if self.saucer.bulletCollision(rock):
                    rockHit = True

                if self.ship.bulletCollision(self.saucer):
                    saucerHit = True
                    self.score += self.saucer.scoreValue

            if self.ship.bulletCollision(rock):
                rockHit = True

            if rockHit:
                self.rockList.remove(rock)
                self.stage.spriteList.remove(rock)

                if rock.rockType == Rock.largeRockType:
                    playSound("explode1")
                    newRockType = Rock.mediumRockType
                    self.score += 50
                elif rock.rockType == Rock.mediumRockType:
                    playSound("explode2")
                    newRockType = Rock.smallRockType
                    self.score += 100
                else:
                    playSound("explode3")
                    self.score += 200

                if rock.rockType != Rock.smallRockType:
                    # new rocks
                    for _ in range(0,2):
                        position = Vector2d(rock.position.x, rock.position.y)
                        newRock = Rock(self.stage, position, newRockType)
                        self.stage.addSprite(newRock)
                        self.rockList.append(newRock)

                self.createDebris(rock)


        # Saucer bullets
        if self.saucer is not None:
            if not self.ship.inHyperSpace:
                if self.saucer.bulletCollision(self.ship):
                    shipHit = True

                if self.saucer.collidesWith(self.ship):
                    shipHit = True
                    saucerHit = True

            if saucerHit:
                self.createDebris(self.saucer)
                self.killSaucer()

        if shipHit:
            self.killShip()

            # comment in to pause on collision
            #self.paused = True

    def killShip(self):
        stopSound("thrust")
        playSound("explode2")
        self.explodingCount = 0
        self.lives -= 1
        if (self.livesList):
            ship = self.livesList.pop()
            self.stage.removeSprite(ship)

        self.stage.removeSprite(self.ship)
        self.stage.removeSprite(self.ship.thrustJet)
        self.gameState = 'exploding'
        self.ship.explode()

    def killSaucer(self):
        stopSound("lsaucer")
        stopSound("ssaucer")
        playSound("explode2")
        self.stage.removeSprite(self.saucer)
        self.saucer = None

    def createDebris(self, sprite):
        for _ in range(0, 25):
            position = Vector2d(sprite.position.x, sprite.position.y)
            debris = Debris(position, self.stage)
            self.stage.addSprite(debris)

    def displayFps(self):
        font2 = pygame.font.Font(None, 15)
        fpsStr = str(self.fps)
        scoreText = font2.render(fpsStr, True, (255, 255, 255))
        scoreTextRect = scoreText.get_rect(centerx=(self.stage.width/2), centery=15)
        self.stage.screen.blit(scoreText, scoreTextRect)

    def checkScore(self):
        if self.score > 0 and self.score > self.nextLife:
            playSound("extralife")
            self.nextLife += 10000
            self.addLife(self.lives)

## Script to run the game
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

initSoundManager()
AI = AI()
game = Asteroids()

####
