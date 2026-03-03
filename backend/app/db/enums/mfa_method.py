from enum import Enum


class MFAMethod(str, Enum):
    TOTP = "TOTP"
    OTP = "OTP"
