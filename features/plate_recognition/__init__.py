def read_plate_from_upload(*args, **kwargs):
    from .reader import read_plate_from_upload as _read_plate_from_upload

    return _read_plate_from_upload(*args, **kwargs)


__all__ = ["read_plate_from_upload"]
