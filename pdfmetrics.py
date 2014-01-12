#fontmetrics.py - part of PDFgen - copyright Andy Robinson 1999
"""This contains pre-canned text metrics for the PDFgen package, and may also
be used for any other PIDDLE back ends or packages which use the standard
Type 1 postscript fonts.

Its main function is to let you work out the width of strings; it exposes a
single function, stringwidth(text, fontname), which works out the width of a
string in the given font. This is an integer defined in em-square units - each
character is defined in a 1000 x 1000 box called the em-square - for a 1-point high
character.  So to convert to points, multiply by 1000 and then by point size.

The AFM loading stuff worked for me but is not being heavily tested, as pre-canning
the widths for the standard 14 fonts in Acrobat Reader is so much more useful. One
could easily extend it to get the exact bounding box for each characterm useful for
kerning.


The ascent_descent attribute of the module is a dictionary mapping font names
(with the proper Postscript capitalisation) to ascents and descents.  I ought
to sort out the fontname case issue and the resolution of PIDDLE fonts to
Postscript font names within this module, but have not yet done so.


13th June 1999
"""

from __future__ import print_function

import string



StandardEnglishFonts = [
    'Courier', 'Courier-Bold', 'Courier-Oblique', 'Courier-BoldOblique',
    'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique',
    'Helvetica-BoldOblique',
    'Times-Roman', 'Times-Bold', 'Times-Italic', 'Times-BoldItalic',
    'Symbol','ZapfDingbats']

##############################################################
#
#                    PDF Metrics
# This is a preamble to give us a stringWidth function.
# loads and caches AFM files, but won't need to as the
# standard fonts are there already
##############################################################

widths = {'courier': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,600,600,600,600,0,600,600,600,600,600,600,600,600,0,600,0,600,600,600,600,600,600,600,600,0,600,600,0,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,0,600,0,0,0,0,600,600,600,600,0,0,0,0,0,600,0,0,0,600,0,0,600,600,600,600,0,0,600],'courier-bold': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,600,600,600,600,0,600,600,600,600,600,600,600,600,0,600,0,600,600,600,600,600,600,600,600,0,600,600,0,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,0,600,0,0,0,0,600,600,600,600,0,0,0,0,0,600,0,0,0,600,0,0,600,600,600,600,0,0,600],'courier-boldoblique': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,600,600,600,600,0,600,600,600,600,600,600,600,600,0,600,0,600,600,600,600,600,600,600,600,0,600,600,0,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,0,600,0,0,0,0,600,600,600,600,0,0,0,0,0,600,0,0,0,600,0,0,600,600,600,600,0,0,600],'courier-oblique': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,0,600,600,600,600,0,600,600,600,600,600,600,600,600,0,600,0,600,600,600,600,600,600,600,600,0,600,600,0,600,600,600,600,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,600,0,600,0,0,0,0,600,600,600,600,0,0,0,0,0,600,0,0,0,600,0,0,600,600,600,600,0,0,600],'helvetica': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,278,278,355,556,556,889,667,222,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,222,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,333,556,556,167,556,556,556,556,191,333,556,333,333,500,500,0,556,556,556,278,0,537,350,222,333,333,556,1000,1000,0,611,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,0,370,0,0,0,0,556,778,1000,365,0,0,0,0,0,889,0,0,0,278,0,0,222,611,944,611,0,0,834],'helvetica-bold': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,278,333,474,556,556,889,722,278,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,278,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,333,556,556,167,556,556,556,556,238,500,556,333,333,611,611,0,556,556,556,278,0,556,350,278,500,500,556,1000,1000,0,611,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,0,370,0,0,0,0,611,778,1000,365,0,0,0,0,0,889,0,0,0,278,0,0,278,611,944,611,0,0,834],'helvetica-boldoblique': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,278,333,474,556,556,889,722,278,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,333,333,584,584,584,611,975,722,722,722,722,667,611,778,722,278,556,722,611,833,722,778,667,778,722,667,611,722,667,944,667,667,611,333,278,333,584,556,278,556,611,556,611,556,333,611,611,278,278,556,278,889,611,611,611,611,389,556,333,611,556,778,556,556,500,389,280,389,584,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,333,556,556,167,556,556,556,556,238,500,556,333,333,611,611,0,556,556,556,278,0,556,350,278,500,500,556,1000,1000,0,611,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,0,370,0,0,0,0,611,778,1000,365,0,0,0,0,0,889,0,0,0,278,0,0,278,611,944,611,0,0,834],'helvetica-oblique': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,278,278,355,556,556,889,667,222,333,333,389,584,278,333,278,278,556,556,556,556,556,556,556,556,556,556,278,278,584,584,584,556,1015,667,667,722,722,667,611,778,722,278,500,667,556,833,722,778,667,778,722,667,611,722,667,944,667,667,611,278,278,278,469,556,222,556,556,500,556,556,278,556,556,222,222,500,222,833,556,556,556,556,333,500,278,556,500,722,500,500,500,334,260,334,584,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,333,556,556,167,556,556,556,556,191,333,556,333,333,500,500,0,556,556,556,278,0,537,350,222,333,333,556,1000,1000,0,611,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,0,370,0,0,0,0,556,778,1000,365,0,0,0,0,0,889,0,0,0,278,0,0,222,611,944,611,0,0,834],'symbol': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,250,333,713,500,549,833,778,439,333,333,500,549,250,549,250,278,500,500,500,500,500,500,500,500,500,500,278,278,549,549,549,444,549,722,667,722,612,611,763,603,722,333,631,722,686,889,722,722,768,741,556,592,611,690,439,768,645,795,611,333,863,333,658,500,500,631,549,549,494,439,521,411,603,329,603,549,549,576,521,549,549,521,549,603,439,576,713,686,493,686,494,480,200,480,549,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,620,247,549,167,713,500,753,753,753,753,1042,987,603,987,603,400,549,411,549,549,713,494,460,549,549,549,549,1000,603,1000,658,823,686,795,987,768,768,823,768,768,713,713,713,713,713,713,713,768,713,790,790,890,823,549,250,713,603,603,1042,987,603,987,603,494,329,790,790,786,713,384,384,384,384,384,384,494,494,494,494,0,329,274,686,686,686,384,384,384,384,384,384,494,494,790],'times-bold': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,250,333,555,500,500,1000,833,333,333,333,500,570,250,333,250,278,500,500,500,500,500,500,500,500,500,500,333,333,570,570,570,500,930,722,667,722,722,667,611,778,778,389,500,778,667,944,722,778,611,778,722,556,667,722,722,1000,722,722,667,333,278,333,581,500,333,500,556,444,556,444,333,500,556,278,333,556,278,833,556,500,556,556,444,389,333,556,500,722,500,500,444,394,220,394,520,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,333,500,500,167,500,500,500,500,278,500,500,333,333,556,556,0,500,500,500,250,0,540,350,333,500,500,500,1000,1000,0,500,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1000,0,300,0,0,0,0,667,778,1000,330,0,0,0,0,0,722,0,0,0,278,0,0,278,500,722,556,0,0,750],'times-bolditalic': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,250,389,555,500,500,833,778,333,333,333,500,570,250,333,250,278,500,500,500,500,500,500,500,500,500,500,333,333,570,570,570,500,832,667,667,667,722,667,667,722,778,389,500,667,611,889,722,722,611,722,667,556,611,722,667,889,667,611,611,333,278,333,570,500,333,500,500,444,500,444,333,500,556,278,278,500,278,778,556,500,500,500,389,389,278,556,444,667,500,444,389,348,220,348,570,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,389,500,500,167,500,500,500,500,278,500,500,333,333,556,556,0,500,500,500,250,0,500,350,333,500,500,500,1000,1000,0,500,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,944,0,266,0,0,0,0,611,722,944,300,0,0,0,0,0,722,0,0,0,278,0,0,278,500,722,500,0,0,750],'times-italic': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,250,333,420,500,500,833,778,333,333,333,500,675,250,333,250,278,500,500,500,500,500,500,500,500,500,500,333,333,675,675,675,500,920,611,611,667,722,611,611,722,722,333,444,667,556,833,667,722,611,722,611,500,556,722,611,833,611,556,556,389,278,389,422,500,333,500,500,444,500,444,278,500,500,278,278,444,278,722,500,500,500,500,389,389,278,500,444,667,444,444,389,400,275,400,541,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,389,500,500,167,500,500,500,500,214,556,500,333,333,500,500,0,500,500,500,250,0,523,350,333,556,556,500,889,1000,0,500,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,889,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,889,0,276,0,0,0,0,556,722,944,310,0,0,0,0,0,667,0,0,0,278,0,0,278,500,667,500,0,0,750],'times-roman': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,250,333,408,500,500,833,778,333,333,333,500,564,250,333,250,278,500,500,500,500,500,500,500,500,500,500,278,278,564,564,564,444,921,722,667,667,722,611,556,722,722,333,389,722,611,889,722,722,556,722,667,556,611,722,722,944,722,722,611,333,278,333,469,500,333,444,500,444,500,444,333,500,500,278,278,500,278,778,500,500,500,500,333,389,278,500,500,722,500,500,444,480,200,480,541,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,333,500,500,167,500,500,500,500,180,444,500,333,333,556,556,0,500,500,500,250,0,453,350,333,444,444,500,1000,1000,0,444,0,333,333,333,333,333,333,333,333,0,333,333,0,333,333,333,1000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,889,0,276,0,0,0,0,611,722,889,310,0,0,0,0,0,667,0,0,0,278,0,0,278,500,722,500,0,0,750],'zapfdingbats': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,278,974,961,974,980,719,789,790,791,690,960,939,549,855,911,933,911,945,974,755,846,762,761,571,677,763,760,759,754,494,552,537,577,692,786,788,788,790,793,794,816,823,789,841,823,833,816,831,923,744,723,749,790,792,695,776,768,792,759,707,708,682,701,826,815,789,789,707,687,696,689,786,787,713,791,785,791,873,761,762,762,759,759,892,892,788,784,438,138,277,415,392,392,668,668,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,732,544,544,910,667,760,760,776,595,694,626,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,788,894,838,1016,458,748,924,748,918,927,928,928,834,873,828,924,924,917,930,931,463,883,836,836,867,867,696,696,874,0,874,760,946,771,865,771,888,967,888,831,873,927,970,234]
}

ascent_descent = {'Courier': (629, -157), 'Courier-Bold': (626, -142), 'Courier-BoldOblique': (626, -142), 'Courier-Oblique': (629, -157), 'Helvetica': (718, -207), 'Helvetica-Bold': (718, -207), 'Helvetica-BoldOblique': (718, -207), 'Helvetica-Oblique': (718, -207), 'Symbol': (0, 0), 'Times-Bold': (676, -205), 'Times-BoldItalic': (699, -205), 'Times-Italic': (683, -205), 'Times-Roman': (683, -217), 'ZapfDingbats': (0, 0)}

def parseAFMfile(filename):
    """Returns an array holding the widths of all characters in the font.
    Ultra-crude parser"""
    alllines = open(filename, 'r').readlines()
    # get stuff between StartCharMetrics and EndCharMetrics
    metriclines = []
    between = 0
    for line in alllines:
        if string.find(string.lower(line), 'endcharmetrics') > -1:
            between = 0
            break
        if between:
            metriclines.append(line)
        if string.find(string.lower(line), 'startcharmetrics') > -1:
            between = 1

    # break up - very shaky assumption about array size
    widths = [0] * 255

    for line in metriclines:
        chunks = string.split(line, ';')

        (c, cid) = string.split(chunks[0])
        (wx, width) = string.split(chunks[1])
        #(n, name) = string.split(chunks[2])
        #(b, x1, y1, x2, y2) = string.split(chunks[3])
        widths[string.atoi(cid)] = string.atoi(width)

    # by default, any empties should get the width of a space
    for i in range(len(widths)):
        if widths[i] == 0:
            widths[i] == widths[32]

    return widths



class FontCache(object):
    """Load and cache font width information on demand.

    Font names converted to lower case for indexing.
    Public interface is stringwidth.
    """
    def __init__(self):
        global widths
        self.__widtharrays = widths


    def loadfont(self, fontname):
        filename = AFMDIR + os.sep + fontname + '.afm'
        print('cache loading', filename)
        assert os.path.exists(filename)
        widths = parseAFMfile(filename)
        self.__widtharrays[fontname] = widths


    def getfont(self, fontname):
        try:
            return self.__widtharrays[fontname]
        except:
            try:
                self.loadfont(fontname)
                return self.__widtharrays[fontname]
            except:
                # font not found, use Courier
                print('Font', fontname, 'not found - using Courier for widths')
                return self.getfont('courier')


    def stringwidth(self, text, font):
        widths = self.getfont(string.lower(font))
        w = 0
        for char in text:
            w = w + widths[ord(char)]
        return w


    def status(self):
        #returns loaded fonts
        return self.__widtharrays.keys()



TheFontCache = FontCache()

#expose the singleton as a single function
stringwidth = TheFontCache.stringwidth

