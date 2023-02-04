import cv2
import mediapipe as mp

class Hand():
    def __init__(self, mode = False):
        self.mode = mode
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findHand(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        
        return img
    
    def checkLRC(self, img):
        h, w, _ = img.shape
        LRC = []
        h_center = h / 2
        w_center = w / 2
        
        if self.results.multi_hand_landmarks:
            for i in self.results.multi_hand_landmarks:
                if (i.landmark[8].x * w) < (w_center - 100):
                    LRC.append('L')
                elif (i.landmark[8].x * w) > (w_center + 100):
                    LRC.append('R')
                else:
                    LRC.append('C')
            return LRC[-1]

    def checkJSD(self, img):
        h, w, _ = img.shape
        h_center = h / 2
        w_center = w / 2
        JDS = []
        if self.results.multi_hand_landmarks:

            for i in self.results.multi_hand_landmarks:
                if (i.landmark[8].y * h) < (w_center - 100):
                    JDS.append('J')
                elif (i.landmark[8].y * h) > (w_center + 100):
                    JDS.append('D')
                else:
                    JDS.append('S')
            return JDS[-1]