# flask blueprint
from flask import Blueprint
# date utils
import babel

macros = Blueprint('macros',
               __name__,
               template_folder='templates',
               static_folder='static',)
               
# date formatting
@macros.app_template_filter()
def format_datetime(value, format="medium"):
    if format == "full":
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == "medium":
        format = "EE dd.MM.y HH:mm"
    elif format == "short":
        format = "MMM d. y"
    return babel.dates.format_datetime(value, format)