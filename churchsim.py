#import libraries
import pygame as pg
import enum
#initialise pygame
pg.init()

#game window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

#create game window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Churchsim')

#set frame rate
clock = pg.time.Clock()
FPS = 60

#game variables
GRAVITY = 1

#foot movement
FOOTMOVEMENTS = 4

#define sprite size of each frame
SPRITESIZE	= 200 

#define number of character types
NUMBEROFCHARTYPES = 5

#define colours
WHITE = (255, 255, 255)

#load images
bg_image = pg.image.load('assets/background.png').convert_alpha()



CHARACTERCHOICEBACKGROUND = pg.image.load('assets/charBackground.png').convert_alpha()
SPRITE = ['assets/FChristian.png','assets/Fpuritan.png','assets/MChristian.png','assets/Mpope.png', 'assets/eli.png']
CHARNAMES = ['assets/characternames/FChristianSign.png','assets/characternames/FPuritanSign.png.png','assets/characternames/MChristianSign.png','assets/characternames/MPopeSign.png','assets/characternames/Eli.png']

#the enum array is structured like so:
	#stand
	#walk 1(x?,y?) 2(x?,y?)
	#... to be continued
class Item(enum.Enum):
    none = [[0,1000],[0,400,200,400]]
    staff = [[200,1000],[400,400,600,400]]
    goblet = [[400,1000],[0,600,200,600]]
    pitchFork = [[600,1000],[400,600,600,600]]

class CharScreen():
	def __init__(self):
		self.charChosen = False #ill use this later for character choosing
		self.count = 0 #counts the passes
		self.charScreen = CHARACTERCHOICEBACKGROUND
		self.charImage = (pg.image.load(SPRITE[self.count]).convert_alpha()).subsurface((Item.none.value[0][0],Item.none.value[0][1],SPRITESIZE,SPRITESIZE))#yes its a fucking messyy, this crops the sprite sheet
		self.charName = (pg.image.load(CHARNAMES[self.count]))
		#time interval wait didnt work
		self.interval = 200
		self.lastGameTime = 0
		self.walkAnimationCount = 0
		self.item = Item.staff
		self.chosenImage = pg.image.load(SPRITE[0]).convert_alpha() #this helps switch up the images
		self.left = False #helps with walking

		"""
		if self.count >= FPS//FOOTMOVEMENTS:
					self.count = 0
					self.left = not self.left #negates value
		"""

	def walkAmation(self): #makes a walk cycle depending on the file and item #I want enum value maybe
		#probably can do this with the game clock
		array = [Item.none, Item.staff, Item.goblet, Item.pitchFork]
		count = 0
		if self.walkAnimationCount >= FPS//FOOTMOVEMENTS:
			self.walkAnimationCount = 0
			self.left = not self.left #negates value
		if ((pg.time.get_ticks())%1) == 0: #enum not working--------------------------------------------------------------------!
			#print("here")
			self.item = array[count%3]
			count += 1
			
		if(self.left == False):
			self.charImage = pg.image.load(SPRITE[self.count]).convert_alpha().subsurface((self.item.value[1][0],self.item.value[1][1],SPRITESIZE,SPRITESIZE))
		else:
			self.charImage = pg.image.load(SPRITE[self.count]).convert_alpha().subsurface((self.item.value[1][2],self.item.value[1][3],SPRITESIZE,SPRITESIZE))
	#choose characters
	def changeChars(self):#too fast atm
		charScreen.walkAmation()
		self.walkAnimationCount += 1
		key = pg.key.get_pressed()
		if key[pg.K_d] and (pg.time.get_ticks() > self.lastGameTime + self.interval):
			self.count += 1
			self.lastGameTime = pg.time.get_ticks()
			if self.count >= NUMBEROFCHARTYPES:
				self.count = 0
			self.charImage = (pg.image.load(SPRITE[self.count]).convert_alpha()).subsurface((Item.none.value[0][0],Item.none.value[0][1],SPRITESIZE,SPRITESIZE))#another mess :D
			self.charName = (pg.image.load(CHARNAMES[self.count]))
		if key[pg.K_y]:
			self.charChosen = True

	def draw(self):
		screen.blit(CHARACTERCHOICEBACKGROUND,(0,0))
		screen.blit(self.charName,(375,155))
		screen.blit(self.charImage,(400,226))
		

#player class
class Player():
	def __init__(self):
		self.item = Item.none
		self.chosenImage = pg.image.load(SPRITE[0]).convert_alpha()#this will have to change
		self.image = pg.image.load(SPRITE[0]).convert_alpha()#pygame.transform.scale(jumpy_image, (200,100))
		#self.width = 200
		#self.height = 200
		self.count = 0
		#self.rect = pg.Rect(0, 0, self.width, self.height)
		#self.rect.center = (x, y)
		self.flip = False
		self.left = False #helps set right or left leg in walk cycle
		
		#background moving
		self.backGroundX = -538
		self.backGroundY = -446
		
	def walkAmation(self): #makes a walk cycle depending on the file and item #I want enum value maybe
		#probably can do this with the game clock
		if self.count >= FPS//FOOTMOVEMENTS:
			self.count = 0
			self.left = not self.left #negates value
			
			
			
		if(self.left == False):
			self.image = pg.transform.flip(self.chosenImage.subsurface((self.item.value[1][0],self.item.value[1][1],SPRITESIZE,SPRITESIZE)), self.flip, False)
		else:
			self.image = pg.transform.flip(self.chosenImage.subsurface((self.item.value[1][2],self.item.value[1][3],SPRITESIZE,SPRITESIZE)), self.flip, False)
		
			
	def move(self):
		key = pg.key.get_pressed()
		#individual keys dont work... not sure why! probably how i structured the if statements
		if key[pg.K_a] or key[pg.K_d] or key[pg.K_s] or key[pg.K_w]:
			self.walkAmation()
			if key[pg.K_a]:
				self.backGroundX += 2
				self.flip = True
			if key[pg.K_d]:
				self.backGroundX -= 2
				self.flip = False
			if key[pg.K_s]:
				self.backGroundY -= 2
			if key[pg.K_w]:
				self.backGroundY += 2
		else:
			self.image = pg.transform.flip(self.chosenImage.subsurface((self.item.value[0][0],self.item.value[0][1],SPRITESIZE,SPRITESIZE)), self.flip, False)#this will have to change
		#update rectangle position
		#self.rect.x += dx
		#self.rect.y += dy

	def draw(self):
		#screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))#this is where ya wanna changethe picture
		self.count += 1 #this is for walk cycle i think????
		screen.blit(bg_image, (self.backGroundX, self.backGroundY))#need to resize obviously maybe make its own class later
		screen.blit(self.image,((SCREEN_WIDTH//2)-(SPRITESIZE/2),(SCREEN_HEIGHT//2)-(SPRITESIZE/2)))#character drawn
		#pygame.draw.rect(screen, WHITE, self.rect, 2)#to see the outline of hitbox

charScreen = CharScreen()
player = Player()

#jumpy.item.
#game loop
print()
print()
print()
print("Move around with awsd keys")
run = True
while run:

	clock.tick(FPS)
	if charScreen.charChosen:
		player.move()
		player.draw()
	else:
		charScreen.changeChars()
		if charScreen.charChosen:
			player.image = pg.image.load(SPRITE[charScreen.count]).convert_alpha()
			player.chosenImage = pg.image.load(SPRITE[charScreen.count]).convert_alpha()
		charScreen.draw()
		charScreen.changeChars()
		

	#event handler
	for event in pg.event.get():
		if event.type == pg.QUIT:
			run = False


	#update display window
	pg.display.update()



pg.quit()

"""
this was code that didnt work
		if key[pygame.K_d]:
			self.walkAmation()
			self.flip = False
		if key[pygame.K_w]:
			self.walkAmation()
		if key[pygame.K_s]:
			self.walkAmation()"""

