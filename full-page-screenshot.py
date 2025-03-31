import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog,
                             QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = 'en'  # Default language is English
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Full Page Screenshot')
        self.setGeometry(100, 100, 600, 250)

        # Language selection dropdown
        self.language_selector = QComboBox()
        self.language_selector.addItems(["English", "Türkçe"])
        self.language_selector.currentIndexChanged.connect(self.update_language)

        # URL input
        self.url_label = QLabel('URL:')
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Enter website URL...')

        # Save location
        self.save_label = QLabel('Save Location:')
        self.save_input = QLineEdit()
        self.save_input.setPlaceholderText('Select file save location...')
        self.browse_btn = QPushButton('Browse...')
        self.browse_btn.clicked.connect(self.browse_save_location)

        # Capture button
        self.capture_btn = QPushButton('Capture Screenshot')
        self.capture_btn.clicked.connect(self.capture_screenshot)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.language_selector)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.save_label)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.save_input)
        h_layout.addWidget(self.browse_btn)

        layout.addLayout(h_layout)
        layout.addWidget(self.capture_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_language(self):
        """ Updates UI texts based on selected language """
        languages = {"English": "en", "Türkçe": "tr"}
        self.language = languages[self.language_selector.currentText()]
        self.refresh_texts()

    def refresh_texts(self):
        """ Refresh UI elements based on language selection """
        if self.language == 'en':
            self.setWindowTitle('Full Page Screenshot')
            self.url_label.setText('URL:')
            self.url_input.setPlaceholderText('Enter website URL...')
            self.save_label.setText('Save Location:')
            self.save_input.setPlaceholderText('Select file save location...')
            self.browse_btn.setText('Browse...')
            self.capture_btn.setText('Capture Screenshot')
        else:
            self.setWindowTitle('Tam Sayfa Ekran Görüntüsü')
            self.url_label.setText('URL:')
            self.url_input.setPlaceholderText('Web sitesi adresini girin...')
            self.save_label.setText('Kayıt Konumu:')
            self.save_input.setPlaceholderText('Dosya kayıt konumunu seçin...')
            self.browse_btn.setText('Gözat...')
            self.capture_btn.setText('Ekran Görüntüsü Al')

    def browse_save_location(self):
        """ Opens a file dialog to select the save location """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Save Location" if self.language == 'en' else "Kayıt Konumu Seç", "",
            "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)",
            options=options
        )
        if file_path:
            self.save_input.setText(file_path)

    def capture_screenshot(self):
        """ Captures a full-page screenshot of the given URL """
        url = self.url_input.text().strip()
        save_path = self.save_input.text().strip()

        if not url:
            QMessageBox.warning(self, 'Warning' if self.language == 'en' else 'Uyarı',
                                'Please enter a valid URL.' if self.language == 'en' else 'Lütfen geçerli bir URL girin.')
            return

        if not save_path:
            QMessageBox.warning(self, 'Warning' if self.language == 'en' else 'Uyarı',
                                'Please select a save location.' if self.language == 'en' else 'Lütfen kayıt konumu seçin.')
            return

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--start-maximized')

            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)

            total_width = driver.execute_script("return document.body.offsetWidth")
            total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
            driver.set_window_size(total_width, total_height)

            screenshot = driver.get_screenshot_as_png()
            with open(save_path, 'wb') as f:
                f.write(screenshot)

            driver.quit()

            QMessageBox.information(self, 'Success' if self.language == 'en' else 'Başarılı',
                                    f'Screenshot saved successfully:\n{save_path}' if self.language == 'en'
                                    else f'Ekran görüntüsü başarıyla kaydedildi:\n{save_path}')

        except Exception as e:
            QMessageBox.critical(self, 'Error' if self.language == 'en' else 'Hata',
                                 f'Error capturing screenshot:\n{str(e)}' if self.language == 'en'
                                 else f'Ekran görüntüsü alınırken hata oluştu:\n{str(e)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScreenshotApp()
    window.show()
    sys.exit(app.exec_())
