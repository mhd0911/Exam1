from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class MonAn(Base):
    __tablename__ = "monan"
    MaMon = Column(Integer, primary_key=True, index=True)
    TenMon = Column(String(255))
    Gia = Column(Float)
    MoTa = Column(String(255))

class KhachHang(Base):
    __tablename__ = "khachhang"
    MaKH = Column(Integer, primary_key=True, index=True)
    TenKH = Column(String(255))
    SDT = Column(String(20))
    DiaChi = Column(String(255))

class HoaDon(Base):
    __tablename__ = "hoadon"
    MaHD = Column(Integer, primary_key=True, index=True)
    NgayLap = Column(Date)
    MaKH = Column(Integer, ForeignKey("khachhang.MaKH"))
    khachhang = relationship("KhachHang")

class ChiTietHoaDon(Base):
    __tablename__ = "chitiethoadon"
    MaHD = Column(Integer, ForeignKey("hoadon.MaHD"), primary_key=True)
    MaMon = Column(Integer, ForeignKey("monan.MaMon"), primary_key=True)
    SoLuong = Column(Integer)
    GhiChu = Column(String(100))
