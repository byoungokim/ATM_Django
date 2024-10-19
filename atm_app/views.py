from django.http import JsonResponse

def atm(request):
    return JsonResponse({"message":"dummy api output"})
