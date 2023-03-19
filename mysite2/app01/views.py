from django.shortcuts import render, HttpResponse, redirect
from django.templatetags.static import static
import os
import time

# Create your views here.

def index(request):
    return HttpResponse("Welcome to use!")


def user_list(request):
    name = "hannnn"
    roles = ["admin", "user"]
    user_info = {"name": "han", "role": "admin"}
    return render(request, "user_list.html", {"n1": name, "n2": roles, "n3": user_info})


def something(request):
    # get parameters from request, e.g., ?fesfesg
    print(request.GET)

    # redirect
    return redirect("https://www.baidu.com")


def log_in(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # if post, get user submitted data
        print(request.POST)

        username = request.POST.get("user")
        password = request.POST.get("pwd")

        if username == "root" and password == "123":
            return HttpResponse("Success")
        else:
            return render(request, "login.html", {"error_msg": "Fail"})


def images(request):
    if request.method == "GET":
        return render(request, "images.html")
    
    file_object = request.FILES.get("img")
    #print(file_object.name)
    #img_path = "/mnt/f/club-stuff/tutorial/parallel_test/mysite2/app01/static/uploads/" + file_object.name
    input_path = "/mnt/f/club-stuff/tutorial/parallel_test/mysite2/app01/static/uploads/" + file_object.name
    with open(input_path, mode='wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)
    
    # show image
    file_url_show = "uploads/" + file_object.name
    return render(request, "images.html", {"n1": "show", "img_path": file_url_show})


def images_analysis(request):
    if request.method == "GET":
        return render(request, "images_analysis.html")
    
    output_name = str(time.time()) + ".png"
    # need absolute path
    output_path = "/mnt/f/club-stuff/tutorial/parallel_test/mysite2/app01/static/results/" + output_name
    print(output_path)

    centroid_algo = request.POST.get("centroid_algo")
    centroid_mag_filter = request.POST.get("centroid_mag_filter")
    star_id_algo = request.POST.get("star_id_algo")
    database = request.POST.get("database")
    attitude_algo = request.POST.get("attitude_algo")

    command_to_lost = "./lost pipeline --generate 1 --plot-output {output_path} \
        --centroid-algo {centroid_algo} \
        --centroid-mag-filter {centroid_mag_filter} \
        --star-id-algo {star_id_algo} \
        --database {database} \
        --attitude-algo {attitude_algo}"
    command_to_lost = command_to_lost.format(
        output_path=output_path, centroid_algo=centroid_algo,
        centroid_mag_filter=centroid_mag_filter, star_id_algo=star_id_algo,
        database=database, attitude_algo=attitude_algo)
    
    os.chdir('/mnt/f/club-stuff/lost')
    os.system(command_to_lost)

    # show image
    file_url_show = "results/" + output_name
    return render(request, "images_analysis.html", {"n1": "show", "img_url": file_url_show})