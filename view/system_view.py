from tkinter import *
from tkinter import messagebox, ttk
from controller.car_controller import CarController
from controller.parking_session_controller import ParkingSessionController
from model.entity.park_spot import ParkSpot


class ParkingSystemView:
    def __init__(self):
        # Controller ها
        self.car_controller = CarController()
        self.parking_controller = ParkingSessionController()

        # پنجره اصلی
        self.window = Tk()
        self.window.title("سیستم پارکینگ")
        self.window.geometry("550x550")
        self.window.configure(bg="#333333")

        # متغیرهای پلاک
        self.plate_part1 = StringVar()  # 2 رقم اول
        self.plate_part2 = StringVar()  # حرف
        self.plate_part3 = StringVar()  # 3 رقم وسط
        self.plate_part4 = StringVar()  # 2 رقم آخر (کد استان)

        # متغیرهای دیگر
        self.model_var = StringVar()
        self.mobile_var = StringVar()
        self.floor_var = IntVar(value=1)
        self.place_var = IntVar(value=1)
        self.exit_plate_var = StringVar()
        self.cost_var = StringVar()

        # حروف معتبر پلاک
        self.valid_letters = ['ب', 'ج', 'د', 'س', 'ص', 'ط', 'ق', 'ل', 'م', 'ن', 'و', 'ه', 'ی',
                              'الف', 'پ', 'ت', 'ث', 'ح', 'خ', 'ذ', 'ر', 'ز', 'ژ', 'ش', 'ض', 'ع', 'غ', 'ف', 'ک']

        # عنوان
        Label(self.window, text="سیستم مدیریت پارکینگ",
              font=("Arial", 16, "bold"), bg="#333333", fg="white").place(x=190, y=10)

        # بخش پارک خودرو
        self.create_park_section()

        # بخش خروج خودرو
        self.create_exit_section()

        # بخش وضعیت
        self.create_status_section()

        # بارگذاری اولیه وضعیت و لیست پلاک‌ها
        self.update_status()
        self.update_exit_plates()

        self.window.mainloop()

    def create_park_section(self):
        """بخش پارک خودرو"""
        frame = Frame(self.window, bg="#444444", bd=2, relief="groove")
        frame.place(x=30, y=50, width=490, height=280)

        Label(frame, text="پارک خودرو", font=("Arial", 12, "bold"),
              bg="#444444", fg="white").place(x=200, y=5)

        # پلاک (ورودی حرفه‌ای)
        Label(frame, text="پلاک:", bg="#444444", fg="white").place(x=30, y=40)

        # بخش اول: 2 رقم
        Entry(frame, textvariable=self.plate_part1, width=2, font=("Arial", 12),
              justify="center").place(x=80, y=38)

        # بخش دوم: حرف (Dropdown)
        self.letter_combo = ttk.Combobox(frame, textvariable=self.plate_part2,
                                         values=self.valid_letters, width=2,
                                         font=("Arial", 12), state="readonly")
        self.letter_combo.place(x=120, y=38)

        # بخش سوم: 3 رقم
        Entry(frame, textvariable=self.plate_part3, width=4, font=("Arial", 12),
              justify="center").place(x=180, y=38)

        Label(frame, text="ایران", bg="#444444", fg="white",
              font=("Arial", 10)).place(x=240, y=40)

        # بخش چهارم: 2 رقم (کد استان)
        Entry(frame, textvariable=self.plate_part4, width=3, font=("Arial", 12),
              justify="center").place(x=280, y=38)

        Label(frame, text="مثال: 12 ب 345 67", bg="#444444", fg="gray",
              font=("Arial", 8)).place(x=80, y=65)

        # مدل
        Label(frame, text="مدل:", bg="#444444", fg="white").place(x=30, y=100)
        Entry(frame, textvariable=self.model_var, width=30).place(x=80, y=98)

        # موبایل
        Label(frame, text="موبایل:", bg="#444444", fg="white").place(x=30, y=135)
        Entry(frame, textvariable=self.mobile_var, width=30).place(x=80, y=133)

        # طبقه
        Label(frame, text="طبقه:", bg="#444444", fg="white").place(x=30, y=170)
        Spinbox(frame, from_=1, to=8, textvariable=self.floor_var, width=28).place(x=80, y=168)

        # جای پارک
        Label(frame, text="جای پارک:", bg="#444444", fg="white").place(x=30, y=205)
        Spinbox(frame, from_=1, to=50, textvariable=self.place_var, width=28).place(x=80, y=203)

        # دکمه پارک
        Button(frame, text="ثبت و پارک", bg="green", fg="white",
               command=self.park_car).place(x=200, y=240, width=100)

    def create_exit_section(self):
        """بخش خروج خودرو با Dropdown"""
        frame = Frame(self.window, bg="#444444", bd=2, relief="groove")
        frame.place(x=30, y=340, width=490, height=100)

        Label(frame, text="خروج خودرو", font=("Arial", 12, "bold"),
              bg="#444444", fg="white").place(x=200, y=5)

        Label(frame, text="پلاک:", bg="#444444", fg="white").place(x=30, y=40)

        # Dropdown برای انتخاب پلاک
        self.exit_combo = ttk.Combobox(frame, textvariable=self.exit_plate_var,
                                        width=22, font=("Arial", 10), state="readonly")
        self.exit_combo.place(x=80, y=38)

        Label(frame, text="هزینه:", bg="#444444", fg="white").place(x=280, y=40)
        Entry(frame, textvariable=self.cost_var, width=10, state="readonly").place(x=340, y=38)

        Button(frame, text="خروج", bg="orange", fg="white",
               command=self.exit_car).place(x=430, y=35, width=45)

    def create_status_section(self):
        """بخش وضعیت پارکینگ"""
        frame = Frame(self.window, bg="#444444", bd=2, relief="groove")
        frame.place(x=30, y=450, width=490, height=60)

        Label(frame, text="وضعیت پارکینگ:", font=("Arial", 10, "bold"),
              bg="#444444", fg="white").place(x=20, y=10)

        self.status_label = Label(frame, text="0", font=("Arial", 10, "bold"),
                                  bg="#444444", fg="yellow")
        self.status_label.place(x=150, y=10)

        Label(frame, text="دستگاه داخل پارکینگ", bg="#444444", fg="white").place(x=180, y=10)

        Button(frame, text="بروزرسانی", bg="blue", fg="white",
               command=self.update_all).place(x=380, y=8, width=80)

    def make_plate(self):
        """ساخت پلاک کامل از بخش‌های جداگانه"""
        part1 = self.plate_part1.get().strip()
        part2 = self.plate_part2.get().strip()
        part3 = self.plate_part3.get().strip()
        part4 = self.plate_part4.get().strip()

        if not part1 or not part2 or not part3 or not part4:
            return None

        if not part1.isdigit() or len(part1) != 2:
            return None

        if not part3.isdigit() or len(part3) != 3:
            return None

        if not part4.isdigit() or len(part4) != 2:
            return None

        return f"{part1}{part2}{part3}{part4}"

    def get_parked_cars(self):
        """دریافت لیست پلاک خودروهای داخل پارکینگ"""
        parked_plates = []
        try:
            sessions = self.parking_controller.bl.session_list
            for session in sessions:
                if session.out_time is None:
                    parked_plates.append(session.car.plate)
        except:
            pass
        return parked_plates

    def update_exit_plates(self):
        """به‌روزرسانی لیست پلاک‌های داخل پارکینگ برای Dropdown خروج"""
        parked_plates = self.get_parked_cars()
        if parked_plates:
            self.exit_combo['values'] = parked_plates
            self.exit_plate_var.set(parked_plates[0])
        else:
            self.exit_combo['values'] = []
            self.exit_plate_var.set("")

    def update_all(self):
        """به‌روزرسانی همه چیز"""
        self.update_status()
        self.update_exit_plates()

    def park_car(self):
        """ثبت و پارک خودرو"""
        plate = self.make_plate()

        if not plate:
            messagebox.showerror("خطا", "پلاک را به درستی وارد کنید!\nفرمت: 12 ب 345 67")
            return

        model = self.model_var.get()
        mobile = self.mobile_var.get()
        floor = self.floor_var.get()
        place = self.place_var.get()

        if not model or not mobile:
            messagebox.showerror("خطا", "مدل و موبایل را وارد کنید!")
            return

        # ثبت خودرو
        result = self.car_controller.save(plate, model, mobile)

        if "Error" in result and "already exists" not in result:
            messagebox.showerror("خطا", result)
            return

        # پیدا کردن خودرو
        car = self.car_controller.find_by_plate(plate)
        if not car:
            messagebox.showerror("خطا", "خطا در پیدا کردن خودرو")
            return

        # پارک کردن
        try:
            spot = ParkSpot(place, floor)
            result = self.parking_controller.park_car(car, spot)

            if "Error" in result:
                messagebox.showerror("خطا", result)
            else:
                messagebox.showinfo("موفق", f"خودرو با پلاک {plate} با موفقیت پارک شد")
                # پاک کردن فرم
                self.plate_part1.set("")
                self.plate_part2.set("")
                self.plate_part3.set("")
                self.plate_part4.set("")
                self.model_var.set("")
                self.mobile_var.set("")
                self.floor_var.set(1)
                self.place_var.set(1)
                # به‌روزرسانی وضعیت و لیست پلاک‌ها
                self.update_all()
        except Exception as e:
            messagebox.showerror("خطا", str(e))

    def exit_car(self):
        """خروج خودرو از روی Dropdown"""
        plate = self.exit_plate_var.get()

        if not plate:
            messagebox.showerror("خطا", "پلاکی برای خروج وجود ندارد!")
            return

        result = self.parking_controller.exit_car(plate)

        if "Error" in result:
            messagebox.showerror("خطا", result)
            self.cost_var.set("")
        else:
            cost = result.replace("COST : ", "")
            self.cost_var.set(cost)
            messagebox.showinfo("خروج", f"خودرو با پلاک {plate} خارج شد.\nهزینه: {cost}")
            # به‌روزرسانی وضعیت و لیست پلاک‌ها
            self.update_all()
            # پاک کردن هزینه بعد از 2 ثانیه
            self.window.after(2000, lambda: self.cost_var.set(""))

    def update_status(self):
        """به‌روزرسانی تعداد ماشین‌های داخل پارکینگ"""
        try:
            sessions = self.parking_controller.bl.session_list
            active_count = 0
            for session in sessions:
                if session.out_time is None:
                    active_count += 1
            self.status_label.config(text=str(active_count))
        except:
            self.status_label.config(text="0")


if __name__ == "__main__":
    app = ParkingSystemView()