import re
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
import unidecode

from apps.common.types import Validated

def validate_iran_mobile_number(self, value: str) -> Validated[str]:
    # Accept Irancell, Rightel, Talia, Hamrahe-Aval
    value = unidecode(value)
    if not re.fullmatch(r'^(\+98|0)?9(0[1-5]|1[0-9]|9[0-9]|3[0-9]|2[0-2])?[0-9]{7}', value):
        raise ValidationError(_('Mobile number is not valid.'))
    return value
