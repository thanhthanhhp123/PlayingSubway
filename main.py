import cv2
from hand import Hand
import pyautogui as ui
import time

class Play():
	def __init__(self):
		self.hand = Hand()
		self.started = False
		self.x_position = 1
		self.y_postion = 1

	def moveLRC(self, LRC):
		if LRC == 'L':
			for i in range(1, self.x_position):
				ui.press('left')
			self.x_position = 0
		elif LRC == 'R':
			for i in range(2, self.x_position, -1):
				ui.press('right')
			self.x_position = 2
		else:
			if self.x_position == 0:
				ui.press('right')
			elif self.x_position == 2:
				ui.press('left')

			self.x_position = 1

	def moveJSD(self, JSD):
		if JSD == 'J' and self.y_postion == 1:
			ui.press('up')
			self.y_postion = 2
		elif JSD == 'D' and self.y_postion == 1:
			ui.press('down')
		elif JSD == 'S' and self.y_postion != 1:
			self.y_postion = 1

	def played(self):
		cap = cv2.VideoCapture(1)
		start = time.time()
		fc = 0
		display_time = 0.001
		fps = 0
		
		while True:
			success, img = cap.read()
			fc += 1
			if success:
				img = cv2.flip(img, 1)
				h, w, _ = img.shape
				h_center = int(h / 2)
				w_center = int(w / 2)
				img = self.hand.findHand(img)

				if self.hand.results.multi_hand_landmarks:
					if self.started:
						LRC = self.hand.checkLRC(img)
						self.moveLRC(LRC)

						JSD = self.hand.checkJSD(img)
						self.moveJSD(JSD)
					
					else:
						cv2.rectangle(img, (w_center - 100, h_center - 100), (w_center + 100, h_center + 100), (0, 200, 200), 2)
						cv2.putText(img, 'Put your hand on for starting', (w_center - 70, h_center - 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 100, 150))

				TIME = time.time() - start
				if TIME >= display_time:
					fps = fc / TIME
					fc= 0 
					start = time.time()
				fps_disp = 'FPS: ' + str(fps)[:5]
				cv2.putText(img, fps_disp, (100, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
				cv2.imshow('img', img)
			if cv2.waitKey(1) == ord('q'):
				break
		cap.release()
		cv2.destroyAllWindows()
play = Play()
play.played()