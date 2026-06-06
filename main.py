import pygame
import threading
import pygame.image
import threading
from datetime import datetime
import cv2

cv2.CAP_PROP_BUFFERSIZE = 1

CameraNum = 0
Capturer = cv2.VideoCapture(CameraNum)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

pygame.init()

IsInFlicker = False
Color = False

Image = pygame.image.load("/Flip.png")
Shutter = pygame.mixer.Sound("/Shutter1.mp3")

def PlayShutter():
	Shutter.play()

Image = pygame.transform.scale(Image, (200, 200))
ScreenSize = screen.get_size()

CoveredYStart = 0
CoveredYSize = 100
LastFrame = None

while True:
	def Frame():
		global IsInFlicker, Color, CameraNum, Capturer
		global CoveredYSize, CoveredYStart, LastFrame
		
		FlipPos = (100, int(ScreenSize[1] * 0.86))
		Continue = False
		
		HoldingMouse = not not pygame.mouse.get_pressed()[0]
		
		if HoldingMouse:
			MousePos = pygame.mouse.get_pos()
			
			if (MousePos[0] >= FlipPos[0] and MousePos[1] >= FlipPos[1] and MousePos[0] <= FlipPos[0] + 200 and MousePos[1] <= FlipPos[1] + 200):
				if HoldingMouse != IsInFlicker:
					CameraNum = CameraNum == 1 and 0 or 1
				
				#	Capturer.open(CameraNum)
				#	Capturer = cv2.VideoCapture(CameraNum)
			
				Continue = True
			elif HoldingMouse != IsInFlicker:
				print("cool")
				try:
					threading.Thread(target=cv2.imwrite, args=(f'/plssavwlala.jpg', LastFrame,)).start()
				#	threading.Thread(target=cv2.imwrite, args=(f'{datetime.now().isoformat(sep=' ', timespec='miliseconds')}.jpg', LastFrame,)).start()
				except:
					print("bruhh")
		
		IsInFlicker = HoldingMouse
		Color = (IsInFlicker and not Color) or False
	
		screen.fill("black")
	
		if Color:
			if not Continue:
				threading.Thread(target=PlayShutter).start()
				pygame.draw.rect(screen, (255, 255, 255), (0, CoveredYStart, ScreenSize[0], CoveredYSize))
		else:
			if Capturer.isOpened() and not Continue:
				Ret, Frame = Capturer.read()
		
				if Ret:
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
					LastFrame = Cv2Image
		
		screen.blit(Image, FlipPos)	
		pygame.draw.circle(screen, (200, 200, 200), (int(ScreenSize[0] / 2), int(ScreenSize[1] * 0.9)), 100)
	
	Frame()
	
	clock.tick(50)
	pygame.display.flip()
