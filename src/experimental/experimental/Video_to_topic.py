import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node

def nothing(x):
    pass

class VideoPublisher(Node):
    def __init__(self):
        super().__init__('video_publisher_node')
        self.publisher_ = self.create_publisher(Image, '/camera', 10)
        self.bridge = CvBridge()
        
        self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/autonomous_main_1.mp4') 
        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/autonomous_top2.mp4') 
        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/autonomous_marine_growth.mp4') 
        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/autonomous_main_2.mp4') 
        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/autonomous_shackle.mp4') 
        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/autonomous_seafloor.mp4') 

        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/autonomous_TBS.mp4') 
        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/blender2.mp4') 

        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/m1_AKER_BP.mp4') 

        # self.cap = cv2.VideoCapture('/home/nikolai/Sintef_bouy_22_03_24/Old_inspection5.mp4') 


        if not self.cap.isOpened():
            self.get_logger().error('Unable to open video file.')
            exit()

        self.desired_fps = 30.0
        self.width = 1920
        self.height = 1080

        self.timer = self.create_timer(1.0 / self.desired_fps, self.timer_callback)

        # Initialize OpenCV window and trackbar
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video', 1000, 700)

        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cv2.createTrackbar('Seek', 'Video', 0, self.total_frames, nothing)
        
        self.last_trackbar_val = 0  # Keep track of the last trackbar value to detect changes

    def timer_callback(self):
        # Check if the trackbar position has changed (i.e., the user has sought to a new position)
        trackbar_val = cv2.getTrackbarPos('Seek', 'Video')
        if trackbar_val != self.last_trackbar_val:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, trackbar_val)
            self.last_trackbar_val = trackbar_val
        
        ret, frame = self.cap.read()
        if ret:
            # Update the trackbar position based on the current video frame
            cv2.setTrackbarPos('Seek', 'Video', int(self.cap.get(cv2.CAP_PROP_POS_FRAMES)))
            
            resized_frame = cv2.resize(frame, (self.width, self.height))
            cv2.imshow('Video', resized_frame)
            msg = self.bridge.cv2_to_imgmsg(resized_frame, 'bgr8')
            self.publisher_.publish(msg)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                rclpy.shutdown()
        else:
            self.get_logger().info('Video has ended, looping.')
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

def main(args=None):
    rclpy.init(args=args)
    video_publisher = VideoPublisher()
    rclpy.spin(video_publisher)
    video_publisher.cap.release()
    cv2.destroyAllWindows()
    video_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()