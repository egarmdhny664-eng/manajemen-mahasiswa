import streamlit as st
import pandas as pd

# --- 1. INISIALISASI SESSION STATE ---
# Untuk mengecek status login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Untuk menyimpan banyak data mahasiswa
if "data_mahasiswa" not in st.session_state:
    st.session_state.data_mahasiswa = []


# --- 2. FUNGSI HALAMAN LOGIN ---
def halaman_login():
    st.markdown("<h2 style='text-align: center;'>🔐 Login Sistem Manajemen</h2>", unsafe_allow_html=True)
    
    # Membuat form login agar rapi
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        tombol_login = st.form_submit_button("Masuk")
        
        if tombol_login:
            # Kamu bisa ubah username & password sesuai keinginanmu di sini
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.success("Login Berhasil!")
                st.rerun()  # Refresh halaman untuk masuk ke menu utama
            else:
                st.error("Username atau Password salah. Silakan coba lagi!")


# --- 3. FUNGSI HALAMAN UTAMA (MANAJEMEN DATA) ---
def halaman_utama():
    # Tombol Logout ditaruh di Sidebar agar rapi
    st.sidebar.title("Navigasi")
    if st.sidebar.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.rerun()

    # Judul Aplikasi Utama
    st.title("🎓 Aplikasi Manajemen Data Mahasiswa")
    st.write("---")

    # Form Input Data Mahasiswa
    # `clear_on_submit=True` membuat form otomatis kosong setelah klik 'Simpan'
    with st.form("form_mahasiswa", clear_on_submit=True):
        st.write("### Input Data Baru")
        nim = st.text_input("NIM")
        nama = st.text_input("Nama")
        prodi = st.text_input("Program Studi")
        ipk = st.number_input("IPK", min_value=0.0, max_value=4.0, value=3.0, step=0.01)
        
        simpan_button = st.form_submit_button("Simpan Data")
        
        if simpan_button:
            if nim and nama and prodi:
                # Membuat dictionary data baru
                mahasiswa_baru = {
                    "NIM": nim,
                    "Nama": nama,
                    "Program Studi": prodi,
                    "IPK": ipk
                }
                # Memasukkan data baru ke dalam list session_state
                st.session_state.data_mahasiswa.append(mahasiswa_baru)
                st.success(f"Data mahasiswa atas nama **{nama}** berhasil ditambahkan!")
            else:
                st.error("Gagal menyimpan! Mohon isi semua kolom (NIM, Nama, dan Prodi).")

    st.write("---")

    # --- 4. MENAMPILKAN BANYAK DATA (TABEL) ---
    st.write("### 📊 Daftar Mahasiswa Terdaftar")
    
    if st.session_state.data_mahasiswa:
        # Mengubah list data menjadi Pandas DataFrame agar rapi berbentuk tabel
        df = pd.DataFrame(st.session_state.data_mahasiswa)
        
        # Menampilkan tabel interaktif di Streamlit
        st.dataframe(df, use_container_width=True)
        
        # Fitur tambahan: Menghitung total mahasiswa saat ini
        st.metric(label="Total Mahasiswa", value=len(df))
    else:
        st.info("Belum ada data mahasiswa yang dimasukkan.")


# --- 5. LOGIKA KONTROL HALAMAN ---
if not st.session_state.logged_in:
    halaman_login()
else:
    halaman_utama()