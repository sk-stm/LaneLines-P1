import matplotlib.image as mpimg
import os
import numpy as np
from PIL import Image
from typing import List
import cv2


def get_images(path: str) -> List[str]:
    '''
    Collects the images from a directory.
    :param path: the directory to collect the image from.
    :return: the image paths
    '''
    assert os.path.isdir(path), "The path to the data is not a directory. Data could not be found."
    data_file_names = os.listdir(path)

    file_paths = []
    for file  in data_file_names:
        file_paths.append(file)
    return file_paths


def _transform_image(image) -> np.array:
    '''
    Transforms the image to gray scale and blurres it.
    :param image: image to transform
    :return: array representation of transformed image.
    '''
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Define a kernel size and apply Gaussian smoothing
    kernel_size = 5
    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)
    return blur_gray


def _canny_edge(img: np.array, low_th: int=50, high_th: int=150 ) -> np.array:
    '''
    Performs Canny edge detection on input image.
    :param img: input image
    :param low_th: lower threshold to keep edges in canny algorithm
    :param high_th: upper bound to keep edges in canny algorithm
    :return: array of the image containing the edges found by canny
    '''
    # Define our parameters for Canny and apply
    edges = cv2.Canny(img, low_th, high_th)
    return edges

def _mask_edges(image: np.array, edges) -> np.array:
    '''
    Defines a polygon to crop out the part of the street containing the lanes, and crops that part from the image.
    :param image: the image to crop.
    :param edges: the edges of that image.
    :return: a croped version of the edge image containing all the edges in the polygon.
    '''
    mask = np.zeros_like(edges)
    ignore_mask_color = 255

    # This time we are defining a four sided polygon to mask
    # TODO we dont need the image here I guess the size can also be taken from the edges array
    imshape = image.shape
    im_x = image.shape[1]
    im_y = image.shape[0]
    vertices = np.array([[(0, im_y), (im_x / 2.1, im_y / 1.65), (im_x / 1.8, im_y / 1.65), (im_x, im_y)]],
                        dtype=np.int32)
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_edges = cv2.bitwise_and(edges, mask)
    return masked_edges


def _hough_transform(edges_img: np.array, rho: int=1, theta: float=np.pi/180, threshold: int=50,
                     min_line_length: int=10, max_line_gap: int=150):
    '''
    Performs hough transform line detection in the masked edges image and
    :param edges_img: the edge image to search lines in
    :param rho: distance resolution in pixels of the Hough grid
    :param theta: angular resolution in radians of the Hough grid
    :param threshold: minimum number of votes (intersections in Hough grid cell)
    :param min_line_length: minimum number of pixels making up a line
    :param max_line_gap: maximum gap in pixels between connectable line segments
    :return: the lines found in the image in (x1,y1) (x2,y2) pairs
    '''
    # Make a blank the same size as our image to draw on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges_img, rho, theta, threshold, np.array([]),
                                min_line_length, max_line_gap)
    return lines

def main():
    data_path = '../test_images/'

    # get images as list
    img_names = get_images(data_path)

    for img_name in img_names:
        img = mpimg.imread(os.path.join(data_path,img_name))
        # Get blurred gray image
        blurr_gray = _transform_image(img)

        # Get edges using canny
        edges = _canny_edge(blurr_gray)

        # get masked edges
        masked_edges = _mask_edges(img, edges)

        # get line from hough transformation
        lines = _hough_transform(masked_edges)

        # Create output image
        line_image = np.copy(img)*0 # creating a blank to draw lines on
        # Iterate over the output "lines" and draw lines on a blank image
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)

        # Draw the lines on the edge image
        lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)

        result = Image.fromarray((lines_edges).astype(np.uint8))
        result.save('out_' + img_name[:-4] + '.png')

        # plt.imshow(lines_edges)

if __name__ == '__main__':
    main()