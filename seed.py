from main.models import Phong, SinhVien, QuanLi, HopDong
from datetime import date
from django.contrib.auth.models import User


def init():
    all_phong = Phong.objects.all()
    all_sv = SinhVien.objects.all()
    all_ql = QuanLi.objects.all()
    all_user = User.objects.all()
    all_con = HopDong.objects.all()
    all_user.delete()
    all_phong.delete()
    all_sv.delete()
    all_ql.delete()
    all_con.delete()

    # Create 5 Phong objects
    Phong.objects.create(MaPhong='P001', TrangThai=True, SoluongSV=4,
                         LoaiPhong='double', Gia=200, TenToaNha='Toa nha A')
    Phong.objects.create(MaPhong='P002', TrangThai=True, SoluongSV=2,
                         LoaiPhong='single', Gia=150, TenToaNha='Toa nha A')
    Phong.objects.create(MaPhong='P003', TrangThai=False, SoluongSV=6,
                         LoaiPhong='double', Gia=250, TenToaNha='Toa nha B')
    Phong.objects.create(MaPhong='P004', TrangThai=False, SoluongSV=2,
                         LoaiPhong='single', Gia=150, TenToaNha='Toa nha C')
    Phong.objects.create(MaPhong='P005', TrangThai=False, SoluongSV=4,
                         LoaiPhong='double', Gia=200, TenToaNha='Toa nha D')

    p1 = Phong.objects.filter(MaPhong='P001')[0]
    p2 = Phong.objects.filter(MaPhong='P002')[0]

    # Create 5 SinhVien objects
    SinhVien.objects.create(
        MSSV='SV001',
        HoTen='Nguyen Van A',
        GioiTinh=True,
        NgaySinh=date(2000, 1, 1),
        DiaChi='123 Nguyen Van Cu',
        Email='sv001@myuniversity.edu.vn',
        SoDienThoai='0123456789',
        MaPhong_id=p1.id,
    )

    SinhVien.objects.create(
        MSSV='SV002',
        HoTen='Tran Thi B',
        GioiTinh=False,
        NgaySinh=date(2001, 2, 2),
        DiaChi='456 Le Loi',
        Email='sv002@myuniversity.edu.vn',
        SoDienThoai='0987654321',
        MaPhong_id=p1.id,
    )

    SinhVien.objects.create(
        MSSV='SV003',
        HoTen='Hoang Van C',
        GioiTinh=True,
        NgaySinh=date(2002, 3, 3),
        DiaChi='789 Nguyen Trai',
        Email='sv003@myuniversity.edu.vn',
        SoDienThoai='0123456789',
        MaPhong_id=p2.id,
    )

    SinhVien.objects.create(
        MSSV='SV004',
        HoTen='Le Thi D',
        GioiTinh=False,
        NgaySinh=date(2003, 4, 4),
        DiaChi='147 Tran Phu',
        Email='sv004@myuniversity.edu.vn',
        SoDienThoai='0987654321',
        MaPhong_id=p2.id,
    )

    SinhVien.objects.create(
        MSSV='SV005',
        HoTen='Pham Van E',
        GioiTinh=True,
        NgaySinh=date(2004, 5, 5),
        DiaChi='258 Nguyen Van Linh',
        Email='sv005@myuniversity.edu.vn',
        SoDienThoai='0123456789',
        MaPhong_id=p1.id,
    )

    QuanLi.objects.create(id=1, MaQuanLi='QL001', HoTen='Nguyen Van A', NgaySinh=date(
        1980, 1, 1), SoDienThoai='0987654321', Email='nguyenvana@gmail.com', Role='Admin')

    QuanLi.objects.create(MaQuanLi='QL001', HoTen='Le Anh', NgaySinh=date(
        1990, 2, 2), SoDienThoai='0123456789', Email='anh@gmail.com', Role='ADMIN')
    QuanLi.objects.create(MaQuanLi='QL002', HoTen='Duong Bao', NgaySinh=date(
        1990, 2, 2), SoDienThoai='0123456789', Email='bao@gmail.com', Role='ADMIN')
    QuanLi.objects.create(MaQuanLi='QL003', HoTen='Vo Khang', NgaySinh=date(
        1990, 2, 2), SoDienThoai='0123456789', Email='khang@gmail.com', Role='ADMIN')
    QuanLi.objects.create(MaQuanLi='QL004', HoTen='Hoang Long', NgaySinh=date(
        1990, 2, 2), SoDienThoai='0123456789', Email='long@gmail.com', Role='ADMIN')
    QuanLi.objects.create(MaQuanLi='QL005', HoTen='Pham Van C', NgaySinh=date(
        2000, 3, 3), SoDienThoai='0912345678', Email='phamvanc@gmail.com', Role='NORMAL')
    QuanLi.objects.create(MaQuanLi='QL006', HoTen='Le Thi D', NgaySinh=date(
        1970, 4, 4), SoDienThoai='0845678901', Email='lethid@gmail.com', Role='NORMAL')
    QuanLi.objects.create(MaQuanLi='QL007', HoTen='Hoang Van E', NgaySinh=date(
        1985, 5, 5), SoDienThoai='0777777777', Email='hoangvane@gmail.com', Role='Admin')

    User.objects.create_user('anh@gmail.com', 'anh@gmail.com', '123456')

    sinhviens = SinhVien.objects.all()
    ql = QuanLi.objects.all()[0]

    for sinhvien in sinhviens:
        HopDong.objects.create(
            NgayBatDau=date(2023, 5, 1),
            NgayKetThuc=date(2024, 4, 30),
            GiaTien=5000000,
            TrangThaiThanhToan=False,
            MSSV=SinhVien.objects.get(id=sinhvien.id),
            MaQuanLi=QuanLi.objects.get(id=ql.id),
            MaPhong=Phong.objects.get(id=sinhvien.MaPhong_id)
        )

    # User.objects.create_user('anh@gmail.com' , 'anh@gmail.com' , '123456')


# import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect('db.sqlite3')

# # Create a cursor object
# cursor = conn.cursor()

# # Execute the SQL command to rename the table
# cursor.execute("ALTER TABLE QuanLi RENAME TO NhanVien;")

# # Commit the changes to the database
# conn.commit()

# # Close the database connection
# conn.close()
