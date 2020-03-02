# Author: Ankush Gupta
# Date: 2015

"""
Entry-point for generating synthetic text images, as described in:

@InProceedings{Gupta16,
      author       = "Gupta, A. and Vedaldi, A. and Zisserman, A.",
      title        = "Synthetic Data for Text Localisation in Natural Images",
      booktitle    = "IEEE Conference on Computer Vision and Pattern Recognition",
      year         = "2016",
    }
"""

import numpy as np
import h5py
import os, sys, traceback
import os.path as osp
from synthgen import *
from common import *
import wget, tarfile


## Define some configuration variables:
NUM_IMG = -1 # no. of images to use for generation (-1 to use all available):
INSTANCE_PER_IMAGE = 6 # no. of times to use the same image
SECS_PER_IMG = 1 #max time per image in seconds

# path to the data-file, containing image, depth and segmentation:
DATA_PATH = 'data'
DB_FNAME = '/mnt/data/Rohit/3SYnthBG/dset_8000.h5'#/mnt/data/1SceneTextBangla/data/synth_il.h5'#/mnt/data/Rohit420GBVol/3SYnthBG/dset_8000.h5'
# url of the data (google-drive public file):
DATA_URL = 'https://www.dropbox.com/s/gnzbtvdemy06xyq/data.tar.gz?dl=1'
OUT_FILE = 'results/trainsmall.h5'

def get_data():
  """
  Download the image,depth and segmentation data:
  Returns, the h5 database.
  """
  if not osp.exists(DB_FNAME):
    try:
      colorprint(Color.BLUE,'\tdownloading data (56 M) from: '+DATA_URL,bold=True)
      print()
      sys.stdout.flush()
      out_fname = 'data.tar.gz'
      wget.download(DATA_URL,out=out_fname)
      tar = tarfile.open(out_fname)
      tar.extractall()
      tar.close()
      os.remove(out_fname)
      colorprint(Color.BLUE,'\n\tdata saved at:'+DB_FNAME,bold=True)
      sys.stdout.flush()
    except:
      print (colorize(Color.RED,'Data not found and have problems downloading.',bold=True))
      sys.stdout.flush()
      sys.exit(-1)
  # open the h5 file and return:
  return h5py.File(DB_FNAME,'r')


def add_res_to_db(imgname,res,db):
  """
  Add the synthetically generated text image instance
  and other metadata to the dataset.
  """
  ninstance = len(res)
  for i in range(ninstance):
    dname = "%s_%d"%(imgname, i)
    db['data'].create_dataset(dname,data=res[i]['img'])
    db['data'][dname].attrs['charBB'] = res[i]['charBB']
    db['data'][dname].attrs['wordBB'] = res[i]['wordBB']
    db['data'][dname].attrs['lineBB'] = res[i]['lineBB']                       
    #db['data'][dname].attrs['txt'] = res[i]['txt']
    L = res[i]['txt']
    print("1:",L)
    L = [n.encode("utf-8", "ignore") for n in L]#"ascii"
    print("2:",L)
    db['data'][dname].attrs['txt'] = L


def main(viz=False):
  # open databases:
  print (colorize(Color.BLUE,'getting data..',bold=True))
  db = get_data()#downlaod and return h5py.File(DB_FNAME,'r') DB_FNAME = osp.join(DATA_PATH,'dset.h5') DATA_PATH = 'data/'
  print (colorize(Color.BLUE,'\t-> done',bold=True))

  # open the output h5 file:
  out_db = h5py.File(OUT_FILE,'w')#results/SynthText.h5
  out_db.create_group('/data')
  print (colorize(Color.GREEN,'Storing the output in: '+OUT_FILE, bold=True))

  # get the names of the image files in the dataset:
  imnames = sorted(db['image'].keys())
  N = len(imnames)
  global NUM_IMG
  if NUM_IMG < 0:
    NUM_IMG = N
  start_idx,end_idx = 0,min(NUM_IMG, N)
  cntr = 0
  RV3 = RendererV3(DATA_PATH,max_time=SECS_PER_IMG)
  trainlist = list(range(start_idx,end_idx))#end_idx-16
  testlist = list(range(end_idx-16,end_idx))
  for i in trainlist:
    imname = imnames[i]
    try:
    #if(1):
      # get the image:
      img = Image.fromarray(db['image'][imname][:])
      # get the pre-computed depth:
      #  there are 2 estimates of depth (represented as 2 "channels")
      #  here we are using the second one (in some cases it might be
      #  useful to use the other one):
      depth = db['depth'][imname][:].T
      depth = depth[:,:,1]
      # get segmentation:
      seg = db['seg'][imname][:].astype('float32')
      #print("here: ", seg.shape, img.size , depth.shape)# = db['seg'][imname][:].astype('float32')
      area = db['seg'][imname].attrs['area']
      label = db['seg'][imname].attrs['label']

      # re-size uniformly:
      sz = depth.shape[:2][::-1]
      img = np.array(img.resize(sz,Image.ANTIALIAS))# resize img to size of depth map
      seg = np.array(Image.fromarray(seg).resize(sz,Image.NEAREST))#resize seg to same size as of depth map
      #print("here1: ", seg.shape, img.size , depth.shape, sz)# = db['seg'][imname][:].astype('float32')

      print (colorize(Color.RED,'%d of %d'%(i,end_idx-1), bold=True))#0 of 4 , 1 of 4.....
      res = RV3.render_text(img,depth,seg,area,label,
                            ninstance=INSTANCE_PER_IMAGE,viz=viz)
      if len(res) > 0:
        # non-empty : successful in placing text:
        add_res_to_db(imname,res,out_db)
        cntr+=len(res)
      # visualize the output:
      if viz:
        if 'q' in input(colorize(Color.RED,'continue? (enter to continue, q to exit): ',True)):
          break
    except:
      traceback.print_exc()
      print (colorize(Color.GREEN,'>>>> CONTINUING....', bold=True))
      continue
  print("no images", cntr)
  db.close()
  out_db.close()


if __name__=='__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Genereate Synthetic Scene-Text Images')
  parser.add_argument('--viz',action='store_true',dest='viz',default=False,help='flag for turning on visualizations')
  args = parser.parse_args()
  main(args.viz)
