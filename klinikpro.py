"""
KlinikPro — Doktor Randevu Sistemi
PyQt5 Modern Arayüz | Orman Yeşili Tema
Tek dosya — harici bağımlılık yok (sadece PyQt5)

Kurulum:
    pip install PyQt5

Çalıştırma:
    python klinikpro.py
"""

import sys
from datetime import date
from typing import Optional, List, Dict

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit,
    QTableWidget, QTableWidgetItem, QStackedWidget, QFrame,
    QScrollArea, QMessageBox, QHeaderView, QAbstractItemView,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush, QPen


# ═══════════════════════════════════════════════════════════════
#  BACKEND — VERİ KATMANI
# ═══════════════════════════════════════════════════════════════

_hasta_sayac = 0
_doktor_sayac = 0
_randevu_sayac = 0


def _yeni_hasta_id():
    global _hasta_sayac
    _hasta_sayac += 1
    return _hasta_sayac


def _yeni_doktor_id():
    global _doktor_sayac
    _doktor_sayac += 1
    return _doktor_sayac


def _yeni_randevu_id():
    global _randevu_sayac
    _randevu_sayac += 1
    return _randevu_sayac


class Hasta:
    def __init__(self, ad, tc, telefon):
        if not ad.strip():
            raise ValueError("Hasta adı boş olamaz.")
        if not tc.isdigit() or len(tc) != 11:
            raise ValueError("TC kimlik numarası 11 haneli rakam olmalıdır.")
        if not telefon.strip():
            raise ValueError("Telefon numarası boş olamaz.")
        self.hasta_id = _yeni_hasta_id()
        self.ad = ad.strip()
        self.tc = tc
        self.telefon = telefon.strip()
        self._randevular = []

    def randevu_al(self, doktor, tarih, saat):
        if not doktor.uygunluk_kontrol(tarih, saat):
            raise ValueError(
                f"Dr. {doktor.ad} için {tarih} tarihinde {saat} saati müsait değil."
            )
        r = Randevu(tarih, saat, doktor, self)
        r.randevu_olustur()
        self._randevular.append(r)
        return r

    def randevularim(self):
        return list(self._randevular)


class Doktor:
    def __init__(self, ad, uzmanlik, uygun_saatler=None):
        if not ad.strip():
            raise ValueError("Doktor adı boş olamaz.")
        if not uzmanlik.strip():
            raise ValueError("Uzmanlık alanı boş olamaz.")
        self.doktor_id = _yeni_doktor_id()
        self.ad = ad.strip()
        self.uzmanlik = uzmanlik.strip()
        self.uygun_saatler = uygun_saatler or {}

    def uygunluk_kontrol(self, tarih, saat):
        return saat in self.uygun_saatler.get(tarih, [])

    def saat_ekle(self, tarih, saat):
        self.uygun_saatler.setdefault(tarih, []).append(saat)

    def saat_kaldir(self, tarih, saat):
        if tarih in self.uygun_saatler and saat in self.uygun_saatler[tarih]:
            self.uygun_saatler[tarih].remove(saat)


class Randevu:
    def __init__(self, tarih, saat, doktor, hasta):
        self.randevu_id = _yeni_randevu_id()
        self.tarih = tarih
        self.saat = saat
        self.doktor = doktor
        self.hasta = hasta
        self.aktif = False

    def randevu_olustur(self):
        self.aktif = True
        self.doktor.saat_kaldir(self.tarih, self.saat)

    def randevu_iptal(self):
        if not self.aktif:
            raise ValueError("Bu randevu zaten iptal edilmiş.")
        self.aktif = False
        self.doktor.saat_ekle(self.tarih, self.saat)
        if self in self.hasta._randevular:
            self.hasta._randevular.remove(self)


class RandevuSistemi:
    def __init__(self):
        self.hastalar = {}
        self.doktorlar = {}
        self.randevular = {}

    def hasta_kaydet(self, ad, tc, telefon):
        h = Hasta(ad, tc, telefon)
        self.hastalar[h.hasta_id] = h
        return h

    def doktor_kaydet(self, ad, uzmanlik):
        d = Doktor(ad, uzmanlik)
        self.doktorlar[d.doktor_id] = d
        return d

    def randevu_olustur(self, hasta, doktor, tarih, saat):
        r = hasta.randevu_al(doktor, tarih, saat)
        self.randevular[r.randevu_id] = r
        return r

    def gunluk_randevu_listesi(self, tarih):
        return [r for r in self.randevular.values() if r.tarih == tarih and r.aktif]


# ═══════════════════════════════════════════════════════════════
#  RENK PALETİ — ORMAN YEŞİLİ
# ═══════════════════════════════════════════════════════════════

G = {
    "bg":         "#070F0C",
    "surface":    "#0C1A14",
    "card":       "#10211A",
    "card2":      "#162D23",
    "border":     "#1E4030",
    "border2":    "#2A5540",

    "green":      "#22C55E",
    "green_l":    "#4ADE80",
    "green_ll":   "#86EFAC",
    "mint":       "#10B981",
    "mint_l":     "#34D399",
    "lime":       "#84CC16",

    "danger":     "#F43F5E",
    "danger_l":   "#FB7185",
    "warning":    "#F59E0B",
    "warning_l":  "#FCD34D",
    "info":       "#06B6D4",

    "text":       "#DCFCE7",
    "text2":      "#6EE7B7",
    "text3":      "#4B7A63",
    "white":      "#FFFFFF",

    "nav0":       "#22C55E",
    "nav1":       "#10B981",
    "nav2":       "#06B6D4",
    "nav3":       "#F59E0B",
}

STYLE = """
QMainWindow, QWidget {
    background-color: """ + G["bg"] + """;
    color: """ + G["text"] + """;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}
QLabel { background: transparent; color: """ + G["text"] + """; }

QLineEdit, QComboBox, QDateEdit {
    background-color: """ + G["card2"] + """;
    color: """ + G["text"] + """;
    border: 1.5px solid """ + G["border2"] + """;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    min-height: 18px;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 1.5px solid """ + G["green"] + """;
    background-color: """ + G["card"] + """;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
    background: transparent;
}
QComboBox::down-arrow {
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid """ + G["text3"] + """;
    margin-right: 10px;
}
QComboBox QAbstractItemView {
    background-color: """ + G["card2"] + """;
    color: """ + G["text"] + """;
    border: 1.5px solid """ + G["border2"] + """;
    selection-background-color: """ + G["green"] + """;
    selection-color: """ + G["bg"] + """;
    outline: none;
    padding: 4px;
}
QDateEdit::drop-down {
    border: none;
    width: 28px;
    background: transparent;
}
QCalendarWidget {
    background-color: """ + G["card"] + """;
    color: """ + G["text"] + """;
}
QCalendarWidget QToolButton {
    color: """ + G["text"] + """;
    background: """ + G["card2"] + """;
    border: 1px solid """ + G["border"] + """;
    border-radius: 6px;
    padding: 4px 10px;
    margin: 2px;
}
QCalendarWidget QToolButton:hover {
    background: """ + G["border2"] + """;
}
QCalendarWidget QAbstractItemView:enabled {
    background-color: """ + G["card"] + """;
    color: """ + G["text"] + """;
    selection-background-color: """ + G["green"] + """;
    selection-color: """ + G["bg"] + """;
}
QCalendarWidget QAbstractItemView:disabled {
    color: """ + G["text3"] + """;
}
QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: """ + G["card2"] + """;
    border-bottom: 1px solid """ + G["border"] + """;
}

QTableWidget {
    background-color: """ + G["card"] + """;
    color: """ + G["text"] + """;
    border: 1.5px solid """ + G["border"] + """;
    border-radius: 12px;
    gridline-color: """ + G["border"] + """;
    outline: none;
}
QTableWidget::item {
    padding: 8px 14px;
    border: none;
    border-bottom: 1px solid """ + G["border"] + """;
}
QTableWidget::item:selected {
    background-color: rgba(34,197,94,0.15);
    color: """ + G["green_l"] + """;
}
QTableWidget::item:hover {
    background-color: rgba(34,197,94,0.07);
}
QHeaderView::section {
    background-color: """ + G["card2"] + """;
    color: """ + G["text3"] + """;
    border: none;
    border-bottom: 1px solid """ + G["border2"] + """;
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
}
QHeaderView { background: transparent; }

QScrollBar:vertical {
    background: transparent;
    width: 5px;
    margin: 4px;
}
QScrollBar::handle:vertical {
    background: """ + G["border2"] + """;
    border-radius: 3px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: """ + G["green"] + """; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { height: 0; }
QScrollArea { border: none; background: transparent; }

QMessageBox {
    background-color: """ + G["card"] + """;
    color: """ + G["text"] + """;
}
QMessageBox QLabel { color: """ + G["text"] + """; }
QMessageBox QPushButton {
    background-color: """ + G["green"] + """;
    color: """ + G["bg"] + """;
    border: none;
    border-radius: 8px;
    padding: 8px 24px;
    font-weight: 700;
    min-width: 80px;
}
QMessageBox QPushButton:hover { background-color: """ + G["green_l"] + """; }
"""


# ═══════════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR & WIDGET'LAR
# ═══════════════════════════════════════════════════════════════

def mk_lbl(text, size=13, bold=False, color=None, align=Qt.AlignLeft):
    w = QLabel(text)
    f = QFont("Segoe UI", size)
    f.setBold(bold)
    w.setFont(f)
    w.setStyleSheet(f"color: {color or G['text']}; background: transparent;")
    w.setAlignment(align)
    return w


def add_shadow(widget, blur=30, dy=6, color="#000000", alpha=90):
    e = QGraphicsDropShadowEffect(widget)
    e.setBlurRadius(blur)
    e.setXOffset(0)
    e.setYOffset(dy)
    c = QColor(color)
    c.setAlpha(alpha)
    e.setColor(c)
    widget.setGraphicsEffect(e)


class GradientCard(QFrame):
    """Üst kenarda ince renkli çizgi olan koyu kart."""
    def __init__(self, accent=None, parent=None):
        super().__init__(parent)
        self.accent = accent or G["green"]
        self.setStyleSheet(
            f"QFrame {{ background-color: {G['card']};"
            f"border: 1.5px solid {G['border2']};"
            f"border-radius: 16px; }}"
        )
        add_shadow(self, blur=35, dy=8, alpha=80)

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), 0)
        c1 = QColor(self.accent); c1.setAlpha(220)
        c2 = QColor(G["mint_l"]); c2.setAlpha(160)
        grad.setColorAt(0, c1)
        grad.setColorAt(1, c2)
        p.setBrush(QBrush(grad))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), 3, 2, 2)
        p.end()


class GlowBtn(QPushButton):
    """Gradient yeşil buton."""
    def __init__(self, text, c1=None, c2=None, parent=None):
        super().__init__(text, parent)
        self.c1 = c1 or G["green"]
        self.c2 = c2 or G["mint"]
        self.setMinimumHeight(44)
        self.setCursor(Qt.PointingHandCursor)
        self._set_style(False)

    def _set_style(self, hover):
        if hover:
            c1, c2 = G["green_l"], G["mint_l"]
        else:
            c1, c2 = self.c1, self.c2
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {c1}, stop:1 {c2});
                color: {G['bg']};
                border: none;
                border-radius: 11px;
                font-size: 13px;
                font-weight: 700;
                padding: 0 26px;
            }}
        """)

    def enterEvent(self, e):
        self._set_style(True)

    def leaveEvent(self, e):
        self._set_style(False)


class DangerBtn(QPushButton):
    def __init__(self, text="✕ İptal", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(34)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: rgba(244,63,94,0.10);
                color: {G['danger_l']};
                border: 1px solid rgba(244,63,94,0.30);
                border-radius: 8px;
                font-size: 12px;
                font-weight: 600;
                padding: 0 12px;
            }}
            QPushButton:hover {{
                background: rgba(244,63,94,0.20);
                border-color: {G['danger']};
            }}
        """)


class NavBtn(QPushButton):
    COLORS = [G["nav0"], G["nav1"], G["nav2"], G["nav3"]]

    def __init__(self, icon, text, idx, parent=None):
        super().__init__(parent)
        self.icon_ch = icon
        self.label = text
        self.accent = self.COLORS[idx % 4]
        self._active = False
        self.setFixedHeight(52)
        self.setCursor(Qt.PointingHandCursor)
        self._draw()

    def set_active(self, v):
        self._active = v
        self._draw()

    def _draw(self):
        r, g, b = self._rgb(self.accent)
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba({r},{g},{b},0.15);
                    color: {self.accent};
                    border: none;
                    border-left: 3px solid {self.accent};
                    border-radius: 0px;
                    text-align: left;
                    padding-left: 22px;
                    font-size: 13px;
                    font-weight: 700;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {G['text3']};
                    border: none;
                    border-left: 3px solid transparent;
                    border-radius: 0px;
                    text-align: left;
                    padding-left: 22px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: rgba({r},{g},{b},0.07);
                    color: {G['text2']};
                    border-left: 3px solid {G['border2']};
                }}
            """)
        self.setText(f"  {self.icon_ch}   {self.label}")

    @staticmethod
    def _rgb(h):
        h = h.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


class StatCard(QFrame):
    def __init__(self, icon, num, label, accent, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"QFrame {{ background-color: {G['card2']};"
            f"border: 1.5px solid {G['border2']};"
            f"border-radius: 14px; }}"
        )
        add_shadow(self, 20, 4, accent, 80)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(4)
        lay.addWidget(mk_lbl(icon, 20))
        self._num = mk_lbl(str(num), 26, bold=True, color=accent)
        lay.addWidget(self._num)
        lay.addWidget(mk_lbl(label, 10, color=G["text3"]))

    def set_value(self, v):
        self._num.setText(str(v))


def field_group(label_text, widget, hint=""):
    v = QVBoxLayout(); v.setSpacing(6)
    row = QHBoxLayout(); row.setSpacing(6)
    row.addWidget(mk_lbl(label_text, 10, color=G["text3"]))
    if hint:
        hl = mk_lbl(hint, 10, color=G["green"])
        hl.setStyleSheet(
            f"color:{G['green']};background:rgba(34,197,94,0.1);"
            f"border:1px solid rgba(34,197,94,0.25);border-radius:10px;padding:1px 8px;"
        )
        row.addWidget(hl)
    row.addStretch()
    v.addLayout(row)
    v.addWidget(widget)
    return v


def make_table(headers, stretch_last=True):
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setSelectionBehavior(QAbstractItemView.SelectRows)
    t.setShowGrid(False)
    t.setAlternatingRowColors(True)
    t.setStyleSheet(
        t.styleSheet() +
        f"QTableWidget {{alternate-background-color: {G['card2']};}}"
    )
    return t


def tbl_item(text):
    item = QTableWidgetItem(text)
    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    return item


# ═══════════════════════════════════════════════════════════════
#  SAYFALAR
# ═══════════════════════════════════════════════════════════════

class HastaPage(QWidget):
    sig_refresh = pyqtSignal()

    def __init__(self, sistem):
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 30, 36, 30)
        root.setSpacing(24)

        # Başlık satırı
        hrow = QHBoxLayout()
        col = QVBoxLayout(); col.setSpacing(4)
        col.addWidget(mk_lbl("👤  Hasta Yönetimi", 20, bold=True))
        col.addWidget(mk_lbl("Yeni hasta ekleyin ve kayıtları görüntüleyin.", 12, color=G["text3"]))
        hrow.addLayout(col); hrow.addStretch()
        self.stat = StatCard("🏥", 0, "Toplam Hasta", G["green"])
        self.stat.setFixedSize(150, 88)
        hrow.addWidget(self.stat)
        root.addLayout(hrow)

        # Form kartı
        card = GradientCard(G["green"])
        fl = QVBoxLayout(card); fl.setContentsMargins(28, 26, 28, 26); fl.setSpacing(18)
        fl.addWidget(mk_lbl("Yeni Hasta Kaydı", 13, bold=True, color=G["green_l"]))

        self.inp_ad  = QLineEdit(); self.inp_ad.setPlaceholderText("Ad Soyad")
        self.inp_tc  = QLineEdit(); self.inp_tc.setPlaceholderText("11 haneli TC No"); self.inp_tc.setMaxLength(11)
        self.inp_tel = QLineEdit(); self.inp_tel.setPlaceholderText("0555 xxx xx xx")

        frow = QHBoxLayout(); frow.setSpacing(14)
        frow.addLayout(field_group("AD SOYAD", self.inp_ad))
        frow.addLayout(field_group("TC KİMLİK", self.inp_tc, "11 hane"))
        frow.addLayout(field_group("TELEFON", self.inp_tel))
        fl.addLayout(frow)

        btn = GlowBtn("  ✦  Kaydet")
        btn.setFixedWidth(160); btn.clicked.connect(self._kaydet)
        br = QHBoxLayout(); br.addWidget(btn); br.addStretch()
        fl.addLayout(br)
        root.addWidget(card)

        root.addWidget(mk_lbl("Hasta Listesi", 14, bold=True))
        self.tablo = make_table(["ID", "Ad Soyad", "TC Kimlik", "Telefon"])
        root.addWidget(self.tablo)

    def _kaydet(self):
        try:
            h = self.sistem.hasta_kaydet(
                self.inp_ad.text(), self.inp_tc.text(), self.inp_tel.text()
            )
            r = self.tablo.rowCount(); self.tablo.insertRow(r)
            for c, v in enumerate([str(h.hasta_id), h.ad, h.tc, h.telefon]):
                self.tablo.setItem(r, c, tbl_item(v))
            self.tablo.setRowHeight(r, 44)
            self.inp_ad.clear(); self.inp_tc.clear(); self.inp_tel.clear()
            self.stat.set_value(len(self.sistem.hastalar))
            self.sig_refresh.emit()
            QMessageBox.information(self, "KlinikPro", f"✅  {h.ad} başarıyla kaydedildi.")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def refresh_combos(self):
        pass


class DoktorPage(QWidget):
    sig_refresh = pyqtSignal()

    def __init__(self, sistem):
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 30, 36, 30)
        root.setSpacing(24)

        hrow = QHBoxLayout()
        col = QVBoxLayout(); col.setSpacing(4)
        col.addWidget(mk_lbl("🩺  Doktor Yönetimi", 20, bold=True))
        col.addWidget(mk_lbl("Doktor kaydı ve müsait saat yönetimi.", 12, color=G["text3"]))
        hrow.addLayout(col); hrow.addStretch()
        self.stat = StatCard("👨‍⚕️", 0, "Toplam Doktor", G["mint"])
        self.stat.setFixedSize(150, 88)
        hrow.addWidget(self.stat)
        root.addLayout(hrow)

        # Doktor kayıt kartı
        card = GradientCard(G["mint"])
        fl = QVBoxLayout(card); fl.setContentsMargins(28, 26, 28, 26); fl.setSpacing(18)
        fl.addWidget(mk_lbl("Yeni Doktor Kaydı", 13, bold=True, color=G["mint_l"]))

        self.inp_ad  = QLineEdit(); self.inp_ad.setPlaceholderText("Dr. Ad Soyad")
        self.inp_uzm = QLineEdit(); self.inp_uzm.setPlaceholderText("Kardiyoloji, Nöroloji…")

        frow = QHBoxLayout(); frow.setSpacing(14)
        frow.addLayout(field_group("DOKTOR ADI", self.inp_ad))
        frow.addLayout(field_group("UZMANLIK", self.inp_uzm))
        fl.addLayout(frow)

        btn = GlowBtn("  ✦  Kaydet", G["mint"], G["green"])
        btn.setFixedWidth(160); btn.clicked.connect(self._kaydet)
        br = QHBoxLayout(); br.addWidget(btn); br.addStretch()
        fl.addLayout(br)
        root.addWidget(card)

        # Saat ekleme kartı
        scard = GradientCard(G["info"])
        sf = QVBoxLayout(scard); sf.setContentsMargins(28, 26, 28, 26); sf.setSpacing(18)
        sf.addWidget(mk_lbl("Müsait Saat Ekle", 13, bold=True, color=G["info"]))

        self.cmb_doktor = QComboBox()
        self.inp_tarih  = QDateEdit(QDate.currentDate()); self.inp_tarih.setCalendarPopup(True)
        self.inp_saat   = QLineEdit(); self.inp_saat.setPlaceholderText("09:00")

        srow = QHBoxLayout(); srow.setSpacing(14)
        srow.addLayout(field_group("DOKTOR", self.cmb_doktor))
        srow.addLayout(field_group("TARİH", self.inp_tarih))
        srow.addLayout(field_group("SAAT", self.inp_saat, "SS:DD"))
        sf.addLayout(srow)

        sbtn = GlowBtn("  ＋  Saat Ekle", G["info"], G["mint"])
        sbtn.setFixedWidth(160); sbtn.clicked.connect(self._saat_ekle)
        sbr = QHBoxLayout(); sbr.addWidget(sbtn); sbr.addStretch()
        sf.addLayout(sbr)
        root.addWidget(scard)

        root.addWidget(mk_lbl("Doktor Listesi", 14, bold=True))
        self.tablo = make_table(["ID", "Doktor Adı", "Uzmanlık"])
        root.addWidget(self.tablo)

    def _kaydet(self):
        try:
            d = self.sistem.doktor_kaydet(self.inp_ad.text(), self.inp_uzm.text())
            r = self.tablo.rowCount(); self.tablo.insertRow(r)
            for c, v in enumerate([str(d.doktor_id), d.ad, d.uzmanlik]):
                self.tablo.setItem(r, c, tbl_item(v))
            self.tablo.setRowHeight(r, 44)
            self.cmb_doktor.addItem(f"[{d.doktor_id}]  {d.ad}", d.doktor_id)
            self.inp_ad.clear(); self.inp_uzm.clear()
            self.stat.set_value(len(self.sistem.doktorlar))
            self.sig_refresh.emit()
            QMessageBox.information(self, "KlinikPro", f"✅  Dr. {d.ad} kaydedildi.")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def _saat_ekle(self):
        idx = self.cmb_doktor.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir doktor seçin."); return
        did = self.cmb_doktor.itemData(idx)
        d = self.sistem.doktorlar.get(did)
        qd = self.inp_tarih.date()
        t = date(qd.year(), qd.month(), qd.day())
        s = self.inp_saat.text().strip()
        if not s:
            QMessageBox.warning(self, "Hata", "Saat boş olamaz."); return
        d.saat_ekle(t, s)
        self.inp_saat.clear()
        QMessageBox.information(self, "KlinikPro", f"✅  {t}  —  {s} saati eklendi.")

    def refresh_combos(self):
        pass


class RandevuPage(QWidget):
    sig_refresh = pyqtSignal()

    def __init__(self, sistem):
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 30, 36, 30)
        root.setSpacing(24)

        hrow = QHBoxLayout()
        col = QVBoxLayout(); col.setSpacing(4)
        col.addWidget(mk_lbl("📅  Randevu Yönetimi", 20, bold=True))
        col.addWidget(mk_lbl("Hasta-doktor eşleştirerek randevu oluşturun.", 12, color=G["text3"]))
        hrow.addLayout(col); hrow.addStretch()
        self.stat = StatCard("📋", 0, "Aktif Randevu", G["info"])
        self.stat.setFixedSize(150, 88)
        hrow.addWidget(self.stat)
        root.addLayout(hrow)

        card = GradientCard(G["info"])
        fl = QVBoxLayout(card); fl.setContentsMargins(28, 26, 28, 26); fl.setSpacing(18)
        fl.addWidget(mk_lbl("Randevu Oluştur", 13, bold=True, color=G["info"]))

        self.cmb_hasta   = QComboBox()
        self.cmb_doktor  = QComboBox()
        self.inp_tarih   = QDateEdit(QDate.currentDate()); self.inp_tarih.setCalendarPopup(True)
        self.inp_saat    = QLineEdit(); self.inp_saat.setPlaceholderText("10:00")

        r1 = QHBoxLayout(); r1.setSpacing(14)
        r1.addLayout(field_group("HASTA", self.cmb_hasta))
        r1.addLayout(field_group("DOKTOR", self.cmb_doktor))
        fl.addLayout(r1)

        r2 = QHBoxLayout(); r2.setSpacing(14)
        r2.addLayout(field_group("TARİH", self.inp_tarih))
        r2.addLayout(field_group("SAAT", self.inp_saat, "SS:DD"))
        r2.addStretch(1)
        fl.addLayout(r2)

        btn = GlowBtn("  📅  Randevu Oluştur", G["info"], G["green"])
        btn.setFixedWidth(210); btn.clicked.connect(self._olustur)
        br = QHBoxLayout(); br.addWidget(btn); br.addStretch()
        fl.addLayout(br)
        root.addWidget(card)

        root.addWidget(mk_lbl("Aktif Randevular", 14, bold=True))
        self.tablo = make_table(["ID", "Hasta", "Doktor", "Tarih", "Saat", ""])
        self.tablo.horizontalHeader().setSectionResizeMode(5, QHeaderView.Fixed)
        self.tablo.setColumnWidth(5, 100)
        root.addWidget(self.tablo)

    def refresh_combos(self):
        self.cmb_hasta.clear()
        for h in self.sistem.hastalar.values():
            self.cmb_hasta.addItem(f"[{h.hasta_id}]  {h.ad}", h.hasta_id)
        self.cmb_doktor.clear()
        for d in self.sistem.doktorlar.values():
            self.cmb_doktor.addItem(f"[{d.doktor_id}]  {d.ad}", d.doktor_id)

    def _olustur(self):
        hi = self.cmb_hasta.currentIndex()
        di = self.cmb_doktor.currentIndex()
        if hi < 0 or di < 0:
            QMessageBox.warning(self, "Hata", "Hasta ve doktor seçin."); return
        h = self.sistem.hastalar.get(self.cmb_hasta.itemData(hi))
        d = self.sistem.doktorlar.get(self.cmb_doktor.itemData(di))
        qd = self.inp_tarih.date()
        t = date(qd.year(), qd.month(), qd.day())
        s = self.inp_saat.text().strip()
        if not s:
            QMessageBox.warning(self, "Hata", "Saat boş olamaz."); return
        try:
            r = self.sistem.randevu_olustur(h, d, t, s)
            self._tablo_ekle(r)
            self.inp_saat.clear()
            aktif_sayi = sum(1 for x in self.sistem.randevular.values() if x.aktif)
            self.stat.set_value(aktif_sayi)
            self.sig_refresh.emit()
            QMessageBox.information(self, "KlinikPro", f"✅  Randevu oluşturuldu — ID: {r.randevu_id}")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def _tablo_ekle(self, r):
        row = self.tablo.rowCount(); self.tablo.insertRow(row)
        for c, v in enumerate([str(r.randevu_id), r.hasta.ad, r.doktor.ad, str(r.tarih), r.saat]):
            self.tablo.setItem(row, c, tbl_item(v))
        btn = DangerBtn()
        rid = r.randevu_id
        btn.clicked.connect(lambda _, i=rid: self._iptal(i))
        self.tablo.setCellWidget(row, 5, btn)
        self.tablo.setRowHeight(row, 48)

    def _iptal(self, rid):
        r = self.sistem.randevular.get(rid)
        if not r: return
        try:
            r.randevu_iptal()
            for row in range(self.tablo.rowCount()):
                item = self.tablo.item(row, 0)
                if item and item.text() == str(rid):
                    self.tablo.removeRow(row)
                    break
            aktif_sayi = sum(1 for x in self.sistem.randevular.values() if x.aktif)
            self.stat.set_value(aktif_sayi)
            self.sig_refresh.emit()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))


class GunlukPage(QWidget):
    def __init__(self, sistem):
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(36, 30, 36, 30)
        root.setSpacing(24)

        root.addWidget(mk_lbl("📋  Günlük Randevu Listesi", 20, bold=True))
        root.addWidget(mk_lbl("Seçili güne ait tüm aktif randevuları görüntüleyin.", 12, color=G["text3"]))

        card = GradientCard(G["warning"])
        fl = QVBoxLayout(card); fl.setContentsMargins(28, 24, 28, 24); fl.setSpacing(14)
        fl.addWidget(mk_lbl("Tarih Seçin", 13, bold=True, color=G["warning_l"]))

        ctrl = QHBoxLayout(); ctrl.setSpacing(12)
        self.inp_tarih = QDateEdit(QDate.currentDate()); self.inp_tarih.setCalendarPopup(True)
        self.inp_tarih.setFixedWidth(190)
        btn = GlowBtn("  🔍  Listele", G["warning"], G["green"])
        btn.setFixedWidth(140); btn.clicked.connect(self._listele)
        self.lbl_sayi = mk_lbl("", 12, color=G["green_l"])
        ctrl.addWidget(self.inp_tarih); ctrl.addWidget(btn); ctrl.addWidget(self.lbl_sayi)
        ctrl.addStretch()
        fl.addLayout(ctrl)
        root.addWidget(card)

        root.addWidget(mk_lbl("Sonuçlar", 14, bold=True))
        self.tablo = make_table(["Randevu ID", "Doktor", "Hasta", "Saat"])
        root.addWidget(self.tablo)

    def _listele(self):
        qd = self.inp_tarih.date()
        t = date(qd.year(), qd.month(), qd.day())
        liste = self.sistem.gunluk_randevu_listesi(t)
        self.tablo.setRowCount(0)
        for r in sorted(liste, key=lambda x: x.saat):
            row = self.tablo.rowCount(); self.tablo.insertRow(row)
            for c, v in enumerate([str(r.randevu_id), r.doktor.ad, r.hasta.ad, r.saat]):
                self.tablo.setItem(row, c, tbl_item(v))
            self.tablo.setRowHeight(row, 44)
        self.lbl_sayi.setText(f"  {len(liste)} randevu bulundu")

    def refresh_combos(self):
        pass


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════

class Sidebar(QWidget):
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        grad = QLinearGradient(0, 0, 0, self.height())
        grad.setColorAt(0.0, QColor("#0A1A13"))
        grad.setColorAt(1.0, QColor("#060E09"))
        p.fillRect(self.rect(), grad)
        p.setPen(QPen(QColor(G["border"]), 1))
        p.drawLine(self.width() - 1, 0, self.width() - 1, self.height())
        p.end()


# ═══════════════════════════════════════════════════════════════
#  ANA PENCERE
# ═══════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistem = RandevuSistemi()
        self.setWindowTitle("KlinikPro — Doktor Randevu Sistemi")
        self.resize(1160, 750)
        self.setMinimumSize(920, 620)
        self._build()

    def _build(self):
        central = QWidget(); self.setCentralWidget(central)
        row = QHBoxLayout(central); row.setContentsMargins(0, 0, 0, 0); row.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────
        sb_widget = Sidebar(); sb_widget.setFixedWidth(228)
        sb = QVBoxLayout(sb_widget); sb.setContentsMargins(0, 0, 0, 0); sb.setSpacing(0)

        # Logo alanı
        logo = QWidget(); logo.setFixedHeight(74)
        logo.setStyleSheet(f"background: transparent; border-bottom: 1px solid {G['border']};")
        ll = QHBoxLayout(logo); ll.setContentsMargins(20, 0, 0, 0); ll.setSpacing(10)
        ll.addWidget(mk_lbl("🏥", 24))
        lc = QVBoxLayout(); lc.setSpacing(1)
        lc.addWidget(mk_lbl("KlinikPro", 15, bold=True, color=G["green_l"]))
        lc.addWidget(mk_lbl("Randevu Sistemi", 9, color=G["text3"]))
        ll.addLayout(lc); ll.addStretch()
        sb.addWidget(logo)

        sb.addSpacing(14)
        ml = mk_lbl("  NAVİGASYON", 9, color=G["text3"])
        ml.setContentsMargins(20, 4, 0, 6)
        sb.addWidget(ml)

        nav_items = [("👤", "Hasta Kaydı"), ("🩺", "Doktor Kaydı"),
                     ("📅", "Randevu Al"), ("📋", "Günlük Liste")]
        self.nav_btns = []
        for i, (icon, text) in enumerate(nav_items):
            btn = NavBtn(icon, text, i)
            btn.clicked.connect(lambda _, idx=i: self._switch(idx))
            sb.addWidget(btn)
            self.nav_btns.append(btn)

        sb.addStretch()

        # Versiyon badge
        vw = QWidget(); vl = QHBoxLayout(vw); vl.setContentsMargins(16, 0, 16, 16)
        ver = mk_lbl("  KlinikPro v2.0  ", 9, color=G["green"])
        ver.setStyleSheet(
            f"color:{G['green']};background:rgba(34,197,94,0.08);"
            f"border:1px solid rgba(34,197,94,0.2);border-radius:12px;padding:4px 10px;"
        )
        vl.addWidget(ver); vl.addStretch()
        sb.addWidget(vw)

        # ── İçerik alanı ─────────────────────────────────────
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background: {G['bg']};")

        self.pages = [
            HastaPage(self.sistem),
            DoktorPage(self.sistem),
            RandevuPage(self.sistem),
            GunlukPage(self.sistem),
        ]

        for page in self.pages:
            scroll = QScrollArea()
            scroll.setWidget(page)
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet(f"QScrollArea {{ border: none; background: {G['bg']}; }}")
            page.setMinimumWidth(700)
            self.stack.addWidget(scroll)
            if hasattr(page, "sig_refresh"):
                page.sig_refresh.connect(self._on_refresh)

        row.addWidget(sb_widget)
        row.addWidget(self.stack)
        self._switch(0)

    def _switch(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, b in enumerate(self.nav_btns):
            b.set_active(i == idx)
        page = self.pages[idx]
        if hasattr(page, "refresh_combos"):
            page.refresh_combos()

    def _on_refresh(self):
        self.pages[2].refresh_combos()


# ═══════════════════════════════════════════════════════════════
#  GİRİŞ NOKTASI
# ═══════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
