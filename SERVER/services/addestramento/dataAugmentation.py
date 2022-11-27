from PIL import Image,ImageOps
import imageio
import imgaug as ia
import imgaug.augmenters as iaa

#images must be saved as n.png, where n is an integer
#folder has to be passed as "r'dir\dir\last_dir"
def dataAugmentation(path,start,end):
    #start is the number of the first pictures, end referedd to the last + 1
    count = start
    for count in range(start,end):
        # Construct old file name
        source = path +'\\'+ str(count)+".png"
        dest_m = path +'\\'+ str(count)+"_m.png"
        dest_f = path +'\\'+ str(count)+"_f.png"
        img = Image.open(source)
        img_g = img.convert('LA')
        img_g.save(source)
        img = Image.open(source)
        im_mirror = ImageOps.mirror(img)
        im_mirror.save(dest_m)
        im_flip = ImageOps.flip(img)
        im_flip.save(dest_f)