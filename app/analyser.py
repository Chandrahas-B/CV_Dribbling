from ultralytics import YOLO
import mediapipe as mp
import cv2

class BasketballAnalysis:
    def __init__(self, args):
        self.model = YOLO(args.model_dir)
        self.mp_hands = mp.solutions.hands.Hands(
            static_image_mode=False, model_complexity=1,
            min_detection_confidence=0.75, min_tracking_confidence=0.75, max_num_hands=2
        )
        self.cap = cv2.VideoCapture(args.source)
        self.WIDTH = int(self.cap.get(3))
        self.HEIGHT = int(self.cap.get(4))
        self.FRAMES = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.play = args.play
                
        self.save_vid = args.save_vid
        if args.save_vid == 'Y':
            self.video = cv2.VideoWriter('outputs/video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.FRAMES , (self.WIDTH,self.HEIGHT))
        
        self.nearHand = True
        self.d = {'Up': 0, 'Down': 0, 'Dribbles': 0, "LeftDribble": 0, "RightDribble": 0, "CrossDribble": 0}
        self.other_hand = None
        self.prev_hand = None

    def statistics(self, frame):
        frame = cv2.rectangle(frame, (0, 0), (self.WIDTH, 100), (0, 0, 0), -1)
        frame = cv2.putText(frame, f"Upward movement: {self.d['Up']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, f"Downward movement: {self.d['Down']}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, f"Dribbles: {self.d['Dribbles']}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        frame = cv2.rectangle(frame, (0, self.HEIGHT - 150), (self.WIDTH, self.HEIGHT), (0, 0, 0), -1)
        frame = cv2.putText(frame, f"Left Dribbles: {self.d['LeftDribble']}", (10, self.HEIGHT - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, f"Right Dribbles: {self.d['RightDribble']}", (10, self.HEIGHT - 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        frame = cv2.putText(frame, f"Cross Dribbles: {self.d['CrossDribble']}", (10, self.HEIGHT - 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return frame

    def process_frame(self, bboxes):
        for box in bboxes:
            x1, y1, x2, y2 = (int(x) for x in box.xyxy[0])  
            cy =  (y2 - y1)//2 + y1
            cls = int(box.cls)
                      
            if cls == 0:
                self.knee_height = 2*(y2 - y1)//3 + y1
                        
            if self.knee_height - 20 < cy < self.knee_height + 20:
                if self.nearHand:
                    self.d['Down'] += 1
                    if self.other_hand == 'Left':
                        if self.prev_hand == self.other_hand:
                            self.d['RightDribble'] += 1
                        else:
                            self.d['CrossDribble'] += 1
                        self.prev_hand = 'Left'
                                
                    elif self.other_hand == 'Right':
                        if self.prev_hand == self.other_hand:
                            self.d['LeftDribble'] += 1
                        else:
                            self.d['CrossDribble'] += 1
                        self.prev_hand = 'Right'
                    self.nearHand = False
                    self.d['Dribbles'] += 1
                else:
                    self.d['Up'] += 1
                    self.nearHand = True
    
    def hand_landmarks(self, frame):
        hand_results = self.mp_hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if hand_results.multi_hand_landmarks is not None:
            if len(hand_results.multi_hand_landmarks) == 1 and self.nearHand:
                self.other_hand = hand_results.multi_handedness[0].classification[0].label
        

    def run_analysis(self):
        
        while self.cap.isOpened():
            success, frame = self.cap.read()

            if success:
                self.obj_detection = self.model(frame, verbose=False)

                self.hand_landmarks(frame)
                
                for result in self.obj_detection:
                    bboxes = result.boxes
                    self.process_frame(bboxes)

                frame = self.statistics(frame)
                
                if self.play == 'Y':
                    cv2.imshow("Frame", frame)
                
                if self.save_vid == 'Y':
                    self.video.write(frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        self.cap.release()
        self.mp_hands.close()
        if self.save_vid == 'Y':
            self.video.release()
        
        cv2.destroyAllWindows()

        print(self.d)