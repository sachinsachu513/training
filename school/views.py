from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentName, School
from .serializer import StudentSerializer,schoolserializer


# Create your views here.
class student(APIView):

 def post(self, request):

  if request.method == 'POST':
    action = request.data['action']

    if action == 'add_student':
      try:
        school_name = request.data['student_school']
        school = School.objects.get(name=school_name)
      except School.DoesNotExist:
        return Response({'error': 'school does not exist'}, status=status.HTTP_400_BAD_REQUEST)

      student_name = request.data['student_name']
      student_age = request.data['student_age']
      gender = request.data['gender']

      if StudentName.objects.filter(name=student_name, school=school).exists():
         return Response({'error': 'The Student already exists in this school'},
                                    status=status.HTTP_400_BAD_REQUEST)
      StudentName.objects.create(name=student_name, age=student_age, gender=gender, school=school)
      return Response({"sucess": "student was sucessfully added"}, status=status.HTTP_201_CREATED)


    elif action == 'update_student':
        student_id = request.data['student_id']
        student_name = request.data["student_name"]
        gender = request.data["gender"]

        try:
            school_name = request.data['student_school']
            student_age = request.data['student_age']
            school = School.objects.get(name=school_name)
        except School.DoesNotExist:
                return Response({'error': 'school does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        StudentName.objects.filter(id=student_id).update(name=student_name, age=student_age, gender=gender,
                                                                 school=school)
        return Response({'success': "Student data updated successfully"}, status=status.HTTP_200_OK)


    elif action == 'add_school':
       school_name = request.data["school_name"]
       school_location = request.data["school_location"]
       if School.objects.filter(name=school_name):
        return Response({'error': 'The School already exists in this school'},
                                    status=status.HTTP_400_BAD_REQUEST)
       else:
         School.objects.create(name=school_name, location=school_location)
         return Response({'success': "School data added successfully"}, status=status.HTTP_200_OK)

    elif action == 'delete_student':
       try:
         student_id = request.data['student_id']
         obj = StudentName.objects.get(id=student_id)
         obj.delete()
         return Response({'success': "Student data deleted successfully"}, status=status.HTTP_200_OK)
       except StudentName.DoesNotExist:
        return Response({'error': "Student id does not exist"}, status=status.HTTP_400_BAD_REQUEST)


    elif action == 'View_student':
        obj = StudentName.objects.all()
        ser = StudentSerializer(obj, many=True)
        return Response(ser.data)


    elif action=='View_school':
        obj=School.objects.all()
        ser=schoolserializer(obj,many=True)
        return Response(ser.data)

    elif action=='update_school':
        school_id=request.data["school_id"]
        location=request.data["school_location"]


        school_name = request.data["school_name"]
        if School.objects.filter(name=school_name):
          return Response({'error': "School does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        else:
         School.objects.filter(id=school_id).update(name=school_name, location=location)

         return Response({'sucess': "School updated Sucessfully"}, status=status.HTTP_400_BAD_REQUEST)









# {
#     "action": "update_student",
#     "student_id": 1,
#     "student_name": "shanil",
#     "student_age": 45,
#     "gender": "male",
#     "student_school": "Holy queen"
# }
