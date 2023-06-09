from django.db import models

# Create your models here.


class Phong(models.Model):
    id = models.IntegerField(primary_key=True)
    MaPhong = models.CharField(max_length=5)
    TrangThai = models.BooleanField(max_length=50)
    SoluongSV = models.IntegerField()
    LoaiPhong = models.CharField(max_length=50)
    Gia = models.IntegerField()
    TenToaNha = models.CharField(max_length=50)

    class Meta:
        db_table = 'Phong'
    @classmethod
    def create_Phong(cls, MaPhong, TrangThai, SoluongSV, LoaiPhong, Gia,TenToaNha):
        new_Phong = cls(MaPhong = MaPhong, TrangThai = TrangThai, SoluongSV = SoluongSV,
                         LoaiPhong = LoaiPhong, Gia = Gia,TenToaNha = TenToaNha)
        new_Phong.save()

class SinhVien(models.Model):
    id = models.IntegerField(primary_key=True)
    MSSV = models.CharField(max_length=50)
    HoTen = models.CharField(max_length=50)
    GioiTinh = models.BooleanField()
    NgaySinh = models.DateField()
    DiaChi = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    SoDienThoai = models.CharField(max_length=10)
    MaPhong = models.ForeignKey(Phong, on_delete=models.CASCADE)

    class Meta:
        db_table = 'SinhVien'


class QuanLi(models.Model):
    id = models.IntegerField(primary_key=True)
    MaQuanLi = models.CharField(max_length=50)
    HoTen = models.CharField(max_length=50)
    NgaySinh = models.DateField()
    SoDienThoai = models.CharField(max_length=10)
    Email = models.CharField(max_length=100)
    Role = models.CharField(max_length=50)

    class Meta:
        db_table = 'NhanVien'


class HopDong(models.Model):
    NgayBatDau = models.DateField()
    NgayKetThuc = models.DateField()
    GiaTien = models.IntegerField()
    TrangThaiThanhToan = models.BooleanField()
    MSSV = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    MaQuanLi = models.ForeignKey(QuanLi, on_delete=models.CASCADE)
    MaPhong = models.ForeignKey(Phong, on_delete=models.CASCADE)

    class Meta:
        db_table = 'HopDong'
