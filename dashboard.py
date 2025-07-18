import streamlit as st
from gdrive_upload import upload_to_drive
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Dashboard Upload Dokumen", layout="centered")

st.title("📂 Dashboard Upload & Monitoring Dokumen")
st.markdown("Gunakan form di bawah untuk mengunggah file Excel, Word, atau PDF ke Google Drive.")

# === Form Upload ===
with st.form("upload_form"):
    name = st.text_input("Nama Pengunggah", max_chars=50)
    uploaded_file = st.file_uploader("Pilih file (.pdf, .docx, .xlsx)", type=["pdf", "docx", "xlsx"])
    submit = st.form_submit_button("Upload ke Google Drive")

if submit and name and uploaded_file:
    # Simpan sementara
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        # Upload ke Google Drive
        file_url = upload_to_drive(temp_path, uploaded_file.name)
        st.success(f"✅ Berhasil diupload: [Lihat File]({file_url})")

        # Log Upload
        new_entry = {
            "Nama Pengupload": name,
            "Nama File": uploaded_file.name,
            "Tanggal Upload": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Link Google Drive": file_url
        }

        log_file = "upload_log.csv"
        if os.path.exists(log_file):
            df_log = pd.read_csv(log_file)
            df_log = pd.concat([pd.DataFrame([new_entry]), df_log], ignore_index=True)
        else:
            df_log = pd.DataFrame([new_entry])

        df_log.to_csv(log_file, index=False)

        st.info("📋 Riwayat upload diperbarui.")

    except Exception as e:
        st.error(f"Gagal upload: {e}")
    finally:
        os.remove(temp_path)  # Hapus file sementara

# === Monitoring Table ===
st.subheader("📊 Riwayat Upload Semua Anggota")
if os.path.exists("upload_log.csv"):
    df_monitor = pd.read_csv("upload_log.csv")
    st.dataframe(df_monitor, use_container_width=True)
else:
    st.write("Belum ada file yang diupload.")
