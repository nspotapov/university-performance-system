from math import ceil


def mask_string(s: str, mask: str = "*", visible_percentage: float = 0.1) -> str:
    s_len = len(s)
    non_masked_count = ceil(s_len * visible_percentage)
    masked_string = (s[:non_masked_count] + mask *
                     (s_len - 2 * non_masked_count) + s[-non_masked_count:])
    return masked_string


def mask_email(email: str, mask: str = "*") -> str:
    domain = email[email.rfind("@"):]
    address = email[:email.find("@")]
    masked_email = mask_string(address, mask) + domain
    return masked_email
