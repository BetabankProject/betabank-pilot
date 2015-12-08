import logging

import simplejson as simplejson
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from basic_data.models import Request

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello, world. Pilot!!")


# TODO remove the decorator when done with testing
@csrf_exempt
def service_request(request):
    json = simplejson.loads(request.body)

    try:
        Request.objects.create(user=request.user, json=json)
        return HttpResponse(status=201)
    except KeyError as e:

        return JsonResponse({"error": "Missing attribute: " + str(e)}, status=400)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"

        logging.error(template.format(type(ex).__name__, ex.args))

        logging.error(ex)
        return HttpResponse(status=500)
