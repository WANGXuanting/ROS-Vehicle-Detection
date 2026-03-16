#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import CompressedImage
from ultralytics import YOLO

class VehicleDetector:
    def __init__(self):
        # 初始化 ROS 节点
        rospy.init_node('vehicle_detector_node', anonymous=True)
        
        rospy.loginfo("正在加载 YOLOv8 模型...")
        # 加载 YOLOv8 nano 模型 (第一次运行会自动下载 yolov8n.pt)
        self.model = YOLO('yolov8n.pt')
        
        # 在 COCO 数据集中，车辆相关的类别 ID: 2(car), 3(motorcycle), 5(bus), 7(truck)
        self.vehicle_classes = [2, 3, 5, 7]
        
        # 订阅你 rosbag 中的压缩图像话题
        self.subscriber = rospy.Subscriber(
            '/hikcamera/image_2/compressed',
            CompressedImage,
            self.image_callback,
            queue_size=1
        )
        rospy.loginfo("车辆检测节点已启动！等待接收图像...")

    def image_callback(self, msg):
        try:
            # 1. 将 ROS 压缩图像转换为 OpenCV 图像
            np_arr = np.frombuffer(msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            # 假设你的图像变量叫 cv_image
            print(f"Image Resolution: {cv_image.shape[1]}x{cv_image.shape[0]}")
            
            if cv_image is None:
                return

            # 2. 使用 YOLOv8 进行目标检测 (只检测车辆类别)
            results = self.model(cv_image, classes=self.vehicle_classes, verbose=False)
            
            # 3. 在图像上绘制检测框 (YOLOv8 自带的 plot 方法)
            annotated_frame = results[0].plot()
            
            # 4. 显示结果 (满足作业的 UI 要求)
            cv2.imshow("YOLOv8 Vehicle Detection", annotated_frame)
            cv2.waitKey(1) # 1毫秒刷新
            
        except Exception as e:
            rospy.logerr(f"图像处理出错: {e}")

if __name__ == '__main__':
    try:
        detector = VehicleDetector()
        rospy.spin() # 保持节点运行
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()
