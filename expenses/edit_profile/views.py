from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Profile
# Create your views here.

@login_required(login_url="/authentication/login/")
def index(request):
    user=request.user
    profile=user.profile
    created_at=user.profile.created_at
    print(created_at)
    context = {
        'user': user,
        'created_at':created_at
    }
    return render(request, 'edit/index.html', context)


@login_required(login_url="/authentication/login/")
@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        new_password2 = request.POST['new_password2']
        profile_image = request.FILES.get('profile_image')
        
        try:
       
            user = request.user  
            user.username = username
            user.email = email

            if profile_image:
                profile=user.profile
                user.profile.profile_image = profile_image
                print(user.profile.profile_image)
                profile.save()
                return redirect('edit_profile') 
                

            if current_password and new_password:
                if user.check_password(current_password):
                    if new_password==new_password2:

                        user.set_password(new_password)
                        update_session_auth_hash(request, user)  
                        user.save()
                        messages.success(request, "Profile and password updated successfully.")
                        return redirect('edit_profile')
                    else:
                        messages.error(request, "The new passwords do not match up !")
                        return redirect('edit_profile')
                else:
                    messages.error(request, "Current password is incorrect.")
                    return redirect('edit_profile')


            user.save()  

            messages.success(request, "Profile updated successfully.")
            return redirect('edit_profile')  

        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")
        
         

    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'profile_image': user.profile.profile_image.url,
        

    }
    return render(request, 'edit/index.html', context)