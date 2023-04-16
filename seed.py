from main.models import Phong, SinhVien
import django
from datetime import date
# Create 5 Phong objects
p1 = Phong(MaPhong='P001', TrangThai='available', SoluongSV=4,
           LoaiPhong='double', Gia=200, TenToaNha='Toa nha A')
p2 = Phong(MaPhong='P002', TrangThai='available', SoluongSV=2,
           LoaiPhong='single', Gia=150, TenToaNha='Toa nha A')
p3 = Phong(MaPhong='P003', TrangThai='unavailable', SoluongSV=6,
           LoaiPhong='double', Gia=250, TenToaNha='Toa nha B')
p4 = Phong(MaPhong='P004', TrangThai='unavailable', SoluongSV=2,
           LoaiPhong='single', Gia=150, TenToaNha='Toa nha C')
p5 = Phong(MaPhong='P005', TrangThai='available', SoluongSV=4,
           LoaiPhong='double', Gia=200, TenToaNha='Toa nha D')

p1 = Phong.objects.filter(id=1)[0]
p2 = Phong.objects.filter(id=2)[0]

SinhVien.objects.filter(id=6).delete()

# Create 5 SinhVien objects
sinhvien1 = SinhVien.objects.create(
    MSSV='SV001',
    HoTen='Nguyen Van A',
    GioiTinh=True,
    NgaySinh=date(2000, 1, 1),
    DiaChi='123 Nguyen Van Cu',
    Email='sv001@myuniversity.edu.vn',
    SoDienThoai='0123456789',
    MaPhong=p1,
)

sinhvien2 = SinhVien.objects.create(
    MSSV='SV002',
    HoTen='Tran Thi B',
    GioiTinh=False,
    NgaySinh=date(2001, 2, 2),
    DiaChi='456 Le Loi',
    Email='sv002@myuniversity.edu.vn',
    SoDienThoai='0987654321',
    MaPhong=p1,
)

sinhvien3 = SinhVien.objects.create(
    MSSV='SV003',
    HoTen='Hoang Van C',
    GioiTinh=True,
    NgaySinh=date(2002, 3, 3),
    DiaChi='789 Nguyen Trai',
    Email='sv003@myuniversity.edu.vn',
    SoDienThoai='0123456789',
    MaPhong=p2,
)

sinhvien4 = SinhVien.objects.create(
    MSSV='SV004',
    HoTen='Le Thi D',
    GioiTinh=False,
    NgaySinh=date(2003, 4, 4),
    DiaChi='147 Tran Phu',
    Email='sv004@myuniversity.edu.vn',
    SoDienThoai='0987654321',
    MaPhong=p2,
)

sinhvien5 = SinhVien.objects.create(
    MSSV='SV005',
    HoTen='Pham Van E',
    GioiTinh=True,
    NgaySinh=date(2004, 5, 5),
    DiaChi='258 Nguyen Van Linh',
    Email='sv005@myuniversity.edu.vn',
    SoDienThoai='0123456789',
    MaPhong=p1,
)
