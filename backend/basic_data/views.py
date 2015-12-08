import logging

import simplejson as simplejson
from django.http import HttpResponse
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
        Request.objects.create(user=request.user,
                               title=json['title'],
                               description=json['title'],
                               hours=json['hours'],
                               category=json['category'])
        return HttpResponse(status=201)
    except Exception as e:
        logging.error(e)
        return HttpResponse(status=500)
