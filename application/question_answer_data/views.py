import json

from django.shortcuts import render
import rest_framework as rf
from rest_framework.decorators import api_view

# Create your views here.

@api_view("POST")
def readQuestion(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
#    try:
#     res = Task.objects.filter(userID=body_data['id'])
#     ser_res = json.loads(serializers.serialize('json', res))
#     tasks = []
#     for i in ser_res:
#         tasks.append(i['fields'])
#     return JsonResponse(json.dumps(tasks), safe=False, status=status.HTTP_200_OK)
#
# except Task.DoesNotExist:
# return JsonResponse({'message': 'No one tasks'}, safe=False, status=status.HTTP_404_NOT_FOUND)





