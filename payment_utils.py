import qrcode

UPI_ID = "7067851830@ybl"   # yahan apni real UPI ID daalo
STORE_NAME = "BookHub"

def generate_upi_link(amount: float) -> str:
    name_encoded = STORE_NAME.replace(" ", "%20")
    return f"upi://pay?pa={UPI_ID}&pn={name_encoded}&am={amount:.2f}&cu=INR"

def generate_qr_image(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white").convert("RGB")