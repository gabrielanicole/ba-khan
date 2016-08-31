""" """
from django.shortcuts import render,HttpResponseRedirect,render_to_response, redirect, HttpResponse
from django.template.context import RequestContext
from bakhanapp.forms import AssesmentConfigForm,AssesmentForm
from django.contrib.auth import  login,authenticate,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Count
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


from django import template
from bakhanapp.models import Assesment_Skill
from bakhanapp.models import Administrator
from bakhanapp.models import Teacher,Class_Subject
from bakhanapp.models import Schedule

register = template.Library()
from configs import timeSleep

import json


##
## @brief      Gets the schedules.
##
## @param      request  The request
##
## @return     The schedules.
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def getSchedules(request):
    request.session.set_expiry(timeSleep)
    try:
        teacher = Teacher.objects.get(email=request.user.email)
    except:
        return render_to_response('horario.html', context_instance=RequestContext(request))
    schedules = Schedule.objects.filter(id_institution_id=teacher.id_institution_id).order_by('start_time')
    teachers = Teacher.objects.filter(id_institution_id=teacher.id_institution_id)
    return render_to_response('horario.html', {'schedules': schedules, 'teachers': teachers}, context_instance=RequestContext(request))


##
## @brief      Deletes a schedule.
##
## @param      request  The request
##
## @return     HttpResponse
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def deleteSchedule(request):
	try:
	    request.session.set_expiry(timeSleep)
	    user = Teacher.objects.get(email=request.user.email)
	    if request.is_ajax():
	        if request.method == 'POST':
	            json_str = json.loads(request.body)
	            sched = Schedule.objects.filter(name_block=json_str["schBlock"], start_time=json_str["schStart"], end_time=json_str["schEnd"],id_institution_id=user.id_institution_id).delete()
	            return HttpResponse("Bloque eliminado correctamente")

	    return HttpResponse("Error al eliminar")
	except Exception as e:
		print e


##
## @brief      Create a schedule
##
## @param      request  The request
##
## @return     HttpResponse
##
@permission_required('bakhanapp.isAdmin', login_url="/")
def newSchedule(request):
    request.session.set_expiry(timeSleep)
    user = Teacher.objects.get(email=request.user.email)
    if request.method == 'POST':
        args = request.POST
        try:
            schedule = Schedule.objects.create(name_block=args['block'],
                start_time=args['start'],
                end_time=args['end'],
                id_institution_id=user.id_institution_id)
            return HttpResponse("Bloque guardado correctamente")
        except Exception as e:
        	print e
        	return HttpResponse("Error al guardar")
    return HttpResponse("Error al guardar")