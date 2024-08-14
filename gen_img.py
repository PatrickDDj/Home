import os 
from glob import glob
import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
def get_dominant_color(image):
    image = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=1).fit(image)
    return kmeans.cluster_centers_[0]

def classify_color(dominant_color):
    hue = cv2.cvtColor(np.uint8([[dominant_color]]), cv2.COLOR_BGR2HSV)[0][0][0]
    if hue < 15 or hue > 330:
        return '0-red'
    elif hue < 45:
        return '1-orange'
    elif hue < 75:
        return '2-yellow'
    elif hue < 165:
        return '3-green'
    elif hue < 195:
        return '4-cyan'
    elif hue < 255:
        return '5-blue'
    else:
        return '6-purple'


if __name__ == '__main__':

  image_folder = 'images/photos'
  image_files = glob(f'{image_folder}/*.jpeg')

  for image_file in image_files:
      src = image_file
      image = cv2.imread(src)
      dominant_color = get_dominant_color(image)
      color_class = classify_color(dominant_color)
      print(f'The image {image_file} is classified as {color_class}.')

      dst = os.path.join(image_folder, color_class)
      os.makedirs(dst, exist_ok=True)
      os.system(f'cp {src} {dst}')


  photos = sorted(glob('images/photos/*/*.jpeg'))
  k=7
  res = """<div class="rows is-mobile is-centered">"""
  for i in range(0, len(photos), k):
      res +=  """<div class="row is-mobile is-centered">
                  <div class="columns is-mobile is-centered">
                    <div class="column is-mobile is-centered"></div>"""
      
      for j in range(k):
          try:
              res += f"""<div class="column is-mobile is-centered"><img src="{photos[i+j]}" class="gallery_img"/></div>"""
          except:
              print("")
      res += """</div></div><br />"""
  res += """</div>"""
  print(res)
