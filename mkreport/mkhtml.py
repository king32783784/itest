import os
import sys
import shutil
from subprocess import call, PIPE, Popen
from mkchart import *
from temp_html import *


class MkHtml(object):
    def __init__(self, oslist, testitem, resultdata):
        self.oslist = oslist
        self.itemlist = testitem
        self.resultdata = resultdata

    def wraptreatment(self, length, charters):
        temp = ''
        t = 0
        for i, charter in enumerate(charters, 1):
            if i % length == 0:
                temp = temp + charters[t:i] + "\n"
                t = i
        temp = temp + charters[t:]
        return temp

    def _mkchartdata(self, itemmddata, offset):
        for osname in self.oslist:
            ostest = self.wraptreatment(30, osname)
            chartditlist[self.itemlist][offset]['osnames'].append(ostest)
        chartditlist[self.itemlist][offset]['scores'] = itemmddata
        if os.path.isdir("current-report/svgfile/") is not True:
            try:
                retcode = call("mkdir current-report/svgfile", shell=True)
                if retcode < 0:
                    print >> sys.stderr, "Child was terminated by signal", -retcode
                else:
                    print >>sys.stderr, "Child returned", retcode
            except OSError as e:
                print >>sys.stderr, "Execution failed:", e
        return chartditlist[self.itemlist][offset]

    def _mkchart(self, mdfile, charttmpdict):
        mkcontrol(charttmpdict)
        f = open(mdfile, 'a+')
        a = charttmpdict['pngname']
        f.write("\n")
        f.write("![](./%s)" % (a.split("/")[1] + '/' + a.split("/")[2]))
        f.close()

    def _mkmdfile(self, mdfile, itemmdtitle, itemmddata, offset):
        f = open(mdfile, 'a+')
        f.write(itemmdtitle)
        f.write("\n")
        for i, osname in enumerate(self.oslist):
            datatemp = ""
            for datalist in itemmddata[i]:
                datatemp = datatemp + '|' + '%s' % datalist
            f.write("%s" % self.oslist[i] + datatemp + "|" + "\n")
        f.close()
        charttmpdict = self._mkchartdata(itemmddata, offset)
        self._mkchart(mdfile, charttmpdict)

    def _mkresult(self):
        mdfile = os.path.join('current-report', 'src.md')
        step = len(self.oslist)
        finaldata = []
        datatemp = []
        for i, data in enumerate(self.resultdata[self.itemlist]):
            datatemp.append(data)
            if step > 1:
                if i % step == step-1:
                    finaldata.append(datatemp)
                    datatemp = []
            else:
                finaldata.append(datatemp)
                datatemp = []
        for i, itemmdtitle in enumerate(mdtitle[self.itemlist]):
            self._mkmdfile(mdfile, itemmdtitle, finaldata[i], i)

mdtitle = {'sysbenchcpu': md_syscpu, 'sysbenchmem': md_sysmem, 'iozone': md_iozone, 'pingpong':
           md_pingpong, 'lmbench': md_lmbench, 'stream': md_stream, 'Perf_graphics': md_graphics,
           'unixbench': md_system, 'Perf_browser': md_browser}
chartditlist = {'sysbenchcpu': chart_syscpu, 'sysbenchmem': chart_sysmem, 'iozone': chart_iozone,
                'pingpong': chart_pingpong, 'lmbench': chart_lmbench, 'stream': chart_stream,
                'Perf_graphics': chart_graphics, 'unixbench': chart_system, 'Perf_browser': chart_browser}


def mkhtml(htmldata, itemlist, oslist):
    if os.path.isdir("current-report") is not True:
        try:
            retcode = call("mkdir current-report", shell=True)
            if retcode < 0:
                print >> sys.stderr, "Child was terminated by signal", -retcode
            else:
                print >>sys.stderr, "Child returned", retcode
        except OSError as e:
            print >>sys.stderr, "Execution failed:", e
    for testitem in itemlist:
        mkhtml = MkHtml(oslist, testitem, htmldata)
        mkhtml._mkresult()
    shutil.copy("style.css", "current-report")
    try:
        retcode = call("pandoc --toc -c ./style.css -o current-report/test.html \
                       current-report/src.md", shell=True)
        if retcode < 0:
            print >> sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e


mkhtml({'Perf_stream': [], 'sysbenchcpu': [[9.94, 24.92, 42.09]], 'Perf_thread': [], 'Perf_system': [], 'Perf_kernel': [], 'Perf_io': [], 'Perf_browser': [], 'Perf_graphics': [], 'Perf_mem': []}, ['sysbenchcpu'], ['Fedora_24'])
