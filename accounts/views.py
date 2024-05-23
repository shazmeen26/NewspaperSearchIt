import json
import environ
import random

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from accounts.models import User, Uploads, NewsRecord
from accounts.forms import UserForm, UploadsForm, NewsRecordForm

from SearchEngine.model import extract

env = environ.Env()
environ.Env.read_env()

# Create your views here.


def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("upload"))
        else:
            return HttpResponseRedirect(reverse("loginSignup"))


def loginSignup(request):
    error = ""

    if request.method == "POST":
        name = request.POST.get("name", None)

        # Register user
        if name != None:

            user_form = UserForm(request.POST)

            if user_form.is_valid():
                print(user_form)
                user = user_form.save()

                user.set_password(user.password)

                user.save()

                login(request, User.objects.get(
                    email=user.email,
                    password=user.password
                ))

                return HttpResponseRedirect(reverse("home"))

            error = ""
            if "User with this Email address already exists." in str(user_form.errors):
                error = "User with this Email address already exists."
            elif "Password invalid" in str(user_form.errors):
                error = "Password invalid"

        # Login user
        else:
            email = request.POST.get("email", None)
            password = request.POST.get("password", None)

            user = authenticate(email=email, password=password)

            print(user)

            if user:
                login(request, user)

                return HttpResponseRedirect(reverse("home"))
            error = "Invalid email / password!"

    return render(request,  "LoginSignup.html", {"error": error})


@login_required
def upload(request):
    if request.method == "POST":
        upload = UploadsForm({"user": request.user}, request.FILES)
        print(upload)
        filepath = f"{env('IMAGE_BASE_URL')}/media/"
        if upload.is_valid():
            filepath += str(upload.save())

        if upload.is_valid():
            upload.save()

        if (request.user.is_staff):
            post = Uploads.objects.get(
                file="images/" + filepath.split("/")[-1])

            preprocessed_text = extract(filepath)

            newsrecord_form = NewsRecordForm({
                'user': User.objects.get(email=request.user),
                'file_path': filepath,
                'extracted_text': preprocessed_text,
            })

            if newsrecord_form.is_valid():
                newsrecord_form.save()

            post.delete()

        return HttpResponse(json.dumps({
            "success": True,
        }))

    return render(request, "upload.html")


@staff_member_required
def listUnapprovedPost(request):
    if request.method == "GET":
        print(Uploads.objects.filter(approved=False))
        return render(request, "approvePost.html", {"posts": list(Uploads.objects.filter(approved=False))})


# @staff_member_required
def approvePost(request):

    if request.method == "POST":
        upload_id = request.POST.get("id", None)
        print(upload_id)

        post = Uploads.objects.get(id=upload_id)

        filepath = f"{env('IMAGE_BASE_URL')}/media/"
        filepath += str(post)

        preprocessed_text = extract(filepath)

        newsrecord_form = NewsRecordForm({
            'user': post.user,
            'file_path': filepath,
            'extracted_text': preprocessed_text,
        })

        if newsrecord_form.is_valid():
            newsrecord_form.save()

        print("deleting...")
        post.delete()

        return HttpResponse(json.dumps({
            "success": True,
        }))


def rejectPost(request):
    if request.method == "POST":
        upload_id = request.POST.get("id", None)

        post = Uploads.objects.get(id=upload_id)
        print("deleting...")

        post.delete()

        return HttpResponse(json.dumps({
            "success": True,
        }))


@login_required
def accountLogout(request):
    if request.method == "GET":
        logout(request)

    return HttpResponseRedirect(reverse("home"))


@login_required
def search(request):
    if request.method == "POST":
        search_query = request.POST.get("searchQuery", None)

        results = list(
            NewsRecord.objects.filter(
                extracted_text__contains=search_query.lower(),
            )
            .order_by("-timestamp")
            .values_list("file_path", "external_file_path")
        )

        random.shuffle(results)

        return HttpResponse(json.dumps({
            'results': list(results)
        }))

    return render(request, "search.html")
