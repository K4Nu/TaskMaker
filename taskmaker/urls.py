from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path("employee/", admin.site.urls),
    path("",user_views.index,name='index'),
    path("register/",user_views.register,name="register"),
    path('login/', user_views.custom_login_view, name='login'),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("profile/",user_views.profile,name="profile"),
    path("update/",user_views.profile_update,name="profile_update"),
    path('verify_email/<str:token>/', user_views.verify_email, name='verify_email'),
    path("resend_verification_email/",user_views.resend_verification_email,name="resend_verification_email"),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="users/reset_password.html"), name="password_reset"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="users/reset_password_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="users/reset.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="users/reset_password_complete.html"), name="password_reset_complete"),
    path("project/",include("projects.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)