#!/usr/bin/env python2
#-*- coding: utf-8 -*-

from random import randrange as rand
import pygame, sys

import threading
import time

from openni import openni2, nite2, utils

#Frames que quero pegar
frames = 7

#variavel de movimento
StatusMovimentoPlayer1 = '0'
StatusMovimentoPlayer2 = '0'

#variaveis para ver o movimento
player1HandRightx = []
player1HandRighty = []
player1HandLeftx = []
player1HandLefty = []

player2HandRightx = []
player2HandRighty = []
player2HandLefty = []
player2HandLeftx = []

# The configuration
cell_size =	18
cols =		10
rows =		22
maxfps = 	30

colors = [
(0,   0,   0  ),
(255, 85,  85),
(100, 200, 115),
(120, 108, 245),
(255, 140, 50 ),
(50,  120, 52 ),
(146, 202, 73 ),
(150, 161, 218 ),
(35,  35,  35) # Helper color for background grid
]

# Define the shapes of the single parts
tetris_shapes = [
	[[1, 1, 1],
	 [0, 1, 0]],
	
	[[0, 2, 2],
	 [2, 2, 0]],
	
	[[3, 3, 0],
	 [0, 3, 3]],
	
	[[4, 0, 0],
	 [4, 4, 4]],
	
	[[0, 0, 5],
	 [5, 5, 5]],
	
	[[6, 6, 6, 6]],
	
	[[7, 7],
	 [7, 7]]
]

def rotate_clockwise(shape):
	return [ [ shape[y][x]
			for y in xrange(len(shape)) ]
		for x in xrange(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
	off_x, off_y = offset
	for cy, row in enumerate(shape):
		for cx, cell in enumerate(row):
			try:
				if cell and board[ cy + off_y ][ cx + off_x ]:
					return True
			except IndexError:
				return True
	return False

def remove_row(board, row):
	del board[row]
	return [[0 for i in xrange(cols)]] + board
	
def join_matrixes(mat1, mat2, mat2_off):
	off_x, off_y = mat2_off
	for cy, row in enumerate(mat2):
		for cx, val in enumerate(row):
			mat1[cy+off_y-1	][cx+off_x] += val
	return mat1

def new_board():
	board = [ [ 0 for x in xrange(cols) ]
			for y in xrange(rows) ]
	board += [[ 1 for x in xrange(cols)]]
	return board

# Função para verificar os movimentos---------------------------------------------------------------------------------------------------------------------------------------------
def verificarMovimentos():
	global player1HandRightx
	global player1HandRighty
	global player1HandLeftx 
	global player1HandLefty
	global frames
	
	global player2HandRightx
	global player2HandRighty
	global player2HandLefty
	global player2HandLeftx
	
	global StatusMovimentoPlayer1
	global StatusMovimentoPlayer2
	
	#controladores
	#parado = 0
	contRxD = 0
	contRxE = 0
	
	contRyD = 0
	contRyE = 0
	
	verifica = (frames * 0.7)
	while True:
		if len(player1HandRightx) == frames:
			x = 1
			while x < frames:
				if player1HandRightx[x] < player1HandRightx[x-1]:
					contRxD += 1	
				if player1HandRightx[x] > player1HandRightx[x-1]:
					contRxE += 1
				x+=1
			
			verifica2 = player1HandRightx[len(player1HandRightx)-1] - player1HandRightx[0] 
			
			player1HandRightx=[]
			
			if verifica2<0:
				verifica2 = verifica2 * -1
			#print verifica2
			if contRxD > verifica and verifica2 > 10 :
				#print "direita"
				StatusMovimentoPlayer1 = '1'
			elif contRxE > verifica and verifica2 > 10 :
				#print "esquerda"
				StatusMovimentoPlayer1 = '2'
			else:
				#print "parado"
				StatusMovimentoPlayer1 = '0'
			contRxC=0
			contRxB=0
			
		if len(player2HandRighty) == frames:
			y = 1
			while y < frames:
				if player2HandRighty[y] > player2HandRighty[y-1]:
					contRyC += 1	
				if player2HandRighty[y] > player2HandRighty[y-1]:
					contRyB += 1
				y+=1
				
			verUltimo	= player2HandRighty[len(player2HandRighty)-1] * -1
			VerPrimeiro	= player2HandRighty[0]  * -1
			
			#print 'primeiro ' + str(VerPrimeiro)
			#print 'ultimo ' + str(verUltimo)
			
			verifica3 = 1 
			
			player2HandRighty=[]	
				
			if verifica3<0:
				verifica3 = verifica3 * -1
			print verifica2
			if contRyD > verifica and verifica3 > 10 :
				print "cima"
				StatusMovimentoPlayer2 = '4'
			elif contRyE > verifica and verifica3 > 10 :
				print "Baixo"
				StatusMovimentoPlayer2 = '3'
			else:
				print "parado"
				StatusMovimentoPlayer2 = '0'
			contRyD=0
			contRyE=0	
				
				
				
				
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Função para pegar os movimentos--------------------------------------------------------------------------------------------------------------------------------------------------
def preenchermovimento(ident, joints):
	global player1HandRightx
	global player1HandRighty
	global player1HandLeftx 
	global player1HandLefty 
	
	global player2HandRightx
	global player2HandRighty
	global player2HandLefty 
	global player2HandLeftx

	leftHand = joints[nite2.JointType.NITE_JOINT_LEFT_HAND]
	rightHand = joints[nite2.JointType.NITE_JOINT_RIGHT_HAND]
	
	print 'leo '+ str(ident)
	print leftHand
	print rightHand
	
	
def pegarMovimentos():
	global player1HandRightx
	global player1HandRighty
	global player1HandLeftx 
	global player1HandLefty 
	
	global player2HandRightx
	global player2HandRighty
	global player2HandLefty 
	global player2HandLeftx
	
	global joints
	
	#openni2.initialize("/home/leonardo/Downloads/OpenNI-Linux-x64-2.2/Redist")
	openni2.initialize("/home/leonardo/Tcc/OpenNI-Linux-x64-2.2/Redist")
	#nite2.initialize("/home/leonardo/Downloads/NiTE-Linux-x64-2.2/Redist")
	nite2.initialize("/home/leonardo/Tcc/NiTE-2.0.0/Redist")
	
	dev = openni2.Device.open_any()
	device_info = dev.get_device_info()
	try:
		userTracker = nite2.UserTracker(dev)
	except utils.NiteError as ne:
		print "entrou em exept"
		print("Unable to start the NiTE human tracker. Check the error messages in the console. Model data (s.dat, h.dat...) might be inaccessible.")
		print(ne)
		sys.exit(-1)
		print "antes do while"
	
	while True:
		frame = userTracker.read_frame()
		depth_frame = frame.get_depth_frame()
			
		if frame.users:
			#i=0
			for user in frame.users:
				#i+=1
				#user.id = i
				print( "Skeleton state: " + str(user.skeleton.state))
				#print 'leo' + str(user.id) 
				if user.is_new():
					print("New human detected! ID: %d Calibrating...", user.id)
					userTracker.start_skeleton_tracking(user.id)
				#elif user.skeleton.state == nite2.SkeletonState.NITE_SKELETON_TRACKED:                           	
				else:
					print user.skeleton.joints
					print user.id
					#print str(user.is_visible())
					preenchermovimento(user.id, user.skeleton.joints)
		else:
			print("No users")
	
	nite2.unload()
	openni2.unload()
		
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Classe thread para pegar os movimentos--------------------------------------------------------------------------------------------------------------------------------------------

class ThreadPegarMovimento (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		pegarMovimentos()

class ThreadVerificarMovimentos (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		verificarMovimentos()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class TetrisApp(object):
	def __init__(self):
		global StatusMovimentoPlayer1
		pygame.init()
		pygame.key.set_repeat(250,25)
		self.width = cell_size*(cols+6)
		self.height = cell_size*rows
		self.rlim = cell_size*cols
		self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in xrange(cols)] for y in xrange(rows)]
		
		self.default_font =  pygame.font.Font(
			pygame.font.get_default_font(), 12)
		
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.event.set_blocked(pygame.MOUSEMOTION) # Bloquear o mouse

		self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
		self.init_game()
	
	def new_stone(self):
		self.stone = self.next_stone[:]
		self.next_stone = tetris_shapes[rand(len(tetris_shapes))]
		self.stone_x = int(cols / 2 - len(self.stone[0])/2)
		self.stone_y = 0
		
		if check_collision(self.board,
		                   self.stone,
		                   (self.stone_x, self.stone_y)):
			self.gameover = True
	
	def init_game(self):
		self.board = new_board()
		self.new_stone()
		self.level = 1
		self.score = 0
		self.lines = 0
		pygame.time.set_timer(pygame.USEREVENT+1, 1000)
	
	def disp_msg(self, msg, topleft):
		x,y = topleft
		for line in msg.splitlines():
			self.screen.blit(
				self.default_font.render(
					line,
					False,
					(255,255,255),
					(0,0,0)),
				(x,y))
			y+=14
	
	def center_msg(self, msg):
		for i, line in enumerate(msg.splitlines()):
			msg_image =  self.default_font.render(line, False,
				(255,255,255), (0,0,0))
		
			msgim_center_x, msgim_center_y = msg_image.get_size()
			msgim_center_x //= 2
			msgim_center_y //= 2
		
			self.screen.blit(msg_image, (
			  self.width // 2-msgim_center_x,
			  self.height // 2-msgim_center_y+i*22))
	
	def draw_matrix(self, matrix, offset):
		off_x, off_y  = offset
		for y, row in enumerate(matrix):
			for x, val in enumerate(row):
				if val:
					pygame.draw.rect(
						self.screen,
						colors[val],
						pygame.Rect(
							(off_x+x) *
							  cell_size,
							(off_y+y) *
							  cell_size, 
							cell_size,
							cell_size),0)
	
	def add_cl_lines(self, n):
		linescores = [0, 40, 100, 300, 1200]
		self.lines += n
		self.score += linescores[n] * self.level
		if self.lines >= self.level*6:
			self.level += 1
			newdelay = 1000-50*(self.level-1)
			newdelay = 100 if newdelay < 100 else newdelay
			pygame.time.set_timer(pygame.USEREVENT+1, newdelay)
	
	def move(self, delta_x):
		if not self.gameover and not self.paused:
			new_x = self.stone_x + delta_x
			if new_x < 0:
				new_x = 0
			if new_x > cols - len(self.stone[0]):
				new_x = cols - len(self.stone[0])
			if not check_collision(self.board,
			                       self.stone,
			                       (new_x, self.stone_y)):
				self.stone_x = new_x
	def quit(self):
		self.center_msg("Exiting...")
		pygame.display.update()
		sys.exit()
	
	def drop(self, manual):
		if not self.gameover and not self.paused:
			self.score += 1 if manual else 0
			self.stone_y += 1
			if check_collision(self.board,
			                   self.stone,
			                   (self.stone_x, self.stone_y)):
				self.board = join_matrixes(
				  self.board,
				  self.stone,
				  (self.stone_x, self.stone_y))
				self.new_stone()
				cleared_rows = 0
				while True:
					for i, row in enumerate(self.board[:-1]):
						if 0 not in row:
							self.board = remove_row(
							  self.board, i)
							cleared_rows += 1
							break
					else:
						break
				self.add_cl_lines(cleared_rows)
				return True
		return False
	
	def insta_drop(self):
		if not self.gameover and not self.paused:
			while(not self.drop(True)):
				pass
	
	def rotate_stone(self):
		if not self.gameover and not self.paused:
			new_stone = rotate_clockwise(self.stone)
			if not check_collision(self.board,
			                       new_stone,
			                       (self.stone_x, self.stone_y)):
				self.stone = new_stone
	
	def toggle_pause(self):
		self.paused = not self.paused
	
	def start_game(self):
		if self.gameover:
			self.init_game()
			self.gameover = False
	
	def run(self):
		key_actions = {
			'ESCAPE':	self.quit,
			'2':	lambda:self.move(-1),
			'1':	lambda:self.move(+1),
			'3':		lambda:self.drop(True),
			'4':		self.rotate_stone,
			'p':		self.toggle_pause,
			'SPACE':	self.start_game,
			'RETURN':	self.insta_drop
		}
		
		self.gameover = False
		self.paused = False
		
		dont_burn_my_cpu = pygame.time.Clock()
		while 1:
			self.screen.fill((0,0,0))
			if self.gameover:
				self.center_msg("""Game Over!\nYour score: %d
Press space to continue""" % self.score)
			else:
				if self.paused:
					self.center_msg("Paused")
				else:
					pygame.draw.line(self.screen,
						(255,255,255),
						(self.rlim+1, 0),
						(self.rlim+1, self.height-1))
					self.disp_msg("Next:", (
						self.rlim+cell_size,
						2))
					self.disp_msg("Score: %d\n\nLevel: %d\
\nLines: %d" % (self.score, self.level, self.lines),
						(self.rlim+cell_size, cell_size*5))
					self.draw_matrix(self.bground_grid, (0,0))
					self.draw_matrix(self.board, (0,0))
					self.draw_matrix(self.stone,
						(self.stone_x, self.stone_y))
					self.draw_matrix(self.next_stone,
						(cols+1,2))
			pygame.display.update()
			for event in pygame.event.get():
				print StatusMovimentoPlayer2
				if event.type == pygame.USEREVENT+1:
					self.drop(False)
				if event.type == pygame.QUIT:
					self.quit()
				if StatusMovimentoPlayer1 != '0':
					#print 'entrou no else'
					key_actions[StatusMovimentoPlayer1]()
				if StatusMovimentoPlayer2 != '0':
					print 'entrou no else'
					key_actions[StatusMovimentoPlayer2]()
					
			dont_burn_my_cpu.tick(maxfps)

if __name__ == '__main__':
	
	App = TetrisApp()
	thread1 = ThreadPegarMovimento()
	thread2 = ThreadVerificarMovimentos()
	print "Iniciou Thread"
	thread1.start()
	thread2.start()
	print "comecou Jogo"
	App.run()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	