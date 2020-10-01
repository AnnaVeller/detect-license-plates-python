<<<<<<< HEAD
import os
import numpy as np
import sys
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import cv2
import warnings
warnings.filterwarnings('ignore')
from regions import *
#from detector import *
import model

all_regions = load_regions()
print(all_regions)
image = cv2.imread("test.jpg")
state, textArr, status = model.detect_number(image, "A001MP05")
print(state, textArr, status)


=======
import os
import numpy as np
import sys
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import cv2
import warnings
warnings.filterwarnings('ignore')
from regions import *
#from detector import *
import model

all_regions = load_regions()
print(all_regions)
image = cv2.imread("test.jpg")
state, textArr, status = model.detect_number(image, "A001MP05")
print(state, textArr, status)


>>>>>>> refresh code by old repo with jupyter code
