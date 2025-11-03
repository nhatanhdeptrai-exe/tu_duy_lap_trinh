import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from giaodiennew import Ui_MainWindow
import xulymonan4 as xuly
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Hệ thống gợi ý món ăn")
        self.ui.tablemonan.verticalHeader().setVisible(False)
        self.ui.pushtinh.clicked.connect(self.thuc_hien_tim_kiem)
        self.ui.hiennlchinh.setText("Nguyên liệu đã nhận diện:")

    def thuc_hien_tim_kiem(self):
        input_nguyen_lieu_chung = self.ui.nguyenlieuchinh.text()
        (str_hien_thi_chung, danh_sach_goi_y, tat_ca_khong_biet, cac_tu_BIET_raw) = xuly.tim_kiem_mon_an(input_nguyen_lieu_chung)
        if tat_ca_khong_biet:
            QMessageBox.warning(self,
                                "Không nhận diện được",
                                "Xin lỗi vì hiện tại hệ thống chưa có dữ liệu về nguyên liệu của bạn.\n"
                                "Chúng tôi đã lưu lại những nguyên liệu này và sẽ bổ sung trong tương lai.")

            chuoi_da_loc = ", ".join(cac_tu_BIET_raw)
            self.ui.nguyenlieuchinh.setText(chuoi_da_loc)
            self.ui.nguyenlieuchinh.setFocus()
        self.ui.hiennlchinh.setText(f"Nguyên liệu đã nhận diện: {str_hien_thi_chung}")
        self.ui.hiennlchinh.setStyleSheet("color: black;")  # Ép màu đen
        self.ui.tablemonan.setRowCount(0)
        for row_index, mon_an in enumerate(danh_sach_goi_y):
            self.ui.tablemonan.insertRow(row_index)
            self.ui.tablemonan.setItem(row_index, 0, QTableWidgetItem(mon_an["ten"]))
            self.ui.tablemonan.setItem(row_index, 1, QTableWidgetItem(mon_an["chinh"]))
            self.ui.tablemonan.setItem(row_index, 2, QTableWidgetItem(mon_an["phu"]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
