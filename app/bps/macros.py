"""
    macros.py: contains global prettifying functions / render helpers
"""
# flask blueprint
from flask import Blueprint

# date parsing util
import babel

macros = Blueprint(
    "macros",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@macros.app_template_filter()
def format_datetime(value, date_format="medium"):
    """
    format python date time object to string

    params:
        - value: date time value
        - date_format: date format
    """
    if date_format == "full":
        date_format = "EEEE, d. MMMM y 'at' HH:mm"
    elif date_format == "medium":
        date_format = "EE dd.MM.y HH:mm"
    elif date_format == "short":
        date_format = "MMM d. y"
    return babel.dates.format_datetime(value, date_format)
