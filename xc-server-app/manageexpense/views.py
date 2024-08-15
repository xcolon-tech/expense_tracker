from rest_framework import generics
from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
import io
import matplotlib.pyplot as plt
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse

# View to list and create expenses
class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# View to retrieve, update, and delete a single expense
class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

# View to list all categories
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MonthlySummaryView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.filter(user=request.user)
        summary = {}

        for expense in expenses:
            category_name = expense.category.name
            summary[category_name] = summary.get(category_name, 0) + float(expense.amount)
        
        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(summary.values(), labels=summary.keys(), autopct='%1.1f%%')
        ax.axis('equal')
        
        # Save chart to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        # Return the summary data as well as chart
        return Response({
            "summary": summary,
            "chart": buf.read().hex()
        })

class TrendAnalysisView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.filter(user=request.user).order_by('date')
        trend_data = {}

        for expense in expenses:
            date_str = expense.date.strftime('%Y-%m')
            trend_data[date_str] = trend_data.get(date_str, 0) + float(expense.amount)
        
        # Create a bar chart
        fig, ax = plt.subplots()
        ax.bar(trend_data.keys(), trend_data.values())
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Expenses')
        ax.set_title('Expense Trend Analysis')
        
        # Save chart to a buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)

        return Response({
            "trend_analysis": trend_data,
            "chart": buf.read().hex()
        })

class DownloadSummaryPDFView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Create a PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "Monthly Expense Summary")
        
        expenses = Expense.objects.filter(user=request.user)
        y = 700
        for expense in expenses:
            p.drawString(100, y, f"{expense.date}: {expense.category.name} - {expense.amount} - {expense.reason}")
            y -= 20
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='summary.pdf')

class DownloadAnalysisPDFView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Create a PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "Trend Analysis Report")
        
        expenses = Expense.objects.filter(user=request.user).order_by('date')
        y = 700
        for expense in expenses:
            p.drawString(100, y, f"{expense.date}: {expense.category.name} - {expense.amount} - {expense.reason}")
            y -= 20
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='analysis.pdf')