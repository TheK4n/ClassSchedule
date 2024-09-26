import datetime


class DateConverter:
    regex = r'\d{2}-\d{2}-\d{2}'
    format = '%d-%m-%y'

    def to_python(self, value: str) -> datetime.date:
        return datetime.datetime.strptime(value, self.format).date()

    def to_url(self, value: datetime.date) -> str:
        return value.strftime(self.format)
