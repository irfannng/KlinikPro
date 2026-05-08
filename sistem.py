"""
KlinikPro — PyQt5 Modern Arayüz
Tasarım: Orman Yeşili koyu tema, mint/limon aksan, kartlı layout
"""

import sys
from datetime import date
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit,
    QTableWidget, QTableWidgetItem, QStackedWidget, QFrame,
    QScrollArea, QMessageBox, QHeaderView, QSizePolicy, QSpacerItem,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QDate, QPropertyAnimation, QEasingCurve, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap, QPainter, QBrush, QPen

# ─── Backend (önceki dosyadan) ────────────────────────────────────────────────

# ─── Renk Paleti ─────────────────────────────────────────────────────────────
C = {
    "bg":        "#081210",   # çok koyu orman yeşili
    "surface":   "#0D1C18",   # koyu yeşil yüzey
    "card":      "#122A22",   # kart arka planı
    "border":    "#1E4035",   # sınır rengi
    "accent":    "#4ADE80",   # parlak limon yeşili
    "accent2":   "#34D399",   # mint yeşil
    "danger":    "#F87171",
    "success":   "#86EFAC",
    "text":      "#E2F5EE",   # yeşilimsi beyaz
    "muted":     "#5E9E80",   # soluk yeşil
    "hover":     "#163328",   # hover yeşil
}

GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {C['bg']};
    color: {C['text']};
    font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
}}
QLabel {{
    color: {C['text']};
    background: transparent;
}}
QLineEdit, QComboBox, QDateEdit {{
    background-color: {C['card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    selection-background-color: {C['accent']};
}}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {{
    border: 1.5px solid {C['accent']};
    background-color: {C['surface']};
}}
QLineEdit::placeholder {{
    color: {C['muted']};
}}
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {C['muted']};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background-color: {C['card']};
    color: {C['text']};
    border: 1px solid {C['border']};
    selection-background-color: {C['accent']};
    selection-color: {C['bg']};
    outline: none;
}}
QTableWidget {{
    background-color: {C['surface']};
    color: {C['text']};
    border: 1px solid {C['border']};
    border-radius: 10px;
    gridline-color: {C['border']};
    outline: none;
}}
QTableWidget::item {{
    padding: 10px 14px;
    border-bottom: 1px solid {C['border']};
}}
QTableWidget::item:selected {{
    background-color: {C['hover']};
    color: {C['accent']};
}}
QHeaderView::section {{
    background-color: {C['card']};
    color: {C['muted']};
    border: none;
    border-bottom: 1px solid {C['border']};
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
QScrollBar:vertical {{
    background: {C['surface']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {C['border']};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {C['muted']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""

# ─── Yardımcı Widget'lar ──────────────────────────────────────────────────────

def make_label(text, size=13, bold=False, color=None, align=Qt.AlignLeft):
    lbl = QLabel(text)
    font = QFont("Segoe UI", size)
    font.setBold(bold)
    lbl.setFont(font)
    lbl.setStyleSheet(f"color: {color or C['text']}; background: transparent;")
    lbl.setAlignment(align)
    return lbl


def shadow(widget, blur=20, offset=(0, 4), color="#000000", alpha=120):
    eff = QGraphicsDropShadowEffect(widget)
    eff.setBlurRadius(blur)
    eff.setXOffset(offset[0])
    eff.setYOffset(offset[1])
    c = QColor(color)
    c.setAlpha(alpha)
    eff.setColor(c)
    widget.setGraphicsEffect(eff)
    return eff


class Card(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {C['card']};
                border: 1px solid {C['border']};
                border-radius: 14px;
            }}
        """)
        shadow(self)


class PrimaryButton(QPushButton):
    def __init__(self, text, icon_char="", parent=None):
        super().__init__(f"  {icon_char}  {text}" if icon_char else text, parent)
        self.setMinimumHeight(44)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {C['accent']}, stop:1 {C['accent2']});
                color: {C['bg']};
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 700;
                padding: 0 24px;
                letter-spacing: 0.5px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #5EEAD4, stop:1 #38BDF8);
            }}
            QPushButton:pressed {{
                background: {C['accent']};
            }}
        """)


class DangerButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(38)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {C['danger']};
                border: 1px solid {C['danger']};
                border-radius: 8px;
                font-size: 12px;
                font-weight: 600;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                background-color: rgba(248,113,113,0.1);
            }}
        """)


class NavButton(QPushButton):
    def __init__(self, icon_char, label, parent=None):
        super().__init__(parent)
        self.label_text = label
        self.icon_char = icon_char
        self._active = False
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(52)
        self._refresh()

    def set_active(self, active: bool):
        self._active = active
        self._refresh()

    def _refresh(self):
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(74,222,128,0.12);
                    color: {C['accent']};
                    border: none;
                    border-left: 3px solid {C['accent']};
                    border-radius: 0;
                    text-align: left;
                    padding-left: 20px;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {C['muted']};
                    border: none;
                    border-left: 3px solid transparent;
                    border-radius: 0;
                    text-align: left;
                    padding-left: 20px;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background-color: {C['hover']};
                    color: {C['text']};
                }}
            """)
        self.setText(f"  {self.icon_char}   {self.label_text}")


class FieldGroup(QVBoxLayout):
    def __init__(self, label, widget):
        super().__init__()
        lbl = make_label(label, size=11, color=C['muted'])
        lbl.setContentsMargins(2, 0, 0, 0)
        self.addWidget(lbl)
        self.addWidget(widget)
        self.setSpacing(6)


# ─── Sayfa: Hasta Kaydı ───────────────────────────────────────────────────────

class HastaPage(QWidget):
    refreshSignal = pyqtSignal()

    def __init__(self, sistem: RandevuSistemi): 
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(24)

        root.addWidget(make_label("Hasta Kaydı", 22, bold=True))
        root.addWidget(make_label("Yeni hasta bilgilerini girerek sisteme kaydedin.", 13, color=C['muted']))

        card = Card()
        form = QVBoxLayout(card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(20)

        self.ad_input = QLineEdit(); self.ad_input.setPlaceholderText("Örn: Ayşe Kaya")
        self.tc_input = QLineEdit(); self.tc_input.setPlaceholderText("11 haneli TC kimlik numarası")
        self.tc_input.setMaxLength(11)
        self.tel_input = QLineEdit(); self.tel_input.setPlaceholderText("Örn: 05551234567")

        row1 = QHBoxLayout(); row1.setSpacing(16)
        g1 = QVBoxLayout(); g1.addWidget(make_label("Ad Soyad", 11, color=C['muted'])); g1.addWidget(self.ad_input); g1.setSpacing(6)
        g2 = QVBoxLayout(); g2.addWidget(make_label("TC Kimlik No", 11, color=C['muted'])); g2.addWidget(self.tc_input); g2.setSpacing(6)
        g3 = QVBoxLayout(); g3.addWidget(make_label("Telefon", 11, color=C['muted'])); g3.addWidget(self.tel_input); g3.setSpacing(6)
        row1.addLayout(g1, 2); row1.addLayout(g2, 2); row1.addLayout(g3, 1)
        form.addLayout(row1)

        btn = PrimaryButton("Kaydet", "✦")
        btn.setFixedWidth(160)
        btn.clicked.connect(self._kaydet)
        form.addWidget(btn)
        root.addWidget(card)

        # Hasta tablosu
        root.addWidget(make_label("Kayıtlı Hastalar", 15, bold=True))
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "TC", "Telefon"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(self.table.styleSheet() + f"""
            QTableWidget {{alternate-background-color: {C['hover']};}}
        """)
        root.addWidget(self.table)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        tc = self.tc_input.text().strip()
        tel = self.tel_input.text().strip()
        try:
            h = self.sistem.hasta_kaydet(ad, tc, tel)
            self._tablo_satir_ekle(h)
            self.ad_input.clear(); self.tc_input.clear(); self.tel_input.clear()
            self._toast(f"✅  {h.ad} başarıyla kaydedildi (ID: {h.hasta_id})")
            self.refreshSignal.emit()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def _tablo_satir_ekle(self, h):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, val in enumerate([str(h.hasta_id), h.ad, h.tc, h.telefon]):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.table.setItem(row, col, item)
        self.table.setRowHeight(row, 44)

    def _toast(self, msg):
        QMessageBox.information(self, "Bilgi", msg)

    def refresh_combos(self): pass


# ─── Sayfa: Doktor Kaydı ─────────────────────────────────────────────────────

class DoktorPage(QWidget):
    refreshSignal = pyqtSignal()

    def __init__(self, sistem: RandevuSistemi):
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(24)

        root.addWidget(make_label("Doktor Kaydı", 22, bold=True))
        root.addWidget(make_label("Doktor bilgilerini ve müsait saatlerini yönetin.", 13, color=C['muted']))

        card = Card()
        form = QVBoxLayout(card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(20)

        self.ad_input = QLineEdit(); self.ad_input.setPlaceholderText("Dr. Ad Soyad")
        self.uzm_input = QLineEdit(); self.uzm_input.setPlaceholderText("Örn: Kardiyoloji")

        row = QHBoxLayout(); row.setSpacing(16)
        g1 = QVBoxLayout(); g1.addWidget(make_label("Doktor Adı", 11, color=C['muted'])); g1.addWidget(self.ad_input); g1.setSpacing(6)
        g2 = QVBoxLayout(); g2.addWidget(make_label("Uzmanlık", 11, color=C['muted'])); g2.addWidget(self.uzm_input); g2.setSpacing(6)
        row.addLayout(g1); row.addLayout(g2)
        form.addLayout(row)

        btn = PrimaryButton("Kaydet", "✦")
        btn.setFixedWidth(160)
        btn.clicked.connect(self._kaydet)
        form.addWidget(btn)
        root.addWidget(card)

        # Saat ekleme
        saat_card = Card()
        saat_form = QVBoxLayout(saat_card)
        saat_form.setContentsMargins(28, 28, 28, 28)
        saat_form.setSpacing(16)
        saat_form.addWidget(make_label("Müsait Saat Ekle", 14, bold=True))

        self.doktor_combo = QComboBox()
        self.tarih_edit = QDateEdit(QDate.currentDate())
        self.tarih_edit.setCalendarPopup(True)
        self.saat_input = QLineEdit(); self.saat_input.setPlaceholderText("HH:MM  (örn: 09:00)")

        srow = QHBoxLayout(); srow.setSpacing(12)
        for lbl_text, widget in [("Doktor", self.doktor_combo), ("Tarih", self.tarih_edit), ("Saat", self.saat_input)]:
            g = QVBoxLayout(); g.setSpacing(6)
            g.addWidget(make_label(lbl_text, 11, color=C['muted']))
            g.addWidget(widget)
            srow.addLayout(g)
        saat_form.addLayout(srow)

        saat_btn = PrimaryButton("Saat Ekle", "＋")
        saat_btn.setFixedWidth(160)
        saat_btn.clicked.connect(self._saat_ekle)
        saat_form.addWidget(saat_btn)
        root.addWidget(saat_card)

        root.addWidget(make_label("Kayıtlı Doktorlar", 15, bold=True))
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Ad Soyad", "Uzmanlık"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        root.addWidget(self.table)

    def _kaydet(self):
        ad = self.ad_input.text().strip()
        uzm = self.uzm_input.text().strip()
        try:
            d = self.sistem.doktor_kaydet(ad, uzm)
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, val in enumerate([str(d.doktor_id), d.ad, d.uzmanlik]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.table.setItem(row, col, item)
            self.table.setRowHeight(row, 44)
            self.ad_input.clear(); self.uzm_input.clear()
            self.doktor_combo.addItem(f"[{d.doktor_id}] {d.ad}", d.doktor_id)
            self.refreshSignal.emit()
            QMessageBox.information(self, "Bilgi", f"✅  Dr. {d.ad} kaydedildi (ID: {d.doktor_id})")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def _saat_ekle(self):
        idx = self.doktor_combo.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Hata", "Lütfen bir doktor seçin."); return
        did = self.doktor_combo.itemData(idx)
        doktor = self.sistem.doktorlar.get(did)
        saat = self.saat_input.text().strip()
        qd = self.tarih_edit.date()
        tarih = date(qd.year(), qd.month(), qd.day())
        doktor.saat_ekle(tarih, saat)
        self.saat_input.clear()
        QMessageBox.information(self, "Bilgi", f"✅  {tarih} — {saat} saati eklendi.")

    def refresh_combos(self): pass


# ─── Sayfa: Randevu Al ────────────────────────────────────────────────────────

class RandevuPage(QWidget):
    refreshSignal = pyqtSignal()

    def __init__(self, sistem: RandevuSistemi):
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(24)

        root.addWidget(make_label("Randevu Al", 22, bold=True))
        root.addWidget(make_label("Hasta ve doktor seçerek randevu oluşturun.", 13, color=C['muted']))

        card = Card()
        form = QVBoxLayout(card)
        form.setContentsMargins(28, 28, 28, 28)
        form.setSpacing(20)

        self.hasta_combo = QComboBox()
        self.doktor_combo = QComboBox()
        self.tarih_edit = QDateEdit(QDate.currentDate())
        self.tarih_edit.setCalendarPopup(True)
        self.saat_input = QLineEdit(); self.saat_input.setPlaceholderText("HH:MM  (örn: 10:00)")

        row1 = QHBoxLayout(); row1.setSpacing(16)
        for lbl_text, widget in [("Hasta", self.hasta_combo), ("Doktor", self.doktor_combo)]:
            g = QVBoxLayout(); g.setSpacing(6)
            g.addWidget(make_label(lbl_text, 11, color=C['muted']))
            g.addWidget(widget)
            row1.addLayout(g)
        form.addLayout(row1)

        row2 = QHBoxLayout(); row2.setSpacing(16)
        for lbl_text, widget in [("Tarih", self.tarih_edit), ("Saat", self.saat_input)]:
            g = QVBoxLayout(); g.setSpacing(6)
            g.addWidget(make_label(lbl_text, 11, color=C['muted']))
            g.addWidget(widget)
            row2.addLayout(g)
        form.addLayout(row2)

        btn = PrimaryButton("Randevu Oluştur", "📅")
        btn.setFixedWidth(220)
        btn.clicked.connect(self._olustur)
        form.addWidget(btn)
        root.addWidget(card)

        root.addWidget(make_label("Aktif Randevular", 15, bold=True))
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Hasta", "Doktor", "Tarih", "Saat", "İşlem"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        root.addWidget(self.table)

    def refresh_combos(self):
        self.hasta_combo.clear()
        for h in self.sistem.hastalar.values():
            self.hasta_combo.addItem(f"[{h.hasta_id}] {h.ad}", h.hasta_id)
        self.doktor_combo.clear()
        for d in self.sistem.doktorlar.values():
            self.doktor_combo.addItem(f"[{d.doktor_id}] {d.ad}", d.doktor_id)

    def _olustur(self):
        hi = self.hasta_combo.currentIndex()
        di = self.doktor_combo.currentIndex()
        if hi < 0 or di < 0:
            QMessageBox.warning(self, "Hata", "Hasta ve doktor seçin."); return
        hid = self.hasta_combo.itemData(hi)
        did = self.doktor_combo.itemData(di)
        hasta = self.sistem.hastalar.get(hid)
        doktor = self.sistem.doktorlar.get(did)
        saat = self.saat_input.text().strip()
        qd = self.tarih_edit.date()
        tarih = date(qd.year(), qd.month(), qd.day())
        try:
            r = self.sistem.randevu_olustur(hasta, doktor, tarih, saat)
            self._tablo_ekle(r)
            self.saat_input.clear()
            self.refreshSignal.emit()
            QMessageBox.information(self, "Başarılı", f"✅  Randevu oluşturuldu (ID: {r.randevu_id})")
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))

    def _tablo_ekle(self, r):
        row = self.table.rowCount()
        self.table.insertRow(row)
        vals = [str(r.randevu_id), r.hasta.ad, r.doktor.ad, str(r.tarih), r.saat]
        for col, val in enumerate(vals):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            item.setData(Qt.UserRole, r.randevu_id)
            self.table.setItem(row, col, item)
        btn = DangerButton("İptal")
        btn.clicked.connect(lambda _, rid=r.randevu_id, rw=row: self._iptal(rid, rw))
        self.table.setCellWidget(row, 5, btn)
        self.table.setRowHeight(row, 48)

    def _iptal(self, randevu_id, row):
        r = self.sistem.randevular.get(randevu_id)
        if not r: return
        try:
            r.randevu_iptal()
            self.table.removeRow(row)
            # satır indekslerini güncelle
            for new_row in range(self.table.rowCount()):
                btn = self.table.cellWidget(new_row, 5)
                if btn:
                    rid_item = self.table.item(new_row, 0)
                    if rid_item:
                        rid = int(rid_item.text())
                        btn.clicked.disconnect()
                        btn.clicked.connect(lambda _, r2=rid, rw2=new_row: self._iptal(r2, rw2))
            self.refreshSignal.emit()
        except ValueError as e:
            QMessageBox.warning(self, "Hata", str(e))


# ─── Sayfa: Günlük Liste ─────────────────────────────────────────────────────

class GunlukPage(QWidget):
    def __init__(self, sistem: RandevuSistemi):
        super().__init__()
        self.sistem = sistem
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(24)

        root.addWidget(make_label("Günlük Randevu Listesi", 22, bold=True))
        root.addWidget(make_label("Seçilen güne ait tüm aktif randevuları görüntüleyin.", 13, color=C['muted']))

        ctrl = QHBoxLayout()
        self.tarih_edit = QDateEdit(QDate.currentDate())
        self.tarih_edit.setCalendarPopup(True)
        self.tarih_edit.setFixedWidth(180)
        btn = PrimaryButton("Listele", "🔍")
        btn.setFixedWidth(140)
        btn.clicked.connect(self._listele)
        self.count_lbl = make_label("", 12, color=C['muted'])
        ctrl.addWidget(self.tarih_edit)
        ctrl.addWidget(btn)
        ctrl.addWidget(self.count_lbl)
        ctrl.addStretch()
        root.addLayout(ctrl)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Randevu ID", "Doktor", "Hasta", "Saat"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        root.addWidget(self.table)

    def _listele(self):
        qd = self.tarih_edit.date()
        tarih = date(qd.year(), qd.month(), qd.day())
        liste = self.sistem.gunluk_randevu_listesi(tarih)
        self.table.setRowCount(0)
        for r in sorted(liste, key=lambda x: x.saat):
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, val in enumerate([str(r.randevu_id), r.doktor.ad, r.hasta.ad, r.saat]):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                self.table.setItem(row, col, item)
            self.table.setRowHeight(row, 44)
        self.count_lbl.setText(f"{len(liste)} randevu bulundu")

    def refresh_combos(self): pass


# ─── Ana Pencere ──────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistem = RandevuSistemi()
        self.setWindowTitle("KlinikPro — Doktor Randevu Sistemi")
        self.resize(1100, 720)
        self.setMinimumSize(900, 600)
        self._build()

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_row = QHBoxLayout(central)
        main_row.setContentsMargins(0, 0, 0, 0)
        main_row.setSpacing(0)

        # ── Sidebar ──
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"background-color: {C['surface']}; border-right: 1px solid {C['border']};")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(0)

        # Logo
        logo_widget = QWidget()
        logo_widget.setFixedHeight(72)
        logo_widget.setStyleSheet(f"background: {C['surface']}; border-bottom: 1px solid {C['border']};")
        logo_layout = QHBoxLayout(logo_widget)
        logo_layout.setContentsMargins(20, 0, 0, 0)
        icon_lbl = make_label("🏥", 22)
        title_lbl = make_label("KlinikPro", 15, bold=True, color=C['accent'])
        logo_layout.addWidget(icon_lbl)
        logo_layout.addWidget(title_lbl)
        logo_layout.addStretch()
        sb_layout.addWidget(logo_widget)

        sb_layout.addSpacing(12)
        nav_lbl = make_label("  MENÜ", 10, color=C['muted'])
        nav_lbl.setContentsMargins(20, 8, 0, 8)
        sb_layout.addWidget(nav_lbl)

        nav_items = [
            ("👤", "Hasta Kaydı"),
            ("🩺", "Doktor Kaydı"),
            ("📅", "Randevu Al"),
            ("📋", "Günlük Liste"),
        ]
        self.nav_buttons = []
        for icon, label in nav_items:
            btn = NavButton(icon, label)
            sb_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sb_layout.addStretch()
        version_lbl = make_label("  KlinikPro v2.0", 10, color=C['border'])
        version_lbl.setContentsMargins(0, 0, 0, 16)
        sb_layout.addWidget(version_lbl)

        # ── Content Stack ──
        self.stack = QStackedWidget()
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
            scroll.setStyleSheet(f"QScrollArea {{ border: none; background: {C['bg']}; }}")
            page.setMinimumWidth(700)
            self.stack.addWidget(scroll)
            if hasattr(page, 'refreshSignal'):
                page.refreshSignal.connect(self._on_refresh)

        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda _, idx=i: self._switch(idx))

        main_row.addWidget(sidebar)
        main_row.addWidget(self.stack)

        self._switch(0)

    def _switch(self, idx):
        self.stack.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_buttons):
            btn.set_active(i == idx)
        # Combo'ları güncelle
        page = self.pages[idx]
        if hasattr(page, 'refresh_combos'):
            page.refresh_combos()

    def _on_refresh(self):
        # Randevu sayfasının combo'larını güncelle
        self.pages[2].refresh_combos()


# ─── Giriş Noktası ───────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()