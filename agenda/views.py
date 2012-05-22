# -*- coding: utf-8 -*-
# HTTP
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

# Template
from django.template import RequestContext

# Models
from agenda.models import isDateEmpty, getPeriod, changeDailyPeriod, changeTypePeriod

# login_required decorator
from django.contrib.auth.decorators import login_required

"""
index()
# url: /agenda/

"""
@login_required
def index(request):
    
    context = {}
    return render_to_response('agenda/agenda.html',context)

"""
year_view()

"""
@login_required
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
@login_required
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
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_today'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)
                    
                # Not empty date
                elif not isDateEmpty(user_id,datetime.date(year,month,day)):
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_notempty'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)
                    
                # Weekend date    
                elif weekday == 5 or weekday ==6:
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_weekend'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)
                # Normal date
                else:
                    htmltb += "<td><a href='/agenda/%s/%s/%s/'><span class='agenda_day'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)
                    
        htmltb += "</tr>"
        
    htmltb += "</table>\n"

    context = {'htmltb':htmltb,'date':date,'prev':prev,'next':next}
    return render_to_response('agenda/agenda_month.html',context)


"""
day_view()

"""
@login_required
def day_view(request,year,month,day,type=None,action=None,period=None):
    
    # Render the day view
    if action == None and period == None:
        year = int(year)
        month = int(month)
        day = int(day)
        user_id = request.user.id
        daily_period_status = [0 for i in range(0,16)]
        pref_period = [1 for i in range(0,16)]
        best_period = [1 for i in range(0,16)]
        import datetime
        date = datetime.date(year,month,day)
        
        if isDateEmpty(user_id, date):
            # Render an empty date for daily period
            pass
            
        else:
            agenda = getPeriod(user_id, date)
            dp = agenda.daily_period
            pp = agenda.pref_period
            bp = agenda.best_period
            if dp:
                daily_period_status = dailyPeriod2list(dp)
            if pp != None:
                pref_period = dailyPeriod2list(pp)
            if bp != None:
                best_period = dailyPeriod2list(bp)
            
        prev = prevDay(date)
        next = nextDay(date)
        
        time = [str(i).zfill(2) for i in range(6,23)]
        context = {'date':date,'daily_period_status':daily_period_status,'pref_period':pref_period,'best_period':best_period,'time':time,'prev':prev,'next':next}
        
        return render_to_response('agenda/agenda_day.html',context, context_instance=RequestContext(request))
    
    # Update agenda
    else:
         # Update agenda daily period and redirect
        if type == None:
            year = int(year)
            month = int(month)
            day = int(day)
            period = int(period)
            user_id = request.user.id
            
            import datetime
            date = datetime.date(year,month,day)
            
            # Submit change
            changeDailyPeriod(user_id, date, action, period)
            
            # Redirect 
            return HttpResponseRedirect("/agenda/%s/%s/%s/"%(year,str(month).zfill(2),str(day).zfill(2)))
        
        # Update pref_period and best_period, and then redirect
        else:
            year = int(year)
            month = int(month)
            day = int(day)
            period = int(period)
            user_id = request.user.id
            
            import datetime
            date = datetime.date(year,month,day)

            changeTypePeriod(user_id, date, action, period, type)
            
            #return HttpResponse((type,action,period,date,isDateEmpty(user_id, date)))
            
            # Redirect 
            return HttpResponseRedirect("/agenda/%s/%s/%s/"%(year,str(month).zfill(2),str(day).zfill(2)))

"""
##################

Non-view functions

"""
"""
prevDay()
Calculate the previous date
"""
def prevDay(date):
    from dateutil.relativedelta import relativedelta
    prev = date + relativedelta( days = -1 )
    return prev


"""
nextDay()
Calculate the previous date
"""
def nextDay(date):
    from dateutil.relativedelta import relativedelta
    next = date + relativedelta( days = +1 )
    return next


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

"""
dailyPeriod2list()
Convert a daily period (integer) into a 16-element list, each representing a status with 0 or 1
"""
def dailyPeriod2list(daily_period):
    bstring = bin(daily_period)
    string = bstring[2:]
    
    # Make sure the string is 16-digit, padding with 0
    string = string.zfill(16)
    list = [int(i) for i in string]
    return list