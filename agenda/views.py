# -*- coding: utf-8 -*-

from django.http import HttpResponse

def show(request,year,month):
    import calendar
    agendaCalendar = calendar.Calendar(6)
    """
    for i in agendaCalendar.itermonthdays2(2012,3):
        print i
    """
    #year = 2012
    #month = 3
    monthsdays = agendaCalendar.monthdays2calendar(int(year),int(month))
    htmltb = "<html><style>td {border: 1px solid silver}</style><body>"
    htmltb += "<table cellpadding = '4'><tr>\n"
    htmltb += u"<td>日</td>"
    htmltb += u"<td>一</td>"
    htmltb += u"<td>二</td>"
    htmltb += u"<td>三</td>"
    htmltb += u"<td>四</td>"
    htmltb += u"<td>五</td>"
    htmltb += u"<td>六</td>"
    htmltb += "</tr>\n"
    for weeklist in monthsdays:
        htmltb +=  "<tr>"
        for datetuple in weeklist:
            if datetuple[0] == 0:
                htmltb += "<td>&nbsp;</td>"
            else:
                htmltb += "<td><a href='/%s%s%s'>"%(year,month,str(datetuple[0])) + str(datetuple[0]) + "</a></td>"
        htmltb += "</tr>"
    htmltb += "</table>\n"
    htmltb += "</body></html>\n"
    return HttpResponse(htmltb)