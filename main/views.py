from django.shortcuts import render,get_object_or_404, redirect
from .models import Phong
# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

def phong(request):
    data = Phong.objects.all()
    return render(request, './pages/phong.html',{'data': data})

def update_phong(request,id):
    data = get_object_or_404(Phong, id=id)
    if request.method == 'POST':
        data.MaPhong = request.POST['MaPhong']
        data.TrangThai =  request.POST['TrangThai']
        data.SoluongSV = request.POST['SoluongSV']
        data.LoaiPhong = request.POST['LoaiPhong']
        data.Gia = request.POST['Gia']
        data.TenToaNha = request.POST['TenToaNha']
        data.save()
        return redirect(phong)
    return render(request, './pages/update.html',{'data': data})


def add_Phong(request):
    # phongs = Phong.objects.all()
    if request.method == 'POST':
        Phong.create_Phong(
            request.POST['MaPhong'],
            request.POST['TrangThai'],
            request.POST['SoluongSV'],
            request.POST['LoaiPhong'],
            request.POST['Gia'],
            request.POST['TenToaNha']
            )
        return redirect(phong)
    return render(request, './pages/add.html')