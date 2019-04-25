from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.conf import settings
import json

# Create your views here.
def closest(arr, val):
    keys=[]
    for x in arr:
        try:
            keys.append(float(x))
        except:
            pass
    return get_closest_value(keys, val)

def get_closest_value(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    # edge case - last or above all
    if target >= arr[n - 1]:
        return arr[n - 1]
    # edge case - first or below all
    if target <= arr[0]:
        return arr[0]
    # BSearch solution: Time & Space: Log(N)

    while left < right:
        mid = (left + right) // 2  # find the mid
        if target < arr[mid]:
            right = mid
        elif target > arr[mid]:
            left = mid + 1
        else:
            return arr[mid]

    if target < arr[mid]:
        return find_closest(arr[mid - 1], arr[mid], target)
    else:
        return find_closest(arr[mid], arr[mid + 1], target)

def find_closest(val1, val2, target):
    return val2 if target - val1 >= val2 - target else val1

@api_view(["GET"])
def fetch(request):
    try:
        seconds=float(request.GET['seconds'])
        with open('resources/backend.json') as f:
            miliseconds=seconds*1000.0
            data=json.load(f)
            close=closest(data.keys(), miliseconds)
            index=data[str(close)]
            ans={"input":miliseconds, "closest":close, "index":index, "height":data["height"], "width":data["width"]}
            return JsonResponse(ans)
    except:
        return Response("Error!!", status.HTTP_400_BAD_REQUEST)

def index(request):
    #context={"test":"this is test statement"}
    return render(request, 'fetchData/index.html')#, context)