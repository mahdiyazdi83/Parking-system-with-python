from flask import Flask, render_template, request, jsonify
from controller.car_controller import CarController
from controller.parking_session_controller import ParkingSessionController
from model.entity.park_spot import ParkSpot

app = Flask(__name__)

car_controller = CarController()
parking_controller = ParkingSessionController()


def format_plate(plate):
    """12ب34511 → 12 ب 345 - ایران 11"""
    try:
        p = str(plate).strip()
        for i, c in enumerate(p):
            if '\u0600' <= c <= '\u06FF':
                digits_before = p[:i]
                letter = p[i]
                rest = p[i+1:]
                digits_mid = rest[:3]
                province = rest[3:]
                return f"{digits_before} {letter} {digits_mid} - ایران {province}"
        return plate
    except:
        return plate


def get_active_sessions():
    sessions = parking_controller.bl.session_list
    return [s for s in sessions if s.out_time is None]


def get_spot_map():
    """Returns 8 floors x 50 spots with occupied info"""
    active = get_active_sessions()
    occupied = {(s.spot.floor, s.spot.place): s.car.plate for s in active}

    floors = []
    for floor in range(1, 9):
        spots = []
        for place in range(1, 51):
            key = (floor, place)
            raw_plate = occupied.get(key, None)
            spots.append({
                "place": place,
                "floor": floor,
                "occupied": key in occupied,
                "plate": raw_plate,
                "plate_display": format_plate(raw_plate) if raw_plate else None
            })
        floors.append({"floor": floor, "spots": spots})
    return floors


@app.route("/")
def index():
    active_sessions = get_active_sessions()
    floors = get_spot_map()
    total_spots = 8 * 50
    occupied_count = len(active_sessions)
    return render_template("index.html",
                           active_sessions=active_sessions,
                           floors=floors,
                           total_spots=total_spots,
                           occupied_count=occupied_count,
                           free_count=total_spots - occupied_count,
                           format_plate=format_plate)


@app.route("/park", methods=["POST"])
def park():
    data = request.json
    plate = data.get("plate", "").strip()
    model = data.get("model", "").strip()
    mobile = data.get("mobile", "").strip()
    floor = int(data.get("floor", 1))
    place = int(data.get("place", 1))

    if not plate or not model or not mobile:
        return jsonify({"success": False, "message": "همه فیلدها الزامی هستند"})

    result = car_controller.save(plate, model, mobile)
    if "Error" in result and "already exists" not in result:
        return jsonify({"success": False, "message": result})

    car = car_controller.find_by_plate(plate)
    if not car:
        return jsonify({"success": False, "message": "خطا در یافتن خودرو"})

    try:
        spot = ParkSpot(place, floor)
        result = parking_controller.park_car(car, spot)
        if "Error" in result:
            return jsonify({"success": False, "message": result})
        return jsonify({"success": True, "message": f"خودرو {format_plate(plate)} پارک شد"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route("/exit", methods=["POST"])
def exit_car():
    data = request.json
    plate = data.get("plate", "").strip()
    if not plate:
        return jsonify({"success": False, "message": "پلاک وارد نشده"})

    result = parking_controller.exit_car(plate)
    if "Error" in result:
        return jsonify({"success": False, "message": result})

    cost = result.replace("COST : ", "").replace("$", "")
    return jsonify({
        "success": True,
        "message": f"خودرو {format_plate(plate)} خارج شد",
        "cost": cost,
        "plate_display": format_plate(plate)
    })


@app.route("/api/spots")
def api_spots():
    return jsonify(get_spot_map())


@app.route("/api/status")
def api_status():
    active = get_active_sessions()
    total = 8 * 50
    return jsonify({
        "occupied": len(active),
        "free": total - len(active),
        "total": total
    })


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
