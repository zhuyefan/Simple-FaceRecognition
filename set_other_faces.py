# -*- codeing: utf-8 -*-
import sys
import os
import cv2
import dlib

input_dir = './input_img'
output_dir = './other_faces'
size = 64

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

#使用dlib自带的frontal_face_detector作为我们的特征提取器
detector = dlib.get_frontal_face_detector()

index = 1
for (path, dirnames, filenames) in os.walk(input_dir):

    """
    top -- 是你所要遍历的目录的地址, 返回的是一个三元组(root,dirs,files)。

root 所指的是当前正在遍历的这个文件夹的本身的地址
dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
topdown --可选，为 True，则优先遍历 top 目录，否则优先遍历 top 的子目录(默认为开启)。如果 topdown 参数为 True，walk 会遍历top文件夹，与top 文件夹中每一个子目录。

onerror -- 可选，需要一个 callable 对象，当 walk 需要异常时，会调用。

followlinks -- 可选，如果为 True，则会遍历目录下的快捷方式(linux 下是软连接 symbolic link )实际所指的目录(默认关闭)，如果为 False，则优先遍历 top 的子目录。
    
    """#os.walk() 方法用于通过在目录树中游走输出在目录中的文件名，向上或者向下。
                                                        # os.walk() 方法是一个简单易用的文件、目录遍历器，可以帮助我们高效的处理文件、目录方面的事情。
    for filename in filenames:
        if filename.endswith('.jpg'):  #  判断是否以.jpg结尾，是的话为ture
            print('Being processed picture %s' % index)
            img_path = path+'/'+filename
            # 从文件读取图片
            img = cv2.imread(img_path)
            # 转为灰度图片
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 使用detector进行人脸检测 dets为返回的结果
            dets = detector(gray_img, 1)

            #使用enumerate 函数遍历序列中的元素以及它们的下标
            #下标i即为人脸序号
            #left：人脸左边距离图片左边界的距离 ；right：人脸右边距离图片左边界的距离 
            #top：人脸上边距离图片上边界的距离 ；bottom：人脸下边距离图片上边界的距离
            for i, d in enumerate(dets):
                x1 = d.top() if d.top() > 0 else 0
                y1 = d.bottom() if d.bottom() > 0 else 0
                x2 = d.left() if d.left() > 0 else 0
                y2 = d.right() if d.right() > 0 else 0
                # img[y:y+h,x:x+w]
                face = img[x1:y1,x2:y2]
                # 调整图片的尺寸
                face = cv2.resize(face, (size,size))
                cv2.imshow('image',face)
                # 保存图片
                cv2.imwrite(output_dir+'/'+str(index)+'.jpg', face)
                index += 1

            key = cv2.waitKey(30) & 0xff
            if key == 27:
                sys.exit(0)
