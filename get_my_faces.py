import cv2
import dlib
import os
import sys
import random

output_dir = 'D:/photos/myself'
size = 64

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 改变图片的亮度与对比度
def relight(img, light=1, bias=0):
    w = img.shape[1]
    h = img.shape[0]
    #image = []
    for i in range(0,w):
        for j in range(0,h):
            for c in range(3):
                tmp = int(img[j,i,c]*light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j,i,c] = tmp
    return img

#使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()

"""

dlib.get_frontal_face_datector(PythonFunction，in Classes)

其中in Classes 表示采样（upsample）次数

返回值是<class 'dlib.dlib.rectangle'>，就是一个矩形

坐标为[(x1, y1) (x2, y2)]

可以通过函数的left,right,top,bottom方法分别获取对应的x1, x2, y1, y2值:

采样次数代表将原始图像是否进行放大，1表示放大1倍再检查，提高小人脸的检测效果
"""

# 打开摄像头 参数为输入流，可以为摄像头或视频文件
camera = cv2.VideoCapture(0) # 为0 是使用当前摄像头

index = 1
while True:
    if (index <= 10000):
        print('Being processed picture %s' % index)
        # 从摄像头读取照片
        success, img = camera.read()
        # 转为灰度图片
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        """
        1、cv2.imread()接口读图像，读进来直接是BGR 格式数据格式在 0~255
       需要特别注意的是图片读出来的格式是BGR，不是我们最常见的RGB格式，颜色肯定有区别。
       2、cv2.cvtColor(p1,p2) 是颜色空间转换函数，p1是需要转换的图片，p2是转换成何种格式。
        """
        # 使用detector进行人脸检测
        dets = detector(gray_img, 1)

        for i, d in enumerate(dets):
            x1 = d.top() if d.top() > 0 else 0
            y1 = d.bottom() if d.bottom() > 0 else 0
            x2 = d.left() if d.left() > 0 else 0
            y2 = d.right() if d.right() > 0 else 0

            face = img[x1:y1,x2:y2]
            # 调整图片的对比度与亮度， 对比度与亮度值都取随机数，这样能增加样本的多样性
            face = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))

            face = cv2.resize(face, (size,size))

            cv2.imshow('image', face)

            cv2.imwrite(output_dir+'/'+str(index)+'.jpg', face)

            index += 1
        key = cv2.waitKey(30) & 0xff # 等待键盘触发时间为30ms
        if key == 27:
            break


    else:
        print('Finished!')
        break
"""
首先&运算即“and”运算。
ESC键的ASCALL码为27

其次0xFF是16进制数，对应的二进制数为1111 1111。

然后cv2.waitkey（delay）函数

1.若参数delay≤0：表示一直等待按键；

2、若delay取正整数：表示等待按键的时间，比如cv2.waitKey(30)，就是等待30（milliseconds）；（视频中一帧数据显示（停留）的时间）

cv2.waitKey(delay)返回值：

1、等待期间有按键：返回按键的ASCII码（比如：Esc的ASCII码为27，即0001  1011）；

2、等待期间没有按键：返回 -1；

我们知道，当按下按键时，waitkey函数的输入值一定是一个正整数。任何一个正整数，与1111 1111做&运算，其结果必然是他本身（因为正数的补码等于原码），例

0001 1011

1111  1111

&运算结果为：0001 1011

那么这个&0xff到底有什么用呢？

解释
查阅资料我才知道，原来系统中按键对应的ASCII码值并不一定仅仅只有8位，同一按键对应的ASCII并不一定相同（但是后8位一定相同）

为什么会有这个差别？是系统为了区别不同情况下的同一按键。

比如说“q”这个按键

当小键盘数字键“NumLock”激活时，“q”对应的ASCII值为100000000000001100011 。

而其他情况下，对应的ASCII值为01100011。

相信你也注意到了，它们的后8位相同，其他按键也是如此。

为了避免这种情况，引用&0xff，正是为了只取按键对应的ASCII值后8位来排除不同按键的干扰进行判断按键是什么

"""