#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from scipy.spatial import Delaunay
import argparse
import sys

def parseArgs():
# just some cmdline arg parsing
  parser = argparse.ArgumentParser(description='Create a SEES python course certificate.',
    epilog="Author: hexatedjuice")
  parser.add_argument('--user', metavar='userName', type=str, help='The name of the student')
  parser.add_argument('--level', metavar='userLevel', type=str, help='The level of the student')
  parser.add_argument('--theme', metavar='userTheme', type=str, help='Theme of certificate favicon. Uses matplotlib naming schemes. (default: plasma)', default='plasma')
  parser.add_argument('--file', metavar='usersFile', type=str, help='Provide a file with respective student names, levels, and themes separated by a newline. (line format: [name] [level] [theme])')

  global args
  args = parser.parse_args()

# arg error catching
  if args.user or args.level:
    if not args.level or not args.user or args.file:
      print('[-] Incorrect usage. Options --user and --level should be used together without the --file option. If using a file, specify theme on each line if preferred.')
      exit()
    return False
  elif args.file:
    if args.level or args.user:
      print('[-] Incorrect usage. Options --user and --level should be used together without the --file option. Specify theme within the file.')
      exit()
    return True
  elif len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    exit()

def faviconGen(theme):
  # point generation
  x = np.rad2deg(np.random.uniform(low=-0.100, high=0.030, size=(74,))).T
  y = np.rad2deg(np.random.uniform(low=0.800, high=1.010, size=(74,))).T

  # generate Delauny array to make vertice offsets
  xOffset = np.rad2deg(np.random.uniform(low=-0.100, high=0.030, size=(74,))).T
  yOffset = np.rad2deg(np.random.uniform(low=0.800, high=1.010, size=(74,))).T

  frame = list(zip(xOffset, yOffset))
  tri = Delaunay(frame)
  triangles = np.asarray(tri.vertices)

  # calculating points to be drawn
  xmid = x[triangles].mean(axis = 1)
  ymid = y[triangles].mean(axis = 1)
  x0 = -8
  y0 = 70
  # color variation and determination per face
  zfaces = np.exp(np.random.uniform(low=0, high=-0.01) * ((xmid - x0) * (xmid - x0) + (ymid - y0) * (ymid - y0)))
  fig3, ax3 = plt.subplots()

  # formatting and saving
  ax3.set_aspect('equal')
  tpc = ax3.tripcolor(x, y, triangles, facecolors = zfaces, cmap = theme, edgecolors ='k', alpha = 0.3)
  plt.axis('off')
  plt.savefig("favicon.png", dpi=300)

def certBuild(user, level):
# setting graph formatting
  rc = {"axes.spines.left" : False,
      "axes.spines.right" : False,
      "axes.spines.bottom" : False,
      "axes.spines.top" : False,
      "xtick.bottom" : False,
      "xtick.labelbottom" : False,
      "ytick.labelleft" : False,
      "ytick.left" : False,
      "figure.dpi" : 300,
      "font.family" : 'Source Code Pro'}
  plt.rcParams.update(rc)
  mpl.rc('font', family='Serif')

  # initiating plot and setting favicon as bg
  fig = plt.figure(figsize=(11, 8.5), facecolor='w', constrained_layout=True)
  gs = fig.add_gridspec(nrows=7, ncols=11, figure=fig)
  img = mpimg.imread('favicon.png')
  imgplot = plt.imshow(img, extent=[-500, 500.0, -500, 500], aspect=0.5, origin='lower')

  empty = fig.add_subplot(gs[:2,:], facecolor='none')

# annotating subplots to make the cert
  mpl.rcParams['font.size'] = 40
  headerAx = fig.add_subplot(gs[2,:], facecolor='none')
  headerAx.annotate('CERTIFICATE OF RECOGNITION', xy=(0.5, 0), xycoords='axes fraction', ha='center', color='#222222')

  mpl.rcParams['font.size'] = 20
  subHeadAx2 = fig.add_subplot(gs[3,:], facecolor='none')
  subHeadAx2.annotate('\nSEES Recognizes\n', xy=(0.5, 0), xycoords='axes fraction', ha='center', color='#ffffff')

  mpl.rcParams['font.size'] = 60
  name = fig.add_subplot(gs[4,:], facecolor='none')
  name.annotate(user.upper() +"\n", xy=(0.5, 0), xycoords='axes fraction', ha='center')

  mpl.rcParams['font.size'] = 18
  completionParam = fig.add_subplot(gs[5,:], facecolor='none')
  completionParam.annotate("For their completion of the {} Python Certification Course".format(level.title()), xy=(0.5, 1.2), xycoords='axes fraction', ha='center')

  empty2 = fig.add_subplot(gs[6,:], facecolor='none')

  plt.savefig(user.title().replace(" ", "") + level.title() +".png", dpi=300)

def fileRun(fileName):
  # for runnign thru lines of a file to make many certs
  file = open(fileName, 'r')
  lines = file.readlines()
  for line in lines:
    name = str(" ".join(line.strip().split(' ')[:2]))
    level = str("".join(line.strip().split(' ')[2:3]))
    theme = str("".join(line.strip().split(' ')[3:]))
    if not theme:
      theme = 'plasma'
    print("[+] Working on {}'s certificate.".format(name.title()))
    faviconGen(theme)
    certBuild(name, level)
  file.close()

if __name__ == '__main__':
  fileUsage = parseArgs()
  if fileUsage:
    fileRun(args.file)
  else:
    print("[+] Working on the certificate.")
    faviconGen(args.theme)
    certBuild(args.user, args.level)