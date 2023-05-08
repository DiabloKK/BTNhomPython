

from .models import Phong,SinhVien

import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from main.models import QuanLi
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')


def phong(request):
    data = Phong.objects.all()
    for phong in data:
        sinh_vien = SinhVien.objects.filter(MaPhong_id=phong.id)
        so_luong = sinh_vien.count()
        phong.count = so_luong
    
    # Tạo một đối tượng Paginator với all_records và số lượng bản ghi mỗi trang
    paginator = Paginator(data, 3)
    
    # Lấy số trang từ query parameter (nếu không có sẽ trả về trang đầu tiên)
    page_number = int(request.GET.get('page', 1))
    
    # Lấy dữ liệu trang cụ thể từ Paginator
    data_page = paginator.get_page(page_number)
    
    # Tìm số page chia được
    totaldata = len(data)
    if totaldata%3==0: 
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
    }

    return render(request, './pages/phong.html',context)

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

def nhanViens(request):
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
    
    nhanviens = QuanLi.objects.filter(Q(MaQuanLi__icontains=keyword) | Q(HoTen__icontains=keyword) | Q(SoDienThoai__icontains=keyword) | Q(Email__icontains=keyword) | Q(Role__icontains=keyword)).order_by(sort)

    # Tạo một đối tượng Paginator với all_records và số lượng bản ghi mỗi trang
    paginator = Paginator(nhanviens, 5)
    
    # Lấy số trang từ query parameter (nếu không có sẽ trả về trang đầu tiên)
    page_number = int(request.GET.get('page', 1))
    
    # Lấy dữ liệu trang cụ thể từ Paginator
    nhanviens_page = paginator.get_page(page_number)
    
    # Tìm số page chia được
    totalNhanVien = len(nhanviens)
    if totalNhanVien%5==0: 
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
        data['nhanvien']['NgaySinh'] = birthday and datetime.datetime.strptime(birthday, '%Y-%m-%d')
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
    if(id == ""):
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
    if(name == "" or birthday == "" or phone == "" or email == "" or role == ""):
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
        if(nhanvien == None) :
            maQuanLi = "KTX1"
        else:
            stt = nhanvien.id + 1
            maQuanLi = "KTX" + str(stt)
        
        # Lưu nhân viên mới    
        nhanvien = QuanLi(MaQuanLi = maQuanLi, HoTen=name, NgaySinh=birthday, SoDienThoai=phone, Email=email, Password="123456", Role=role)
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
        nhanvien.Role = role
        nhanvien.save()
        return redirect('/nhanviens/')
    
def nhanVien_delete(request, id):
    nhanvien = QuanLi.objects.get(id = id)
    nhanvien.delete()
    return nhanViens(request)

        
        


