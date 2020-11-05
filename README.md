# Simple-FaceRecognition
This project describes a simple face recofnition
It uses CNN model construction,thuough the camera to obtain photos for trainning,and finally test
它用了三层卷积，两层全连接层，卷积层各自含有池化层和relu激活函数、
输入为opencv中的摄像头捕捉照片，存放到一个文件夹中myself，并对照片进行亮度和对比度调节，增加样本的范化性，others为一个文件夹
将照片进行dlib的人脸特征捕捉，找到人脸位置，并
