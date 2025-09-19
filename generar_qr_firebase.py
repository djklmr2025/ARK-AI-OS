import qrcode
from PIL import Image

# Configuración de Firebase (reemplaza con tus propios datos)
firebase_config = {
    "apiKey": "tu_api_key",
    "authDomain": "tu_proyecto.firebaseapp.com",
    "projectId": "tu_proyecto_id",
    "storageBucket": "tu_proyecto.appspot.com",
    "messagingSenderId": "tu_sender_id",
    "appId": "tu_app_id"
}

# Convertir el diccionario a una cadena con formato
config_str = "\n".join([f"{key}: {value}" for key, value in firebase_config.items()])

# Crear instancia de QRCode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alto nivel de corrección de errores
    box_size=10,
    border=4,
)

# Añadir datos al QR
qr.add_data(config_str)
qr.make(fit=True)

# Crear imagen del QR
img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

# (Opcional) Añadir un logo en el centro
try:
    logo = Image.open('logo.png')  # Reemplaza con la ruta de tu logo
    logo_size = 50
    logo = logo.resize((logo_size, logo_size))
    
    pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
    img.paste(logo, pos)
except:
    print("Logo no encontrado. Generando QR sin logo.")

# Guardar la imagen
img.save('firebase_qr.png')
print("Código QR generado como 'firebase_qr.png'")