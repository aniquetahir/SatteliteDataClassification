from sys import argv
from gmap_utils import *
import os
import urllib.request
import sys, time
import random

class TileDownloader:
    def __init__(self, min_lng, max_lng, min_lat, max_lat, zoom):
        self.minLat = min_lat
        self.maxLat = max_lat
        self.minLng = min_lng
        self.maxLng = max_lng
        self.zoom = zoom

    def getTiles(self, folder_path):
        xmin,ymin = latlon2xy(self.zoom, self.minLat, self.minLng)
        xmax, ymax = latlon2xy(self.zoom, self.maxLat, self.maxLng)

        user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'

        headers = {'User-Agent': user_agent}

        for x in range(xmin, xmax):
            for y in range(ymin, ymax):

                url = None
                filename = None

                url = "https://khms1.google.com/kh/v=802?x=%d&y=%d&z=%d" % (x, y, self.zoom)
                filename = os.path.join(folder_path, "%d_%d_%d_s.jpg" % (self.zoom, x, y))

                if not os.path.exists(filename):

                    bytes = None

                    try:
                        req = urllib.request.Request(url, data=None, headers=headers)
                        response = urllib.request.urlopen(req)
                        bytes = response.read()
                    except Exception as e:
                        print
                        "--", filename, "->", e
                        sys.exit(1)

                    if str(bytes).startswith("<html>"):
                        print
                        "-- forbidden", filename
                        sys.exit(1)

                    print
                    "-- saving", filename

                    f = open(filename, 'wb')
                    f.write(bytes)
                    f.close()
    time.sleep(1 + random.random())


if __name__ == "__main__":
    tdl = TileDownloader(float(argv[1]), float(argv[2]), float(argv[3]), float(argv[4]), float(argv[5]))
    tdl.getTiles('./tiles')

