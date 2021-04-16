import cv2
import imutils
import numpy as np
import pytesseract

def showImage(img):
    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread('../img/car2.jpeg',cv2.IMREAD_GRAYSCALE)
ogImage = img.copy()
img = cv2.bilateralFilter(img, 13, 15, 15)
img = cv2.Canny(img, 30, 150) #Perform Edge detection

contours=cv2.findContours(img.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
contours = sorted(contours,key=cv2.contourArea, reverse = True)[:10]
screenCnt = None
showImage(img)
for c in contours:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

mask = np.zeros(ogImage.shape,np.uint8)
new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
new_image = cv2.bitwise_and(ogImage,ogImage,mask=mask)

(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
cropped = ogImage[topx:bottomx+1, topy:bottomy+1]

text = pytesseract.image_to_string(cropped, config='--psm 11')
print("Detected license plate Number is:",text)

