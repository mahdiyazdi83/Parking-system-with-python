import re
from persian_tools import plate


class Validation:

    @staticmethod
    def plate_validator(car_plate):
        """اعتبارسنجی پلاک خودرو"""

        cleaned = str(car_plate).replace(" ", "").replace("-", "").strip()

        if not plate.is_valid(cleaned):
            if any(c.isalpha() and not ('\u0600' <= c <= '\u06FF') for c in cleaned):
                raise ValueError("لطفاً حروف پلاک را به فارسی وارد کنید (مثال: 12ب34567)")
            elif len(cleaned) == 7:
                raise ValueError("فرمت پلاک خودرو صحیح نیست. فرمت صحیح: 12ب34567")
            elif len(cleaned) == 8 and cleaned.isdigit():
                raise ValueError("فرمت پلاک موتورسیکلت صحیح نیست. فرمت صحیح: 12345678")
            else:
                raise ValueError("پلاک وارد شده معتبر نیست")

        return cleaned

    @staticmethod
    def mobile_validator(mobile):
        """اعتبارسنجی شماره موبایل"""

        cleaned = str(mobile).replace(" ", "").replace("-", "").strip()

        if not re.match(r'^09\d{9}$', cleaned):
            raise ValueError("شماره موبایل معتبر نیست. فرمت صحیح: 09123456789")
        return cleaned