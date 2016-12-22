import re


class ModifyFile():
    def __init__(self, newcontent, oldcontent, newfile, oldfile):
        self.newcontent = newcontent
        self.oldcontent = oldcontent
        self.newfile = newfile
        self.oldfile = oldfile
        self._modifyfile()

    def _modifyfile(self):
        fp = open(self.oldfile, 'r')
        filelines = fp.readlines()
        fp.close()
        fp = open(self.newfile, 'w')
        for eachline in filelines:
            filebuffer = re.sub(self.oldcontent, self.newcontent, eachline)
            fp.writelines(filebuffer)
        fp.close()

# test case
# ip = ModifyFile("--ip=192.168.32.48", "--ip=192.168.32.47", "ks.cfg")
