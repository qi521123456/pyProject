from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import cv2
import time
time1 = time.time()

########################自定义图像压缩函数############################
def img_zip(path,filename1,filename2):
    image = cv2.imread(path+filename1)
    cv2.imshow('image',image)
    size = image.shape
    # cv2.namedWindow('hello',cv2.WINDOW_AUTOSIZE)
    print(size)
    high = size[0]//4
    whith = (high*size[1])//(size[0])
    res = cv2.resize(image, (whith,high), interpolation=cv2.INTER_AREA)
    cv2.imshow('new res',res)
    cv2.imwrite(path+filename2, res)
    # imgE = Image.open(path+filename2)
    # imgEH = ImageEnhance.Contrast(imgE)
    # img1 = imgEH.enhance(2.8)
    # gray1 = img1.convert("L")
    # gary2 = gray1.filter(ImageFilter.DETAIL)
    # gary3 = gary2.point(lambda i: i * 0.9)
    # gary3.save(path+filename2)

    cv2.waitKey(0)
    # cv2.destroyAllWindows()
################################主函数##################################
if __name__ == '__main__':
    path=u"E:/"
    filename1="0.jpg"
    filename2="1.jpg"
    img_zip(path,filename1,filename2)
    time2 = time.time()
    print(u'总共耗时：' + str(time2 - time1) + 's')