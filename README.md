# WAPerceptionChallenge

I tried a few things before getting this to work.

* I tried using Houghlines transform, but this was needlessly complicated.

* Then, with the advice of Sam, I decided to calculate the centroids of the cones and draw a line of best fit through them.
This came with a few challenges. First, Trackbars in opencv weren't working on my mac for some odd reason, so it was difficult to find a range of HSV values that would be a good mask for the orange cones. Without a good mask there was no way of finding the contours of the cones to find the centroids of the cones. To overcome this I found some HSV values that identfied the edges of the cones, then drew a circle on each of the non-zero values in the masked image. These circles overlapped, creating a sort of blob that I could find the centroids for. From there I just split the centroids into two groups (those to the left of the center of the image and those on the right) and drew a line of best fit. This worked great, except for a couple of values in the mask that weren't related to the cones (the door, etc). So I drew some black polygons over these areas to remove them from the calculation, creating a region of interest. The result is the image in "answer.png".

Methodology Summarized
* Draw polygons over irrelvant areas
* mask over non-orange values
* draw circles over values that show up in the mask, because the mask isn't great
* find centroids
* split centroids into right and left
* draw a line of best fit through left and right

Libraries used: Numpy and OpenCV
