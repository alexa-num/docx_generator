"""Контроллер для управления логикой генерации писем"""

from utils.docx_generator import DocxGenerator
import os


class LetterController:
    """Контроллер для генерации писем"""
    
    def __init__(self):
        self.docx_generator = DocxGenerator()
    
    def check_template(self):
        """Проверяет наличие шаблона"""
        return self.docx_generator.check_template_exists()
    
    def get_template_path(self):
        """Возвращает путь к шаблону"""
        return self.docx_generator.get_template_path()
    
    def validate_letter_data(self, letter_data):
        """
        Валидация данных письма
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not letter_data.get('subject', '').strip():
            return False, "Поле 'Тема письма' обязательно для заполнения!"
        
        if not letter_data.get('text', '').strip():
            return False, "Поле 'Текст письма' обязательно для заполнения!"
        
        if not letter_data.get('to_job_title', '').strip():
            return False, "Поле 'Должность получателя' обязательно для заполнения!"
        
        if not letter_data.get('to_company', '').strip():
            return False, "Поле 'Компания получателя' обязательно для заполнения!"
        
        return True, ""
    
    def validate_logo(self, logo_path):
        """
        Валидация файла логотипа
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not logo_path:
            return True, ""
        
        if not os.path.exists(logo_path):
            return False, "Файл логотипа не найден!"
        
        # Проверяем расширение
        valid_extensions = ('.png', '.jpg', '.jpeg', '.svg', '.bmp', '.gif', '.tiff')
        if not logo_path.lower().endswith(valid_extensions):
            return False, "Неподдерживаемый формат изображения. Используйте PNG, JPG, JPEG, SVG, BMP, GIF или TIFF"
        
        return True, ""
    
    def generate_letter(self, output_path, letter_data, appendices, logo_path=None):
        """
        Генерирует письмо
        
        Args:
            output_path: путь для сохранения
            letter_data: словарь с данными письма
            appendices: список объектов Appendix
            logo_path: путь к файлу логотипа (опционально)
            
        Returns:
            bool: успешность операции
        """
        # Валидация
        is_valid, error_msg = self.validate_letter_data(letter_data)
        if not is_valid:
            raise Exception(error_msg)
        
        is_valid, error_msg = self.validate_logo(logo_path)
        if not is_valid:
            raise Exception(error_msg)
        
        # Генерация
        return self.docx_generator.generate_letter(output_path, letter_data, appendices, logo_path)