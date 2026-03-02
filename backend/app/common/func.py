def mask_email(email: str, mask: str = "*") -> str:
    domain = email[email.find("@"):]
    address = email[:email.find("@")]
    address_len = len(address)
    non_masked_count = round(len(address) * 0.05)
    masked_email = address[:non_masked_count + 1] + mask * (address_len - non_masked_count) + domain
    return masked_email
