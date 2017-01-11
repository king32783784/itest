import os
import urllib2
import urllib


def downloadfile(local_dir, url, filename):
    local_dir = os.path.join(local_dir, filename)
    url = os.path.join(url, filename)
    try:
        response = urllib2.urlopen(url)
        urllib.urlretrieve(url, local_dir)
        return local_dir
    except:
        print '\tError download the file:', local_dir
        exit(1)
