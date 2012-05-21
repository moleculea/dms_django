# -*- coding: utf-8 -*-
# HTTP
from django.http import HttpResponse
from django.shortcuts import render_to_response

# Models
from agenda.models import isDateEmpty


"""
index()
# url: /agenda/

"""
def index(request):
    
    context = {}
    return render_to_response('agenda/agenda.html',context)

"""
year_view()

"""
def year_view(request,year):
    import datetime
    year = int(year)
    months = [] # List of the first days of 12 months in this year
    
    today = datetime.date.today()
    
    for i in range(1,13):
        day = datetime.date(year,i,1)
        months.append(day)
    
    context = {'year':year,'months':months,'today':today}
    return render_to_response('agenda/agenda_year.html',context)


"""
month_view()

"""
def month_view(request,year,month):
    user_id = request.user.id
    import calendar,datetime
    agenda = calendar.Calendar(6)
    year = int(year)
    month = int(month)
    # Requested date
    date = datetime.date(year,month,1)
    monthsdays = agenda.monthdays2calendar(year,month)
    
    prev = prevMonth(date)
    next = nextMonth(date)
    # Generate month table
    htmltb = ""
    htmltb += "<table class=\"agendatable\"><tr>\n"
    htmltb += "<th>SUN</th><th>MON</th><th>TUE</th><th>WED</th><th>THU</th><th>FRI</th><th>SAT</th>"
    htmltb += "</tr>\n"
    for weeklist in monthsdays:
        htmltb +=  "<tr>"
        for datetuple in weeklist:
            day = datetuple[0]
            weekday = datetuple[1] # 0 is Monday, 6 is Sunday
            if day == 0:
                htmltb += "<td>&nbsp;</td>"
            else:
                # Today
                if datetime.date(year,month,day) == datetime.date.today():
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_today'>%s</span></a></td>"%(year,month,day,day)
                    
                # Not empty date
                elif not isDateEmpty(user_id,datetime.date(year,month,day)):
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_notempty'>%s</span></a></td>"%(year,month,day,day)
                    
                # Weekend date    
                elif weekday == 5 or weekday ==6:
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_weekend'>%s</span></a></td>"%(year,month,day,day)
                # Normal date
                else:
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_day'>%s</span></a></td>"%(year,month,day,day)
                    
        htmltb += "</tr>"
        
    htmltb += "</table>\n"

    context = {'htmltb':htmltb,'date':date,'prev':prev,'next':next}
    return render_to_response('agenda/agenda_month.html',context)

"""
prevMonth()
Calculate the date in the previous month
date is datetime.date() instance
"""
def prevMonth(date):
    from dateutil.relativedelta import relativedelta
    prev = date + relativedelta( months = -1 )
    return prev


"""
nextMonth()
Calculate the date in the next month
date is datetime.date() instance
"""

def nextMonth(date):
    from dateutil.relativedelta import relativedelta
    next = date + relativedelta( months = +1 )
    return next