from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/monan")
def show_monan(request: Request, db: Session = Depends(get_db)):
    ds = db.query(models.MonAn).all()
    return templates.TemplateResponse("monan.html", {"request": request, "ds": ds})

@app.post("/monan")
def add_monan(TenMon: str = Form(...), Gia: float = Form(...), MoTa: str = Form(""), db: Session = Depends(get_db)):
    db.add(models.MonAn(TenMon=TenMon, Gia=Gia, MoTa=MoTa))
    db.commit()
    return RedirectResponse("/monan", status_code=303)

@app.get("/khachhang")
def show_kh(request: Request, db: Session = Depends(get_db)):
    ds = db.query(models.KhachHang).all()
    return templates.TemplateResponse("khachhang.html", {"request": request, "ds": ds})

@app.post("/khachhang")
def add_kh(TenKH: str = Form(...), SDT: str = Form(...), DiaChi: str = Form(""), db: Session = Depends(get_db)):
    db.add(models.KhachHang(TenKH=TenKH, SDT=SDT, DiaChi=DiaChi))
    db.commit()
    return RedirectResponse("/khachhang", status_code=303)

@app.get("/hoadon")
def show_hd(request: Request, db: Session = Depends(get_db)):
    ds = db.query(models.HoaDon).all()
    return templates.TemplateResponse("hoadon.html", {"request": request, "ds": ds})

@app.post("/hoadon")
def add_hd(NgayLap: str = Form(...), MaKH: int = Form(...), db: Session = Depends(get_db)):
    db.add(models.HoaDon(NgayLap=NgayLap, MaKH=MaKH))
    db.commit()
    return RedirectResponse("/hoadon", status_code=303)

@app.get("/chitiethoadon")
def show_cthd(request: Request, db: Session = Depends(get_db)):
    ds = db.query(models.ChiTietHoaDon).all()
    return templates.TemplateResponse("chitiethoadon.html", {"request": request, "ds": ds})

@app.post("/chitiethoadon")
def add_cthd(MaHD: int = Form(...), MaMon: int = Form(...), SoLuong: int = Form(...), GhiChu: str = Form(""), db: Session = Depends(get_db)):
    db.add(models.ChiTietHoaDon(MaHD=MaHD, MaMon=MaMon, SoLuong=SoLuong, GhiChu=GhiChu))
    db.commit()
    return RedirectResponse("/chitiethoadon", status_code=303)

# XÓA MÓN ĂN
@app.post("/monan/delete/{ma_mon}")
def delete_monan(ma_mon: int, db: Session = Depends(get_db)):
    mon = db.query(models.MonAn).filter(models.MonAn.MaMon == ma_mon).first()
    if mon:
        db.delete(mon)
        db.commit()
    return RedirectResponse("/monan", status_code=303)

# XÓA KHÁCH HÀNG
@app.post("/khachhang/delete/{ma_kh}")
def delete_kh(ma_kh: int, db: Session = Depends(get_db)):
    kh = db.query(models.KhachHang).filter(models.KhachHang.MaKH == ma_kh).first()
    if kh:
        db.delete(kh)
        db.commit()
    return RedirectResponse("/khachhang", status_code=303)

# XÓA HÓA ĐƠN
@app.post("/hoadon/delete/{ma_hd}")
def delete_hd(ma_hd: int, db: Session = Depends(get_db)):
    hd = db.query(models.HoaDon).filter(models.HoaDon.MaHD == ma_hd).first()
    if hd:
        db.delete(hd)
        db.commit()
    return RedirectResponse("/hoadon", status_code=303)

# XÓA CHI TIẾT HÓA ĐƠN
@app.post("/chitiethoadon/delete")
def delete_cthd(MaHD: int = Form(...), MaMon: int = Form(...), db: Session = Depends(get_db)):
    ct = db.query(models.ChiTietHoaDon).filter_by(MaHD=MaHD, MaMon=MaMon).first()
    if ct:
        db.delete(ct)
        db.commit()
    return RedirectResponse("/chitiethoadon", status_code=303)
