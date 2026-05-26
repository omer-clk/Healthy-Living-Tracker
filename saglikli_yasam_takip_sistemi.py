import sqlite3
import os
from datetime import date
from datetime import datetime

def ekrani_temizle():
    os.system('cls' if os.name == 'nt' else 'clear')

def veritabani_hazirla():
    conn = sqlite3.connect("veriler.db")
    cursor = conn.cursor()
    
    # kullanıcı bilgileri
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            kullaniciAdi TEXT PRIMARY KEY,
            sifre TEXT,
            boy REAL DEFAULT 0.0,
            kilo REAL DEFAULT 0.0,
            vkiDeger REAL DEFAULT 0.0,
            sigara_birakma TEXT DEFAULT 'Yok',
            alkol_birakma TEXT DEFAULT 'Yok',
            son_adet TEXT DEFAULT 'Yok'
        )
    """)
    
    # takip Tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gunluk_takip (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kullaniciAdi TEXT,
            tarih TEXT,
            su_tuketim REAL DEFAULT 0.0,
            kalori REAL DEFAULT 0.0,
            spor_yapti TEXT DEFAULT 'Hayır',
            FOREIGN KEY (kullaniciAdi) REFERENCES kullanicilar(kullaniciAdi)
        )
    """)
    
    cursor.execute("INSERT OR IGNORE INTO kullanicilar (kullaniciAdi, sifre) VALUES ('admin', '12345')")
    conn.commit()
    conn.close()

veritabani_hazirla()

yemekler = {
    "1": {"isim": "Tavuk Göğsü", "kalori": 165, "porsiyon": "100 gram"},
    "2": {"isim": "Kırmızı Et", "kalori": 250, "porsiyon": "100 gram"},
    "3": {"isim": "Ton Balığı", "kalori": 132, "porsiyon": "100 gram"},
    "4": {"isim": "Yumurta", "kalori": 78, "porsiyon": "1 Adet"},
    "5": {"isim": "Lor Peyniri", "kalori": 90, "porsiyon": "100 gram"},
    "6": {"isim": "Tam Yağlı Süt", "kalori": 61, "porsiyon": "100 ml"},
    "7": {"isim": "Yoğurt", "kalori": 60, "porsiyon": "100 gram"},
    "8": {"isim": "Yeşil Mercimek", "kalori": 116, "porsiyon": "100 gram (Haşlanmış)"},
    "9": {"isim": "Nohut", "kalori": 164, "porsiyon": "100 gram (Haşlanmış)"},
    "10": {"isim": "Pirinç Pilavı", "kalori": 130, "porsiyon": "100 gram"},
    "11": {"isim": "Bulgur Pilavı", "kalori": 83, "porsiyon": "100 gram"},
    "12": {"isim": "Makarna", "kalori": 158, "porsiyon": "100 gram (Haşlanmış)"},
    "13": {"isim": "Yulaf Ezmesi", "kalori": 389, "porsiyon": "100 gram"},
    "14": {"isim": "Haşlanmış Patates", "kalori": 87, "porsiyon": "100 gram"},
    "15": {"isim": "Beyaz Ekmek", "kalori": 80, "porsiyon": "1 Dilim"},
    "16": {"isim": "Tam Buğday Ekmeği", "kalori": 65, "porsiyon": "1 Dilim"},
    "17": {"isim": "Simit", "kalori": 275, "porsiyon": "1 Adet"},
    "18": {"isim": "Poğaça", "kalori": 350, "porsiyon": "1 Adet"},
    "19": {"isim": "Brokoli", "kalori": 34, "porsiyon": "100 gram"},
    "20": {"isim": "Mevsim Salata", "kalori": 45, "porsiyon": "1 Porsiyon (Yağsız)"},
    "21": {"isim": "Elma", "kalori": 52, "porsiyon": "1 Adet (Orta Boy)"},
    "22": {"isim": "Muz", "kalori": 89, "porsiyon": "1 Adet (Orta Boy)"},
    "23": {"isim": "Portakal", "kalori": 47, "porsiyon": "1 Adet (Orta Boy)"},
    "24": {"isim": "Karışık Kuruyemiş", "kalori": 600, "porsiyon": "100 gram"},
    "25": {"isim": "Sütlü Çikolata", "kalori": 530, "porsiyon": "100 gram"},
    "26": {"isim": "Patates Cipsi", "kalori": 536, "porsiyon": "100 gram"},
    "27": {"isim": "Kola", "kalori": 140, "porsiyon": "1 Kutu (330ml)"},
    "28": {"isim": "Ayran", "kalori": 60, "porsiyon": "1 Bardak (200ml)"},
    "29": {"isim": "Meyve Suyu", "kalori": 150, "porsiyon": "1 Kutu (330ml)"},
    "30": {"isim": "Sade Soda", "kalori": 0, "porsiyon": "1 Şişe (200ml)"},
    "31": {"isim": "Filtre Kahve", "kalori": 2, "porsiyon": "1 Fincan (Şekersiz)"},
    "32": {"isim": "Çay", "kalori": 1, "porsiyon": "1 Bardak (Şekersiz)"}
}

def ana_menu():
    print("\n===== SAĞLIKLI YAŞAM TAKİP SİSTEMİ =====")
    secim = input("1-Giriş Yap\n2-Kayıt Ol\n3-Çıkış Yap\nSeçiminiz: ")
    return secim

def kayit_ol():
    kullaniciAdi = input("Kullanıcı adınızı belirleyiniz: ")
    sifre = input("Şifrenizi belirleyiniz: ")
    
    conn = sqlite3.connect("veriler.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO kullanicilar (kullaniciAdi, sifre) VALUES (?, ?)", (kullaniciAdi, sifre))
        conn.commit()
        print(f"\n✅ Hoşgeldin {kullaniciAdi}! Kayıt Başarılı.")
    except sqlite3.IntegrityError:
        print("\n❌ Hata: Bu kullanıcı adı zaten alınmış!")
    
    conn.close()
    input("\nDevam etmek için Enter'a basın...")

def admin_paneli():
    while True:
        ekrani_temizle()
        print("\n=== YÖNETİCİ PANELİ ===")
        secim1 = input("1-Kullanıcıları Listele\n2-Geri Bildirim Paneli\n3-Panelden Çık\nSeçiminiz: ")
        
        if secim1 == '1':
            conn = sqlite3.connect("veriler.db")
            cursor = conn.cursor()
            cursor.execute("SELECT kullaniciAdi FROM kullanicilar")
            uyeler = [satir[0] for satir in cursor.fetchall()] 
            conn.close()
            print(f"\n👥 Aktif kullanıcılar : {uyeler}")
            input("\nDevam etmek için Enter'a basın...")
            
        elif secim1 == '2':
            print("\n--- GERİ BİLDİRİMLER ---")
            try:
                with open("geribildirimler.txt", "r", encoding="utf-8") as dosya:
                    print(dosya.read())
            except FileNotFoundError:
                print("Henüz geri bildirim yok.")
            print("------------------------")
            input("\nDevam etmek için Enter'a basın...")
            
        elif secim1 == '3':
            print("Panelden Çıkılıyor...")
            break
        else:
            print("Hatalı seçim yaptınız!")
            input("\nDevam etmek için Enter'a basın...")

def kullanici_paneli(aktifKullanici):
    bugun = str(date.today()) 
    
    conn = sqlite3.connect("veriler.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM gunluk_takip WHERE kullaniciAdi = ? AND tarih = ?", (aktifKullanici, bugun))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO gunluk_takip (kullaniciAdi, tarih) VALUES (?, ?)", (aktifKullanici, bugun))
        conn.commit()
    conn.close()

    while True:
        ekrani_temizle()
        print(f"\n=== {bugun} GÜNLÜK ÖZETİ ===")
        secim2 = input("1-Günlük Su Takibi\n2-VKİ Hesapla\n3-Kalori/Yemek Takibi\n4-Alışkanlık Takibi (Spor vb.)\n5-Sayaçlar: Sigara & Alkol Bırakma / Regl Döngüsü\n6-Geri Bildirim Gönder\n7-Çıkış\nSeçiminiz: ")

        if secim2 == '1':
            su_miktar = float(input("\nBugün içtiğiniz su miktarını litre cinsinden giriniz (Örnek: 1.5): "))
            
            conn = sqlite3.connect("veriler.db")
            cursor = conn.cursor()
            cursor.execute("SELECT su_tuketim FROM gunluk_takip WHERE kullaniciAdi = ? AND tarih = ?", (aktifKullanici, bugun))
            mevcut_su = cursor.fetchone()[0]
            yeni_su = mevcut_su + su_miktar
            
            cursor.execute("UPDATE gunluk_takip SET su_tuketim = ? WHERE kullaniciAdi = ? AND tarih = ?", (yeni_su, aktifKullanici, bugun))
            conn.commit()
            conn.close()
            
            print(f"\n Eklendi! Bugün toplam {yeni_su:.1f} litre su içtiniz.")
            if yeni_su < 1.5:
                print("Vücudun susuz kalmış, daha fazla su iç.")
            elif yeni_su <= 2.5:
                print("Böyle devam 2.5 litreyi geç.")
            elif yeni_su <= 4.0:
                print("Harika bugün yeteri kadar su içtin.")
            else:
                print("Dikkat! 4 litrenin üzeri aşırı su tüketimi böbrekleri yorabilir.")
            
            input("\nMenüye dönmek için Enter'a basın...")

        elif secim2 == '2':
            boy = float(input("\nBoyunuzu (metre) giriniz (Örn: 1.75): "))
            kilo = float(input("Kilonuzu (kilogram) giriniz (Örn: 70): "))
            vkiDeger = kilo / (boy * boy)
            
            conn = sqlite3.connect("veriler.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE kullanicilar SET boy = ?, kilo = ?, vkiDeger = ? WHERE kullaniciAdi = ?", (boy, kilo, vkiDeger, aktifKullanici))
            conn.commit()
            conn.close()
            
            print(f"\n VKİ Değeriniz: {vkiDeger:.2f}")
            if vkiDeger < 18.5:
                print("Durum: Zayıf kategorisindesiniz.")
            elif 18.5 <= vkiDeger <= 25.0:
                print("Durum: Normal kategorisindesiniz.")
            elif vkiDeger > 25.0:
                print("Durum: Kilolu kategorisindesiniz.")
                
            input("\nMenüye dönmek için Enter'a basın...")

        elif secim2 == '3':
            print("\n--- Yemek Menüsü ---")
            for numara, detay in yemekler.items():
                print(f"{numara} - {detay['isim']} : {detay['kalori']} kcal -> {detay['porsiyon']}")
            yemek_secim = input("\nTükettiğiniz besin numarasını giriniz: ")
            
            if yemek_secim in yemekler:
                porsiyon = float(input("Kaç porsiyon tükettiniz? (Yarım için 0.5, Çift için 2): "))
                alinan_kalori = yemekler[yemek_secim]["kalori"] * porsiyon
                
                conn = sqlite3.connect("veriler.db")
                cursor = conn.cursor()
                cursor.execute("SELECT kalori FROM gunluk_takip WHERE kullaniciAdi = ? AND tarih = ?", (aktifKullanici, bugun))
                mevcut_kalori = cursor.fetchone()[0]
                yeni_kalori = mevcut_kalori + alinan_kalori
                
                cursor.execute("UPDATE gunluk_takip SET kalori = ? WHERE kullaniciAdi = ? AND tarih = ?", (yeni_kalori, aktifKullanici, bugun))
                conn.commit()
                conn.close()
                print(f"\n Eklendi! Bugünkü toplam kaloriniz: {yeni_kalori:.1f} kcal")
            else:
                print("\n Hatalı menü numarası!")
                
            input("\nMenüye dönmek için Enter'a basın...")

        elif secim2 == '4':
            cevap = input("\nBugün en az 30 dakika spor yaptın mı? (E/H): ").upper()
            if cevap == 'E':
                conn = sqlite3.connect("veriler.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE gunluk_takip SET spor_yapti = 'Evet' WHERE kullaniciAdi = ? AND tarih = ?", (aktifKullanici, bugun))
                conn.commit()
                conn.close()
                print(" Harika! Bu bilgi günlüğüne kaydedildi.")
            else:
                print("Sorun değil, yarın telafi edersin!")
                
            input("\nMenüye dönmek için Enter'a basın...")

        elif secim2 == '5':
            while True:
                ekrani_temizle()
                print("\n=== SAYAÇLAR & SAĞLIK TAKİBİ ===")
                alt_secim = input("1-Sigara Bırakma Sayacı & Vücut Kazanımları\n2-Alkol Bırakma Sayacı\n3-Regl Döngüsü Takibi\n4-Üst Menüye Dön\nSeçiminiz: ")
                
                conn = sqlite3.connect("veriler.db")
                cursor = conn.cursor()
                cursor.execute("SELECT sigara_birakma, alkol_birakma, son_adet FROM kullanicilar WHERE kullaniciAdi = ?", (aktifKullanici,))
                bilgiler = cursor.fetchone()
                
                sigara_tarihi = bilgiler[0]
                alkol_tarihi = bilgiler[1]
                adet_tarihi = bilgiler[2]

                if alt_secim == '1':
                    if sigara_tarihi == 'Yok':
                        yeni_tarih = input("\nHarika bir karar! Sigarayı bıraktığınız tarihi girin (Örn: 2026-05-20): ")
                        cursor.execute("UPDATE kullanicilar SET sigara_birakma = ? WHERE kullaniciAdi = ?", (yeni_tarih, aktifKullanici))
                        conn.commit()
                        print("Tarih kaydedildi! Başarı durumunuzu görmek için menüye tekrar girin.")
                    else:
                        baslangic = datetime.strptime(sigara_tarihi, "%Y-%m-%d").date()
                        fark = (date.today() - baslangic).days
                        print(f"\n🎉 Tebrikler! Tam {fark} gündür sigara kullanmıyorsunuz.")
                        
                        print("\n--- VÜCUDUNUZDAKİ SAĞLIK KAZANIMLARI ---")
                        if fark == 0:
                            print("• İlk 20 dakika: Kan basıncı ve nabız normale dönüyor.")
                            print("• İlk 8 saat: Kandaki oksijen seviyesi normale yükseliyor.")
                        if fark >= 1:
                            print("[✔] İlk 24 saat: Kalp krizi riski azalmaya başladı.")
                        if fark >= 2:
                            print("[✔] 48 Saat: Nikotin vücuttan tamamen atıldı. Tat ve koku duyularınız keskinleşti.")
                        else:
                            print("[] 48 Saat Hedefi: Nikotinin vücuttan tamamen atılmasına kalan gün: " + str(2 - fark))
                            
                        if fark >= 3:
                            print("[✔] 72 Saat: Akciğer bronşları gevşedi, nefes almanız kolaylaştı.")
                        if fark >= 14:
                            print("[✔] 2 Hafta: Akciğer fonksiyonları %30 arttı, kan dolaşımı mükemmel seviyede.")
                        else:
                            print("[] 2 Hafta Hedefi: Akciğer kapasitesinin %30 artmasına kalan gün: " + str(14 - fark))
                            
                        if fark >= 90:
                            print("[✔] 3 Ay: Öksürük, sinus tıkanıklığı ve nefes darlığı tamamen bitti.")
                        
                        sifirla = input("\n⚠ Maalesef sigara içtiniz mi? Sayacı sıfırlamak ister misiniz? (E/H): ").upper()
                        if sifirla == 'E':
                            cursor.execute("UPDATE kullanicilar SET sigara_birakma = 'Yok' WHERE kullaniciAdi = ?", (aktifKullanici,))
                            conn.commit()
                            print("🚫 Sayacınız sıfırlandı. Asla pes etmek yok! Kendinize inanın ve tekrar başlayın.")
                    
                    conn.close()
                    input("\nDevam etmek için Enter'a basın...")

                elif alt_secim == '2':
                    if alkol_tarihi == 'Yok':
                        yeni_tarih = input("\nSağlıklı yaşam için dev adım! Alkolü bıraktığınız tarihi girin (Örn: 2026-05-20): ")
                        cursor.execute("UPDATE kullanicilar SET alkol_birakma = ? WHERE kullaniciAdi = ?", (yeni_tarih, aktifKullanici))
                        conn.commit()
                        print("Tarih kaydedildi!")
                    else:
                        baslangic = datetime.strptime(alkol_tarihi, "%Y-%m-%d").date()
                        fark = (date.today() - baslangic).days
                        print(f"\n Harika! {fark} gündür alkolsüz temiz bir hayat yaşıyorsunuz.")
                        
                        print("\n--- VÜCUDUNUZDAKİ SAĞLIK KAZANIMLARI ---")
                        if fark >= 7:
                            print("[✔] 1 Hafta: Uyku kaliteniz maksimuma ulaştı, cildiniz nem kazandı.")
                        if fark >= 30:
                            print("[✔] 1 Ay: Karaciğer yağlanmanız %15 azaldı, kilo kontrolünüz kolaylaştı.")
                        else:
                            print("[] 1 Ay Hedefi: Karaciğerin kendini yenilemeye başlamasına kalan gün: " + str(30 - fark))

                        sifirla = input("\n⚠ Sayacı sıfırlamak ister misiniz? (E/H): ").upper()
                        if sifirla == 'E':
                            cursor.execute("UPDATE kullanicilar SET alkol_birakma = 'Yok' WHERE kullaniciAdi = ?", (aktifKullanici,))
                            conn.commit()
                            print("🚫 Alkol bırakma sayacınız sıfırlandı. Yarın yeni bir gün, tekrar deneyebilirsiniz!")
                    
                    conn.close()
                    input("\nDevam etmek için Enter'a basın...")

                elif alt_secim == '3':
                    if adet_tarihi == 'Yok':
                        y_tarih = input("\nSon regl döngünüzün başlangıç tarihini girin (Örn: 2026-05-10): ")
                        cursor.execute("UPDATE kullanicilar SET son_adet = ? WHERE kullaniciAdi = ?", (y_tarih, aktifKullanici))
                        conn.commit()
                        print("Tarih başarıyla kaydedildi!")
                    else:
                        son_tarih = datetime.strptime(adet_tarihi, "%Y-%m-%d").date()
                        gecen_gun = (date.today() - son_tarih).days
                        print(f"\n Son döngü başlangıcından itibaren geçen gün: {gecen_gun}")
                        
                        if gecen_gun >= 28:
                            print("🔔 Hatırlatma: Yeni periyodunuzun başlama zamanı gelmiş veya gecikmiş olabilir.")
                            guncelle = input("Yeni bir döngü başladı mı? Bugünün tarihini kaydetmek için (E/H): ").upper()
                            if guncelle == 'E':
                                cursor.execute("UPDATE kullanicilar SET son_adet = ? WHERE kullaniciAdi = ?", (str(date.today()), aktifKullanici))
                                conn.commit()
                                print("Döngü başlangıcı bugünün tarihiyle güncellendi!")
                        else:
                            kalan = 28 - gecen_gun
                            print(f" Tahmini sonraki döngü başlangıcına kalan süre: {kalan} gün.")
                            
                            if 12 <= gecen_gun <= 16:
                                print("🔥 Bilgi: Şu an yumurtlama (ovülasyon) dönemindesiniz. Vücut enerjiniz yüksek olabilir.")
                    
                    conn.close()
                    input("\nDevam etmek için Enter'a basın...")

                elif alt_secim == '4':
                    conn.close()
                    break
                else:
                    print("Hatalı seçim yaptınız!")
                    conn.close()
                    input("\nDevam etmek için Enter'a basın...")

        elif secim2 == '6':
            mesaj = input("\nSistemle ilgili geribildirimlerinizi lütfen yazın: ")
            with open("geribildirimler.txt", "a", encoding="utf-8") as dosya:
                dosya.write(f"{aktifKullanici} : {mesaj}\n")
            print("Geri bildiriminiz kaydedildi! Teşekkür ederiz.")
            input("\nMenüye dönmek için Enter'a basın...")

        elif secim2 == '7':
            print("Panelden Çıkılıyor...")
            break
        else:
            print("Hatalı seçim yaptınız!")
            input("\nDevam etmek için Enter'a basın...")

def giris_yap():
    nick = input("Kullanıcı adınızı giriniz: ")
    parola = input("Şifrenizi giriniz: ")
    
    conn = sqlite3.connect("veriler.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM kullanicilar WHERE kullaniciAdi = ? AND sifre = ?", (nick, parola))
    kullanici = cursor.fetchone()
    conn.close()
    
    if kullanici:
        if nick == "admin":
            print("\nYönetici paneline yönlendiriliyorsunuz...")
            admin_paneli()
        else:
            print(f"\nSisteme giriş yapıldı! Tekrar hoşgeldin {nick}")
            input("Devam etmek için Enter'a basın...")
            kullanici_paneli(nick)
    else:
        print("\n Hatalı kullanıcı adı veya şifre!")
        input("Devam etmek için Enter'a basın...")

while True:
    ekrani_temizle() 
    gelenSecim = ana_menu()
    if gelenSecim == '1':
        ekrani_temizle()
        print("--- GİRİŞ MENÜSÜ ---")
        giris_yap()
    elif gelenSecim == '2':
        ekrani_temizle()
        print("--- KAYIT MENÜSÜ ---")
        kayit_ol()
    elif gelenSecim == '3':
        print("\nÇıkış Yapılıyor. İyi günler...")
        break
    else:
        print("\n Hatalı Seçim Yaptınız!")
        input("Devam etmek için Enter'a basın...")