import os
from glob import glob
import cv2
import numpy as np
from sklearn.cluster import KMeans
import os
from tqdm import tqdm

def get_dominant_color(image):
    image = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=1).fit(image)
    return kmeans.cluster_centers_[0]


def classify_color(dominant_color):
    hue = cv2.cvtColor(np.uint8([[dominant_color]]), cv2.COLOR_BGR2HSV)[0][0][0]
    if hue < 15 or hue > 330:
        return "01-red", hue
    elif hue < 45:
        return "02-orange", hue
    elif hue < 75:
        return "03-yellow", hue
    elif hue < 165:
        return "04-green", hue
    elif hue < 195:
        return "00-cyan", hue
    elif hue < 255:
        return "05-blue", hue
    else:
        return "06-purple", hue


if __name__ == "__main__":

    image_folder = "gallery_photos"
    image_files = glob(f"{image_folder}/*.png") + glob(f"{image_folder}/*.jpeg")

    for image_file in tqdm(image_files):
        src = image_file
        image = cv2.imread(src)
        dominant_color = get_dominant_color(image)
        color_class, hue = classify_color(dominant_color)
        print(f"The image {image_file} is classified as {color_class}.")

        dst = os.path.join(image_folder, color_class)
        filename = '{hue}-{filename}'.format(hue="{:0>3d}".format(hue), filename=image_file.split('/')[-1])
        os.makedirs(dst, exist_ok=True)
        os.system(f"mv {src} {dst}/{filename}")

    photos = sorted(glob("gallery_photos/*/*"))
    #   k=7
    #   res = """<div class="rows is-mobile is-centered">"""
    #   for i in range(0, len(photos), k):
    #       res +=  """<div class="row is-mobile is-centered">
    #                   <div class="columns is-mobile is-centered">
    #                     <div class="column is-mobile is-centered"></div>"""

    #       for j in range(k):
    #           try:
    #               res += f"""<div class="column is-mobile is-centered"><img src="{photos[i+j]}" class="gallery_img"/></div>"""
    #           except:
    #               print("")
    #       res += """</div></div><br />"""
    #   res += """</div>"""
    #   print(res)

    template = """<!DOCTYPE html>
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dadong Jiang</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    background-color: #f0f0f0;
                    margin: 0;
                    padding: 20px;
                }
                .gallery {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 15px;
                    width: 100%;
                    /* max-width: 800px; */
                }
                .gallery img {
                    width: 100%;
                    border-radius: 8px;
                    transition: transform 0.3s ease;
                }
                .gallery img:hover {
                    transform: scale(1.1);
                }
            </style>
        </head>
        <body>
                <div class="gallery">
                    xxxxx
                </div>

        </body>
        </html>"""

    src_images = ['<img src="{src}">'.format(src=src) for src in photos]
    src_images = '\n'.join(src_images)

    # print(src_images)

    html = template.replace('xxxxx', src_images)

    with open('index_image_gallery.html', 'w') as f:
        f.write(html)