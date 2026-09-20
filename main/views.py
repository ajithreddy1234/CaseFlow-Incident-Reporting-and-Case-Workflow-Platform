from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.urls import reverse
from .models import Profile, UserCrimeReport, EvidencePhoto,Alerts,Notification,EvidenceAudio, EvidenceVideo
from django.http import JsonResponse

def part_of_day():
    present_time = datetime.now().hour
    if present_time < 12:
        return 'Good morning, have a nice day'
    elif present_time < 16:
        return 'Good afternoon'
    elif present_time <= 18:
        return 'Good evening'
    else:
        return 'Good night'

@login_required
def home(request):
    if request.user.is_staff:
        return staff_home(request)

    user_reports = UserCrimeReport.objects.filter(user=request.user).order_by('-submitted_at')

    return render(request, 'usr_home_pg.html', {
        'tm': part_of_day(),
        'user_reports': user_reports,
        "user": request.user,
    })

@login_required
def staff_home(request):
    if not request.user.is_staff:
        return redirect('/')

    crime_reports = UserCrimeReport.objects.all().order_by('-submitted_at')

    status_counts = {
        "pending": crime_reports.filter(status="Pending").count(),
        "investigating": crime_reports.filter(status="Under Investigation").count(),
        "critical": crime_reports.filter(priority=5).count(),
        "resolved": crime_reports.filter(status="Resolved").count(),
    }

    context = {
        "crime_reports": crime_reports,
        "status_counts": status_counts,
        "user": request.user,
    }

    return render(request, "PoliceDashboard.html", context)

@user_passes_test(lambda u: u.is_staff)
def analytics_view(request):
    stats = {
        'total': UserCrimeReport.objects.count(),
        'pending': UserCrimeReport.objects.filter(status="Pending").count(),
        'investigating': UserCrimeReport.objects.filter(status="Under Investigation").count(),
        'resolved': UserCrimeReport.objects.filter(status="Resolved").count(),
        'rejected': UserCrimeReport.objects.filter(status="Rejected").count(),
        'critical': UserCrimeReport.objects.filter(priority=5).count(),
        'high': UserCrimeReport.objects.filter(priority=4).count(),
        'medium': UserCrimeReport.objects.filter(priority=3).count(),
    }
    return render(request, 'police_analytics.html', {'stats': stats})



@login_required
def crime_reporting(request):
    if request.user.is_staff:
        return redirect('/') 
    
    if request.method == 'POST':
        typeofCrime = request.POST.get('typeofCrime')
        description = request.POST.get('description')
        location = request.POST.get('location')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        priority = int(request.POST.get('priority', 3))
        date_str = request.POST.get('incident_date')
        time_str = request.POST.get('incident_time')
        date = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

        report = UserCrimeReport.objects.create(
            user=request.user,
            typeofCrime=typeofCrime,
            description=description,
            location=location,
            latitude=latitude,
            longitude=longitude,
            date=date,
            priority=priority,
        )

        for image_file in request.FILES.getlist('evidence_photos'):
            EvidencePhoto.objects.create(report=report, image=image_file)

        for audio_file in request.FILES.getlist('evidence_audio'):
            EvidenceAudio.objects.create(report=report, audio=audio_file)

        for video_file in request.FILES.getlist('evidence_video'):
            EvidenceVideo.objects.create(report=report, video=video_file)

        Notification.objects.create(
            user=request.user,
            title="Crime Report Submitted",
            message=f"Your crime report '{typeofCrime}' has been submitted successfully.",
            related_report=report
        )

        return redirect('home')

    return render(request, 'reporting.html')


@login_required
def view_report(request, report_id):
    report = get_object_or_404(UserCrimeReport, id=report_id)
    evidence_photos = report.photos.all()
    evidence_audios = report.audios.all()
    evidence_videos = report.videos.all()

    return render(request, 'View_report.html', {
        'report': report,
        'evidence_photos': evidence_photos,
        'evidence_audios': evidence_audios,
        'evidence_videos': evidence_videos,
        'isSuperUser': request.user.is_staff,
    })


@login_required
def update_report(request, report_id):
    if not request.user.is_staff:
        return redirect('/') 

    report = get_object_or_404(UserCrimeReport, id=report_id)

    if request.method == 'POST':
        report.status = request.POST.get('status', report.status)
        report.admin_notes = request.POST.get('adminNotes', report.admin_notes)
        report.save()

        Notification.objects.create(
            user=report.user,
            title=f"Report #{report.id} Status Updated",
            message=f"Your crime report is now marked as '{report.status}'. Message:{report.admin_notes}",
        )

        messages.success(request, "Report updated successfully!")
        return redirect('admin_dashboard')

    return render(request, 'Update_status.html', {'report': report})


@login_required
def logout_user(request):
    auth_logout(request)
    return redirect(reverse('login'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Incorrect username or password')
            return redirect(reverse('login'))

    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'login.html')


def sign_up(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('firstname', '').strip()
        last_name = request.POST.get('lastname', '').strip()
        phone = request.POST.get('phonenumber', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not (email and first_name and last_name and username and password and confirm_password):
            messages.error(request, "All fields are required!")
            return redirect(reverse('register'))

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect(reverse('register'))

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken!")
            return redirect(reverse('register'))

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already used!")
            return redirect(reverse('register'))

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        profile = Profile.objects.create(user=user,phone=phone)
        profile.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect(reverse('login'))

    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'signin.html')


@login_required
def profile_view(request):
    user_reports = UserCrimeReport.objects.filter(user=request.user)
    user = request.user

    analytics = {
        "total": user_reports.count(),
        "pending": user_reports.filter(status="Pending").count(),
        "resolved": user_reports.filter(status="Resolved").count(),
        "critical": user_reports.filter(priority=5).count(),
        "under_investigation": user_reports.filter(status="Under Investigation").count(),
    }

    return render(request, 'staff_user_profile.html', {
        'user': user,
        'analytics': analytics,
        'readonly': False,
    })

@user_passes_test(lambda u: u.is_staff)
def view_user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.get(user=target_user)
    user_reports = UserCrimeReport.objects.filter(user=target_user)

    analytics = {
        "total": user_reports.count(),
        "pending": user_reports.filter(status="Pending").count(),
        "resolved": user_reports.filter(status="Resolved").count(),
        "critical": user_reports.filter(priority=5).count(),
        "under_investigation": user_reports.filter(status="Under Investigation").count(),
    }

    return render(request, 'staff_user_profile.html', {
        'user': target_user,
        'profile': profile,
        'analytics': analytics,
        'readonly': True,
    })

@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        
        user.save()
        profile.save()
        messages.success(request, "Your profile was updated successfully.")
        return redirect('profile_view')

    return render(request, 'edit_profile.html', {
        'user': user,
        'profile': profile,
    })


@login_required
def alerts(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")
        area = request.POST.get("area")
        severity = request.POST.get("severity")

        alert = Alerts.objects.create(
            title=title,
            message=message,
            area=area,
            severity=severity,
            created_at=datetime.now()
        ).save()

        # Notify all non-staff users
        users = User.objects.filter(is_staff=False)
        for user in users:
            Notification.objects.create(
                user=user,
                title=f"New Alert: {title}",
                message=message,
                related_alert=alert
            ).save()

        return redirect('alerts')
    
    alerts = Alerts.objects.all()
    context = {
        "alerts" : alerts,
        "user" : request.user,
    }
    return render(request, 'alerts.html',context)


@login_required
def get_notifications(request):
    latest_notifications = Notification.objects.filter(user=request.user).order_by('-date')[:10]

    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    data = [
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'date': n.date.strftime('%b %d, %H:%M'),
            'is_read': n.is_read,
        }
        for n in latest_notifications
    ]

    return JsonResponse({'notifications': data, 'unread_count': unread_count})

@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'success': True})

@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})
