# Jackson Kunde

# Importing the OpenCV library
import cv2
import numpy as np

def region_of_interest(img):
    # mask over the space we don't care about
    h, w, _ = img.shape
    pts1 = np.array([[0, 0], [1200, 0], [0, 1200]])
    pts1 = pts1.reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts1], 0)
    
    pts2 = np.array([[w, 0], [w-1200, 0], [w, 1200]])
    pts2 = pts2.reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts2], 0)
    
def find_centroids(img):
    # find the centroids of the cones
    circle_mask = np.zeros(img.shape[:2], np.uint8) # empty img now
    
    # to overcome the bad mask, we are going to draw circles on all the non-black values in the img
    # this should create an image that we can contour to find the centroids
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            if img[x][y]>0:
                cv2.circle(circle_mask, (y, x), 15, (255, 255, 255), -1)
                
    # find contours in the image
    contours, hierarchy = cv2.findContours(circle_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    centroids = []
    for c in contours:
        # calculate moments for each contour
        M = cv2.moments(c)

        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centroids.append((cX, cY))
        cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
    
    return centroids

def draw_bestfit(img, points):
    h, w, _ = img.shape
    vx, vy, cx, cy = cv2.fitLine(np.array(points), cv2.DIST_L2, 0, 0.01, 0.01)
    cv2.line(img, (int(cx-vx*w), int(cy-vy*w)), (int(cx+vx*w), int(cy+vy*w)), (0, 0, 255), thickness=10)
    
    
def mask_orange(img):
    # apply blurring
    blur_img = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT)
    # cv2.imshow('blur', blur_img)

    #change to hsv to mask over non-orange colors
    hsv = cv2.cvtColor(blur_img, cv2.COLOR_BGR2HSV)

    light_orange = (1, 100, 160)
    dark_orange = (50, 255, 255)

    # get a mask over non-orange colors
    mask = cv2.inRange(hsv, light_orange, dark_orange)
    
    return mask

def main():
    # Reading the image using imread() function
    img = cv2.imread('red.png')
    
    final_img = img.copy()
    
    h, w, _ = img.shape
    
    #apply a ROI for our image
    region_of_interest(img)
    
    # remove all but the orange values on the image
    orange_mask = mask_orange(img)
    
    # find the centroids of the cones
    centroids = find_centroids(orange_mask)

    # split the centroids of the cones into a left group and a right group
    left_centroids = []
    right_centroids = []
    middle = w//2
    for centroid in centroids:
        if centroid[0] > middle:
            right_centroids.append(centroid)
        else:
            left_centroids.append(centroid)
            
    # draw best fit lines on our final image for each of the groups
    draw_bestfit(final_img, left_centroids)
    draw_bestfit(final_img, right_centroids)
    
    cv2.imwrite("answer.png", final_img)
        
if __name__ == '__main__':
    main()