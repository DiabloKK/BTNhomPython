import datetime
from django.shortcuts import redirect, render
from django.db.models import Q
from main.models import QuanLi, HopDong, SinhVien, Phong
from django.core.paginator import Paginator
from .forms import HopDongForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def profile(request):
    return render(request, 'profile.html')

# Show all the constracts
def all_constracts(request):
    constract_list = HopDong.objects.all()
    room_list = Phong.objects.all()
    list = {'constract_list' : constract_list}
    return render(request, 'constracts.html', list)

def search_constracts(request):
    txt = str(request.POST.get('txt')).strip()
    status = str(request.POST.get('status')).strip()
    if status == "":
        constract_list = HopDong.objects.filter(Q(GiaTien__icontains=txt) | Q(NgayBatDau__icontains=txt) | Q(NgayKetThuc__icontains=txt))
        list = {'constract_list' : constract_list}
        return render(request, 'constracts.html', list)
    else:
        constract_list = HopDong.objects.filter(Q(TrangThaiThanhToan__icontains=status))
        list = {'constract_list' : constract_list}
        return render(request, 'constracts.html', list)
def edit_constract(request, id):
    constract = HopDong.objects.get(id=id)
    SV_list = SinhVien.objects.all()
    QL_list = QuanLi.objects.all()
    room_list = Phong.objects.all()
    list = {'SV_list' : SV_list,
            'constract' : constract,
            'QL_list' : QL_list,
            'room_list' : room_list
            }
    return render(request, 'constract_detail.html', list)

def add_constract(request):
    constract_list = HopDong.objects.all()
    SV_list = SinhVien.objects.all()
    QL_list = QuanLi.objects.all()
    room_list = Phong.objects.all()
    list = {'SV_list' : SV_list,
            'constract_list' : constract_list,
            'QL_list' : QL_list,
            'room_list' : room_list
            }
    return render(request, 'constract_detail.html', list)

def constract_saved(request):
    id = request.POST.get('id')
    NgayBatDau = str(request.POST.get('NgayBatDau')).strip()
    NgayKetThuc = str(request.POST.get('NgayKetThuc')).strip()
    GiaTien = request.POST.get('GiaTien')
    TrangThaiThanhToan = bool(request.POST.get('TrangThaiThanhToan'))
    MSSV_id = str(request.POST.get('MSSV_id')).strip()
    MaQuanLi_id = str(request.POST.get('MaQuanLi_id')).strip()
    MaPhong_id = str(request.POST.get('MaPhong_id')).strip()

    if (id==''):
        new_constract = HopDong(NgayBatDau=NgayBatDau, NgayKetThuc=NgayKetThuc, GiaTien=GiaTien, TrangThaiThanhToan=TrangThaiThanhToan,MSSV_id=MSSV_id, MaQuanLi_id=MaQuanLi_id, MaPhong_id=MaPhong_id)
        new_constract.save()
        return redirect('/themhopdong/')
    else:
        new_constract = HopDong(id=id, NgayBatDau=NgayBatDau, NgayKetThuc=NgayKetThuc, GiaTien=GiaTien, TrangThaiThanhToan=TrangThaiThanhToan,MSSV_id=MSSV_id, MaQuanLi_id=MaQuanLi_id, MaPhong_id=MaPhong_id)
        new_constract.save()
        form = HopDongForm(request.POST)
        return redirect('/suahopdong/' + str(id) + '/')

def delete_constract(request, id):
    constract = HopDong.objects.get(id=id)
    constract.delete()
    return all_constracts(request)

def nhanViens(request):
    if request.method == 'GET':
        nhanviens = QuanLi.objects.all()
    elif request.method == 'POST':
        txt = str(request.POST.get('txt')).strip()
        print(txt)
        nhanviens = QuanLi.objects.filter(Q(MaQuanLi__icontains=txt) | Q(HoTen__icontains=txt) | Q(SoDienThoai__icontains=txt) | Q(Email__icontains=txt))

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
        nhanvien = QuanLi(MaQuanLi = maQuanLi, HoTen=name, NgaySinh=birthday, SoDienThoai=phone, Email=email, Password="123456", Role="NORMAL")
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
    nhanvien = QuanLi.objects.get(id = id)
    nhanvien.delete()
    return nhanViens(request)

        
        

        