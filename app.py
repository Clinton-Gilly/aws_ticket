from flask import Flask, render_template, request, send_file
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
import io

app = Flask(__name__)

def create_elegant_ticket(name, gender, event_name, date, time, price, address):
    # Create a new image with a dark gradient background
    ticket_width, ticket_height = 1220, 450
    ticket = Image.new('RGB', (ticket_width, ticket_height))
    draw = ImageDraw.Draw(ticket)

    # Create gradient background
    for y in range(ticket_height):
        r = int(25 * (1 - y / ticket_height))
        g = int(25 * (1 - y / ticket_height))
        b = int(35 * (1 - y / ticket_height))
        draw.line([(0, y), (ticket_width, y)], fill=(r, g, b))

    # Try to use a nicer font, fall back to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 30)
        details_font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        title_font = ImageFont.load_default().font_variant(size=60)
        subtitle_font = ImageFont.load_default().font_variant(size=30)
        details_font = ImageFont.load_default().font_variant(size=20)

    # Add main title (ATTENDEE + name)
    draw.text((50, 40), f"ATTENDEE: {name.upper()}", font=title_font, fill='white')

    # Add gender
    draw.text((50, 110), f"Gender: {gender}", font=details_font, fill='white')

    # Add event name
    draw.text((50, 140), event_name.upper(), font=subtitle_font, fill='white')

    # Add event details
    draw.text((50, 190), f"Date: {date}", font=details_font, fill='white')
    draw.text((50, 220), f"Time: {time}", font=details_font, fill='white')
    draw.text((50, 250), f"Price: ${price}", font=details_font, fill='white')
    draw.text((50, 280), f"Address: {address}", font=details_font, fill='white')

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=5, border=0)
    qr.add_data(f"Name: {name}, Gender: {gender}, Event: {event_name}, Date: {date}, Time: {time}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="white", back_color=None)
    
    # Paste QR code onto ticket
    ticket.paste(qr_img, (ticket_width - 270, 50))

    # Add decorative elements
   # draw.line([(30, 30), (30, ticket_height-30)], fill='white', width=2)
   # draw.line([(30, 30), (ticket_width-30, 30)], fill='white', width=2)
   # draw.line([(ticket_width-30, 30), (ticket_width-30, ticket_height-30)], fill='white', width=2)
    #draw.line([(30, ticket_height-30), (ticket_width-30, ticket_height-30)], fill='white', width=2)

    return ticket

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        ticket = create_elegant_ticket(
            name=name,
            gender=gender,
            event_name="AWS Student Community Day",
            date="Oct 5TH, 2024",
            time="8:30 PM",
            price="free",
            address="Zetech University"
        )
        
        img_io = io.BytesIO()
        ticket.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name=f'{name.replace(" ", "_")}_ticket.png')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)