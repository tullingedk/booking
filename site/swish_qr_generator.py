import qrcode
import qrcode.image.svg

# normal, bc
amount_types = ["100", "50"]

def generate_swish_qr(firstname, lastname, school_class, booking_type):
    amount = amount_types[booking_type]

    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4,
    )

    data = "C+46730333185;{};{}+{}+{};0".format(str(amount), str(firstname), str(lastname), str(school_class))

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    
    img.save("static/temp_swish.png")