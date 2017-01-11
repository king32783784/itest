#!/usr/bin/env python
# coding: utf-8

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import multiprocessing
import matplotlib.patches as mpatches
reload(sys)


# colour
colours = (
    '#4F81BD',  # Blue
    '#C0504D',  # Brown
    '#9BBB59',  # Green
    '#8064A2',  # Orange
    '#E46C0A'  # BlueViolet
    )

sysbenchcpu = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'CPU Execution time (sec)',
          'osnames': ('isoft-4.0-beta3', 'Fedora-23'),
          'subjects': ('1000', '2000', '3000'),
          'scores': [[10844, 28028, 48917], [11304, 28860, 50346]],
          'pngname': 'vsysbench.cpu.png'
           }
lmdouble = {
          'custom_font': '/usr/share/fonts/goffer.ttf',
          'title': 'Basic double (usec)',
          'osnames': ('isoft-4.0-beta3', 'Fedora-23'),
          'subjects': ('double\nadd', 'double\nmul', 'double\ndiv',
                       'double\nbogo'),
          'scores': ([1.39, 2.33, 10.34, 11.77], [0.98, 1.62, 8.74, 8.78],
                     [0.98, 1.62, 8.74, 8.78], [0.98, 1.62, 8.74, 8.78],
                     [0.98, 1.62, 8.74, 8.78]),
          'pngname': 'LMDOUBLE.png'
           }


def _setfigsize(scores):
    ''' 根据对比OS数量及对比项目的多少进行图表尺寸的调整'''
    step = 0.5
    base = 9
    figlong = base + len(scores[0]) / 2.0 * 0.5
    return figlong


def _setbarwidth(names):
    ''' 根据对比OS数量及对比项目的多少及图表的大小进
        行柱形a图宽度的调整'''
    base = 0.32
    rate = 0.9
    barwid = base * (rate ** len(names))
    return barwid


def _setymax(scores):
    '''根据项目数值范围进行Y轴数值的设定'''
    max = 0
    for i in scores:
        for j in i:
            if j > max:
                max = j
    return max * 1.75


def _setlegend(scores):
    if len(scores[0]) < 5:
        return 0.7
    else:
        return 0.75


def graphing(names, subjects, scores, title, custom_font):
    font_size = 10  # 字体大小
    fig_size = (_setfigsize(scores), 4)  # 图表大小 *
    mpl.rcParams['font.size'] = font_size  # 更新字体大小
    mpl.rcParams['figure.figsize'] = fig_size  # 更新图表大小
    bar_width = _setbarwidth(names)  # 设置柱形图宽度 *
    index = np.arange(len(scores[0]))
    for i in range(0, len(names)):
        rects = plt.bar(index + i * bar_width, scores[i], bar_width,
                color=colours[i], label=names[i])
 #       autolabel(rects) # 柱状图添加数字显示
    # X轴标题
    plt.xticks(index + bar_width, subjects, fontproperties=custom_font)
    # Y轴范围
    maxscore = _setymax(scores)
    plt.ylim(ymax=maxscore, ymin=0)
    # 图表标题
    plt.title(u'%s' % title, fontproperties=custom_font)
    # 图例显示在右侧
#    plt.legend(bbox_to_anchor=(_setlegend(), 0.9), loc=2,
#                   prop=custom_font,  borderaxespad=0.)
    # 图例显示在上部
    plt.legend(bbox_to_anchor=(0., 0.9, 1., 0.102), loc=1,
               ncol=2, mode="expand", borderaxespad=0.1)


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1.1*height, height,
                 ha='center', va='bottom')  


def mkchart(chartargs):
    plt.figure()
    custom_font = mpl.font_manager.FontProperties(fname='%s' %
                  chartargs['custom_font'])
    names = chartargs['osnames']   # 对比OS名称 *
    subjects = chartargs['subjects']  # 对比项目 *
    scores = chartargs['scores']  # 项目数值*
    title = chartargs['title']
    pngname = chartargs['pngname']
    graphing(names, subjects, scores, title, custom_font)
    plt.savefig(pngname)


def mkcontrol(chartargs):
    p = multiprocessing.Process(target=mkchart, args=(chartargs,))
    p.start()
# test1
#mkchart(sysbenchcpu)
#mkchart(lmdouble)
# test2
#mkcontrol(sysbenchcpu)
#mkcontrol(lmdouble)
# samples
