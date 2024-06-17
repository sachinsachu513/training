from django.http import HttpResponseServerError


# class  SimpleMiddleware:
#     def __init__(self,get_response):
#         self.get_response=get_response
#
#     def __call__(self,request):
#
#         try:
#             response=self.get_response(request)
#         except Exception as e:
#             return self.process_exception(e)
#         return response
#
#     def process_exception(self,request,exception):
#         return HttpResponseServerError("Internal server Error")
