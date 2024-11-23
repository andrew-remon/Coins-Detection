# Import the necessary modules
import numpy as np
import cv2 as cv


def av_pix(img,circles,size):
    """Calculate the average brightness of every detected circle."""
    av_value = []
    for coords in circles[0,:]:
        col = np.mean(img[coords[1]-size:coords[1]+size,coords[0]-size:coords[0]+size])
        av_value.append(col)
    return av_value


def get_circles_radius(circles):
    """Get the radii of all detected circles and append them to a list"""
    radii =[]
    for coords in circles[0,:]:
        radii.append(coords[2])
    return radii


# Read the original image
original_img = cv.imread("coins.png")

# convert the original photo to grayscale version and apply blurring.
gray_img = cv.imread("coins.png", cv.IMREAD_GRAYSCALE)
gray_img = cv.GaussianBlur(gray_img, (7, 7), 0)

# apply the houghCircle algorithm
circles = cv.HoughCircles(
    gray_img,
    cv.HOUGH_GRADIENT,
    1,
    125,
    param1=55,
    param2=45,
    minRadius=5,
    maxRadius=110,
)

#transferring the data into integers
circles = np.uint16(np.around(circles))

# initiate the first counter
counter_1 = 1

# drawing all possible circles
for circle in circles[0,:]:

    cv.circle(original_img, (circle[0], circle[1]), circle[2], (255, 255, 255), 2)
    # cv.putText(original_img,
    #         f"{counter}",
    #         (circle[0], circle[1]),
    #         cv.FONT_HERSHEY_SIMPLEX,
    #         1.5,
    #         (0, 0, 0), 2)
    counter_1 +=1

# get the list of radii and brightness values to be compared
radii = get_circles_radius(circles)
bright_values = av_pix(original_img, circles, 20)

# determin the value of each coin
values = []
for a, b in zip(bright_values, radii):
    if a > 100 and b > 90:
        values.append(10)
    elif a > 100 and b <= 90:
        values.append(5)
    elif a < 100 and b > 90:
        values.append(2)
    elif a < 100 and b < 90:
        values.append(1)

# initiate the second counter
counter_2 = 0

# get every circle with its values
for circle in circles[0,:]:

    cv.putText(original_img,
            f"{values[counter_2]}c",
            (circle[0], circle[1]),
            cv.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 0), 2)

    counter_2 +=1

# add the sum message in the original photo
cv.putText(original_img, f"estimated sum of coins: {sum(values)}", (100, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# show the original photo after detecting and calculating the value of every coin.
cv.imshow("detected coins", original_img)
cv.waitKey(0)
cv.destroyAllWindows()

