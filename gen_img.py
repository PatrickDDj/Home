import os 
from glob import glob


if __name__ == '__main__':

    photos = glob('images/photos/*.jpeg')
    k=9
    res = ""
    for i in range(0, len(photos), k):
        res +=  """          <div class="row is-mobile is-centered">
            <div class="columns is-mobile is-centered">"""
        
        for j in range(k):
            try:
                res += f"""
<div class="column is-mobile is-centered">
                <img
                  src="{photos[i+j]}"
                  class="gallery_img"
                />
              </div>"""
            except:
                print("")

        res += """            </div>
          </div>
          <br />
          """
    print(res)
