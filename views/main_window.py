from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog,
    QMessageBox, QGroupBox, QFormLayout, QListWidget,
    QSplitter, QScrollArea, QTabWidget, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from models.appendix import Appendix
from controllers.letter_controller import LetterController
import os


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генератор писем")
        self.setMinimumSize(1200, 800)
        
        # Контроллер
        self.controller = LetterController()
        
        # Данные
        self.appendices = []
        self.logo_path = None
        
        # Инициализация интерфейса
        self.init_ui()
        
        # Проверка наличия шаблона
        self.check_template()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель
        left_panel = self.create_left_panel()
        
        # Правая панель (предпросмотр)
        right_panel = self.create_right_panel()
        
        # Разделитель
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([600, 600])
        main_layout.addWidget(splitter)
        
        # Подключаем сигналы
        self.connect_signals()
        
        # Загружаем пример
        self.load_example()
    
    def create_left_panel(self):
        """Создает левую панель с формами ввода"""
        left_panel = QScrollArea()
        left_panel.setWidgetResizable(True)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Информация об отправителе
        sender_group = self.create_sender_group()
        left_layout.addWidget(sender_group)
        
        # Информация о получателе
        receiver_group = self.create_receiver_group()
        left_layout.addWidget(receiver_group)
        
        # Основное содержание письма
        letter_group = self.create_letter_group()
        left_layout.addWidget(letter_group)
        
        # Приложения
        appendices_group = self.create_appendices_group()
        left_layout.addWidget(appendices_group)
        
        # Кнопка генерации
        generate_btn = QPushButton("📄 Сгенерировать письмо (DOCX)")
        generate_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; font-size: 14px;")
        generate_btn.clicked.connect(self.on_generate_clicked)
        left_layout.addWidget(generate_btn)
        
        left_layout.addStretch()
        left_panel.setWidget(left_widget)
        
        return left_panel
    
    def create_sender_group(self):
        """Создает группу информации об отправителе"""
        group = QGroupBox("📤 Информация об отправителе")
        layout = QVBoxLayout()
        
        # Логотип компании
        logo_layout = QVBoxLayout()
        logo_label = QLabel("Логотип компании:")
        logo_label.setStyleSheet("font-weight: bold;")
        logo_layout.addWidget(logo_label)
        
        # Предпросмотр логотипа
        self.logo_preview = QLabel()
        self.logo_preview.setFixedSize(150, 100)
        self.logo_preview.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.logo_preview.setAlignment(Qt.AlignCenter)
        self.logo_preview.setText("Нет логотипа")
        logo_layout.addWidget(self.logo_preview)
        
        # Кнопки для работы с логотипом
        logo_btn_layout = QHBoxLayout()
        self.select_logo_btn = QPushButton("Выбрать логотип")
        self.select_logo_btn.clicked.connect(self.on_select_logo)
        self.clear_logo_btn = QPushButton("Очистить логотип")
        self.clear_logo_btn.clicked.connect(self.on_clear_logo)
        logo_btn_layout.addWidget(self.select_logo_btn)
        logo_btn_layout.addWidget(self.clear_logo_btn)
        logo_layout.addLayout(logo_btn_layout)
        
        layout.addLayout(logo_layout)
        
        # Информация о компании
        info_label = QLabel("Информация о компании:")
        info_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(info_label)
        
        self.company_info = QTextEdit()
        self.company_info.setMaximumHeight(100)
        self.company_info.setPlaceholderText("ул. Лубянка, 10, стр. 2\nМосква, Россия, 120440\ntел. (095) 228 09 78\nфакс 228 09 79\nE-mail: ineks@msk.ru")
        layout.addWidget(self.company_info)
        
        # Подпись отправителя
        sender_info_layout = QFormLayout()
        self.from_title = QLineEdit("Конкурсный управляющий")
        self.from_name = QLineEdit("А.В. Ростовцев")
        sender_info_layout.addRow("Должность отправителя:", self.from_title)
        sender_info_layout.addRow("ФИО отправителя:", self.from_name)
        
        layout.addLayout(sender_info_layout)
        group.setLayout(layout)
        
        return group
    
    def create_receiver_group(self):
        """Создает группу информации о получателе"""
        group = QGroupBox("📥 Информация о получателе")
        layout = QFormLayout()
        
        self.to_job_title = QLineEdit("Генеральному директору")
        self.to_company = QLineEdit("ООО 'Художественная школа имени Репина'")
        self.to_short_name = QLineEdit("И.К. Стрешеневу")
        
        layout.addRow("Должность получателя:", self.to_job_title)
        layout.addRow("Компания получателя:", self.to_company)
        layout.addRow("Краткое имя/ФИО:", self.to_short_name)
        
        group.setLayout(layout)
        return group
    
    def create_letter_group(self):
        """Создает группу основного содержания письма"""
        group = QGroupBox("✉️ Основное содержание письма")
        layout = QFormLayout()
        
        self.subject = QLineEdit("О погашении задолженности")
        self.text = QTextEdit()
        self.text.setPlaceholderText("Введите основной текст письма...")
        
        self.footer = QTextEdit()
        self.footer.setMaximumHeight(60)
        self.footer.setPlaceholderText("Нижний колонтитул (например: С уважением, ...)")
        
        layout.addRow("Тема письма:", self.subject)
        layout.addRow("Текст письма:", self.text)
        layout.addRow("Нижний колонтитул:", self.footer)
        
        group.setLayout(layout)
        return group
    
    def create_appendices_group(self):
        """Создает группу для работы с приложениями"""
        group = QGroupBox("📎 Приложения к письму")
        layout = QVBoxLayout()
        
        # Список приложений
        layout.addWidget(QLabel("Список приложений:"))
        self.appendices_list = QListWidget()
        self.appendices_list.setMaximumHeight(120)
        layout.addWidget(self.appendices_list)
        
        # Кнопки управления (ТРИ КНОПКИ)
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Добавить приложение")
        self.btn_edit = QPushButton("✏️ Редактировать")
        self.btn_remove = QPushButton("🗑 Удалить")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_remove)
        layout.addLayout(btn_layout)
        
        # Поля для ввода/редактирования
        layout.addWidget(QLabel("Заголовок приложения:"))
        self.app_title = QLineEdit()
        self.app_title.setPlaceholderText("Например: Причина отмены лабораторной")
        layout.addWidget(self.app_title)
        
        layout.addWidget(QLabel("Текст приложения:"))
        self.app_text = QTextEdit()
        self.app_text.setPlaceholderText("Введите текст приложения...")
        self.app_text.setMaximumHeight(100)
        layout.addWidget(self.app_text)
        
        layout.addWidget(QLabel("Количество листов:"))
        self.app_pages = QLineEdit()
        self.app_pages.setPlaceholderText("Например: 3")
        self.app_pages.setText("1")
        layout.addWidget(self.app_pages)
        
        # Информация о выбранном приложении
        self.selected_info_label = QLabel("ℹ️ Выберите приложение из списка для редактирования или удаления")
        self.selected_info_label.setStyleSheet("color: #666; font-style: italic; margin-top: 5px;")
        layout.addWidget(self.selected_info_label)
        
        group.setLayout(layout)
        
        return group
    
    def create_right_panel(self):
        """Создает правую панель с предпросмотром"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        preview_label = QLabel("🔍 Предпросмотр письма")
        preview_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(preview_label)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setPlaceholderText("Здесь будет отображаться сгенерированное письмо...")
        self.preview_text.setStyleSheet("font-family: monospace; font-size: 12px;")
        layout.addWidget(self.preview_text)
        
        return panel
    
    def connect_signals(self):
        """Подключает все сигналы"""
        # Кнопки приложений
        self.btn_add.clicked.connect(self.on_add_app)
        self.btn_edit.clicked.connect(self.on_edit_app)
        self.btn_remove.clicked.connect(self.on_remove_app)
        
        # Выбор в списке
        self.appendices_list.itemSelectionChanged.connect(self.on_app_selected)
        
        # Обновление предпросмотра
        self.company_info.textChanged.connect(self.update_preview)
        self.to_job_title.textChanged.connect(self.update_preview)
        self.to_company.textChanged.connect(self.update_preview)
        self.to_short_name.textChanged.connect(self.update_preview)
        self.subject.textChanged.connect(self.update_preview)
        self.text.textChanged.connect(self.update_preview)
        self.footer.textChanged.connect(self.update_preview)
        self.from_title.textChanged.connect(self.update_preview)
        self.from_name.textChanged.connect(self.update_preview)
        
        # Первоначальный предпросмотр
        self.update_preview()
    
    def on_select_logo(self):
        """Выбор файла логотипа"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл логотипа", "",
            "Изображения (*.png *.jpg *.jpeg *.svg *.bmp *.gif *.tiff);;Все файлы (*.*)"
        )
        
        if file_path:
            # Валидация
            is_valid, error_msg = self.controller.validate_logo(file_path)
            if not is_valid:
                QMessageBox.warning(self, "Ошибка", error_msg)
                return
            
            self.logo_path = file_path
            
            # Отображаем превью
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(150, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_preview.setPixmap(scaled_pixmap)
                self.logo_preview.setText("")
            else:
                self.logo_preview.setText("Не удалось загрузить")
            
            self.update_preview()
    
    def on_clear_logo(self):
        """Очищает выбранный логотип"""
        self.logo_path = None
        self.logo_preview.clear()
        self.logo_preview.setText("Нет логотипа")
        self.logo_preview.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")
        self.update_preview()
    
    def check_template(self):
        """Проверяет наличие файла шаблона"""
        if not self.controller.check_template():
            QMessageBox.warning(
                self, 
                "Шаблон не найден",
                f"Файл шаблона не найден по пути:\n{self.controller.get_template_path()}\n\n"
                "Пожалуйста, создайте файл template.docx в папке templates\n\n"
                "Шаблон должен содержать плейсхолдеры:\n"
                "{COMPANY_LOGO}, {COMPANY_INFO}, {TO_JOB_TITLE}, {TO_COMPANY}, "
                "{TO_SHORT_NAME}, {SUBJECT}, {TEXT}, {FOOTER}, {FROM_TITLE}, "
                "{FROM_NAME}, {APPENDICES_LIST}"
            )
    
    def get_letter_data(self):
        """Собирает данные из формы"""
        return {
            'company_info': self.company_info.toPlainText().strip(),
            'to_job_title': self.to_job_title.text().strip(),
            'to_company': self.to_company.text().strip(),
            'to_short_name': self.to_short_name.text().strip(),
            'subject': self.subject.text().strip(),
            'text': self.text.toPlainText().strip(),
            'footer': self.footer.toPlainText().strip(),
            'from_title': self.from_title.text().strip(),
            'from_name': self.from_name.text().strip()
        }
    
    def generate_letter_text(self):
        """Генерирует текст письма для предпросмотра"""
        data = self.get_letter_data()
        
        # Формируем адресата
        to_line = f"{data['to_job_title']}\n{data['to_company']}\n{data['to_short_name']}"
        
        # Формируем подпись
        signature = f"{data['from_title']}\t\t{data['from_name']}"
        
        # Информация о логотипе для предпросмотра
        logo_info = f"[Логотип: {os.path.basename(self.logo_path)}]" if self.logo_path else "[Логотип не добавлен]"
        
        # Список приложений
        appendices_text = self.generate_appendix_list_text()
        
        # Сборка письма
        result = f"""{logo_info}
{data['company_info']}

{to_line}

{data['subject']},

{data['text']}

{data['footer']}

{signature}

{appendices_text}"""
        
        return result
    
    def generate_appendix_list_text(self):
        """Формирует текстовый список приложений"""
        if not self.appendices:
            return ""
        
        lines = ["Приложения:"]
        for idx, app in enumerate(self.appendices, start=1):
            lines.append(f"{idx}. {app.title} — {app.pages} л.")
        
        return "\n".join(lines)
    
    def update_preview(self):
        """Обновляет предпросмотр"""
        # Валидация
        data = self.get_letter_data()
        is_valid, error_msg = self.controller.validate_letter_data(data)
        
        if not is_valid:
            self.preview_text.setStyleSheet("background-color: #ffe6e6; font-family: monospace;")
            self.preview_text.setText(f"⚠️ Ошибка валидации:\n{error_msg}")
            return
        
        self.preview_text.setStyleSheet("background-color: white; font-family: monospace;")
        letter_text = self.generate_letter_text()
        self.preview_text.setText(letter_text)
    
    def on_generate_clicked(self):
        """Обработчик нажатия кнопки генерации"""
        # Собираем данные
        letter_data = self.get_letter_data()
        
        # Выбираем место сохранения
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить письмо как", "generated_letter.docx",
            "Word Documents (*.docx)"
        )
        if not save_path:
            return
        
        try:
            # Генерируем письмо
            self.controller.generate_letter(save_path, letter_data, self.appendices, self.logo_path)
            QMessageBox.information(self, "Успех", f"Письмо успешно создано:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
    
    def on_app_selected(self):
        """При выборе приложения в списке - загружаем данные в поля для редактирования"""
        selected = self.appendices_list.currentRow()
        if selected >= 0 and selected < len(self.appendices):
            app = self.appendices[selected]
            # Загружаем данные выбранного приложения в поля
            self.app_title.setText(app.title)
            self.app_text.setPlainText(app.text)
            self.app_pages.setText(app.pages)
            
            # Обновляем информационную метку
            self.selected_info_label.setText(f"✅ Выбрано приложение: '{app.title}' (данные загружены, нажмите 'Редактировать' для сохранения изменений)")
            self.selected_info_label.setStyleSheet("color: #4CAF50; font-style: italic; margin-top: 5px;")
        else:
            # Если ничего не выбрано, очищаем поля
            self.on_clear_app_fields()
            self.selected_info_label.setText("ℹ️ Выберите приложение из списка для редактирования или удаления")
            self.selected_info_label.setStyleSheet("color: #666; font-style: italic; margin-top: 5px;")
    
    def on_clear_app_fields(self):
        """Очищает поля ввода приложения"""
        self.app_title.clear()
        self.app_text.clear()
        self.app_pages.setText("1")
    
    def on_add_app(self):
        """Добавляет новое приложение"""
        title = self.app_title.text().strip()
        text = self.app_text.toPlainText().strip()
        pages = self.app_pages.text().strip()
        
        # Проверяем заполнение полей
        if not title:
            QMessageBox.warning(self, "Ошибка", "Заголовок приложения обязателен для заполнения!")
            return
        
        if not text:
            QMessageBox.warning(self, "Ошибка", "Текст приложения обязателен для заполнения!")
            return
        
        if not pages:
            pages = "1"
        
        # Проверяем на дубликаты
        for app in self.appendices:
            if app.title.lower() == title.lower():
                QMessageBox.warning(self, "Ошибка", f"Приложение с заголовком '{title}' уже существует!")
                return
        
        # Добавляем новое приложение
        new_app = Appendix(title, text, pages)
        self.appendices.append(new_app)
        self.appendices_list.addItem(title)
        
        # Очищаем поля
        self.on_clear_app_fields()
        
        # Снимаем выделение
        self.appendices_list.setCurrentRow(-1)
        
        # Обновляем предпросмотр
        self.update_preview()
        
        QMessageBox.information(self, "Успех", f"Приложение '{title}' успешно добавлено!")
    
    def on_edit_app(self):
        """Редактирует выбранное приложение"""
        # Проверяем, выбрано ли приложение
        selected = self.appendices_list.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите приложение из списка для редактирования!")
            return
        
        # Получаем новые данные из полей
        new_title = self.app_title.text().strip()
        new_text = self.app_text.toPlainText().strip()
        new_pages = self.app_pages.text().strip()
        
        # Проверяем заполнение полей
        if not new_title:
            QMessageBox.warning(self, "Ошибка", "Заголовок приложения обязателен для заполнения!")
            return
        
        if not new_text:
            QMessageBox.warning(self, "Ошибка", "Текст приложения обязателен для заполнения!")
            return
        
        if not new_pages:
            new_pages = "1"
        
        # Проверяем на дубликаты (исключая текущее приложение)
        for i, app in enumerate(self.appendices):
            if i != selected and app.title.lower() == new_title.lower():
                QMessageBox.warning(self, "Ошибка", f"Приложение с заголовком '{new_title}' уже существует!")
                return
        
        # Сохраняем старый заголовок для сообщения
        old_title = self.appendices[selected].title
        
        # Обновляем приложение
        self.appendices[selected].title = new_title
        self.appendices[selected].text = new_text
        self.appendices[selected].pages = new_pages
        
        # Обновляем список
        self.appendices_list.item(selected).setText(new_title)
        
        # Очищаем поля
        self.on_clear_app_fields()
        
        # Снимаем выделение
        self.appendices_list.setCurrentRow(-1)
        
        # Обновляем предпросмотр
        self.update_preview()
        
        QMessageBox.information(self, "Успех", f"Приложение '{old_title}' успешно обновлено на '{new_title}'!")
    
    def on_remove_app(self):
        """Удаляет выбранное приложение"""
        # Проверяем, выбрано ли приложение
        selected = self.appendices_list.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите приложение из списка для удаления!")
            return
        
        # Получаем заголовок приложения
        title = self.appendices[selected].title
        
        # Спрашиваем подтверждение
        reply = QMessageBox.question(
            self, 
            "Подтверждение удаления", 
            f"Вы действительно хотите удалить приложение '{title}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Удаляем приложение
            del self.appendices[selected]
            self.appendices_list.takeItem(selected)
            
            # Очищаем поля
            self.on_clear_app_fields()
            
            # Обновляем предпросмотр
            self.update_preview()
            
            QMessageBox.information(self, "Успех", f"Приложение '{title}' успешно удалено!")
    
    def load_example(self):
        """Загружает пример письма из вашего файла"""
        example_text = """Сообщаем Вам, что 00.00.2003 Арбитражным судом г. Москвы АКБ "Инкесбанк" признан банкротом. Открыто конкурсное производство. ООО "Художественная школа имени Репина" является дебитором "Инкесбанка" с суммой задолженности 500 000 (Пятьсот тысяч) руб. по кредитному договору от 00.00.1999 № 284-КД - 99.

Прошу Вас письменно известить нас о сроках погашения долга до 00.00.2003.
В случае отказа мы будем вынуждены обратиться в судебные органы о принудительном взыскании задолженности."""
        
        self.text.setPlainText(example_text)
        self.footer.setPlainText("С уважением,")
        
        # Заполняем информацию о компании
        self.company_info.setPlainText("ул. Лубянка, 10, стр. 2\nМосква, Россия, 120440\nтел. (095) 228 09 78\nфакс 228 09 79\nE-mail: ineks@msk.ru")
        
        # Добавляем пример приложения
        example_app = Appendix("Причина отмены лабораторной", 
                              "Лабораторная работа была отменена по техническим причинам. Приносим извинения за неудобства.",
                              "3")
        self.appendices.append(example_app)
        self.appendices_list.addItem(example_app.title)
        
        self.update_preview()