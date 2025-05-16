from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import UserCreationSerializer, ExpenseSerializer
from rest_framework import authentication, permissions
from myapp.models import Expense
from rest_framework import serializers
from api.permissions import IsOwnerPermissionRequired
from django.db.models import Sum
# Create your views here.

class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer_instance=UserCreationSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
class ExpenseCreateView(APIView):

    def get(self,request,*args,**kwargs):
        authentication_class=[authentication.BasicAuthentication]
        permission_classes=[permissions.IsAuthenticated]
        qs=Expense.objects.filter(owner=request.user)
        serializer_instance=ExpenseSerializer(qs,many=True)
        return Response(data=serializer_instance.data)


    def post(self,request,*args,**kwargs):
        authentication_class=[authentication.BasicAuthentication]
        permission_classes=[permissions.IsAuthenticated]
        serializer_instance=ExpenseSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save(owner=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
class ExpenseRetrieceUpdateDeleteView(APIView):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[IsOwnerPermissionRequired]
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        expense_instance=get_object_or_404(Expense,id=id)
        self.check_object_permissions(request,expense_instance)

        serializer_instance=ExpenseSerializer(expense_instance)
        return Response(data=serializer_instance.data)
    
    def delete(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        expense_instance=get_object_or_404(Expense,id=id)

        self.check_object_permissions(request,expense_instance)
        expense_instance.delete()
        return Response(data={'message':'deleted'})
    
    def put(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        expense_instance=get_object_or_404(Expense,id=id)
        self.check_object_permissions(request,expense_instance)
        serializer_instance=ExpenseSerializer(data=request.data,instance=expense_instance)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
class ExpenseSummaryView(APIView):
    def get(self,request,*args,**kwargs):
        expense_total=Expense.objects.filter(owner=request.user).values('amount').aggregate(total=Sum('amount'))
        category_summary=Expense.objects.filter(owner=request.user).values('categories').annotate(total=Sum('amount'))
        context={
            'Total Expense':expense_total.get('total'),
            'Category':category_summary
        }
        return Response(data=context)