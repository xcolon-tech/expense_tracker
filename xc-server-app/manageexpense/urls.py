from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView, CategoryListView, MonthlySummaryView, TrendAnalysisView, DownloadSummaryPDFView, DownloadAnalysisPDFView

urlpatterns = [
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('trend-analysis/', TrendAnalysisView.as_view(), name='trend-analysis'),
    path('summary/download/', DownloadSummaryPDFView.as_view(), name='download-summary-pdf'),
    path('trend-analysis/download/', DownloadAnalysisPDFView.as_view(), name='download-analysis-pdf'),
]