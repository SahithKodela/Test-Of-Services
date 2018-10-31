# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login as login_aut
from forms import LoginForm,Reg
from django import forms
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import PostSerializer, RegSerializer
from rest_framework.response import Response
from .models import Register
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.decorators import api_view
from django_otp.oath import TOTP
from django_otp.util import random_hex
import time
import urllib

class TOTPVerification:

    def __init__(self):
        # secret key that will be used to generate a token,
        # User can provide a custom value to the key.
        self.key = random_hex(20)
        # counter with which last token was verified.
        # Next token must be generated at a higher counter value.
        self.last_verified_counter = -1
        # this value will return True, if a token has been successfully
        # verified.
        self.verified = False
        # number of digits in a token. Default is 6
        self.number_of_digits = 6
        # validity period of a token. Default is 30 second.
        self.token_validity_period = 35

    def totp_obj(self):
        # create a TOTP object
        totp = TOTP(key=self.key,
                    step=self.token_validity_period,
                    digits=self.number_of_digits)
        # the current time will be used to generate a counter
        totp.time = time.time()
        return totp

    def generate_token(self):
        # get the TOTP object and use that to create token
        totp = self.totp_obj()
        # token can be obtained with `totp.token()`
        token = str(totp.token()).zfill(6)
        return token

    def verify_token(self, token, tolerance=0):
        try:
            # convert the input token to integer
            token = int(token)
        except ValueError:
            # return False, if token could not be converted to an integer
            self.verified = False
        else:
            totp = self.totp_obj()
            # check if the current counter value is higher than the value of
            # last verified counter and check if entered token is correct by
            # calling totp.verify_token()
            if ((totp.t() > self.last_verified_counter) and
                    (totp.verify(token, tolerance=tolerance))):
                # if the condition is true, set the last verified counter value
                # to current counter value, and return True
                self.last_verified_counter = totp.t()
                self.verified = True
            else:
                # if the token entered was invalid or if the counter value
                # was less than last verified counter, then return False
                self.verified = False
        return self.verified

    def sms(self,message,mobile):
        url = "http://www.smscountry.com/smscwebservice_bulk.aspx"
        values = {'user' : 'powertex',
                        'passwd' : 'Powertexgst1',
                        'message':message,
                        'mobilenumber':mobile,
                        'mtype':'N',
                         'DR':'Y'
                         }
        data=urllib.urlencode(values)
        data = data.encode('utf-8')
        f = urllib.urlopen(url, data)
        print f.read().decode('utf-8')


@api_view(['POST',])
def otp_gen(request):
    if request.method == 'POST':
        phone1 = TOTPVerification()
        phno = request.data
        generated_token = phone1.generate_token()
        pho = phone1.sms(generated_token, phno)
        if pho:
            return Response({"message": generated_token, "data": request.data, "ststus":'Successful'})
        return Response({"message": generated_token, "data": request.data, "ststus": 'Failure'})
    return Response({"message": "Hello, world!"})

@api_view(['POST,'])
def otp_ver(request):
    if request.method == 'POST':
        phone1 = TOTPVerification()
        token = request.data
        if phone1.verify_token(token):
            return Response({"message": 'Your Successfully ', "data": request.data, "ststus": 'Successful'})
        return Response({"message": 'unable to pair', "data": request.data, "ststus": 'Failure'})

class SerializerUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PostSerializer

class SerializerReg(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = RegSerializer

def login(request):
    form= LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        if user:
            request.session['username'] = username
        login_aut(request, user)
        return HttpResponse("<br><br><center><h1>Logged in </h1></center>")
    return render(request,'login.html',{'form':form,'title':'Login'} )
    # Create your views here.

def reg(request):
    form = Reg(request.POST or None)
    if form.is_valid():
        password = form.cleaned_data.get('password')
        re_enter_password = form.cleaned_data.get('re_enter_password')

        user = form.save(commit=False)
        if re_enter_password==password:
            px =password
            user.set_password(px)
            user.save()
            return redirect ('/')
    return render(request, 'login.html', {'form': form, 'title': 'register'})


class Pro_User(APIView):
   # authentication_classes = []
    #permission_classes = []
    def get(self, request, format=None):
        user=User.objects.all()
        reg = Register.objects.all()
        usernames = PostSerializer(user,many=True)
        re_ser= RegSerializer(reg, many=True)

        return Response({'user data':usernames.data,'reg data': re_ser.data})
