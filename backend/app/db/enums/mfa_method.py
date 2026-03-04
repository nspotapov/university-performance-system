from enum import StrEnum


class MFAMethod(StrEnum):
    TOTP = "TOTP"
    OTP = "OTP"
