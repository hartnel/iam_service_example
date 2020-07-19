import sys
from concurrent.futures import ThreadPoolExecutor
import json
import requests
from django.conf import settings

api_base = settings.api_base

class AuditMiddleware:
    MAX_THREAD_POOL_WORKERS = 10
    def __init__(self, get_response):
        print("init biling middleware")
        self.get_response = get_response
        self.executor = ThreadPoolExecutor(
            max_workers=self.MAX_THREAD_POOL_WORKERS)

    def __call__(self, request):
        # the code for each request
        requestLen = float(sys.getsizeof(request.META["CONTENT_LENGTH"]))
        print("the request length ", requestLen, " bytes")
        response = self.get_response(request)
        # code for each response
        # 'Content-Disposition' is the content type of a downloadable file
        responseLen = float(sys.getsizeof(response)) + \
            float(sys.getsizeof(response.content))
        print("the response length ", responseLen, " bytes")
        totalDataSize = float('%.2f'%((requestLen + responseLen)/1024)) 
        futureData = self.executor.submit(
            self.postForAccounting, request, totalDataSize)
        return response

    def postForAccounting(self, requestInfo, dataInMOctets):
        if hasattr(requestInfo , "authUser"):
            UserIdGetFromRequest = requestInfo.authUser["sub"]
            apiUrlForAccounting = api_base+"accounting/comptes_users_user/"+UserIdGetFromRequest+"/"
            requestResult = requests.put(apiUrlForAccounting,json={"solde":dataInMOctets,"userId": UserIdGetFromRequest})
            print(requestResult.text)
            print("the client has consumed ", dataInMOctets, " Mo")


class JournallingMiddleware:
    MAX_THREAD_POOL_WORKERS = 10

    def __init__(self, get_response):
        print("init journalling middleware")
        self.get_response = get_response
        self.executor = ThreadPoolExecutor(
            max_workers=self.MAX_THREAD_POOL_WORKERS)

    def __call__(self, request):
        # the code for each request
        postParams = request.POST
        requestMethod = request.method
        requestContentType = request.content_type
        path = request.build_absolute_uri()
        response = self.get_response(request)

        journal = json.dumps({"requestMethod" : requestMethod, "requestUri": path, "requestContentType" : requestContentType, "postParams": postParams})
        #print("he did ", journal)
        # code for each response
        futureData = self.executor.submit(self.postForJournalling, request, journal)
        return response

    def postForJournalling(self, requestInfo, journal):
        if hasattr(requestInfo , "authUser"):
            UserIdGetFromRequest = requestInfo.authUser["sub"]
            apiUrlForJournalling = api_base+"journalling/journals/"
            requestResult = requests.post(apiUrlForJournalling,json={"record": journal,"userId": UserIdGetFromRequest})
            print(requestResult.text)
            #print("the client has done ", journal)
