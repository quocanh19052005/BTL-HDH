#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os, shutil, sys
from datetime import datetime, date, timedelta

from PyQt5 import QtWidgets, QtCore, QtGui


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "todos.json")
DT_FMT = "%Y-%m-%d %H:%M"
D_FMT  = "%Y-%m-%d"
WEEKDAY_VN = ["Th 2","Th 3","Th 4","Th 5","Th 6","Th 7","CN"]
QT_D_FMT = "yyyy-MM-dd"
QT_DT_FMT = "yyyy-MM-dd HH:mm"

APP_STYLESHEET = """
/* todo-theme */
QMainWindow { background-color: #f4f6fb; }
QTabWidget::pane { border: 0px; }
QTabBar::tab {
    padding: 10px 20px;
    border-radius: 10px;
    margin: 6px 4px;
    color: #4d5a73;
    background: #e6ebfa;
    font-weight: 600;
}
QTabBar::tab:selected {
    background: #4c6ef5;
    color: white;
}
QFrame#card {
    background: #ffffff;
    border: 1px solid #dfe4f5;
    border-radius: 16px;
}
QLabel#cardTitle {
    font-size: 20px;
    font-weight: 600;
    color: #1f2d3d;
}
QLabel#cardSubtitle {
    color: #647094;
    font-size: 13px;
}
QLabel#cardSubtitle[done="true"] {
    color: #9aa3b9;
}
QLabel#statsLabel {
    font-size: 16px;
    font-weight: 600;
    color: #4c6ef5;
}
QLabel#placeholder {
    color: #8f96a6;
    font-size: 15px;
}
QPushButton, QToolButton {
    background-color: #4c6ef5;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
}
QPushButton:hover, QToolButton:hover {
    background-color: #3b5bdb;
}
QPushButton:disabled, QToolButton:disabled {
    background-color: #ccd4ff;
    color: #f8f9ff;
}
QPushButton[secondary="true"], QToolButton[secondary="true"] {
    background-color: #ecf0ff;
    color: #4c6ef5;
}
QPushButton[secondary="true"]:hover, QToolButton[secondary="true"]:hover {
    background-color: #dee4ff;
}
QPushButton[danger="true"] {
    background-color: #fa5252;
    color: #ffffff;
}
QPushButton[danger="true"]:hover {
    background-color: #f03e3e;
}
QComboBox, QDateEdit, QLineEdit {
    border: 1px solid #d2d8ea;
    border-radius: 10px;
    padding: 6px 10px;
    background-color: #ffffff;
}
QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border-color: #4c6ef5;
}
QListWidget#taskList {
    border: none;
    background-color: transparent;
}
QListWidget#taskList::item {
    margin: 6px 10px;
    border-radius: 12px;
    padding: 12px 14px;
}
QListWidget#taskList::item:selected {
    background-color: rgba(76, 110, 245, 0.16);
    color: #1f2d3d;
}
QTableWidget {
    border: none;
    background-color: transparent;
    gridline-color: #e1e7fb;
}
QHeaderView::section {
    background-color: #f0f3ff;
    border: none;
    padding: 9px;
    font-weight: 600;
    color: #4d5a73;
}
QScrollBar:vertical, QScrollBar:horizontal {
    background: transparent;
    width: 12px;
    margin: 0px;
}
QScrollBar::handle {
    background: rgba(76, 110, 245, 0.35);
    border-radius: 6px;
}
QScrollBar::handle:hover {
    background: rgba(76, 110, 245, 0.5);
}
QFrame#taskCard {
    background: #f9faff;
    border: 2px solid transparent;
    border-radius: 16px;
    padding: 14px 16px;
}
QFrame#taskCard[selected="true"] {
    border-color: #4c6ef5;
    box-shadow: 0 6px 18px rgba(76, 110, 245, 0.18);
}
QFrame#taskCard[done="true"] {
    background: #eef2ff;
}
QLabel#taskTitle {
    font-size: 15px;
    font-weight: 600;
    color: #1f2d3d;
}
QLabel#taskTitle[done="true"] {
    color: #7a839b;
    text-decoration: line-through;
}
QLabel#badge {
    font-size: 24px;
    min-width: 36px;
    color: #4c6ef5;
}
QLabel#badge[done="true"] {
    color: #2b8a3e;
}
QLabel#badge[overdue="true"] {
    color: #e03131;
}
QLabel#chip {
    border-radius: 999px;
    padding: 4px 14px;
    font-weight: 600;
    font-size: 12px;
    background: #e7ecff;
    color: #42527a;
}
QLabel#chip[compact="true"] {
    padding: 3px 10px;
    font-weight: 500;
}
QLabel#chip[variant="status-done"] {
    background: #d3f9d8;
    color: #2b8a3e;
}
QLabel#chip[variant="status-todo"] {
    background: #fff3bf;
    color: #d9480f;
}
QLabel#chip[variant="priority-high"] {
    background: #ffe3e3;
    color: #e03131;
}
QLabel#chip[variant="priority-normal"] {
    background: #dee2ff;
    color: #3b5bdb;
}
QLabel#chip[variant="priority-low"] {
    background: #e6fcf5;
    color: #0ca678;
}
QLabel#chip[variant="due"] {
    background: #dbe4ff;
    color: #3b5bdb;
}
QLabel#chip[variant="overdue"] {
    background: #ffe3e3;
    color: #c92a2a;
}
QProgressBar {
    background: #e7ecff;
    border-radius: 999px;
    border: 1px solid transparent;
    color: #1f2d3d;
    text-align: center;
    padding: 2px;
}
QProgressBar::chunk {
    border-radius: 999px;
    background: #4c6ef5;
}
"""

def now_iso():
    return datetime.now().isoformat(timespec="seconds")


def start_of_week(d: date) -> date:
    return d - timedelta(days=d.weekday())


def end_of_week(d: date) -> date:
    return start_of_week(d) + timedelta(days=6)


def parse_dt(s):
    try:
        return datetime.strptime(s, DT_FMT) if s else None
    except Exception:
        return None


def qdatetime_from_str(s):
    if not s:
        return QtCore.QDateTime.currentDateTime()

    qdt = QtCore.QDateTime.fromString(s, QT_DT_FMT)
    if qdt.isValid():
        return qdt

    dt = parse_dt(s)
    if not dt:
        return QtCore.QDateTime.currentDateTime()

    return QtCore.QDateTime(
        QtCore.QDate(dt.year, dt.month, dt.day),
        QtCore.QTime(dt.hour, dt.minute, dt.second)
    )


def format_qdatetime(dt: QtCore.QDateTime) -> str:
    if not dt or not dt.isValid():
        return ""
    return dt.toString(QT_DT_FMT)


class Store:
    def __init__(self, path):
        self.path = path
        self.items = []

    def migrate(self, it):
        it = dict(it) if isinstance(it, dict) else {"text": str(it)}
        it.setdefault("text", "")
        it.setdefault("done", False)
        it.setdefault("priority", 1)          # 0 thấp, 1 thường, 2 cao
        if "due_dt" not in it:
            due = it.get("due")               # nâng cấp từ bản cũ
            it["due_dt"] = f"{due} 23:59" if due else None
        it.pop("due", None)
        it.setdefault("created_at", now_iso())
        it.setdefault("done_at", None)
        it.setdefault("note", None)
        it.setdefault("notified", False)
        return it

    def load(self):
        if not os.path.exists(self.path):
            self.items = []
            return

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.items = [self.migrate(x) for x in (raw if isinstance(raw, list) else [])]
        except Exception as e:
            self.items = []
            QtWidgets.QMessageBox.warning(None, "Lỗi đọc dữ liệu",
                                          f"Không thể đọc tệp {os.path.basename(self.path)}:\n{e}")

    def save(self):
        try:
            if os.path.exists(self.path):
                shutil.copyfile(self.path, self.path + ".bak")
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.items, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Lỗi lưu", str(e))


class TaskDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, *, title="Thêm công việc", task=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(420)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        title_lbl = QtWidgets.QLabel("Chi tiết công việc")
        title_lbl.setObjectName("cardTitle")
        layout.addWidget(title_lbl)

        form = QtWidgets.QFormLayout()
        form.setSpacing(12)
        layout.addLayout(form)

        self.text_edit = QtWidgets.QLineEdit()
        self.text_edit.setPlaceholderText("Nội dung công việc")
        form.addRow("Tiêu đề", self.text_edit)

        self.priority_combo = QtWidgets.QComboBox()
        self.priority_combo.addItem("Thấp", 0)
        self.priority_combo.addItem("Thường", 1)
        self.priority_combo.addItem("Cao", 2)
        form.addRow("Ưu tiên", self.priority_combo)

        due_row = QtWidgets.QHBoxLayout()
        due_row.setSpacing(8)
        self.due_checkbox = QtWidgets.QCheckBox("Đặt hạn chót")
        self.due_checkbox.toggled.connect(self._sync_due_state)
        due_row.addWidget(self.due_checkbox)
        due_row.addStretch()
        form.addRow("", due_row)

        self.due_edit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.due_edit.setDisplayFormat(QT_DT_FMT)
        self.due_edit.setCalendarPopup(True)
        self.due_edit.setEnabled(False)
        form.addRow("Hạn chót", self.due_edit)

        self.note_edit = QtWidgets.QPlainTextEdit()
        self.note_edit.setPlaceholderText("Ghi chú (tuỳ chọn)")
        self.note_edit.setFixedHeight(80)
        form.addRow("Ghi chú", self.note_edit)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        self.button_box.accepted.connect(self._accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        if task:
            self.text_edit.setText(task.get("text", ""))
            target_idx = self.priority_combo.findData(int(task.get("priority", 1)))
            if target_idx != -1:
                self.priority_combo.setCurrentIndex(target_idx)
            due = task.get("due_dt")
            if due:
                self.due_checkbox.setChecked(True)
                self.due_edit.setDateTime(qdatetime_from_str(due))
            note = task.get("note")
            if note:
                self.note_edit.setPlainText(note)

        self._sync_due_state()

    def _sync_due_state(self):
        self.due_edit.setEnabled(self.due_checkbox.isChecked())

    def _accept(self):
        text = self.text_edit.text().strip()
        if not text:
            QtWidgets.QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập nội dung công việc.")
            return
        self.accept()

    def get_data(self):
        text = self.text_edit.text().strip()
        priority = int(self.priority_combo.currentData())
        due = None
        if self.due_checkbox.isChecked():
            due_str = format_qdatetime(self.due_edit.dateTime())
            due = due_str or None
        note = self.note_edit.toPlainText().strip() or None
        return {"text": text, "priority": priority, "due_dt": due, "note": note}


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo List")
        self.resize(1040, 660)

        self._apply_theme()

        self.store = Store(DATA_FILE)
        self.store.load()
        self._undo = None
        
        # === DÒNG MỚI ĐƯỢC THÊM VÀO ĐÂY ===
        self.app_notifications = [] 
        # =================================

        tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(tabs)

        # ==== Tab 1: Danh sách ====
        self.tab_list = QtWidgets.QWidget()
        tabs.addTab(self.tab_list, "Danh sách")
        self._build_tab_list()

        # ==== Tab 2: Trong ngày ====
        self.tab_day = QtWidgets.QWidget()
        tabs.addTab(self.tab_day, "Trong ngày")
        self._build_tab_day()

        # ==== Tab 3: Trong tuần ====
        self.tab_week = QtWidgets.QWidget()
        tabs.addTab(self.tab_week, "Trong tuần")
        self._build_tab_week()

        self.refresh_all()

        # === KHỐI CODE THÔNG BÁO HỆ THỐNG CỦA BẠN ===
        # 1. Thiết lập System Tray Icon
        self.tray_icon = None
        if QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QtWidgets.QSystemTrayIcon(self)
            # Dùng 1 icon tiêu chuẩn của Qt, bạn có thể thay bằng file .ico
            icon = self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation)
            self.tray_icon.setIcon(icon)
            self.tray_icon.setToolTip("Todo List")
            self.tray_icon.show()
        
        # 2. Thiết lập Timer để kiểm tra công việc
        self.check_timer = QtCore.QTimer(self)
        self.check_timer.timeout.connect(self.check_due_tasks)
        self.check_timer.start(60000) # Kiểm tra mỗi 60,000 ms (1 phút)
        
        # 3. Kiểm tra ngay khi khởi động 1 lần
        self.check_due_tasks() 
        # ==========================================

    # ---------------- Styling helpers ----------------
    def _apply_theme(self):
        app = QtWidgets.QApplication.instance()
        if app:
            current = app.styleSheet() or ""
            if "todo-theme" not in current:
                app.setStyleSheet(current + APP_STYLESHEET)

    def _create_card(self):
        card = QtWidgets.QFrame()
        card.setObjectName("card")
        card.setFrameShape(QtWidgets.QFrame.NoFrame)
        card.setFrameShadow(QtWidgets.QFrame.Plain)
        return card

    def _make_chip(self, text, variant, *, compact=False):
        lbl = QtWidgets.QLabel(text)
        lbl.setObjectName("chip")
        lbl.setProperty("variant", variant)
        lbl.setProperty("compact", compact)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.setMargin(0)
        return lbl

    def _refresh_widget_style(self, widget):
        if not widget:
            return
        style = widget.style()
        if style:
            style.unpolish(widget)
            style.polish(widget)
        for child in widget.findChildren(QtWidgets.QWidget):
            c_style = child.style()
            if c_style:
                c_style.unpolish(child)
                c_style.polish(child)

    def _make_task_widget(self, it, *, dt=None, overdue=False):
        card = QtWidgets.QFrame()
        card.setObjectName("taskCard")
        card.setProperty("done", it.get("done", False))
        card.setProperty("selected", False)

        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        badge = QtWidgets.QLabel("✔" if it.get("done") else "⏳")
        badge.setObjectName("badge")
        badge.setProperty("done", it.get("done"))
        badge.setProperty("overdue", overdue)
        layout.addWidget(badge, 0, QtCore.Qt.AlignTop)

        body = QtWidgets.QVBoxLayout()
        body.setSpacing(8)
        body.setContentsMargins(0, 0, 0, 0)

        title = QtWidgets.QLabel(it.get("text", ""))
        title.setObjectName("taskTitle")
        title.setProperty("done", it.get("done"))
        title.setWordWrap(True)
        body.addWidget(title)

        chips = QtWidgets.QHBoxLayout()
        chips.setSpacing(8)

        priority = int(it.get("priority", 1))
        pr_variant = {2: "priority-high", 1: "priority-normal", 0: "priority-low"}.get(priority, "priority-normal")
        pr_text = {2: "Ưu tiên cao", 1: "Ưu tiên thường", 0: "Ưu tiên thấp"}.get(priority, "Ưu tiên")
        chips.addWidget(self._make_chip(pr_text, pr_variant, compact=True))

        status_variant = "status-done" if it.get("done") else "status-todo"
        status_text = "Đã hoàn thành" if it.get("done") else "Đang thực hiện"
        chips.addWidget(self._make_chip(status_text, status_variant, compact=True))

        if dt:
            # === SỬA DÒNG NÀY ===
            due_variant = "overdue" if overdue else "due"
            # ===================
            due_label = dt.strftime("Hạn: %d/%m %H:%M")
            chips.addWidget(self._make_chip(due_label, due_variant, compact=True))
        elif it.get("due_dt"):
            chips.addWidget(self._make_chip(f"Hạn: {it['due_dt']}", "due", compact=True))

        created = it.get("created_at")
        if created:
            created_date = created.split('T')[0] if 'T' in created else created
            chips.addWidget(self._make_chip(f"Tạo: {created_date}", "priority-normal", compact=True))

        chips.addStretch()
        body.addLayout(chips)

        note = it.get("note")
        if note:
            note_lbl = QtWidgets.QLabel(note)
            note_lbl.setObjectName("cardSubtitle")
            note_lbl.setWordWrap(True)
            note_lbl.setProperty("done", it.get("done"))
            body.addWidget(note_lbl)

        layout.addLayout(body, 1)

        self._refresh_widget_style(card)
        return card

    def _sync_task_selection(self):
        for i in range(self.list.count()):
            item = self.list.item(i)
            widget = self.list.itemWidget(item)
            if widget:
                widget.setProperty("selected", item.isSelected())
                self._refresh_widget_style(widget)

    def _update_statistics(self):
        total = len(self.store.items)
        done = sum(1 for x in self.store.items if x.get("done"))
        todo = total - done
        pct = int(done * 100 / total) if total else 0

        # === LOGIC MỚI ĐỂ ĐẾM QUÁ HẠN ===
        now = datetime.now()
        overdue_count = 0
        for it in self.store.items:
            # Chỉ đếm việc "chưa xong"
            if it.get("done"):
                continue
            
            dt = parse_dt(it.get("due_dt"))
            # Nếu có hạn chót VÀ hạn chót đã trôi qua
            if bool(dt and dt < now):
                overdue_count += 1
        # ==================================

        if hasattr(self, "stats_label"):
            self.stats_label.setText(f"{done}/{total} việc đã hoàn thành ({pct}%)" if total else "Chưa có việc nào")
        if hasattr(self, "header_progress"):
            self.header_progress.setMaximum(total if total else 1)
            self.header_progress.setValue(done)
            self.header_progress.setFormat(f"{pct}% hoàn thành" if total else "Chưa có công việc")
        
        if hasattr(self, "stat_total_chip"):
            self.stat_total_chip.setText(f"Tổng: {total}")
        if hasattr(self, "stat_todo_chip"):
            self.stat_todo_chip.setText(f"Đang làm: {todo}")
        if hasattr(self, "stat_done_chip"):
            self.stat_done_chip.setText(f"Hoàn thành: {done}")

        # === CẬP NHẬT CHO CHIP MỚI ===
        if hasattr(self, "stat_overdue_chip"):
            self.stat_overdue_chip.setText(f"Quá hạn: {overdue_count}")
            # Tự động ẩn nhãn đi nếu không có việc nào quá hạn
            self.stat_overdue_chip.setVisible(overdue_count > 0)
            self._refresh_widget_style(self.stat_overdue_chip)
        # ============================

        if hasattr(self, "stats_label"):
            # update window title as well
            self.setWindowTitle(f"Todo List — {done}/{total} ({pct}%)")

    # ---------------- Tab 1 ----------------
    def _build_tab_list(self):
        L = QtWidgets.QVBoxLayout(self.tab_list)
        L.setContentsMargins(24, 24, 24, 24)
        L.setSpacing(18)

        # Header card
        header_card = self._create_card()
        header_layout = QtWidgets.QHBoxLayout(header_card)
        header_layout.setContentsMargins(24, 20, 24, 20)
        header_layout.setSpacing(12)
        info_box = QtWidgets.QVBoxLayout()
        title = QtWidgets.QLabel("Quản lý công việc")
        title.setObjectName("cardTitle")
        subtitle = QtWidgets.QLabel("Sắp xếp mọi đầu việc mỗi ngày với giao diện trực quan.")
        subtitle.setObjectName("cardSubtitle")
        info_box.addWidget(title)
        info_box.addWidget(subtitle)
        info_box.addStretch()
        header_layout.addLayout(info_box)
        header_layout.addStretch()

        # === KHỐI CODE NÚT CHUÔNG MỚI ===
        # (Bạn đã thêm phần này đúng rồi)
        bell_layout = QtWidgets.QHBoxLayout()
        bell_layout.setSpacing(4)
        bell_layout.setContentsMargins(0, 0, 0, 0)

        self.bell_button = QtWidgets.QToolButton()
        self.bell_button.setText("🔔") # Biểu tượng chuông
        self.bell_button.setProperty("secondary", True) # Dùng style nút phụ
        self.bell_button.setToolTip("Thông báo")
        self.bell_button.clicked.connect(self.show_app_notifications) # Kết nối
        bell_layout.addWidget(self.bell_button)

        self.bell_counter = QtWidgets.QLabel("0")
        self.bell_counter.setObjectName("chip") # Tái sử dụng style của chip
        self.bell_counter.setProperty("variant", "priority-high") # Cho nó màu đỏ
        self.bell_counter.setToolTip("Số thông báo mới")
        self.bell_counter.setVisible(False) # Ẩn đi lúc đầu
        bell_layout.addWidget(self.bell_counter)
        
        header_layout.addLayout(bell_layout)
        header_layout.addSpacing(20) # Thêm khoảng cách với sidebar
        # ================================

        sidebar = QtWidgets.QVBoxLayout()
        sidebar.setSpacing(8)
        self.header_progress = QtWidgets.QProgressBar()
        self.header_progress.setFixedWidth(240)
        self.header_progress.setTextVisible(True)
        self.header_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.header_progress.setRange(0, 1)
        self.header_progress.setValue(0)
        self.header_progress.setFormat("Chưa có công việc")
        sidebar.addWidget(self.header_progress)
        self.stats_label = QtWidgets.QLabel("Chưa có việc")
        self.stats_label.setObjectName("statsLabel")
        self.stats_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        sidebar.addWidget(self.stats_label)
        header_layout.addLayout(sidebar)
        L.addWidget(header_card)

        # Input card
        input_card = self._create_card()
        form = QtWidgets.QGridLayout(input_card)
        # ... (code input card giữ nguyên) ...
        form.setContentsMargins(24, 20, 24, 20)
        form.setHorizontalSpacing(16)
        form.setVerticalSpacing(12)
        lbl = QtWidgets.QLabel("Công việc mới")
        lbl.setObjectName("cardSubtitle")
        form.addWidget(lbl, 0, 0, 1, 2)

        self.inp = QtWidgets.QLineEdit()
        self.inp.setPlaceholderText("Nhập nội dung công việc...")
        self.inp.setMinimumHeight(36)
        self.inp.returnPressed.connect(self.add_item)
        form.addWidget(self.inp, 1, 0, 1, 2)

        pr_lbl = QtWidgets.QLabel("Ưu tiên")
        pr_lbl.setObjectName("cardSubtitle")
        form.addWidget(pr_lbl, 0, 2)
        self.prio = QtWidgets.QComboBox()
        self.prio.addItem("Thấp", 0)
        self.prio.addItem("Thường", 1)
        self.prio.addItem("Cao", 2)
        self.prio.setCurrentIndex(1)
        self.prio.setMinimumWidth(140)
        form.addWidget(self.prio, 1, 2)

        btnAdd = QtWidgets.QPushButton("Thêm công việc")
        btnAdd.clicked.connect(self.add_item)
        form.addWidget(btnAdd, 1, 3)
        form.setColumnStretch(0, 3)
        form.setColumnStretch(1, 0)
        form.setColumnStretch(2, 1)
        form.setColumnStretch(3, 0)
        L.addWidget(input_card)


        # Filter card
        filter_card = self._create_card()
        filter_layout = QtWidgets.QGridLayout(filter_card)
        # ... (code filter card giữ nguyên) ...
        filter_layout.setContentsMargins(24, 20, 24, 20)
        filter_layout.setHorizontalSpacing(18)
        filter_layout.setVerticalSpacing(14)

        lbl_search = QtWidgets.QLabel("Tìm kiếm")
        lbl_search.setObjectName("cardSubtitle")
        filter_layout.addWidget(lbl_search, 0, 0)
        self.q = QtWidgets.QLineEdit()
        self.q.setPlaceholderText("Nhập từ khoá...")
        self.q.setClearButtonEnabled(True)
        self.q.textChanged.connect(self.refresh_all)
        filter_layout.addWidget(self.q, 1, 0)

        lbl_sort = QtWidgets.QLabel("Sắp xếp")
        lbl_sort.setObjectName("cardSubtitle")
        filter_layout.addWidget(lbl_sort, 0, 1)
        self.sort = QtWidgets.QComboBox()
        self.sort.addItem("Mặc định", "default")
        self.sort.addItem("Hạn chót", "due_dt")
        self.sort.addItem("Ưu tiên", "priority")
        self.sort.addItem("Ngày tạo", "created_at")
        self.sort.currentIndexChanged.connect(self.refresh_all)
        filter_layout.addWidget(self.sort, 1, 1)

        lbl_range = QtWidgets.QLabel("Phạm vi")
        lbl_range.setObjectName("cardSubtitle")
        filter_layout.addWidget(lbl_range, 0, 2)
        self.range = QtWidgets.QComboBox()
        self.range.addItem("Tất cả", "all")
        self.range.addItem("Hôm nay", "today")
        self.range.addItem("Trong tuần", "week")
        self.range.currentIndexChanged.connect(self.refresh_all)
        filter_layout.addWidget(self.range, 1, 2)

        status_lbl = QtWidgets.QLabel("Trạng thái")
        status_lbl.setObjectName("cardSubtitle")
        filter_layout.addWidget(status_lbl, 0, 3)
        radio_row = QtWidgets.QHBoxLayout()
        radio_row.setSpacing(12)
        self.filter = QtWidgets.QButtonGroup(self)
        rbAll = QtWidgets.QRadioButton("Tất cả")
        rbTodo = QtWidgets.QRadioButton("Chưa xong")
        rbDone = QtWidgets.QRadioButton("Đã xong")
        rbAll.setChecked(True)
        for i, rb in enumerate([rbAll, rbTodo, rbDone]):
            rb.toggled.connect(self.refresh_all)
            self.filter.addButton(rb, i)
            radio_row.addWidget(rb)
        radio_row.addStretch()
        filter_layout.addLayout(radio_row, 1, 3)
        filter_layout.setColumnStretch(0, 1)
        filter_layout.setColumnStretch(1, 1)
        filter_layout.setColumnStretch(2, 1)
        filter_layout.setColumnStretch(3, 2)
        L.addWidget(filter_card)


        # List card
        list_card = self._create_card()
        list_layout = QtWidgets.QVBoxLayout(list_card)
        list_layout.setContentsMargins(16, 16, 16, 16)
        list_layout.setSpacing(14)

        list_title = QtWidgets.QLabel("Danh sách công việc")
        list_title.setObjectName("cardTitle")
        list_layout.addWidget(list_title)

        # === KHỐI CODE NÀY ĐÃ ĐƯỢC SỬA ===
        chips_row = QtWidgets.QHBoxLayout()
        chips_row.setSpacing(12)
        
        self.stat_total_chip = self._make_chip("Tổng: 0", "priority-normal")
        self.stat_todo_chip = self._make_chip("Đang làm: 0", "status-todo")
        self.stat_done_chip = self._make_chip("Hoàn thành: 0", "status-done")
        
        # Dòng mới được thêm vào
        self.stat_overdue_chip = self._make_chip("Quá hạn: 0", "priority-high") 
        
        chips_row.addWidget(self.stat_total_chip)
        chips_row.addWidget(self.stat_todo_chip)
        chips_row.addWidget(self.stat_done_chip)
        chips_row.addWidget(self.stat_overdue_chip) # Thêm chip mới vào layout
        
        chips_row.addStretch()
        list_layout.addLayout(chips_row)
        # =================================

        self.list = QtWidgets.QListWidget()
        self.list.setObjectName("taskList")
        # ... (code list widget giữ nguyên) ...
        self.list.setAlternatingRowColors(False)
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list.setSpacing(10)
        self.list.setWordWrap(True)
        self.list.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.list.setUniformItemSizes(False)
        self.list.itemSelectionChanged.connect(self._sync_task_selection)
        self.list.itemDoubleClicked.connect(lambda *_: self.edit_item())


        self.list_stack = QtWidgets.QStackedLayout()
        self.list_stack.addWidget(self.list)
        # ... (code list stack giữ nguyên) ...
        self.list_placeholder = QtWidgets.QLabel("Chưa có công việc nào. Hãy thêm việc mới để bắt đầu!")
        self.list_placeholder.setObjectName("placeholder")
        self.list_placeholder.setAlignment(QtCore.Qt.AlignCenter)
        self.list_placeholder.setWordWrap(True)
        placeholder_wrap = QtWidgets.QWidget()
        placeholder_layout = QtWidgets.QVBoxLayout(placeholder_wrap)
        placeholder_layout.addStretch()
        placeholder_layout.addWidget(self.list_placeholder)
        placeholder_layout.addStretch()
        self.list_stack.addWidget(placeholder_wrap)
        list_container = QtWidgets.QWidget()
        list_container.setLayout(self.list_stack)
        list_layout.addWidget(list_container, 1)


        style = self.style()
        btnDone = QtWidgets.QPushButton("Hoàn thành")
        # ... (code các nút bấm giữ nguyên) ...
        btnDone.setIcon(style.standardIcon(QtWidgets.QStyle.SP_DialogApplyButton))
        btnDone.clicked.connect(self.toggle_done)

        btnEdit = QtWidgets.QPushButton("Sửa")
        btnEdit.setIcon(style.standardIcon(QtWidgets.QStyle.SP_FileDialogContentsView))
        btnEdit.setProperty("secondary", True)
        btnEdit.clicked.connect(self.edit_item)

        btnDel = QtWidgets.QPushButton("Xoá")
        btnDel.setIcon(style.standardIcon(QtWidgets.QStyle.SP_TrashIcon))
        btnDel.setProperty("danger", True)
        btnDel.clicked.connect(self.delete_item)

        btnUndo = QtWidgets.QPushButton("Hoàn tác")
        btnUndo.setIcon(style.standardIcon(QtWidgets.QStyle.SP_ArrowBack))
        btnUndo.setProperty("secondary", True)
        btnUndo.clicked.connect(self.undo)

        btnUp = QtWidgets.QPushButton("Lên")
        btnUp.setIcon(style.standardIcon(QtWidgets.QStyle.SP_ArrowUp))
        btnUp.setProperty("secondary", True)
        btnUp.clicked.connect(self.move_up)

        btnDown = QtWidgets.QPushButton("Xuống")
        btnDown.setIcon(style.standardIcon(QtWidgets.QStyle.SP_ArrowDown))
        btnDown.setProperty("secondary", True)
        btnDown.clicked.connect(self.move_down)

        actions_bar = QtWidgets.QHBoxLayout()
        actions_bar.setSpacing(12)
        actions_bar.addWidget(btnDone)
        actions_bar.addWidget(btnEdit)
        actions_bar.addWidget(btnDel)
        actions_bar.addWidget(btnUndo)
        actions_bar.addStretch()
        actions_bar.addWidget(btnUp)
        actions_bar.addWidget(btnDown)
        list_layout.addLayout(actions_bar)

        L.addWidget(list_card, 1)

        # Shortcuts
        QtWidgets.QShortcut(QtGui.QKeySequence("Delete"), self, self.delete_item)
        QtWidgets.QShortcut(QtGui.QKeySequence("Space"), self, self.toggle_done)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self, self.undo)

    # ---------------- Tab 2 ----------------
    def _build_tab_day(self):
        L = QtWidgets.QVBoxLayout(self.tab_day)
        L.setContentsMargins(24, 24, 24, 24)
        L.setSpacing(18)

        day_card = self._create_card()
        card_layout = QtWidgets.QVBoxLayout(day_card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        head = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("Công việc trong ngày")
        title.setObjectName("cardTitle")
        head.addWidget(title)
        head.addStretch()
        head.addWidget(QtWidgets.QLabel("Ngày"))
        self.day_sel = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.day_sel.setDisplayFormat(QT_D_FMT)
        self.day_sel.setCalendarPopup(True)
        self.day_sel.setFixedWidth(140)
        self.day_sel.dateChanged.connect(lambda *_: self.refresh_day())
        head.addWidget(self.day_sel)
        btnToday = QtWidgets.QPushButton("Hôm nay")
        btnToday.setProperty("secondary", True)
        btnToday.clicked.connect(self._set_day_today)
        head.addWidget(btnToday)
        self.day_count_label = QtWidgets.QLabel("0 việc")
        self.day_count_label.setObjectName("cardSubtitle")
        head.addSpacing(12)
        head.addWidget(self.day_count_label)
        card_layout.addLayout(head)

        self.day_tbl = QtWidgets.QTableWidget(0, 4)
        self.day_tbl.setHorizontalHeaderLabels(["GIỜ","NỘI DUNG","ƯU TIÊN","TRẠNG THÁI"])
        self.day_tbl.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.day_tbl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.day_tbl.setAlternatingRowColors(True)
        self.day_tbl.verticalHeader().setVisible(False)
        header = self.day_tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.day_tbl.setWordWrap(True)
        self.day_tbl.setShowGrid(False)
        card_layout.addWidget(self.day_tbl)
        L.addWidget(day_card, 1)

    # ---------------- Tab 3 ----------------
    def _build_tab_week(self):
        L = QtWidgets.QVBoxLayout(self.tab_week)
        L.setContentsMargins(24, 24, 24, 24)
        L.setSpacing(18)

        week_card = self._create_card()
        card_layout = QtWidgets.QVBoxLayout(week_card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        head = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("Công việc trong tuần")
        title.setObjectName("cardTitle")
        head.addWidget(title)
        head.addStretch()
        head.addWidget(QtWidgets.QLabel("Tuần chứa ngày"))
        self.week_anchor = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.week_anchor.setDisplayFormat(QT_D_FMT)
        self.week_anchor.setCalendarPopup(True)
        self.week_anchor.setFixedWidth(140)
        self.week_anchor.dateChanged.connect(lambda *_: self.refresh_week())
        head.addWidget(self.week_anchor)
        btnThis = QtWidgets.QPushButton("Tuần này")
        btnThis.setProperty("secondary", True)
        btnThis.clicked.connect(self._set_week_this)
        head.addWidget(btnThis)
        self.week_count_label = QtWidgets.QLabel("0 việc")
        self.week_count_label.setObjectName("cardSubtitle")
        head.addSpacing(12)
        head.addWidget(self.week_count_label)
        card_layout.addLayout(head)

        self.week_tbl = QtWidgets.QTableWidget(0, 6)
        self.week_tbl.setHorizontalHeaderLabels(["THỨ","NGÀY","GIỜ","NỘI DUNG","ƯU TIÊN","TRẠNG THÁI"])
        self.week_tbl.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.week_tbl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.week_tbl.setAlternatingRowColors(True)
        self.week_tbl.verticalHeader().setVisible(False)
        header = self.week_tbl.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.week_tbl.setWordWrap(True)
        self.week_tbl.setShowGrid(False)
        card_layout.addWidget(self.week_tbl)
        L.addWidget(week_card, 1)

    # ---------------- CRUD ----------------
    def add_item(self):
        text = self.inp.text().strip()
        base_priority = self.prio.currentData()
        if base_priority is None:
            base_priority = self.prio.currentIndex()
        dialog = TaskDialog(self, title="Thêm công việc", task={"text": text, "priority": base_priority})
        if text:
            dialog.text_edit.selectAll()
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return
        data = dialog.get_data()
        self.store.items.append({
            "text": data["text"],
            "done": False,
            "priority": data["priority"],
            "due_dt": data.get("due_dt"),
            "note": data.get("note"),
            "created_at": now_iso(),
            "done_at": None
        })
        self.inp.clear()
        self.refresh_all()
        self.store.save()

    def _current_index(self):
        row = self.list.currentRow()
        if row < 0:
            return None
        mapping = self._filtered_indices()
        if 0 <= row < len(mapping):
            return mapping[row]
        return None

    def edit_item(self):
        idx = self._current_index()
        if idx is None:
            return
        it = self.store.items[idx]
        dialog = TaskDialog(self, title="Cập nhật công việc", task=it)
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return
        data = dialog.get_data()
        it["text"] = data["text"]
        it["priority"] = data["priority"]
        it["due_dt"] = data.get("due_dt")
        it["note"] = data.get("note")
        it["notified"] = False  # Reset để có thể thông báo lại
        self.refresh_all()
        self.store.save()

    def delete_item(self):
        idx = self._current_index()
        if idx is None:
            return
        if QtWidgets.QMessageBox.question(self, "Xoá", "Xoá công việc đã chọn?") != QtWidgets.QMessageBox.Yes:
            return
        self._undo = ("del", idx, dict(self.store.items[idx]))
        del self.store.items[idx]
        self.refresh_all()
        self.store.save()

    def undo(self):
        if not self._undo:
            return
        kind, idx, payload = self._undo
        if kind == "del":
            idx = min(idx, len(self.store.items))
            self.store.items.insert(idx, payload)
        self._undo = None
        self.refresh_all()
        self.store.save()

    def toggle_done(self):
        idx = self._current_index()
        if idx is None:
            return
        it = self.store.items[idx]
        it["done"] = not it["done"]
        it["done_at"] = now_iso() if it["done"] else None
        if not it["done"]:
            it["notified"] = False
        self.refresh_all()
        self.store.save()

    # ---------------- Filter + Sort ----------------
    def _is_today(self, it):
        dt = parse_dt(it.get("due_dt"))
        return bool(dt and dt.date() == date.today())

    def _is_in_week(self, it, anchor=None):
        dt = parse_dt(it.get("due_dt"))
        if not dt:
            return False
        a = anchor or date.today()
        return start_of_week(a) <= dt.date() <= end_of_week(a)

    def _filtered_indices(self):
        q = self.q.text().lower()
        mode = ["all", "todo", "done"][self.filter.checkedId()]
        rng = self.range.currentData() or "all"
        idxs = []
        for i, it in enumerate(self.store.items):
            if mode == "todo" and it["done"]:
                continue
            if mode == "done" and not it["done"]:
                continue
            if rng == "today" and not self._is_today(it):
                continue
            if rng == "week" and not self._is_in_week(it):
                continue
            if q and q not in it["text"].lower():
                continue
            idxs.append(i)
        key = self.sort.currentData() or "default"
        if key == "due_dt":
            idxs.sort(key=lambda i: (self.store.items[i]["due_dt"] is None,
                                     self.store.items[i]["due_dt"] or "9999-12-31 23:59"))
        elif key == "priority":
            idxs.sort(key=lambda i: -int(self.store.items[i].get("priority", 1)))
        elif key == "created_at":
            idxs.sort(key=lambda i: self.store.items[i].get("created_at", ""), reverse=True)
        return idxs

    def refresh_list(self):
        self.list.blockSignals(True)
        try:
            self.list.clear()
            now = datetime.now()  # <-- Dòng này đúng
            
            filtered = self._filtered_indices()
            for idx in filtered:
                it = self.store.items[idx]
                dt = parse_dt(it.get("due_dt")) if it.get("due_dt") else None
                
                # === SỬA DÒNG NÀY ===
                overdue = bool(dt and dt < now and not it.get("done")) # So sánh với 'now'
                # ===================

                item = QtWidgets.QListWidgetItem()
                item.setData(QtCore.Qt.UserRole, idx)
                pr = int(it.get("priority", 1))
                pr_txt = {0: "Thấp", 1: "Thường", 2: "Cao"}.get(pr, "Thường")
                due_txt = dt.strftime("%d/%m %H:%M") if dt else "Không hạn"
                tooltip_lines = [f"Ưu tiên: {pr_txt}", f"Hạn chót: {due_txt}"]
                
                # === SỬA DÒNG NÀY (bỏ 'not it.get("done")') ===
                if overdue: # Biến overdue đã bao gồm logic "chưa xong"
                # ============================================
                    tooltip_lines.append("Trạng thái: Quá hạn")
                
                note = it.get("note")
                if note:
                    tooltip_lines.append(f"Ghi chú: {note}")
                
                item.setToolTip("\n".join(tooltip_lines))
                widget = self._make_task_widget(it, dt=dt, overdue=overdue)
                size = widget.sizeHint()
                # Bạn đã tăng size lên 120, rất tốt!
                item.setSizeHint(QtCore.QSize(0, max(size.height(), 120))) 
                self.list.addItem(item)
                self.list.setItemWidget(item, widget)
        finally:
            self.list.blockSignals(False)
        self._sync_task_selection()
        self._update_statistics()
        self._update_list_placeholder()

    def _update_list_placeholder(self):
        if not hasattr(self, "list_stack"):
            return
        if self.list.count():
            self.list_stack.setCurrentIndex(0)
        else:
            if self.store.items:
                self.list_placeholder.setText("Không tìm thấy công việc phù hợp với bộ lọc hiện tại.")
            else:
                self.list_placeholder.setText("Chưa có công việc nào. Hãy thêm việc mới để bắt đầu!")
            self.list_stack.setCurrentIndex(1)

    def _update_title(self):
        self._update_statistics()

    # ---------------- Move ----------------
    def _can_move_linear(self):
        return (self.filter.checkedId() == 0 and
                not self.q.text().strip() and
                (self.sort.currentData() or "default") == "default" and
                (self.range.currentData() or "all") == "all")

    def move_up(self):
        if not self._can_move_linear():
            QtWidgets.QMessageBox.information(self, "Không thể di chuyển",
                "Tắt lọc/tìm/sắp xếp/phạm vi để di chuyển thứ tự.")
            return
        idx = self._current_index()
        if idx is None or idx <= 0:
            return
        self.store.items[idx - 1], self.store.items[idx] = self.store.items[idx], self.store.items[idx - 1]
        self.refresh_list()
        self.list.setCurrentRow(idx - 1)
        self.store.save()

    def move_down(self):
        if not self._can_move_linear():
            QtWidgets.QMessageBox.information(self, "Không thể di chuyển",
                "Tắt lọc/tìm/sắp xếp/phạm vi để di chuyển thứ tự.")
            return
        idx = self._current_index()
        if idx is None or idx >= len(self.store.items) - 1:
            return
        self.store.items[idx + 1], self.store.items[idx] = self.store.items[idx], self.store.items[idx + 1]
        self.refresh_list()
        self.list.setCurrentRow(idx + 1)
        self.store.save()

    # ---------------- Day view ----------------
    def _set_day_today(self):
        self.day_sel.setDate(QtCore.QDate.currentDate())

    def refresh_day(self):
        d = self.day_sel.date().toPyDate()
        now = datetime.now() # Lấy thời gian hiện tại
        
        rows = []
        for it in self.store.items:
            dt = parse_dt(it.get("due_dt"))
            if dt and dt.date() == d:
                # Kiểm tra xem có quá hạn không
                is_overdue = (dt < now and not it.get("done"))
                rows.append((dt, it, is_overdue)) # Truyền trạng thái quá hạn
                
        rows.sort(key=lambda x: x[0])
        self.day_tbl.setRowCount(0)
        
        for dt, it, is_overdue in rows: # Lấy is_overdue
            r = self.day_tbl.rowCount()
            self.day_tbl.insertRow(r)
            
            # === LOGIC TRẠNG THÁI MỚI ===
            status_text = "Đã xong"
            if not it.get("done"):
                status_text = "Quá hạn" if is_overdue else "Chưa xong"
            # ============================

            vals = [dt.strftime("%H:%M"), it["text"],
                    {0: "Thấp", 1: "Thường", 2: "Cao"}.get(int(it.get("priority", 1)), "Thường"),
                    status_text] # Dùng status_text mới
            
            for c, v in enumerate(vals):
                item = QtWidgets.QTableWidgetItem(v)
                if c == 1:
                    item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                    note = it.get("note")
                    if note:
                        item.setToolTip(note)
                else:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # === THÊM MÀU SẮC CHO TRẠNG THÁI ===
                if is_overdue and c == 3: # Cột Trạng thái (index 3)
                    item.setForeground(QtGui.QBrush(QtGui.QColor("#e03131"))) # Màu đỏ
                elif it.get("done") and c == 3:
                    item.setForeground(QtGui.QBrush(QtGui.QColor("#2b8a3e"))) # Màu xanh lá
                # =================================
                
                self.day_tbl.setItem(r, c, item)
                
        self.day_tbl.resizeRowsToContents()
        self.day_count_label.setText(f"{len(rows)} việc" if rows else "Không có việc")
    # ---------------- Week view ----------------
    def _set_week_this(self):
        self.week_anchor.setDate(QtCore.QDate.currentDate())

    def refresh_week(self):
        anchor = self.week_anchor.date().toPyDate()
        monday, sunday = start_of_week(anchor), end_of_week(anchor)
        now = datetime.now() # Lấy thời gian hiện tại
        
        rows = []
        for it in self.store.items:
            dt = parse_dt(it.get("due_dt"))
            if dt and monday <= dt.date() <= sunday:
                # Kiểm tra xem có quá hạn không
                is_overdue = (dt < now and not it.get("done"))
                rows.append((dt, it, is_overdue)) # Truyền trạng thái quá hạn
                
        rows.sort(key=lambda x: (x[0].date(), x[0].time()))
        self.week_tbl.setRowCount(0)
        
        for dt, it, is_overdue in rows: # Lấy is_overdue
            r = self.week_tbl.rowCount()
            self.week_tbl.insertRow(r)
            
            # === LOGIC TRẠNG THÁI MỚI ===
            status_text = "Đã xong"
            if not it.get("done"):
                status_text = "Quá hạn" if is_overdue else "Chưa xong"
            # ============================

            vals = [WEEKDAY_VN[dt.weekday()], dt.strftime(D_FMT), dt.strftime("%H:%M"),
                    it["text"], {0: "Thấp", 1: "Thường", 2: "Cao"}.get(int(it.get("priority", 1)), "Thường"),
                    status_text] # Dùng status_text mới
            
            for c, v in enumerate(vals):
                item = QtWidgets.QTableWidgetItem(v)
                if c in (3,):
                    item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                    note = it.get("note")
                    if note:
                        item.setToolTip(note)
                else:
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # === THÊM MÀU SẮC CHO TRẠNG THÁI ===
                if is_overdue and c == 5: # Cột Trạng thái (index 5)
                    item.setForeground(QtGui.QBrush(QtGui.QColor("#e03131"))) # Màu đỏ
                elif it.get("done") and c == 5:
                    item.setForeground(QtGui.QBrush(QtGui.QColor("#2b8a3e"))) # Màu xanh lá
                # =================================
                
                self.week_tbl.setItem(r, c, item)
                
        self.week_tbl.resizeRowsToContents()
        self.week_count_label.setText(f"{len(rows)} việc" if rows else "Không có việc")


    def refresh_all(self):
        self.refresh_list()
        self.refresh_day()
        self.refresh_week()

    def show_notification(self, title, message):
        """Hiển thị thông báo qua system tray."""
        if self.tray_icon:
            self.tray_icon.showMessage(
                title, 
                message, 
                QtWidgets.QSystemTrayIcon.Information, 
                3000  # Thông báo hiển thị trong 3 giây
            )

    def check_due_tasks(self):
        """Được gọi bởi QTimer, kiểm tra các công việc đến hạn."""
        if not self.tray_icon:
            return  # Không làm gì nếu không có system tray

        now = datetime.now()
        tasks_to_notify = []
        
        for task in self.store.items:
            # Bỏ qua nếu: Đã xong, HOẶC đã thông báo rồi
            if task.get("done") or task.get("notified"):
                continue
            
            due_str = task.get("due_dt")
            if not due_str:
                continue
            
            due_dt = parse_dt(due_str) # parse_dt là hàm toàn cục bạn đã có
            if not due_dt:
                continue

            # Nếu công việc đã (hoặc đang) đến hạn
            if due_dt <= now:
                tasks_to_notify.append(task)
        
        if tasks_to_notify:
            # Đánh dấu tất cả là "đã thông báo" (cho system tray)
            for task in tasks_to_notify:
                task["notified"] = True
            
            # --- Thông báo hệ thống (System Tray) ---
            if len(tasks_to_notify) == 1:
                title = "Công việc đến hạn!"
                message = tasks_to_notify[0].get("text")
            else:
                title = f"{len(tasks_to_notify)} công việc đến hạn!"
                message = f"Việc đầu tiên: {tasks_to_notify[0].get('text')}"
            
            self.show_notification(title, message)
            
            # === CẬP NHẬT CHUÔNG TRONG APP ===
            # Thêm vào danh sách thông báo
            for task in tasks_to_notify:
                msg = f"Đến hạn: {task.get('text')}"
                if msg not in self.app_notifications:
                     self.app_notifications.append(msg)
            
            # Cập nhật số đếm trên chuông
            if hasattr(self, "bell_counter"): # Đảm bảo UI đã được tạo
                self.update_bell_counter()
            # ===============================
            
            # Lưu lại thay đổi (đánh dấu notified=True)
            self.store.save()
    def update_bell_counter(self):
        """Cập nhật số đếm trên biểu tượng chuông."""
        count = len(self.app_notifications)
        if count > 0:
            self.bell_counter.setText(str(count))
            self.bell_counter.setVisible(True)
        else:
            self.bell_counter.setVisible(False)
        # Cập nhật style cho label
        self._refresh_widget_style(self.bell_counter)
        self._refresh_widget_style(self.bell_button)

    def show_app_notifications(self):
        """Hiển thị menu pop-up chứa các thông báo."""
        if not self.app_notifications:
            QtWidgets.QMessageBox.information(self, "Thông báo", "Không có thông báo mới.")
            return

        menu = QtWidgets.QMenu(self)
        
        # Thêm các thông báo vào menu
        for msg in self.app_notifications:
            action = QtWidgets.QAction(msg, self)
            action.setEnabled(False) # Chỉ để hiển thị, không bấm được
            menu.addAction(action)
        
        menu.addSeparator()
        
        # Thêm hành động "Xoá tất cả"
        clear_action = QtWidgets.QAction("✔️ Đánh dấu đã đọc (Xoá tất cả)", self)
        clear_action.triggered.connect(self.clear_app_notifications)
        menu.addAction(clear_action)
        
        # Hiển thị menu ngay bên dưới nút chuông
        menu.exec_(self.bell_button.mapToGlobal(QtCore.QPoint(0, self.bell_button.height())))

    def clear_app_notifications(self):
        """Xoá tất cả thông báo và cập nhật chuông."""
        self.app_notifications.clear()
        self.update_bell_counter()
        # Lưu ý: Phiên bản này chưa lưu danh sách thông báo đã xoá
        # Khi khởi động lại, thông báo có thể hiện lại nếu việc vẫn quá hạn        



def main():
    app = QtWidgets.QApplication(sys.argv)
    default_font = QtGui.QFont("Segoe UI", 9) 
    app.setFont(default_font)
    w = Main()
    w.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()