import streamlit as st
import sqlite3
import time
from datetime import datetime



conn = sqlite3.connect("veritabani.db")
cursor=conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS uyeler(
id INTEGER PRIMARY KEY AUTOINCREMENT,
isim TEXT NOT NULL,
abonelik TEXT NOT NULL,
yumurta TEXT NOT NULL,
secilen_tarih TEXT NOT NULL,
selected_time TEXT NOT NULL,
no TEXT NOT NULL
)
''')

def uye_ekle(isim,abonelik,yumurta,secilen_tarih,selected_time, no):

    cursor.execute('INSERT INTO uyeler(isim,abonelik,yumurta,secilen_tarih,selected_time,no) VALUES (?,?,?,?,?,?)', (isim, abonelik, yumurta, str(secilen_tarih), str(selected_time),  no))
    conn.commit()

st.title("Yumurta Satış Sayfası")

menu = ["Anasayfa", "Kayıt Ol","Yumurta Türü Ekle","Üyeleri Görüntüle", "Yumurtaları Görüntüle", "Üye Sil ve Düzenle", "Yumurta Sil ve Düzenle"]
choice = st.sidebar.selectbox("Menu",menu)
cursor.execute("SELECT * FROM yumurtalar")
data = cursor.fetchall()


if choice=="Kayıt Ol":
    newisim=st.text_input("Adınız Soyadınız")
    newabonelik=st.radio("Hangi aboneliği seçmek istersiniz?", ["Haftalık", "Aylık"])
    newyumurta=st.radio("Hangi yumurta türünü seçmek istersiniz?", data)
    newsecilen_tarih = st.date_input("Tarih Giriniz")
    newselected_time = st.time_input("Saat Seçiniz")
    newno= st.text_input("Numaranızı Giriniz")
    st.write("Üyelikler bir senelik yapılmaktadır")
    submit=st.button("Kaydet")
    if submit:
        uye_ekle(newisim, newabonelik, newyumurta, newsecilen_tarih, newselected_time, newno)
        st.success("Başarıyla Kayıt Oldunuz")

cursor.execute('''
CREATE TABLE IF NOT EXISTS yumurtalar(
id INTEGER PRIMARY KEY AUTOINCREMENT,
tur TEXT NOT NULL,
adet_fiyat INTEGER NOT NULL
)
''')
def yumurta_ekle(tur,adet_fiyat):

    cursor.execute('INSERT INTO yumurtalar(tur,adet_fiyat) VALUES (?,?)', (tur, adet_fiyat))
    conn.commit()
if choice == "Yumurta Türü Ekle":
    newtur=st.text_input("Yumurta Tür Adını Giriniz")
    newadet_fiyat=st.number_input("Yumurta Adet Fiyatı Giriniz")
    gonder = st.button("Kaydet")
    if gonder:
        yumurta_ekle(newtur,newadet_fiyat)
        st.success("Başarıyla Yumurta Türü Eklediiz")

if choice=="Üyeleri Görüntüle":
    cursor.execute("SELECT * FROM uyeler")
    goruntule = cursor.fetchall()
    for veri in goruntule:
        st.write(f"Ad Soyad : {veri[1]} , Abonelik Türü:  {veri[2]} , Yumurta Türü:  {veri[3]} , Teslim Tarihi:  {veri[4]}, Teslim Saati:  {veri[5]}, Numara:  {veri[6]}")
        st.write("---")

if choice=="Yumurtaları Görüntüle":
    cursor.execute("SELECT * FROM yumurtalar")
    data = cursor.fetchall()
    for veri in data:
        st.write(f"Yumurta İsmi: {veri[1]}")
        st.write("---")

if choice=="Üye Sil ve Düzenle":

       st.subheader("Düzenle")
       yeni_isim = st.text_input("Yeni isim ve soyisim giriniz")
       yeni_abonelik = st.radio("Yeni abonelik türünü seçiniz", ["Haftalık", "Aylık"])
       yeni_yumurta = st.radio("Yeni yumurta türünü seçiniz", data)
       yeni_secilen_tarih = st.date_input("Yeni teslim tarhini seçiniz")
       yeni_selected_time = st.time_input("Yeni teslim saatini seçiniz")
       yeni_no = st.text_input("Yeni telefon numarasını giriniz")
       guncellenecek_id = st.text_input("Güllenecek kişinin id numarasını giriniz")
       cursor.execute("UPDATE uyeler SET isim=?, abonelik=?, yumurta=?, secilen_tarih=?, selected_time=?, no=? WHERE id=?",
                      (yeni_isim, yeni_abonelik, str(yeni_yumurta), str(yeni_secilen_tarih), str(yeni_selected_time), yeni_no, guncellenecek_id))
       guncelle=st.button("Güncelle", key="ücüncü")
       if guncelle:
           if cursor.rowcount > 0:
               st.write("Kayıt güncelleme Başarılı")
           else:
               st.write(f"Hatalı işlem kullanıcı bulunamadı {guncellenecek_id}")

       conn.commit()
       st.write("---")



       st.subheader("Sil")
       silinecek_id = st.text_input("Silinecek kişinin id numarasını giriniz.")

       cursor.execute("DELETE FROM uyeler WHERE id=?", (silinecek_id,))
       conn.commit()
       sil=st.button("Üyeyi Sil", key="dorduncu")
       if sil:
            if cursor.rowcount > 0:
                   st.write("Kayıt Silme Başarılı")
            else:
                   st.write(f"Hatalı işlem kullanıcı bulunamadı {silinecek_id}")

if choice=="Yumurta Sil ve Düzenle":
       st.subheader("Düzenle")
       yeni_tur = st.text_input("Yeni yumurta türünü giriniz")
       yeni_adet_fiyat = st.number_input("Yeni yumurta adet fiyatını giriniz")
       guncellenecekk_id = st.text_input("Güllenecek yumurtanın id numarasını giriniz")
       cursor.execute("UPDATE yumurtalar SET tur=?, adet_fiyat=? WHERE id=?",
                      (yeni_tur, yeni_adet_fiyat, guncellenecekk_id))
       guncellee=st.button("Güncelle", key="besinci")
       if guncellee:
           if cursor.rowcount >0:
               st.write("Kayıt güncelleme Başarılı")
           else:
               st.write(f"Hatalı işlem kullanıcı bulunamadı {guncellenecekk_id}")

       conn.commit()
       st.write("---")



       st.subheader("Sil")
       silinecekk_id = st.text_input("Silinecek yumurtanın id numarasını giriniz.")

       cursor.execute("DELETE FROM yumurtalar WHERE id=?", (silinecekk_id,))
       conn.commit()
       sill=st.button("Yumurtayı Sil", key="altıncı")
       if sill:
            if cursor.rowcount > 0:
                   st.write("Kayıt Silme Başarılı")
            else:
                   st.write(f"Hatalı işlem kullanıcı bulunamadı {silinecekk_id}")

if choice=="Anasayfa":
    st.header("Bugünün teslimatları")
    bugun = datetime.now().date()
    cursor.execute("SELECT * FROM uyeler WHERE secilen_tarih = ?", (bugun,))
    teslimatlar = cursor.fetchall()
    if teslimatlar:
        st.subheader(f"({bugun} Tarihindeki Teslimatlar)")
        for teslimat in teslimatlar:
            st.write(f"İsim: {teslimat[1]}")
            st.write(f"Abonelik: {teslimat[2]}")
            st.write(f"Yumurta Türü: {teslimat[3]}")
            st.write(f"Teslim Tarihi: {teslimat[4]} {teslimat[5]}")
            st.write(f"Telefon Numarası: {teslimat[6]}")
            st.write("---")
    else:
        st.write(f"{bugun} Tarihinde Hiç Teslimat Yok")
        st.write("---")

    st.subheader("Toplam Üye Sayısı")
    cursor.execute("SELECT * FROM uyeler")
    uyeler=0
    uyesayısı = cursor.fetchall()
    for i in uyesayısı:
        uyeler=uyeler+1
    st.write("Güncel Üye Sayısı",uyeler)
    st.write("---")

    st.subheader("Günlük Kazanç")
    bugun = datetime.now().date()
    cursor.execute("SELECT * FROM uyeler WHERE secilen_tarih = ?", (bugun,))
    rows = cursor.fetchall()
    kazanc = 0


    for row in rows:
        yumurta_tur = row[3]
        if yumurta_tur == "Standart":
            kazanc += 20 * 30
        elif yumurta_tur == "Çiftlik":
            kazanc += 45 * 30
        elif yumurta_tur == "Gezen":
            kazanc += 30 * 30
        elif yumurta_tur == "Jumbo":
            kazanc += 25 * 30
        elif yumurta_tur == "Mavi Yumurta":
            kazanc += 50 * 30
        elif yumurta_tur == "Çift Sarılı":
            kazanc += 35 * 30

    st.write("Günlük Kazanç ", kazanc)
    st.write("---")

    st.subheader("Aylık Kazanç")
    bugun = datetime.now().date()

    # Ayı al
    simdiki_ay = datetime.now().month

    # Teslimatları al
    cursor.execute("SELECT * FROM uyeler WHERE strftime('%m', secilen_tarih) = ? and strftime('%Y', secilen_tarih) = ?",
                   (str(simdiki_ay).zfill(2), str(bugun.year)))
    rows = cursor.fetchall()
    kazanc = 0


    for row in rows:
        yumurta_tur = row[3]
        abonelik=row[2]
        if yumurta_tur == "Standart":
            if abonelik=="Haftalık":
                 kazanc += (20 * 30)*4
            else:
                kazanc += 20 * 30
        elif yumurta_tur == "Çiftlik":
            if abonelik=="Haftalık":
                 kazanc += (45 * 30)*4
            else:
                kazanc += 45 * 30
        elif yumurta_tur == "Gezen":
            if abonelik=="Haftalık":
                 kazanc += (30 * 30)*4
            else:
                kazanc += 30 * 30
        elif yumurta_tur == "Jumbo":
            if abonelik=="Haftalık":
                 kazanc += (25 * 30)*4
            else:
                kazanc += 25 * 30
        elif yumurta_tur == "Mavi Yumurta":
            if abonelik=="Haftalık":
                 kazanc += (50 * 30)*4
            else:
                kazanc += 50 * 30
        elif yumurta_tur == "Çift Sarılı":
            if abonelik=="Haftalık":
                 kazanc += (35 * 30)*4
            else:
                kazanc += 35 * 30



    st.write("Aylık Kazanç ", kazanc)

    conn.close()









