import os
import shutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QMessageBox, QProgressBar, QListWidget, QListWidgetItem, QComboBox
from PyQt5.QtGui import QIcon

class GTAVInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GTAV Otomatik Mod Yükleyici")
        self.setGeometry(100, 100, 600, 400)
        self.setWindowIcon(QIcon('icon.ico'))

        self.gtav_location_label = QLabel("GTAV Konumu: ")
        self.mod_folder_label = QLabel("Mod Klasörü: ")

        self.select_gtav_btn = QPushButton("GTAV Konumu Seç")
        self.select_gtav_btn.clicked.connect(self.select_gtav_location)

        self.select_mod_btn = QPushButton("Mod Klasörünü Seç")
        self.select_mod_btn.clicked.connect(self.select_mod_folder)

        self.install_btn = QPushButton("Modu Yükle")
        self.install_btn.clicked.connect(self.install_mod)

        self.remove_btn = QPushButton("Seçili Modu Kaldır")
        self.remove_btn.clicked.connect(self.remove_mod)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)

        self.mod_list_widget = QListWidget()

        self.language_label = QLabel("Dil Seçimi: ")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Türkçe", "English", "Deutsch", "Español", "Français", "Português", "中文"])  
        self.language_combo.currentTextChanged.connect(self.change_language)

        layout = QVBoxLayout()
        layout.addWidget(self.gtav_location_label)
        layout.addWidget(self.select_gtav_btn)
        layout.addWidget(self.mod_folder_label)
        layout.addWidget(self.select_mod_btn)
        layout.addWidget(self.mod_list_widget)
        layout.addWidget(self.install_btn)
        layout.addWidget(self.remove_btn)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)

        self.setLayout(layout)

        self.gtav_location = ""
        self.mod_folder_path = ""

    def change_language(self, selected_language):
        if selected_language == "English":
            self.setWindowTitle("GTAV Automatic Mod Installer")
            self.gtav_location_label.setText("GTAV Location: ")
            self.mod_folder_label.setText("Mod Folder: ")
            self.select_gtav_btn.setText("Select GTAV Location")
            self.select_mod_btn.setText("Select Mod Folder")
            self.install_btn.setText("Install Mod")
            self.remove_btn.setText("Remove Selected Mod")
            self.language_label.setText("Language: ")
        elif selected_language == "Türkçe":
            self.setWindowTitle("GTAV Otomatik Mod Yükleyici")
            self.gtav_location_label.setText("GTAV Konumu: ")
            self.mod_folder_label.setText("Mod Klasörü: ")
            self.select_gtav_btn.setText("GTAV Konumu Seç")
            self.select_mod_btn.setText("Mod Klasörünü Seç")
            self.install_btn.setText("Modu Yükle")
            self.remove_btn.setText("Seçili Modu Kaldır")
            self.language_label.setText("Dil Seçimi: ")
        elif selected_language == "Deutsch":
            self.setWindowTitle("GTAV Automatischer Mod Installer")
            self.mod_folder_label.setText("Mod-Ordner: ")
            self.select_mod_btn.setText("Mod-Ordner wählen")
            self.install_btn.setText("Mod installieren")
            self.remove_btn.setText("Ausgewählten Mod entfernen")
            self.language_label.setText("Sprache: ")
        elif selected_language == "Español":
            self.setWindowTitle("Instalador Automático de Mods para GTAV")
            self.mod_folder_label.setText("Carpeta de Mod: ")
            self.select_mod_btn.setText("Seleccionar Carpeta de Mod")
            self.install_btn.setText("Instalar Mod")
            self.remove_btn.setText("Eliminar Mod Seleccionado")
            self.language_label.setText("Idioma: ")
        elif selected_language == "Français":
            self.setWindowTitle("Installeur Automatique de Mods pour GTAV")
            self.mod_folder_label.setText("Dossier Mod: ")
            self.select_mod_btn.setText("Sélectionner le dossier Mod")
            self.install_btn.setText("Installer le Mod")
            self.remove_btn.setText("Supprimer le Mod sélectionné")
            self.language_label.setText("Langue: ")
        elif selected_language == "Português":
            self.setWindowTitle("Instalador Automático de Mods para GTAV")
            self.mod_folder_label.setText("Pasta do Mod: ")
            self.select_mod_btn.setText("Selecionar Pasta do Mod")
            self.install_btn.setText("Instalar Mod")
            self.remove_btn.setText("Remover Mod Selecionado")
            self.language_label.setText("Idioma: ")
        elif selected_language == "中文":
            self.setWindowTitle("GTAV 自动化 Mod 安装程序")
            self.mod_folder_label.setText("Mod 文件夹: ")
            self.select_mod_btn.setText("选择 Mod 文件夹")
            self.install_btn.setText("安装 Mod")
            self.remove_btn.setText("移除所选 Mod")
            self.language_label.setText("语言: ")

    def select_gtav_location(self):
        gtav_location = QFileDialog.getExistingDirectory(self, "GTAV Konumu Seç")
        if gtav_location:
            self.gtav_location = gtav_location
            self.gtav_location_label.setText(f"<b>GTAV Konumu:</b> {self.gtav_location}")

    def select_mod_folder(self):
        mod_folder_path = QFileDialog.getExistingDirectory(self, "Mod Klasörünü Seç")
        if mod_folder_path and os.path.exists(os.path.join(mod_folder_path, "dlc.rpf")):
            self.mod_folder_path = mod_folder_path
            self.mod_folder_label.setText(f"<b>Mod Klasörü:</b> {self.mod_folder_path}")
        else:
            QMessageBox.warning(self, "Uyarı", "Geçerli bir mod klasörü seçilmedi veya dlc.rpf dosyası bulunamadı.")

    def find_mods_in_folder(self, folder_path):
        mods = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith("dlc.rpf"):
                    mods.append(os.path.basename(root))
        return mods

    def populate_mod_list(self):
        if not self.gtav_location:
            QMessageBox.warning(self, "Uyarı", "GTAV konumu seçilmedi.")
            return

        dlcpacks_path = os.path.join(self.gtav_location, "mods", "update", "x64", "dlcpacks")
        if not os.path.exists(dlcpacks_path):
            QMessageBox.warning(self, "Uyarı", "dlcpacks klasörü bulunamadı.")
            return

        mods = self.find_mods_in_folder(dlcpacks_path)
        if not mods:
            QMessageBox.warning(self, "Uyarı", "Mod bulunamadı.")
            return

        self.mod_list_widget.addItems(mods)

    def install_mod(self):
        if not self.gtav_location or not self.mod_folder_path:
            QMessageBox.warning(self, "Uyarı", "GTAV konumu ve mod klasörü seçilmelidir!")
            return

        destination_path = os.path.join(self.gtav_location, "mods", "update", "x64", "dlcpacks", os.path.basename(self.mod_folder_path))
        try:
            shutil.copytree(self.mod_folder_path, destination_path)
            QMessageBox.information(self, "Başarılı", "Mod başarıyla yüklendi.")
            self.progress_bar.setValue(100)
            self.write_to_log("Mod başarıyla yüklendi.")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Mod yüklenirken bir hata oluştu: {str(e)}")
            self.write_to_log(f"Hata: {str(e)}")

    def remove_mod(self):
        selected_items = self.mod_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Kaldırılacak bir mod seçilmedi.")
            return

        for item in selected_items:
            self.mod_list_widget.takeItem(self.mod_list_widget.row(item))
            QMessageBox.information(self, "Başarılı", f"{item.text()} başarıyla kaldırıldı.")

    def write_to_log(self, message):
        with open("log.txt", "a") as f:
            f.write(message + "\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    installer = GTAVInstaller()
    installer.show()
    sys.exit(app.exec_())
