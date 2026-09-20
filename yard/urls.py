from django.urls import path

from . import views


urlpatterns = [
    # Authentication URLs
    path(
        'register/',
        views.register_view,
        name='register'
    ),
    path(
        'login/',
        views.login_view,
        name='login'
    ),
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Dashboard URLs
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'dashboard/export/csv/',
        views.export_container_csv,
        name='export_container_csv'
    ),

    # path(
    #     'dashboard/export/pdf/',
    #     views.export_container_pdf,
    #     name='export_container_pdf'
    # ),

    # Yard URLs
    path(
        'yards/',
        views.yard_list,
        name='yard_list'
    ),

    path(
        'yards/create/',
        views.create_yard,
        name='create_yard'
    ),

    path(
        'yards/<slug:slug>/',
        views.yard_detail,
        name='yard_detail'
    ),

    path(
        'yards/<slug:slug>/delete/',
        views.delete_yard,
        name='delete_yard'
    ),


    # Reference URLs
    path(
        'references/',
        views.reference_list,
        name='reference_list'
    ),

    path(
        'references/create/',
        views.create_reference,
        name='create_reference'
    ),

    path(
        'references/<slug:slug>/',
        views.reference_detail,
        name='reference_detail'
    ),

    path(
        'references/<slug:slug>/delete/',
        views.delete_reference,
        name='delete_reference'
    ),


    # Container URLs
    path(
        'containers/',
        views.container_list,
        name='container_list'
    ),

    path(
        'containers/create/',
        views.create_container,
        name='create_container'
    ),

    path(
        'containers/<slug:slug>/',
        views.container_detail,
        name='container_detail'
    ),

    path(
        'containers/<slug:slug>/delete/',
        views.delete_container,
        name='delete_container'
    ),

    # Invoice URLs
    path(
        'invoices/create/',
        views.create_invoice,
        name='create_invoice'
    ),

    path( 'invoices/', views.invoice_list, name='invoice_list' ),

    path(
        'invoices/<int:pk>/',
        views.invoice_detail,
        name='invoice_detail'
    ),

    # public
    path('contact/', views.submit_inquiry, name='submit_inquiry'),

    # admin side
    path('inquiries/', views.inquiry_list, name='inquiry_list'),
    path('inquiries/<int:pk>/', views.inquiry_detail, name='inquiry_detail'),
    path('inquiries/<int:pk>/read/', views.mark_inquiry_read, name='mark_inquiry_read'),
    path('inquiries/<int:pk>/archive/', views.archive_inquiry, name='archive_inquiry'),
    path('inquiries/<int:pk>/unarchive/', views.unarchive_inquiry, name='unarchive_inquiry'),
    path('inquiries/<int:pk>/delete/', views.delete_inquiry, name='delete_inquiry'),
]