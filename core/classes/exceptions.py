from rest_framework.serializers import ValidationError

class FormatValidationException(ValidationError):
    def __init__(self, field_name, detail, **kwargs):
        super().__init__({
            field_name: detail if  type(detail) is list else [detail]
        }, **kwargs)
        
    