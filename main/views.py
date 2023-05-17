from django.shortcuts import redirect, render, get_object_or_404
from main.models import Phong
from main.models import SinhVien
import datetime
from django.shortcuts import redirect, render
from django.db.models import Q
from main.models import QuanLi, HopDong, SinhVien, Phong
from django.core.paginator import Paginator
from .forms import HopDongForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    # QuanLi.objects.all().delete()
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        email = str(request.POST.get('email')).strip()
        password = str(request.POST.get('password')).strip()

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            nhanvien = QuanLi.objects.get(Email=email)
            request.session['role'] = nhanvien.Role
            request.session['name'] = nhanvien.HoTen
            request.session['id'] = nhanvien.id
            return redirect("/")
        else:
            return render(request, 'login.html', {'message': 'Tài khoản hoặc mật khẩu không chính xác'})


def logout_view(request):
    logout(request)
    response = redirect('/login/')

    return response

# Show all the constracts


@login_required
def change_password(request):

    if request.method == 'POST':
        user = request.user
        print(user)
        if user.check_password(request.POST.get('password_older')):
            if request.POST.get('new_password') == request.POST.get('repeat_new_password'):
                user.set_password(request.POST.get('new_password'))
                user.save()
                return redirect('/login/')
            else:
                return render(request, 'changepassword.html', {
                    'message': "Mật khẩu mới không trùng khớp"
                })
        else:
            return render(request, 'changepassword.html', {
                'message': "Mật khẩu không trùng khớp"
            })
    return render(request, 'changepassword.html')


@login_required
def all_constracts(request):
    constract_list = HopDong.objects.all()
    room_list = Phong.objects.all()
    list = {'constract_list': constract_list}
    return render(request, 'constracts.html', list)


@login_required
def search_constracts(request):
    txt = str(request.POST.get('txt')).strip()
    status = str(request.POST.get('status')).strip()
    if status == "":
        constract_list = HopDong.objects.filter(Q(GiaTien__icontains=txt) | Q(
            NgayBatDau__icontains=txt) | Q(NgayKetThuc__icontains=txt))
        list = {'constract_list': constract_list}
        return render(request, 'constracts.html', list)
    else:
        constract_list = HopDong.objects.filter(
            Q(TrangThaiThanhToan__icontains=status))
        list = {'constract_list': constract_list}
        return render(request, 'constracts.html', list)


@login_required
def edit_constract(request, id):
    constract = HopDong.objects.get(id=id)
    SV_list = SinhVien.objects.all()
    QL_list = QuanLi.objects.all()
    room_list = Phong.objects.all()
    list = {'SV_list': SV_list,
            'constract': constract,
            'QL_list': QL_list,
            'room_list': room_list
            }
    return render(request, 'constract_detail.html', list)


@login_required
def add_constract(request):
    constract_list = HopDong.objects.all()
    SV_list = SinhVien.objects.all()
    QL_list = QuanLi.objects.all()
    room_list = Phong.objects.all()
    list = {'SV_list': SV_list,
            'constract_list': constract_list,
            'QL_list': QL_list,
            'room_list': room_list
            }
    return render(request, 'constract_detail.html', list)


@login_required
def constract_saved(request):
    id = request.POST.get('id')
    NgayBatDau = str(request.POST.get('NgayBatDau')).strip()
    NgayKetThuc = str(request.POST.get('NgayKetThuc')).strip()
    GiaTien = request.POST.get('GiaTien')
    TrangThaiThanhToan = bool(request.POST.get('TrangThaiThanhToan'))
    MSSV_id = str(request.POST.get('MSSV_id')).strip()
    MaQuanLi_id = str(request.POST.get('MaQuanLi_id')).strip()
    MaPhong_id = str(request.POST.get('MaPhong_id')).strip()

    if (id == ''):
        new_constract = HopDong(NgayBatDau=NgayBatDau, NgayKetThuc=NgayKetThuc, GiaTien=GiaTien,
                                TrangThaiThanhToan=TrangThaiThanhToan, MSSV_id=MSSV_id, MaQuanLi_id=MaQuanLi_id, MaPhong_id=MaPhong_id)
        new_constract.save()
        return redirect('/themhopdong/')
    else:
        new_constract = HopDong(id=id, NgayBatDau=NgayBatDau, NgayKetThuc=NgayKetThuc, GiaTien=GiaTien,
                                TrangThaiThanhToan=TrangThaiThanhToan, MSSV_id=MSSV_id, MaQuanLi_id=MaQuanLi_id, MaPhong_id=MaPhong_id)
        new_constract.save()
        form = HopDongForm(request.POST)
        return redirect('/suahopdong/' + str(id) + '/')


@login_required
def delete_constract(request, id):
    constract = HopDong.objects.get(id=id)
    constract.delete()
    return all_constracts(request)


@login_required
def sinhviens(request):

    query = request.GET.get('q', '')
    phong = request.GET.get('rid', '')
    if phong != '':
        sinhviens = SinhVien.objects.select_related('MaPhong').filter(
            HoTen__icontains=query, MaPhong=phong)
    else:
        sinhviens = SinhVien.objects.select_related('MaPhong').filter(
            HoTen__icontains=query)
    # context = {"sinhviens": sinhviens}

    # Tạo một đối tượng Paginator với all_records và số lượng bản ghi mỗi trang
    paginator = Paginator(sinhviens, 5)

    # Lấy số trang từ query parameter (nếu không có sẽ trả về trang đầu tiên)
    page_number = int(request.GET.get('page', 1))

    # Lấy dữ liệu trang cụ thể từ Paginator
    sinhviens_page = paginator.get_page(page_number)

    # Tìm số page chia được
    total_sinhvien = len(sinhviens)

    if total_sinhvien % 5 == 0:
        total_page = int(total_sinhvien/5)
    else:
        total_page = int(total_sinhvien/5) + 1

    index = (page_number - 1)*5

    numbers = list(range(1, total_page+1))

    print(sinhviens)

    context = {
        'sinhviens': sinhviens_page,
        'page': page_number,
        'totalPage': total_page,
        'numbers': numbers,
        'totalSinhvien': total_sinhvien,
        'keyword': query
    }

    return render(request, 'sinhvien.html', context)


@login_required
def sinhvien_detail(request, id):

    if request.method == 'GET':
        phongs = Phong.objects.all()
        sinhvien = SinhVien.objects.filter(id=id)[0]
        sinhvien.NgaySinh = sinhvien.NgaySinh.strftime("%Y-%m-%d")
        context = {"sinhvien": sinhvien,
                   'phongs': phongs
                   }
        return render(request, 'sinhvien_detail.html', context)
    elif request.method == 'POST':
        sinhvien = get_object_or_404(SinhVien, pk=id)
        # Update the SinhVien object with the data submitted in the form
        so_sinh_vien = SinhVien.objects.filter(
            MaPhong_id=request.POST['maphong']).count()
        phong = Phong.objects.get(id=request.POST['maphong'])
        phongs = Phong.objects.all()
        if so_sinh_vien >= phong.SoluongSV:

            return render(request, 'sinhvien_detail.html', {'phongs': phongs, "sinhvien": sinhvien, 'error': "Phòng đầy"})

        sinhvien.HoTen = request.POST['hoten']
        sinhvien.GioiTinh = request.POST['gioitinh']
        sinhvien.NgaySinh = request.POST['ngaysinh']
        sinhvien.DiaChi = request.POST['diachi']
        sinhvien.Email = request.POST['email']
        sinhvien.SoDienThoai = request.POST['sodienthoai']
        sinhvien.MaPhong_id = request.POST['maphong']
        sinhvien.save()

        if so_sinh_vien + 1 == phong.SoluongSV:
            phong.TrangThai = True
            phong.save()
        else:
            phong.TrangThai = False
            phong.save()

        context = {"sinhvien": sinhvien,
                   'phongs': phongs
                   }

        # Redirect to the detail page for the updated SinhVien object
        return render(request, 'sinhvien_detail.html', context)


@login_required
def update_sinhvien(request, id):
    sinhvien = get_object_or_404(SinhVien, pk=id)

    if request.method == 'POST':
        # Update the SinhVien object with the data submitted in the form
        so_sinh_vien = SinhVien.objects.filter(
            MaPhong_id=request.POST['maphong']).count()
        phong = Phong.objects.get(id=request.POST['maphong'])

        if so_sinh_vien >= phong.SoluongSV:
            phongs = Phong.objects.all()
            return render(request, 'sinhvien_detail.html', {'phongs': phongs, 'error': "Phòng đầy"})

        sinhvien.HoTen = request.POST['hoten']
        sinhvien.GioiTinh = request.POST['gioitinh']
        sinhvien.NgaySinh = request.POST['ngaysinh']
        sinhvien.DiaChi = request.POST['diachi']
        sinhvien.Email = request.POST['email']
        sinhvien.SoDienThoai = request.POST['sodienthoai']
        sinhvien.MaPhong_id = request.POST['maphong']
        sinhvien.save()

        if so_sinh_vien + 1 == phong.SoluongSV:
            phong.TrangThai = True
            phong.save()
        else:
            phong.TrangThai = False
            phong.save()

        # Redirect to the detail page for the updated SinhVien object
        return redirect(sinhvien_detail, id=id)

    # Render the update SinhVien form with the current data for the SinhVien object
    return render(request, 'sinhvien_detail.html', {'sinhvien': sinhvien})


@login_required
def add_sinhvien(request):
    if request.method == 'POST':

        phong = Phong.objects.get(id=request.POST['maphong'])

        so_sinh_vien = SinhVien.objects.filter(
            MaPhong_id=request.POST['maphong']).count()
        if so_sinh_vien >= phong[0].SoluongSV:
            phongs = Phong.objects.all()

            return render(request, 'add_sinhvien.html', {'phongs': phongs, 'error': "Phòng đầy"})

        sinhvien = SinhVien(HoTen=request.POST['hoten'],
                            MSSV=request.POST['mssv'],
                            GioiTinh=request.POST['gioitinh'],
                            NgaySinh=request.POST['ngaysinh'],
                            DiaChi=request.POST['diachi'],
                            Email=request.POST['email'],
                            SoDienThoai=request.POST['sodienthoai'],
                            MaPhong_id=request.POST['maphong'],)

        if so_sinh_vien + 1 == phong.SoluongSV:
            phong.TrangThai = True
            phong.save()
        sinhvien.save()

        return redirect(sinhviens)

    phongs = Phong.objects.all()

    return render(request, 'add_sinhvien.html', {'phongs': phongs})


@login_required
def nhanViens(request):
    role = request.session['role']

    if role != 'ADMIN':
        return redirect("/")

    sort = request.GET.get('sort')
    keyword = request.GET.get('keyword', '')
    if sort == None:
        type = '-'
        sort = 'MaQuanLi'
    elif '-' in sort:
        type = ''
    else:
        type = '-'

    if request.method == 'POST':
        txt = str(request.POST.get('txt')).strip()
        keyword = txt

    nhanviens = QuanLi.objects.filter(Q(MaQuanLi__icontains=keyword) | Q(HoTen__icontains=keyword) | Q(
        SoDienThoai__icontains=keyword) | Q(Email__icontains=keyword) | Q(Role__icontains=keyword)).order_by(sort)

    # Tạo một đối tượng Paginator với all_records và số lượng bản ghi mỗi trang
    paginator = Paginator(nhanviens, 5)

    # Lấy số trang từ query parameter (nếu không có sẽ trả về trang đầu tiên)
    page_number = int(request.GET.get('page', 1))

    # Lấy dữ liệu trang cụ thể từ Paginator
    nhanviens_page = paginator.get_page(page_number)

    # Tìm số page chia được
    totalNhanVien = len(nhanviens)
    if totalNhanVien % 5 == 0:
        total_page = int(totalNhanVien/5)
    else:
        total_page = int(totalNhanVien/5) + 1

    index = (page_number - 1)*5
    numbers = list(range(1, total_page+1))

    context = {
        'nhanviens': nhanviens_page,
        'page': page_number,
        'index': index,
        'totalPage': total_page,
        'numbers': numbers,
        'totalNhanVien': totalNhanVien,
        'sort': type,
        'keyword': keyword
    }

    return render(request, 'nhanviens.html', context)


@login_required
def nhanVien(request, id):
    role = request.session['role']

    profile = int(request.GET.get('profile', 0))

    if role != 'ADMIN' and profile == 0:
        return redirect("/")

    data = {}

    data['profile'] = profile

    if id == 0:
        data['title'] = "Thêm nhân viên"
        data['id'] = 0
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


@login_required
def nhanVien_save(request):
    role = request.session['role']

    if role != 'ADMIN':
        return redirect("/")

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
                          SoDienThoai=phone, Email=email, Role=role)
        nhanvien.save()

        # tạo user mới
        user = User.objects.create_user(email, email, '123456')
        # lưu user vào database
        user.save()

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
        nhanvien.Role = role
        nhanvien.save()
        return redirect('/nhanviens/')


@login_required
def nhanVien_delete(request, id):
    role = request.session['role']

    if role != 'ADMIN':
        return redirect("/")

    nhanvien = QuanLi.objects.get(id=id)
    nhanvien.delete()
    return nhanViens(request)


@login_required
def phong(request):

    keyword = request.GET.get('keyword', '')
    if request.method == 'POST':
        txt = str(request.POST.get('txt')).strip()
        keyword = txt

    Phongs = Phong.objects.filter(Q(MaPhong__icontains=keyword) | Q(TrangThai__icontains=keyword) | Q(
        SoluongSV__icontains=keyword) | Q(LoaiPhong__icontains=keyword) | Q(Gia__icontains=keyword))

    # data = Phong.objects.all()
    for phong in Phongs:
        so_luong = SinhVien.objects.filter(MaPhong_id=phong.id).count()
        phong.count = so_luong
        if so_luong == phong.SoluongSV:
            phong.TrangThai = True
        else:
            phong.TrangThai = False
        phong.save()

    # Tạo một đối tượng Paginator với all_records và số lượng bản ghi mỗi trang
    paginator = Paginator(Phongs, 3)

    # Lấy số trang từ query parameter (nếu không có sẽ trả về trang đầu tiên)
    page_number = int(request.GET.get('page', 1))

    # Lấy dữ liệu trang cụ thể từ Paginator
    data_page = paginator.get_page(page_number)

    # Tìm số page chia được
    totaldata = len(Phongs)
    if totaldata % 3 == 0:
        total_page = int(totaldata/3)
    else:
        total_page = int(totaldata/3) + 1

    index = (page_number - 1)*3
    numbers = list(range(1, total_page+1))

    context = {
        'data': data_page,
        'page': page_number,
        'index': index,
        'totalPage': total_page,
        'numbers': numbers,
        'totaldata': totaldata,
        'keyword': keyword

    }

    return render(request, './pages/phong.html', context)


@login_required
def update_phong(request, id):
    data = get_object_or_404(Phong, id=id)
    if request.method == 'POST':
        data.MaPhong = request.POST['MaPhong']
        data.TrangThai = request.POST['TrangThai']
        data.SoluongSV = request.POST['SoluongSV']
        data.LoaiPhong = request.POST['LoaiPhong']
        data.Gia = request.POST['Gia']
        data.TenToaNha = request.POST['TenToaNha']
        data.save()
        return redirect(phong)
    return render(request, './pages/update.html', {'data': data})


@login_required
def add_Phong(request):
    # phongs = Phong.objects.all()
    if request.method == 'POST':
        Phong(
            request.POST['MaPhong'],
            request.POST['TrangThai'],
            request.POST['SoluongSV'],
            request.POST['LoaiPhong'],
            request.POST['Gia'],
            request.POST['TenToaNha']
        )
        return redirect(phong)
    return render(request, './pages/add.html')
