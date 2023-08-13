from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def index(request):
  if request.method == "GET":
    return render(request, "index.html")
  elif request.method == "POST":
    eqStr = request.POST.get("eq")
    eqStr = "".join(eqStr.split())
    opr = "*/+-"
    idx = eqStr.find("*")
    while idx != -1:
      lowbound = max([eqStr.find(s, 0, idx) for s in opr])
      highbound = min([eqStr.find(s, idx) for s in opr])
      
  