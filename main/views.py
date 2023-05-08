from django.shortcuts import redirect, render, get_object_or_404
from main.models import SinhVien
import datetime
from django.shortcuts import redirect, render
from django.db.models import Q
from main.models import QuanLi
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, 'profile.html')


def sinhviens(request):
    query = request.GET.get('q', '')
    sinhviens = SinhVien.objects.filter(HoTen__icontains=query)
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
    if request.method == 'POST':
        sinhvien = SinhVien(HoTen=request.POST['hoten'],
                            MSSV=request.POST['mssv'],
                            GioiTinh=request.POST['gioitinh'],
                            NgaySinh=request.POST['ngaysinh'],
                            DiaChi=request.POST['diachi'],
                            Email=request.POST['email'],
                            SoDienThoai=request.POST['sodienthoai'],
                            MaPhong_id=request.POST['maphong'],)

        sinhvien.save()

        return redirect(sinhviens)

    return render(request, 'add_sinhvien.html')


def nhanViens(request):
    if request.method == 'GET':
        nhanviens = QuanLi.objects.all()
    elif request.method == 'POST':
        txt = str(request.POST.get('txt')).strip()
        print(txt)
        nhanviens = QuanLi.objects.filter(Q(MaQuanLi__icontains=txt) | Q(
            HoTen__icontains=txt) | Q(SoDienThoai__icontains=txt) | Q(Email__icontains=txt))

    context = {'nhanviens': nhanviens}
    return render(request, 'nhanviens.html', context)


def nhanVien(request, id):
    data = {}
    if id == 0:
        data['title'] = "Thêm nhân viên"
    else:
        data['title'] = "Thay đổi thông tin nhân viên"
        nhanvien = QuanLi.objects.get(id=id)
        data['nhanvien'] = nhanvien

    if 'message' in request.session:
        data['message'] = request.session['message']
        del request.session['message']

    if 'nhanvien' in request.session:
        data['nhanvien'] = request.session['nhanvien']
        birthday = data['nhanvien']['NgaySinh']
        data['nhanvien']['NgaySinh'] = birthday and datetime.datetime.strptime(
            birthday, '%Y-%m-%d')
        del request.session['nhanvien']
    return render(request, 'nhanvien.html', data)


def nhanVien_save(request):
    # Nhận dữ liệu
    name = str(request.POST.get('name')).strip()
    birthday = str(request.POST.get('birthday')).strip()
    phone = str(request.POST.get('phone')).strip()
    email = str(request.POST.get('email')).strip()
    role = str(request.POST.get('role')).strip()
    id = request.POST.get('id')
    if (id == ""):
        id = 0
    else:
        id = int(id)

    nhanvienNew = {
        'id': id,
        'HoTen': name,
        'NgaySinh': birthday,
        'SoDienThoai': phone,
        'Email': email,
        'Role': role
    }

    # Kiểm tra điều kiện
    if (name == "" or birthday == "" or phone == "" or email == "" or role == ""):
        request.session['message'] = 'Bạn cần nhập dữ liệu đầy đủ!'
        request.session['nhanvien'] = nhanvienNew
        return redirect('/nhanvien/' + str(id) + "/")

    if id == 0:
        # Kiểm tra số điện thoại
        nhanvien = QuanLi.objects.filter(SoDienThoai=phone)
        if nhanvien.exists():
            request.session['message'] = 'Số điện thoại đã sử dụng'
            request.session['nhanvien'] = nhanvienNew
            return redirect('/nhanvien/' + str(id) + "/")

        # Kiểm tra email
        nhanvien = QuanLi.objects.filter(Email=email)
        if nhanvien.exists():
            request.session['message'] = 'Email đã sử dụng'
            request.session['nhanvien'] = nhanvienNew
            return redirect('/nhanvien/' + str(id) + "/")

        # Tạo mã quản lí
        nhanvien = QuanLi.objects.last()
        if (nhanvien == None):
            maQuanLi = "KTX1"
        else:
            stt = nhanvien.id + 1
            maQuanLi = "KTX" + str(stt)

        # Lưu nhân viên mới
        nhanvien = QuanLi(MaQuanLi=maQuanLi, HoTen=name, NgaySinh=birthday,
                          SoDienThoai=phone, Email=email, Password="123456", Role="NORMAL")
        nhanvien.save()
        request.session['message'] = 'Đã thêm thành công!'
        return redirect('/nhanvien/' + str(id) + "/")
    else:
        nhanvienOld = QuanLi.objects.get(id=id)

        # Kiểm tra số điện thoại
        nhanvien = QuanLi.objects.filter(SoDienThoai=phone)
        if nhanvien.exists() and QuanLi.objects.get(SoDienThoai=phone).MaQuanLi != nhanvienOld.MaQuanLi:
            request.session['message'] = 'Số điện thoại đã sử dụng'
            request.session['nhanvien'] = nhanvienNew
            return redirect('/nhanvien/' + str(id) + "/")

        # Kiểm tra email
        nhanvien = QuanLi.objects.filter(Email=email)
        if nhanvien.exists() and QuanLi.objects.get(Email=email).MaQuanLi != nhanvienOld.MaQuanLi:
            request.session['message'] = 'Email đã sử dụng'
            request.session['nhanvien'] = nhanvienNew
            return redirect('/nhanvien/' + str(id) + "/")

        nhanvien = QuanLi.objects.get(id=id)
        nhanvien.HoTen = name
        nhanvien.NgaySinh = birthday
        nhanvien.SoDienThoai = phone
        nhanvien.Email = email
        nhanvien.save()
        return redirect('/nhanviens/')


def nhanVien_delete(request, id):
    nhanvien = QuanLi.objects.get(id=id)
    nhanvien.delete()
    return nhanViens(request)
