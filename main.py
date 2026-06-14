import pygame
import threading
import pygame.image
import threading
from datetime import datetime as Date
import cv2
import re
import os

cv2.CAP_PROP_BUFFERSIZE = 1

FrameRate = 50

CameraNum = 0
Camera = cv2.VideoCapture(CameraNum)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

pygame.init()

ProjectPath = "/storage/emulated/0/Projects/Assets"

Shutter = pygame.mixer.Sound(os.path.join(ProjectPath, "Shutter1.mp3"))
Image = pygame.image.load(os.path.join(ProjectPath, "Flip.png"))
Image = pygame.transform.scale(Image, (200, 200))

ScreenSize = screen.get_size()

IsInFlicker = False
Color = False
CoveredYStart = 0
CoveredYSize = 100
LastFrame = None

while True:
	FlipPos = (100, int(ScreenSize[1] * 0.86))
	Continue = False
		
	HoldingMouse = not not pygame.mouse.get_pressed()[0]
		
	if HoldingMouse:
		MousePos = pygame.mouse.get_pos()
			
		if (MousePos[0] >= FlipPos[0] and MousePos[1] >= FlipPos[1] and MousePos[0] <= FlipPos[0] + 200 and MousePos[1] <= FlipPos[1] + 200):
			if HoldingMouse != IsInFlicker:
				CameraNum = CameraNum == 1 and 0 or 1
				# pydroid freezes when I make another video captuere, this part of code is useless.
				#
			Continue = True
		elif HoldingMouse != IsInFlicker:
			FilePath = os.path.join(ProjectPath, f'IMG{re.sub(r'[ .:-]', '', str(Date.now()))}.jpg')
			
			cv2.imwrite(FilePath, LastFrame)
			os.system(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{FilePath}')
		
	IsInFlicker = HoldingMouse
	Color = (IsInFlicker and not Color) or False
	
	screen.fill("black")
	
	if Color:
		if not Continue:
			threading.Thread(target=Shutter.play).start()
			pygame.draw.rect(screen, (255, 255, 255), (0, CoveredYStart, ScreenSize[0], CoveredYSize))
	else:
		if not Continue:
			Ret, Frame = Camera.read()
		
			if Ret:
				LastFrame = Frame
					
				Cv2Image = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
				Cv2Image = cv2.transpose(Cv2Image)
				Cv2Image = cv2.rotate(Cv2Image, cv2.ROTATE_90_CLOCKWISE)
				Cv2Image = cv2.flip(Cv2Image, 1)
					
				Height, Width, _ = Cv2Image.shape
				Frame = pygame.image.frombuffer(Cv2Image.tobytes(), (Width, Height), "RGB")
					
				CoveredYSize = int(ScreenSize[0] * (Height / Width))
				CoveredYStart = int((ScreenSize[1] / 2) - (CoveredYSize / 2))
				
				Frame = pygame.transform.scale(Frame, (
					ScreenSize[0],
					CoveredYSize
				))
			
				screen.blit(Frame, (0, CoveredYStart))
		
	screen.blit(Image, FlipPos)	
	pygame.draw.circle(screen, (200, 200, 200), (int(ScreenSize[0] / 2), int(ScreenSize[1] * 0.9)), 100)
	
	clock.tick(FrameRate)
	pygame.display.flip()
