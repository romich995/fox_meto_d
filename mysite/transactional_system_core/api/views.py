from django.http import JsonResponse, HttpRequest
from rest_framework.parsers import JSONParser

from .serializers import TransactionSerializer
from transactional_system_core.tasks import sleep_time_emulates

def create_transfer(request: HttpRequest):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            sleep_time_emulates.delay()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

