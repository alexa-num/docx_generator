class Appendix:
    """Класс для хранения данных одного приложения"""
    
    def __init__(self, title="", text="", pages="1"):
        self.title = title
        self.text = text
        self.pages = pages
    
    def to_dict(self):
        """Конвертирует объект в словарь"""
        return {
            'title': self.title,
            'text': self.text,
            'pages': self.pages
        }
    
    @classmethod
    def from_dict(cls, data):
        """Создает объект из словаря"""
        return cls(data.get('title', ''), data.get('text', ''), data.get('pages', '1'))