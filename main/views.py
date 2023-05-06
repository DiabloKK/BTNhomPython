from django.shortcuts import redirect, render, get_object_or_404
from main.models import SinhVien
# Create your views here.


def index(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, 'profile.html')


def sinhviens(request):
    sinhviens = SinhVien.objects.all()
    context = {"sinhviens": sinhviens}
    return render(request, 'sinhvien.html', context)


def sinhvien_detail(request, id):
    sinhvien = SinhVien.objects.filter(id=id)[0]
    sinhvien.NgaySinh = sinhvien.NgaySinh.strftime("%Y-%m-%d")
    context = {"sinhvien": sinhvien}
    return render(request, 'sinhvien_detail.html', context)


def update_sinhvien(request, id):
    sinhvien = get_object_or_404(SinhVien, pk=id)

    if request.method == 'POST':
        # Update the SinhVien object with the data submitted in the form
        sinhvien.HoTen = request.POST['hoten']
        sinhvien.GioiTinh = request.POST['gioitinh']
        sinhvien.NgaySinh = request.POST['ngaysinh']
        sinhvien.DiaChi = request.POST['diachi']
        sinhvien.Email = request.POST['email']
        sinhvien.SoDienThoai = request.POST['sodienthoai']
        sinhvien.MaPhong_id = request.POST['maphong']
        sinhvien.save()

        # Redirect to the detail page for the updated SinhVien object
        return redirect(sinhvien_detail, id=id)

    # Render the update SinhVien form with the current data for the SinhVien object
    return render(request, 'sinhvien_detail.html', {'sinhvien': sinhvien})


def add_sinhvien(request):

    # if request.method == 'POST':
    #     sinhvien = SinhVien(HoTen=request.POST['hoten'],
    #                         GioiTinh=request.POST['gioitinh'],
    #                         NgaySinh=request.POST['ngaysinh'],
    #                         DiaChi=request.POST['diachi'],
    #                         Email=request.POST['email'],
    #                         SoDienThoai=request.POST['sodienthoai'],
    #                         MaPhong_id=request.POST['maphong'],)

    #     sinhvien.save()

    #     return redirect(sinhviens)

    return render(request, 'add_sinhvien.html')
