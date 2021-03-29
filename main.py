print("EXPECT THE FUTURE")

from matplotlib import image, pyplot
import numpy as np
from PIL import Image
import skimage as sk

pic = Image.open('vis/1.jpg')
arr = np.copy(np.asarray(pic))  # VERTICAL; HORIZONTAL; RGB

# Edition
# arr[1, 1] = np.array([0, 0, 0])
# pic = Image.fromarray(arr)

pyplot.imshow(pic)
pyplot.show()
