"""
Yemek Tarif Platformu — Modern PyQt5 GUI
==========================================
Koyu tema, kart tabanlı tasarım, tam OOP mimarisi.
Gereksinim: pip install PyQt5
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QScrollArea,
    QFrame, QStackedWidget, QComboBox, QSpinBox, QMessageBox,
    QGridLayout, QSizePolicy, QDialog, QFormLayout, QListWidget,
    QListWidgetItem, QSplitter, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QPoint, QTimer,
    pyqtSignal, QSize, QRect
)
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QLinearGradient, QPainter,
    QBrush, QPen, QPixmap, QIcon, QFontDatabase
)


# ═══════════════════════════════════════════════════════════════════
#  RENK PALETİ & STİL SABİTLERİ
# ═══════════════════════════════════════════════════════════════════

RENKLER = {
    "bg_dark":      "#0D0F12",
    "bg_card":      "#161A20",
    "bg_card2":     "#1C2128",
    "bg_input":     "#1E2530",
    "accent":       "#FF6B35",
    "accent2":      "#FF8C5A",
    "accent_dim":   "#3D2318",
    "text_primary": "#F0EDE8",
    "text_secondary":"#8B8F96",
    "text_hint":    "#4A5060",
    "border":       "#252B35",
    "border_active":"#FF6B35",
    "success":      "#2ECC71",
    "warning":      "#F39C12",
    "danger":       "#E74C3C",
    "star":         "#F5C518",
}

STYLE_SHEET = f"""
QMainWindow, QWidget {{
    background-color: {RENKLER['bg_dark']};
    color: {RENKLER['text_primary']};
    font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
}}

/* ── SCROLL AREA ── */
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {RENKLER['bg_card']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {RENKLER['text_hint']};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* ── INPUT ── */
QLineEdit, QTextEdit, QSpinBox, QComboBox {{
    background: {RENKLER['bg_input']};
    color: {RENKLER['text_primary']};
    border: 1px solid {RENKLER['border']};
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 14px;
    selection-background-color: {RENKLER['accent_dim']};
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {RENKLER['accent']};
    background: #1A2030;
}}
QLineEdit::placeholder {{
    color: {RENKLER['text_hint']};
}}
QComboBox::drop-down {{
    border: none;
    padding-right: 10px;
}}
QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
}}
QComboBox QAbstractItemView {{
    background: {RENKLER['bg_card2']};
    border: 1px solid {RENKLER['border']};
    selection-background-color: {RENKLER['accent_dim']};
    color: {RENKLER['text_primary']};
    border-radius: 8px;
    padding: 4px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    background: {RENKLER['bg_card2']};
    border: none;
    width: 20px;
    border-radius: 4px;
}}

/* ── LIST ── */
QListWidget {{
    background: transparent;
    border: none;
    outline: none;
}}
QListWidget::item {{
    padding: 0px;
    border: none;
}}
QListWidget::item:selected {{
    background: transparent;
}}

/* ── DIALOG ── */
QDialog {{
    background: {RENKLER['bg_card']};
    border: 1px solid {RENKLER['border']};
    border-radius: 16px;
}}

/* ── MESSAGE BOX ── */
QMessageBox {{
    background: {RENKLER['bg_card']};
    color: {RENKLER['text_primary']};
}}
QMessageBox QPushButton {{
    background: {RENKLER['accent']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    min-width: 80px;
}}
"""


# ═══════════════════════════════════════════════════════════════════
#  VERİ MODELİ  (OOP)
# ═══════════════════════════════════════════════════════════════════

class Malzeme:
    def __init__(self, adi, miktar, birim="adet"):
        self.adi = adi
        self.miktar = miktar
        self.birim = birim
    def __str__(self):
        return f"{self.miktar} {self.birim} {self.adi}"


class Tarif:
    _sayac = 1
    def __init__(self, adi, kategori, sure, aciklama=""):
        self.id = Tarif._sayac; Tarif._sayac += 1
        self.adi = adi
        self.kategori = kategori
        self.sure = sure
        self.aciklama = aciklama
        self.malzemeler: list[Malzeme] = []
        self.degerlendirmeler: list[tuple] = []   # (puan, yorum, kullanici)

    def ortalama_puan(self):
        if not self.degerlendirmeler: return 0.0
        return round(sum(p for p, _, _ in self.degerlendirmeler) / len(self.degerlendirmeler), 1)

    def degerlendir(self, puan, yorum, kullanici_adi):
        self.degerlendirmeler.append((puan, yorum, kullanici_adi))

    def yildiz_str(self):
        p = self.ortalama_puan()
        if p == 0: return "☆☆☆☆☆"
        dolu = int(round(p))
        return "★" * dolu + "☆" * (5 - dolu)


class Kullanici:
    _sayac = 1
    def __init__(self, ad):
        self.id = Kullanici._sayac; Kullanici._sayac += 1
        self.ad = ad
        self.favoriler: list[int] = []

    def favoriye_ekle(self, tarif_id):
        if tarif_id not in self.favoriler:
            self.favoriler.append(tarif_id)
            return True
        return False


class Platform:
    def __init__(self):
        self.tarifler: dict[int, Tarif] = {}
        self.kullanicilar: dict[int, Kullanici] = {}
        self.kategoriler = ["Ana Yemek", "Çorba", "Tatlı", "Salata", "Kahvaltı", "İçecek"]
        self._demo_yukle()

    def _demo_yukle(self):
        u1 = self.kullanici_ekle("Ayşe")
        u2 = self.kullanici_ekle("Mehmet")

        t1 = Tarif("Çikolatalı Kek", "Tatlı", 60,
                   "Nefis, nemli ve yoğun çikolatalı kek. Her kutlamaya yakışır.")
        t1.malzemeler = [Malzeme("Un", 2, "su bardağı"),
                         Malzeme("Şeker", 1, "su bardağı"),
                         Malzeme("Yumurta", 3, "adet"),
                         Malzeme("Kakao", 4, "yemek kaşığı"),
                         Malzeme("Tereyağı", 100, "gr")]
        self.tarifler[t1.id] = t1
        t1.degerlendir(5, "Mükemmel lezzet!", "Mehmet")
        t1.degerlendir(4, "Harika oldu.", "Zeynep")

        t2 = Tarif("Tavuk Sote", "Ana Yemek", 35,
                   "Sebzeli, hafif baharatlı nefis bir tavuk sote.")
        t2.malzemeler = [Malzeme("Tavuk but", 4, "adet"),
                         Malzeme("Soğan", 2, "adet"),
                         Malzeme("Domates", 3, "adet"),
                         Malzeme("Zeytinyağı", 3, "yemek kaşığı")]
        self.tarifler[t2.id] = t2
        t2.degerlendir(5, "Çok başarılı!", "Ayşe")

        t3 = Tarif("Mercimek Çorbası", "Çorba", 25,
                   "Geleneksel Türk mutfağının vazgeçilmezi.")
        t3.malzemeler = [Malzeme("Kırmızı mercimek", 1, "su bardağı"),
                         Malzeme("Soğan", 1, "adet"),
                         Malzeme("Havuç", 1, "adet"),
                         Malzeme("Tereyağı", 1, "yemek kaşığı")]
        self.tarifler[t3.id] = t3
        t3.degerlendir(5, "Tam kıvamında!", "Mehmet")
        t3.degerlendir(5, "Enfes.", "Ayşe")

        t4 = Tarif("Sezar Salatası", "Salata", 15,
                   "Taze marul, kruton ve özel sos ile klasik sezar.")
        t4.malzemeler = [Malzeme("Marul", 1, "baş"),
                         Malzeme("Parmesan", 50, "gr"),
                         Malzeme("Kruton", 1, "avuç")]
        self.tarifler[t4.id] = t4
        t4.degerlendir(4, "Çok taze.", "Zeynep")

        u1.favoriye_ekle(t2.id)
        u2.favoriye_ekle(t1.id)
        u2.favoriye_ekle(t3.id)

    def kullanici_ekle(self, ad) -> Kullanici:
        k = Kullanici(ad)
        self.kullanicilar[k.id] = k
        return k

    def tarif_ekle(self, tarif: Tarif):
        self.tarifler[tarif.id] = tarif

    def ara(self, sorgu):
        s = sorgu.lower()
        return [t for t in self.tarifler.values()
                if s in t.adi.lower() or s in t.kategori.lower() or s in t.aciklama.lower()]

    def kategori_filtrele(self, kat):
        if kat == "Tümü": return list(self.tarifler.values())
        return [t for t in self.tarifler.values() if t.kategori == kat]

    def en_iyiler(self, n=4):
        return sorted(self.tarifler.values(), key=lambda t: t.ortalama_puan(), reverse=True)[:n]


# ═══════════════════════════════════════════════════════════════════
#  ÖZEL WİDGET'LAR
# ═══════════════════════════════════════════════════════════════════

class AyiriciCizgi(QFrame):
    def __init__(self, yatay=True):
        super().__init__()
        if yatay:
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFrameShape(QFrame.VLine)
        self.setStyleSheet(f"color: {RENKLER['border']}; background: {RENKLER['border']};")
        self.setFixedHeight(1) if yatay else self.setFixedWidth(1)


class ModernButon(QPushButton):
    def __init__(self, text, birincil=True, kucuk=False, tehlikeli=False):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)
        h = "36px" if kucuk else "44px"
        px = "16px" if kucuk else "24px"
        fs = "13px" if kucuk else "14px"

        if tehlikeli:
            bg, hover = RENKLER['danger'], "#C0392B"
        elif birincil:
            bg, hover = RENKLER['accent'], RENKLER['accent2']
        else:
            bg, hover = RENKLER['bg_card2'], RENKLER['bg_input']

        border = "none" if birincil or tehlikeli else f"1px solid {RENKLER['border']}"
        self.setStyleSheet(f"""
            QPushButton {{
                background: {bg};
                color: {"white" if birincil or tehlikeli else RENKLER['text_primary']};
                border: {border};
                border-radius: 10px;
                padding: 0 {px};
                height: {h};
                font-size: {fs};
                font-weight: 600;
                letter-spacing: 0.3px;
            }}
            QPushButton:hover {{
                background: {hover};
            }}
            QPushButton:pressed {{
                background: {bg};
                padding-top: 2px;
            }}
            QPushButton:disabled {{
                background: {RENKLER['bg_card2']};
                color: {RENKLER['text_hint']};
            }}
        """)


class EtiketBadge(QLabel):
    def __init__(self, text, renk="accent"):
        super().__init__(text)
        renkler_map = {
            "accent":  (RENKLER['accent_dim'], RENKLER['accent2']),
            "success": ("#1A3D2B", RENKLER['success']),
            "warning": ("#3D2E0A", RENKLER['warning']),
            "info":    ("#162033", "#5DADE2"),
        }
        bg, fg = renkler_map.get(renk, renkler_map["accent"])
        self.setStyleSheet(f"""
            QLabel {{
                background: {bg};
                color: {fg};
                border-radius: 6px;
                padding: 3px 10px;
                font-size: 12px;
                font-weight: 600;
            }}
        """)
        self.setFixedHeight(24)


class TarifKarti(QFrame):
    """Tarif listesinde görünen kart widget'ı."""
    tiklandı = pyqtSignal(int)   # tarif_id gönderir

    def __init__(self, tarif: Tarif):
        super().__init__()
        self.tarif = tarif
        self.setCursor(Qt.PointingHandCursor)
        self._normal_stil()
        self._kur()

    def _normal_stil(self):
        self.setStyleSheet(f"""
            QFrame {{
                background: {RENKLER['bg_card']};
                border: 1px solid {RENKLER['border']};
                border-radius: 14px;
            }}
            QFrame:hover {{
                border: 1px solid {RENKLER['accent_dim']};
                background: {RENKLER['bg_card2']};
            }}
        """)

    def _kur(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(18, 16, 18, 16)
        lay.setSpacing(10)

        # Üst satır: kategori badge + süre
        ust = QHBoxLayout()
        ust.setSpacing(8)
        kat_badge = EtiketBadge(self.tarif.kategori, "info")
        ust.addWidget(kat_badge)
        ust.addStretch()
        sure_lbl = QLabel(f"⏱ {self.tarif.sure} dk")
        sure_lbl.setStyleSheet(f"color: {RENKLER['text_secondary']}; font-size: 12px;")
        ust.addWidget(sure_lbl)
        lay.addLayout(ust)

        # Tarif adı
        adi = QLabel(self.tarif.adi)
        adi.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 16px; font-weight: 700;")
        adi.setWordWrap(True)
        lay.addWidget(adi)

        # Açıklama
        if self.tarif.aciklama:
            acik = QLabel(self.tarif.aciklama[:80] + ("…" if len(self.tarif.aciklama) > 80 else ""))
            acik.setStyleSheet(f"color: {RENKLER['text_secondary']}; font-size: 13px; line-height: 1.5;")
            acik.setWordWrap(True)
            lay.addWidget(acik)

        lay.addWidget(AyiriciCizgi())

        # Alt satır: yıldız + malzeme sayısı
        alt = QHBoxLayout()
        yildiz = QLabel(f"{self.tarif.yildiz_str()}  {self.tarif.ortalama_puan()}")
        yildiz.setStyleSheet(f"color: {RENKLER['star']}; font-size: 13px;")
        alt.addWidget(yildiz)
        alt.addStretch()
        malzeme_lbl = QLabel(f"🧂 {len(self.tarif.malzemeler)} malzeme")
        malzeme_lbl.setStyleSheet(f"color: {RENKLER['text_hint']}; font-size: 12px;")
        alt.addWidget(malzeme_lbl)
        lay.addLayout(alt)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.tiklandı.emit(self.tarif.id)


class NavButon(QPushButton):
    def __init__(self, icon_text, label, aktif=False):
        super().__init__()
        self.icon_text = icon_text
        self.label = label
        self._aktif = aktif
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setChecked(aktif)
        self._guncelle_stil()
        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 0, 14, 0)
        lay.setSpacing(10)
        self.icon_lbl = QLabel(icon_text)
        self.icon_lbl.setStyleSheet("font-size: 18px; background: transparent; border: none;")
        self.text_lbl = QLabel(label)
        self.text_lbl.setStyleSheet(f"font-size: 14px; font-weight: 600; background: transparent; border: none; color: {RENKLER['text_primary'] if aktif else RENKLER['text_secondary']};")
        lay.addWidget(self.icon_lbl)
        lay.addWidget(self.text_lbl)
        lay.addStretch()
        self.setFixedHeight(48)
        self.toggled.connect(self._on_toggle)

    def _guncelle_stil(self):
        a = self._aktif
        self.setStyleSheet(f"""
            QPushButton {{
                background: {"rgba(255,107,53,0.12)" if a else "transparent"};
                border: none;
                border-radius: 10px;
                border-left: {"3px solid " + RENKLER['accent'] if a else "3px solid transparent"};
                text-align: left;
            }}
            QPushButton:hover {{
                background: rgba(255,107,53,0.07);
            }}
        """)

    def _on_toggle(self, checked):
        self._aktif = checked
        renk = RENKLER['text_primary'] if checked else RENKLER['text_secondary']
        if hasattr(self, 'text_lbl'):
            self.text_lbl.setStyleSheet(f"font-size: 14px; font-weight: 600; background: transparent; border: none; color: {renk};")
        self._guncelle_stil()

    def aktif_yap(self):
        self.setChecked(True)
        self._aktif = True
        self._on_toggle(True)

    def pasif_yap(self):
        self.setChecked(False)
        self._aktif = False
        self._on_toggle(False)


# ═══════════════════════════════════════════════════════════════════
#  SAYFA: ANASAYFA
# ═══════════════════════════════════════════════════════════════════

class AnasayfaSayfasi(QWidget):
    tarif_sec = pyqtSignal(int)

    def __init__(self, platform: Platform):
        super().__init__()
        self.platform = platform
        self._kur()

    def _kur(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 28, 32, 28)
        lay.setSpacing(24)

        # Başlık
        baslik = QLabel("Bugün Ne Pişirelim? 🍽")
        baslik.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 26px; font-weight: 800;")
        lay.addWidget(baslik)

        # İstatistik kartları
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        for ikon, deger, etiket, renk in [
            ("📖", str(len(self.platform.tarifler)), "Tarif", "accent"),
            ("👥", str(len(self.platform.kullanicilar)), "Kullanıcı", "success"),
            ("⭐", str(len([t for t in self.platform.tarifler.values() if t.ortalama_puan() >= 4.5])), "Yüksek Puan", "warning"),
        ]:
            kart = QFrame()
            kart.setStyleSheet(f"""
                QFrame {{
                    background: {RENKLER['bg_card']};
                    border: 1px solid {RENKLER['border']};
                    border-radius: 14px;
                }}
            """)
            klay = QVBoxLayout(kart)
            klay.setContentsMargins(20, 16, 20, 16)
            klay.setSpacing(4)
            ikon_lbl = QLabel(ikon)
            ikon_lbl.setStyleSheet("font-size: 24px;")
            deger_lbl = QLabel(deger)
            deger_lbl.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 28px; font-weight: 800;")
            etiket_lbl = QLabel(etiket)
            etiket_lbl.setStyleSheet(f"color: {RENKLER['text_secondary']}; font-size: 13px;")
            klay.addWidget(ikon_lbl)
            klay.addWidget(deger_lbl)
            klay.addWidget(etiket_lbl)
            stats_row.addWidget(kart)
        lay.addLayout(stats_row)

        # En iyi tarifler
        en_iyi_baslik = QLabel("✨ En Beğenilen Tarifler")
        en_iyi_baslik.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 18px; font-weight: 700;")
        lay.addWidget(en_iyi_baslik)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        icerik = QWidget()
        icerik.setStyleSheet("background: transparent;")
        grid = QGridLayout(icerik)
        grid.setSpacing(14)
        grid.setContentsMargins(0, 0, 0, 0)

        tarifler = self.platform.en_iyiler(4)
        for i, tarif in enumerate(tarifler):
            kart = TarifKarti(tarif)
            kart.tiklandı.connect(self.tarif_sec)
            grid.addWidget(kart, i // 2, i % 2)

        scroll.setWidget(icerik)
        lay.addWidget(scroll)


# ═══════════════════════════════════════════════════════════════════
#  SAYFA: TARİF LİSTESİ
# ═══════════════════════════════════════════════════════════════════

class TarifListesiSayfasi(QWidget):
    tarif_sec = pyqtSignal(int)

    def __init__(self, platform: Platform):
        super().__init__()
        self.platform = platform
        self._kur()

    def _kur(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(32, 28, 32, 28)
        lay.setSpacing(18)

        # Başlık + buton
        ust = QHBoxLayout()
        baslik = QLabel("Tarifler")
        baslik.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 24px; font-weight: 800;")
        ust.addWidget(baslik)
        ust.addStretch()
        self.ekle_btn = ModernButon("＋ Yeni Tarif", birincil=True)
        self.ekle_btn.clicked.connect(self._tarif_ekle_diyalog)
        ust.addWidget(self.ekle_btn)
        lay.addLayout(ust)

        # Arama + filtre
        filtre_row = QHBoxLayout()
        filtre_row.setSpacing(10)
        self.arama = QLineEdit()
        self.arama.setPlaceholderText("🔍  Tarif ara...")
        self.arama.textChanged.connect(self._filtrele)
        filtre_row.addWidget(self.arama, 3)
        self.kategori_combo = QComboBox()
        self.kategori_combo.addItem("Tümü")
        self.kategori_combo.addItems(self.platform.kategoriler)
        self.kategori_combo.currentTextChanged.connect(self._filtrele)
        filtre_row.addWidget(self.kategori_combo, 1)
        lay.addLayout(filtre_row)

        # Liste
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.liste_icerik = QWidget()
        self.liste_icerik.setStyleSheet("background: transparent;")
        self.liste_lay = QGridLayout(self.liste_icerik)
        self.liste_lay.setSpacing(14)
        self.liste_lay.setContentsMargins(0, 0, 6, 0)
        self.scroll.setWidget(self.liste_icerik)
        lay.addWidget(self.scroll)

        self._liste_yenile()

    def _liste_yenile(self, tarifler=None):
        # Mevcut widgetları temizle
        while self.liste_lay.count():
            item = self.liste_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if tarifler is None:
            tarifler = list(self.platform.tarifler.values())

        if not tarifler:
            bos = QLabel("Hiç tarif bulunamadı 🍽")
            bos.setAlignment(Qt.AlignCenter)
            bos.setStyleSheet(f"color: {RENKLER['text_hint']}; font-size: 16px;")
            self.liste_lay.addWidget(bos, 0, 0, 1, 2)
            return

        for i, tarif in enumerate(tarifler):
            kart = TarifKarti(tarif)
            kart.tiklandı.connect(self.tarif_sec)
            self.liste_lay.addWidget(kart, i // 2, i % 2)

    def _filtrele(self):
        sorgu = self.arama.text().strip()
        kat = self.kategori_combo.currentText()
        if sorgu:
            tarifler = self.platform.ara(sorgu)
        else:
            tarifler = self.platform.kategori_filtrele(kat)
        self._liste_yenile(tarifler)

    def _tarif_ekle_diyalog(self):
        dlg = TarifEkleDiyalogu(self.platform, self)
        if dlg.exec_() == QDialog.Accepted:
            self._liste_yenile()

    def yenile(self):
        self._liste_yenile()


# ═══════════════════════════════════════════════════════════════════
#  SAYFA: TARİF DETAY
# ═══════════════════════════════════════════════════════════════════

class TarifDetaySayfasi(QWidget):
    geri_don = pyqtSignal()

    def __init__(self, platform: Platform):
        super().__init__()
        self.platform = platform
        self.tarif: Tarif = None
        self._kur()

    def _kur(self):
        self.ana_lay = QVBoxLayout(self)
        self.ana_lay.setContentsMargins(32, 28, 32, 28)
        self.ana_lay.setSpacing(0)
        self.icerik_widget = QWidget()
        self.icerik_widget.setStyleSheet("background: transparent;")
        self.ana_lay.addWidget(self.icerik_widget)

    def tarifi_goster(self, tarif_id: int):
        self.tarif = self.platform.tarifler.get(tarif_id)
        if not self.tarif:
            return

        # Önceki içeriği temizle
        lay = self.icerik_widget.layout()
        if lay:
            while lay.count():
                item = lay.takeAt(0)
                if item.widget(): item.widget().deleteLater()
            QWidget().setLayout(lay)

        lay = QVBoxLayout(self.icerik_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(20)

        # Geri butonu
        geri = ModernButon("← Geri", birincil=False, kucuk=True)
        geri.clicked.connect(self.geri_don)
        geri.setFixedWidth(100)
        lay.addWidget(geri)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")
        icerik = QWidget(); icerik.setStyleSheet("background: transparent;")
        ilay = QVBoxLayout(icerik)
        ilay.setContentsMargins(0, 0, 8, 24)
        ilay.setSpacing(20)

        # Başlık kartı
        baslik_kart = QFrame()
        baslik_kart.setStyleSheet(f"""
            QFrame {{
                background: {RENKLER['bg_card']};
                border: 1px solid {RENKLER['border']};
                border-radius: 16px;
            }}
        """)
        bklay = QVBoxLayout(baslik_kart)
        bklay.setContentsMargins(24, 20, 24, 20)
        bklay.setSpacing(12)

        ust = QHBoxLayout()
        kat_badge = EtiketBadge(self.tarif.kategori, "info")
        ust.addWidget(kat_badge)
        ust.addStretch()
        sure_lbl = QLabel(f"⏱  {self.tarif.sure} dakika")
        sure_lbl.setStyleSheet(f"color: {RENKLER['text_secondary']}; font-size: 14px;")
        ust.addWidget(sure_lbl)
        bklay.addLayout(ust)

        adi_lbl = QLabel(self.tarif.adi)
        adi_lbl.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 24px; font-weight: 800;")
        adi_lbl.setWordWrap(True)
        bklay.addWidget(adi_lbl)

        if self.tarif.aciklama:
            acik_lbl = QLabel(self.tarif.aciklama)
            acik_lbl.setStyleSheet(f"color: {RENKLER['text_secondary']}; font-size: 14px; line-height: 1.6;")
            acik_lbl.setWordWrap(True)
            bklay.addWidget(acik_lbl)

        puan_row = QHBoxLayout()
        yildiz_lbl = QLabel(f"{self.tarif.yildiz_str()}  {self.tarif.ortalama_puan()}/5")
        yildiz_lbl.setStyleSheet(f"color: {RENKLER['star']}; font-size: 16px; font-weight: 600;")
        puan_row.addWidget(yildiz_lbl)
        puan_row.addStretch()
        deger_say = QLabel(f"{len(self.tarif.degerlendirmeler)} değerlendirme")
        deger_say.setStyleSheet(f"color: {RENKLER['text_hint']}; font-size: 13px;")
        puan_row.addWidget(deger_say)
        bklay.addLayout(puan_row)
        ilay.addWidget(baslik_kart)

        # Malzemeler
        if self.tarif.malzemeler:
            mal_baslik = QLabel("🧂  Malzemeler")
            mal_baslik.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 17px; font-weight: 700;")
            ilay.addWidget(mal_baslik)

            mal_kart = QFrame()
            mal_kart.setStyleSheet(f"""
                QFrame {{
                    background: {RENKLER['bg_card']};
                    border: 1px solid {RENKLER['border']};
                    border-radius: 14px;
                }}
            """)
            mklay = QVBoxLayout(mal_kart)
            mklay.setContentsMargins(20, 16, 20, 16)
            mklay.setSpacing(8)
            for i, m in enumerate(self.tarif.malzemeler):
                row = QHBoxLayout()
                dot = QLabel("•")
                dot.setStyleSheet(f"color: {RENKLER['accent']}; font-size: 18px;")
                dot.setFixedWidth(16)
                row.addWidget(dot)
                adi = QLabel(m.adi)
                adi.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 14px;")
                row.addWidget(adi)
                row.addStretch()
                miktar = QLabel(f"{m.miktar} {m.birim}")
                miktar.setStyleSheet(f"color: {RENKLER['text_secondary']}; font-size: 14px;")
                row.addWidget(miktar)
                mklay.addLayout(row)
                if i < len(self.tarif.malzemeler) - 1:
                    mklay.addWidget(AyiriciCizgi())
            ilay.addWidget(mal_kart)

        # Değerlendirmeler
        deger_baslik = QLabel("💬  Değerlendirmeler")
        deger_baslik.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 17px; font-weight: 700;")
        ilay.addWidget(deger_baslik)

        if self.tarif.degerlendirmeler:
            for puan, yorum, kullanici in self.tarif.degerlendirmeler:
                d_kart = QFrame()
                d_kart.setStyleSheet(f"""
                    QFrame {{
                        background: {RENKLER['bg_card']};
                        border: 1px solid {RENKLER['border']};
                        border-radius: 12px;
                    }}
                """)
                dklay = QVBoxLayout(d_kart)
                dklay.setContentsMargins(16, 14, 16, 14)
                dklay.setSpacing(6)
                ust_d = QHBoxLayout()
                kul_lbl = QLabel(f"👤 {kullanici}")
                kul_lbl.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 13px; font-weight: 600;")
                ust_d.addWidget(kul_lbl)
                ust_d.addStretch()
                yil_lbl = QLabel("★" * puan + "☆" * (5 - puan))
                yil_lbl.setStyleSheet(f"color: {RENKLER['star']}; font-size: 13px;")
                ust_d.addWidget(yil_lbl)
                dklay.addLayout(ust_d)
                if yorum:
                    yor_lbl = QLabel(yorum)
                    yor_lbl.setStyleSheet(f"color: {RENKLER['text_secondary']}; font-size: 13px;")
                    yor_lbl.setWordWrap(True)
                    dklay.addWidget(yor_lbl)
                ilay.addWidget(d_kart)
        else:
            bos_d = QLabel("Henüz değerlendirme yok.")
            bos_d.setStyleSheet(f"color: {RENKLER['text_hint']}; font-size: 14px;")
            ilay.addWidget(bos_d)

        # Değerlendirme ekle butonu
        deger_btn = ModernButon("⭐ Değerlendir", birincil=True)
        deger_btn.clicked.connect(self._degerlendir_diyalog)
        ilay.addWidget(deger_btn)

        ilay.addStretch()
        scroll.setWidget(icerik)
        lay.addWidget(scroll)

    def _degerlendir_diyalog(self):
        if not self.tarif: return
        dlg = DegerlendirmeDiyalogu(self.tarif, self)
        if dlg.exec_() == QDialog.Accepted:
            self.tarifi_goster(self.tarif.id)


# ═══════════════════════════════════════════════════════════════════
#  DİYALOGLAR
# ═══════════════════════════════════════════════════════════════════

class TarifEkleDiyalogu(QDialog):
    def __init__(self, platform: Platform, parent=None):
        super().__init__(parent)
        self.platform = platform
        self.setWindowTitle("Yeni Tarif")
        self.setMinimumWidth(500)
        self.setStyleSheet(f"""
            QDialog {{
                background: {RENKLER['bg_card']};
                border-radius: 16px;
            }}
            QLabel {{
                color: {RENKLER['text_primary']};
                font-size: 13px;
                font-weight: 600;
            }}
        """)
        self._kur()

    def _kur(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        baslik = QLabel("Yeni Tarif Ekle")
        baslik.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 20px; font-weight: 800;")
        lay.addWidget(baslik)
        lay.addWidget(AyiriciCizgi())

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignRight)

        self.adi_input = QLineEdit()
        self.adi_input.setPlaceholderText("Tarif adını girin")
        form.addRow("Tarif Adı:", self.adi_input)

        self.kat_combo = QComboBox()
        self.kat_combo.addItems(self.platform.kategoriler)
        form.addRow("Kategori:", self.kat_combo)

        self.sure_spin = QSpinBox()
        self.sure_spin.setRange(1, 480)
        self.sure_spin.setValue(30)
        self.sure_spin.setSuffix(" dakika")
        form.addRow("Hazırlama Süresi:", self.sure_spin)

        self.acik_input = QTextEdit()
        self.acik_input.setPlaceholderText("Tarif açıklaması...")
        self.acik_input.setMaximumHeight(80)
        form.addRow("Açıklama:", self.acik_input)

        lay.addLayout(form)

        # Malzeme ekle alanı
        mal_lbl = QLabel("Malzemeler")
        mal_lbl.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 14px; font-weight: 700;")
        lay.addWidget(mal_lbl)

        mal_row = QHBoxLayout()
        self.mal_adi = QLineEdit(); self.mal_adi.setPlaceholderText("Malzeme adı")
        self.mal_miktar = QLineEdit(); self.mal_miktar.setPlaceholderText("Miktar")
        self.mal_miktar.setFixedWidth(80)
        self.mal_birim = QLineEdit(); self.mal_birim.setPlaceholderText("Birim")
        self.mal_birim.setFixedWidth(80)
        ekle_mal_btn = ModernButon("Ekle", birincil=False, kucuk=True)
        ekle_mal_btn.setFixedWidth(70)
        ekle_mal_btn.clicked.connect(self._malzeme_ekle)
        mal_row.addWidget(self.mal_adi)
        mal_row.addWidget(self.mal_miktar)
        mal_row.addWidget(self.mal_birim)
        mal_row.addWidget(ekle_mal_btn)
        lay.addLayout(mal_row)

        self.mal_liste = QListWidget()
        self.mal_liste.setFixedHeight(100)
        self.mal_liste.setStyleSheet(f"""
            QListWidget {{
                background: {RENKLER['bg_input']};
                border: 1px solid {RENKLER['border']};
                border-radius: 10px;
                padding: 6px;
                color: {RENKLER['text_primary']};
                font-size: 13px;
            }}
            QListWidget::item {{ padding: 4px; }}
        """)
        lay.addWidget(self.mal_liste)
        self.malzemeler: list[Malzeme] = []

        # Butonlar
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        iptal_btn = ModernButon("İptal", birincil=False)
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn = ModernButon("✓ Kaydet", birincil=True)
        kaydet_btn.clicked.connect(self._kaydet)
        btn_row.addWidget(iptal_btn)
        btn_row.addWidget(kaydet_btn)
        lay.addLayout(btn_row)

    def _malzeme_ekle(self):
        adi = self.mal_adi.text().strip()
        if not adi: return
        try:
            miktar = float(self.mal_miktar.text()) if self.mal_miktar.text() else 1
        except ValueError:
            miktar = 1
        birim = self.mal_birim.text().strip() or "adet"
        m = Malzeme(adi, miktar, birim)
        self.malzemeler.append(m)
        self.mal_liste.addItem(str(m))
        self.mal_adi.clear(); self.mal_miktar.clear(); self.mal_birim.clear()

    def _kaydet(self):
        adi = self.adi_input.text().strip()
        if not adi:
            QMessageBox.warning(self, "Hata", "Tarif adı boş olamaz!")
            return
        tarif = Tarif(adi, self.kat_combo.currentText(),
                      self.sure_spin.value(), self.acik_input.toPlainText().strip())
        tarif.malzemeler = self.malzemeler
        self.platform.tarif_ekle(tarif)
        self.accept()


class DegerlendirmeDiyalogu(QDialog):
    def __init__(self, tarif: Tarif, parent=None):
        super().__init__(parent)
        self.tarif = tarif
        self.setWindowTitle("Değerlendir")
        self.setMinimumWidth(400)
        self.setStyleSheet(f"""
            QDialog {{
                background: {RENKLER['bg_card']};
                border-radius: 16px;
            }}
            QLabel {{
                color: {RENKLER['text_primary']};
            }}
        """)
        self._kur()

    def _kur(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        baslik = QLabel(f'\u201c{self.tarif.adi}\u201d Değerlendir')
        baslik.setStyleSheet(f"color: {RENKLER['text_primary']}; font-size: 17px; font-weight: 700;")
        baslik.setWordWrap(True)
        lay.addWidget(baslik)
        lay.addWidget(AyiriciCizgi())

        # Kullanıcı adı
        kul_lbl = QLabel("Adınız:")
        lay.addWidget(kul_lbl)
        self.kul_input = QLineEdit()
        self.kul_input.setPlaceholderText("Adınızı girin")
        lay.addWidget(self.kul_input)

        # Puan
        puan_lbl = QLabel("Puan (1-5):")
        lay.addWidget(puan_lbl)
        self.puan_spin = QSpinBox()
        self.puan_spin.setRange(1, 5)
        self.puan_spin.setValue(5)
        lay.addWidget(self.puan_spin)

        # Yorum
        yor_lbl = QLabel("Yorumunuz (isteğe bağlı):")
        lay.addWidget(yor_lbl)
        self.yorum_input = QTextEdit()
        self.yorum_input.setPlaceholderText("Yorumunuzu yazın...")
        self.yorum_input.setMaximumHeight(80)
        lay.addWidget(self.yorum_input)

        btn_row = QHBoxLayout()
        iptal = ModernButon("İptal", birincil=False)
        iptal.clicked.connect(self.reject)
        kaydet = ModernButon("⭐ Gönder", birincil=True)
        kaydet.clicked.connect(self._gonder)
        btn_row.addWidget(iptal)
        btn_row.addWidget(kaydet)
        lay.addLayout(btn_row)

    def _gonder(self):
        kul = self.kul_input.text().strip() or "Anonim"
        self.tarif.degerlendir(self.puan_spin.value(),
                               self.yorum_input.toPlainText().strip(), kul)
        self.accept()


# ═══════════════════════════════════════════════════════════════════
#  ANA PENCERE
# ═══════════════════════════════════════════════════════════════════

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.platform = Platform()
        self.setWindowTitle("TarifDünyası")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 760)
        self._kur_arayuz()

    def _kur_arayuz(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana = QHBoxLayout(merkez)
        ana.setContentsMargins(0, 0, 0, 0)
        ana.setSpacing(0)

        # ── SOL NAVİGASYON PANEL ──────────────────────────────────
        nav_panel = QWidget()
        nav_panel.setFixedWidth(220)
        nav_panel.setStyleSheet(f"""
            QWidget {{
                background: {RENKLER['bg_card']};
                border-right: 1px solid {RENKLER['border']};
            }}
        """)
        nav_lay = QVBoxLayout(nav_panel)
        nav_lay.setContentsMargins(12, 24, 12, 24)
        nav_lay.setSpacing(4)

        # Logo
        logo = QLabel("🍽  TarifDünyası")
        logo.setStyleSheet(f"""
            color: {RENKLER['accent']};
            font-size: 17px;
            font-weight: 800;
            padding: 0 8px 16px 8px;
        """)
        nav_lay.addWidget(logo)
        nav_lay.addWidget(AyiriciCizgi())
        nav_lay.addSpacing(8)

        # Nav butonları
        self.nav_butonlar = []
        nav_items = [
            ("🏠", "Anasayfa", 0),
            ("📖", "Tarifler", 1),
        ]
        for ikon, etiket, idx in nav_items:
            btn = NavButon(ikon, etiket, aktif=(idx == 0))
            btn.clicked.connect(lambda checked, i=idx: self._sayfa_degistir(i))
            self.nav_butonlar.append(btn)
            nav_lay.addWidget(btn)

        nav_lay.addStretch()
        nav_lay.addWidget(AyiriciCizgi())
        nav_lay.addSpacing(8)

        # Alt bilgi
        alt_lbl = QLabel("v1.0  •  PyQt5")
        alt_lbl.setStyleSheet(f"color: {RENKLER['text_hint']}; font-size: 11px; padding: 0 8px;")
        nav_lay.addWidget(alt_lbl)
        ana.addWidget(nav_panel)

        # ── ANA İÇERİK ALANI ─────────────────────────────────────
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background: {RENKLER['bg_dark']};")

        self.anasayfa = AnasayfaSayfasi(self.platform)
        self.anasayfa.tarif_sec.connect(self._tarif_detay_goster)

        self.tarif_listesi = TarifListesiSayfasi(self.platform)
        self.tarif_listesi.tarif_sec.connect(self._tarif_detay_goster)

        self.tarif_detay = TarifDetaySayfasi(self.platform)
        self.tarif_detay.geri_don.connect(self._geri_don)

        self.stack.addWidget(self.anasayfa)      # 0
        self.stack.addWidget(self.tarif_listesi) # 1
        self.stack.addWidget(self.tarif_detay)   # 2

        ana.addWidget(self.stack)
        self._onceki_sayfa = 0

    def _sayfa_degistir(self, idx):
        self._onceki_sayfa = idx
        for i, btn in enumerate(self.nav_butonlar):
            if i == idx:
                btn.aktif_yap()
            else:
                btn.pasif_yap()
        self.stack.setCurrentIndex(idx)

    def _tarif_detay_goster(self, tarif_id: int):
        self._onceki_sayfa = self.stack.currentIndex()
        self.tarif_detay.tarifi_goster(tarif_id)
        self.stack.setCurrentIndex(2)

    def _geri_don(self):
        self.tarif_listesi.yenile()
        self.stack.setCurrentIndex(self._onceki_sayfa)


# ═══════════════════════════════════════════════════════════════════
#  BAŞLAT
# ═══════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLE_SHEET)

    # Koyu palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(RENKLER['bg_dark']))
    palette.setColor(QPalette.WindowText, QColor(RENKLER['text_primary']))
    palette.setColor(QPalette.Base, QColor(RENKLER['bg_input']))
    palette.setColor(QPalette.AlternateBase, QColor(RENKLER['bg_card']))
    palette.setColor(QPalette.ToolTipBase, QColor(RENKLER['bg_card2']))
    palette.setColor(QPalette.ToolTipText, QColor(RENKLER['text_primary']))
    palette.setColor(QPalette.Text, QColor(RENKLER['text_primary']))
    palette.setColor(QPalette.Button, QColor(RENKLER['bg_card2']))
    palette.setColor(QPalette.ButtonText, QColor(RENKLER['text_primary']))
    palette.setColor(QPalette.Highlight, QColor(RENKLER['accent']))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))
    app.setPalette(palette)

    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
