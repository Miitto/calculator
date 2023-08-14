from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.

def index(request):
  if request.method == "GET":
    return render(request, "index.html")
  elif request.method == "POST":
    eqStr = request.POST.get("eq") # Get equation from POST
    eqStr = "".join(eqStr.split()) # Remove all whitespace by splitting at whitespace then rejoining without
    
    opr = {
      '^': lambda x, y: x ** y,
      '*': lambda x, y: x * y,
      '/': lambda x, y: x / y,
      '+': lambda x, y: x + y,
      '-': lambda x, y: x - y
    }
    for op, operation in opr.items(): # iterate through the operators with op being the string of the symbol, and operation being a function to use the operator
      idx = eqStr.find(op) # Find first *
      while idx != -1: # Loop through all multiplication, if applicable
        
        #    Line 29 is a contracted version of the following
        # lowbound = []
        # for s in opr.keys():
        #   lowbound.append(eqStr.find(s, 0, idx))
        # lowbound = max(tmp)
        
        lowbound = max([eqStr.find(s, 0, idx) for s in opr.keys()]) # get operator before current
        
        #    Lines 33-34 is a contracted version of the following
        # highbound = []
        # for s in opr.keys():
        #   i = eqStr.find(s, idx + 1)
        #   if i != -1:
        #     highbound.append(i)
        # highbound = min(highbound) if len(highbound) > 0 else len(eqStr)
        
        tmp = [eqStr.find(s, idx+1) for s in opr.keys() if eqStr.find(s, idx+1) != -1] # store index list of operators to prevent duplicate processing
        highbound = min(tmp) if len(tmp) > 0 else len(eqStr) # check for next operator, else set to end of string
        prev = int(eqStr[max(lowbound, 0):idx]) # get number before current operator, and after previous operator
        post = int(eqStr[idx+1:highbound]) # get number after current operator, and before next operator
        eqStr = eqStr[:lowbound+1] + str(operation(prev, post)) + eqStr[highbound:] # recombine before the previous operator (inclusive) and after the next operator (inclusive) while replacing everything in the current opertation with the result

        idx = eqStr.find(op) # find any more multiplication for the next loop
    return JsonResponse({"ans": eqStr}) # return answer
      