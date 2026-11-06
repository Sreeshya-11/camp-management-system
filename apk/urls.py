from .import views
from django.urls import path
urlpatterns=[
    
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    
    path('donorregistration/',views.donor_registration,name='donorregistration'),
    path('donorlogin/',views.donor_login,name='donorlogin'),
    path('donorprofile/',views.donorprofile,name='donorprofile'),
    path('editdonorprofile/',views.editdonorprofile,name='editdonorprofile'),
    path('donorhome/',views.donorhome,name='donorhome'),
    
    path('logout/',views.logout,name='logout'),
   
    path('product1/',views.product1,name='product1'),
    path('productlist/',views.productlist,name='productlist'),
    path('profilelist/',views.profilelist,name='profilelist'),
    
    path('deluser/<int:id>',views.deluser,name='deluser'),
    path('delproduct/<int:id>',views.delproduct,name='delproduct'),
    path('camp/',views.camp,name='camp'),
    path('chome/',views.chome,name='chome'),
    path('clogin/',views.clogin,name='clogin'),
    path('camplist/',views.camplist,name='camplist'),
    path('approve-camp/<int:camp_id>/', views.approve_camp, name='approve_camp'),


    path('u_camplist/',views.u_camplist,name='u_camplist'),
    path('cneeds/',views.needs,name='cneeds'),
    path('camp_vrequest/',views.camp_vol_req,name='camp_vrequest'),
    path('createreport/',views.create_report,name='create_report'),
    path('viewreport/',views.viewreports,name='viewreport'),
    path('delete_report/<int:report_id>/',views.delete_report,name='delete_report'),
    
    # path('donation_requests_view/', views.donation_requests_view, name='donation_requests_view'),
    path('donation_requests/', views.donation_requests_view, name='donation_requests_view'),
    path('confirm_donation/<int:need_id>/', views.confirm_donation, name='confirm_donation'),
    path('volunteer_requests_view/', views.volunteer_requests_view, name='volunteer_requests_view'),

    path('offer/<int:request_id>/', views.donation_offer_view, name='donation_offer'),
    path('tracking/', views.donation_tracking_view, name='donation_tracking'),
    
    path('adlogin/', views.adlogin, name='adlogin'),
    path('adhome/', views.adhome, name='adhome'),
    
    path('vregister/', views.vregister, name='vregister'),
    path('vlogin/', views.vlogin, name='vlogin'),
    path('vhome/', views.vdashboard, name='vdashboard'),
    path('vprofile/', views.vprofile, name='vprofile'),
    path('editvprofile/', views.editvprofile, name='editvprofile'),
    path('volunteerlist/',views.volunteerlist,name='volunteerlist'),
    path('update-status/<int:volunteer_id>/', views.update_volunteer_status, name='update_volunteer_status'),

    
    path('addnotification/', views.add_notification, name='addnotification'),
    path('notifications/', views.notifications, name='notifications'),
    path('addroute/', views.add_route, name='add_route'),
    path('listroute/', views.route_list, name='route_list'),
    path('edit/<int:route_id>/', views.edit_route, name='edit_route'),
    path('delete/<int:route_id>/', views.delete_route, name='delete_route'),

    path('update_status/', views.update_status, name='update_status'),
    path('vol_notification/', views.vol_notification, name='vol_notification'),
    path('v_notifications/', views.v_notifications, name='v_notifications'),
    path('donation_form/', views.donation_form, name='donation_form'),
    path('payment_form/<int:nid>/', views.payment_form, name='payment_form'),
    # Map the payment confirmation view
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),


    path('payment_form1/<int:camp_id>/', views.payment_form1, name='payment_form1'),
    path('confirm_payment1/', views.confirm_payment1, name='confirm_payment1'),
    path('cleanup-payments/', views.cleanup_invalid_payments, name='cleanup_invalid_payments'),
    path('check_payments/', views.check_payments, name='check_payments'),
    path('fix-broken-payments/', views.fix_broken_payments, name='fix_broken_payments'),


    path('v_notif_from_camp/',views.v_notif_from_camp,name='v_notif_from_camp'),
    path('apply/',views.apply,name='apply'),
    path('v_notif_to_volunteer/',views.v_notif_to_volunteer,name='v_notif_to_volunteer'),
    path('apply2/<int:nid>/', views.apply2, name='apply2'),
    path('applications/', views.applications, name='applications'),
    path('camp_applications/', views.camp_applications, name='camp_applications'),
    path('update_application_status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('donation_details/', views.donation_details, name='donation_details'),
    path('get_user_session/', views.get_user_session, name='get_user_session'),
    path('notif_from_camp_to_evry1/', views.notif_from_camp_to_evry1, name='notif_from_camp_to_evry1'),
    path('not_list_from_camp/', views.not_list_from_camp, name='not_list_from_camp'),
    path('delete_notif/<int:id>/', views.delete_notif, name='delete_notif'),
    path('delete_all_notifs/', views.delete_all_notifs, name='delete_all_notifs'),
    path('notif_on_user/',views.notif_on_user,name='notif_on_user'),
    path('reportlist/',views.reportlist,name='reportlist'),
    path('notif_list_from_admin/',views.notif_list_from_admin,name='notif_list_from_admin'),


    #Donor
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    #user
    path('forgot_pwd_emp/', views.forgot_pwd_emp, name='forgot_pwd_emp'),
    path('verify_otp_emp/', views.verify_otp_emp, name='verify_otp_emp'),
    path('reset_password_emp/', views.reset_password_emp, name='reset_password_emp'),


    #volunteer
    path('forgot_pwd_vol/', views.forgot_pwd_vol, name='forgot_pwd_vol'),
    path('verify_otp_vol/', views.verify_otp_vol, name='verify_otp_vol'),
    path('reset_password_vol/', views.reset_password_vol, name='reset_password_vol'),


    #camp
    path('fpwd_camp/', views.fpwd_camp, name='fpwd_camp'),    
    path('votp_camp/', views.votp_camp, name='votp_camp'),
    path('rpwd_camp/', views.rpwd_camp, name='rpwd_camp'),
    path('view_on_map/<int:report_id>/', views.view_on_map, name='view_on_map'),
]



