import json
from api.tasks import CloneRepoTask, NuclieTestingTask
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from authenticate.tasks import sendVulnerabilityEmailTask, sendMarketingEmailTask, sendSubscriptionEmailTask, sendInvoiceEmailTask, sendWaitlistEmailTask
from .models import *
from .serializers import *


# Create your views here.
class SendAlertEmailAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            email= request.data.get('email')
            sendVulnerabilityEmailTask.delay(email)
            return Response({'message':'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SendMarketingEmailAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            email= request.data.get('email')
            sendMarketingEmailTask.delay(email)
            return Response({'message':'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SendSubscriptionEmailAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            email= request.data.get('email')
            sendSubscriptionEmailTask.delay(email)
            return Response({'message':'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SendInvoiceEmailAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            email= request.data.get('email')
            sendInvoiceEmailTask.delay(email)
            return Response({'message':'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class SendWaitlistEmailAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def post(self, request):
        try:
            email= request.data.get('email')
            sendWaitlistEmailTask.delay(email)
            return Response({'message':'Email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProjectAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def get(self, request,id):
        try:
            user_id= id
            data= Project.objects.filter(user_id=user_id)
            serializer= ProjectSerializer(data, many=True)
            if serializer.data:
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'message':'Project not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            serializer= ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, id):
        try:
            data= Project.objects.get(pk=id)
            serializer= ProjectSerializer(data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # def delete(self, request, pk):
    #     try:
    #         data= Project.objects.get(pk=pk)
    #         data.delete()
    #         return Response({'message':'Data deleted successfully'}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TestingAPIView(APIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    def get(self, request,id):
        try:
            data= Testing.objects.filter(user_id=id)
            serializer= TestingSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            if request.data.get('user_id') is None or request.data.get('user_id') == '':
                return Response({'message':'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('project_id') is None or request.data.get('project_id') == '':
                return Response({'message':'project_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('source_url') is None or request.data.get('source_url') == '':
                return Response({'message':'source_url is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('repo_username') is None or request.data.get('repo_username') == '':
                return Response({'message':'repo_username is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('repo_token') is None or request.data.get('repo_token') == '':
                return Response({'message':'repo_token is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('repo_type') is None or request.data.get('repo_type') == '':
                return Response({'message':'repo_type is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('testing_type') is None or request.data.get('testing_type') == '':
                return Response({'message':'testing_type is required'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('testing_type') not in ['LLM', 'Nuclie', 'CVEscan']:
                return Response({'message':'Invalid testing type'}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('repo_type') not in ['Github', 'Gitlab', 'Bitbucket']:
                return Response({'message':'Invalid repo type'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_obj= User.objects.get(pk=request.data.get('user_id'))
            project_obj= Project.objects.get(pk=request.data.get('project_id'))
            # save data to database
            testing_obj = Testing.objects.create(
                user_id= user_obj,
                project_id= project_obj,
                testing_type= request.data.get('testing_type'),
                source_url= request.data.get('source_url')
            )
            testing_id = testing_obj.pk 
            request.data['test_id'] = testing_id
            if request.data.get('testing_type') == 'LLM' or request.data.get('testing_type') == 'GitLeaks' or request.data.get('testing_type') == 'CVEscan':
                CloneRepoTask.delay(json.dumps(request.data))
            elif request.data.get('testing_type') == 'Nuclie':
                NuclieTestingTask.delay(json.dumps(request.data))
            
            return Response({'message':'Data saved successfully'}, status=status.HTTP_200_OK)
            

            # old code
            # serializer= TestingSerializer(data=request.data)
            # if serializer.is_valid():
            #     serializer.save()
            #     # check the testing type

            #     # if testing type is LLM or gitleaks then call LLMtesting background task
            #     if request.data.get('testing_type') == 'LLM':
            #         CloneRepoTask.delay(serializer.data)
                    

            #     # if testing type is Nuclie then call NuclieTesting background task
            #     elif request.data.get('testing_type') == 'Nuclie':
            #         NuclieTestingTask.delay(serializer.data)

            #     serializer.save()
            #     return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # def put(self, request, pk):
    #     try:
    #         data= Testing.objects.get(pk=pk)
    #         serializer= TestingSerializer(data, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # def delete(self, request, pk):
    #     try:
    #         data= Testing.objects.get(pk=pk)
    #         data.delete()
    #         return Response({'message':'Data deleted successfully'}, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)