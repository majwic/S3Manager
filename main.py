import sys
import controller as controller
from Widgets.S3FileManager import S3FileManagerWidget
from Widgets.S3BucketManager import S3BucketManagerWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QMainWindow
from qt_material import apply_stylesheet # type: ignore

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('S3 Utility')
        self.setGeometry(100, 100, 1000, 500)

        main_layout = QHBoxLayout()

        # Create and add widgets
        s3_bucket_manager_widget = S3BucketManagerWidget()
        s3_file_manager_widget = S3FileManagerWidget()

        controller.connect_handlers(s3_bucket_manager_widget)

        main_layout.addWidget(s3_bucket_manager_widget)
        main_layout.addWidget(s3_file_manager_widget)

        # Central widget containing the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme='dark_pink.xml')
    window.show()
    sys.exit(app.exec_())
