from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def sender_func(user,data):
    receipt = f'''
        <p>
            We are pleased to inform you that the payment of <span style="color: #28A745;">$ {data["price"]}</span> associated
             with Transaction <span style="color: #343A40; font-weight: 700;">ID {data["id"]}</span> has been successfully processed. And 
             your order is on its way.
        </p>
    '''
    delivery= f'''
        <p>
            We are thrilled to inform you that your recent order with <span style="color: #343A40; font-weight: 700;">ID {data["id"]}</span> has been successfully processed and delivered to the provided address. We trust that you will enjoy your new item{"s" if data["counter"] > 1 else ""}.
        </p>
    '''
    html_massage = f'''
    <body 
        style="
            font-family:  -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
            'Oxygen','Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
                sans-serif;
            color: #3F3F1C;
            background-color: #f1f1f1;
        "
    >
        <div style="padding-top: 25px;">
            <h1 style="text-align: center; margin-top: 20px;">
                <span style="color: #3F3F1C; font-size: 30px; font-weight: 900 !important;">
                    <b>
                        Krys Patra
                    </b>
                </span>
            </h1>
        </div>
        <div 
            style="
                max-width: 600px;
                background-color: #fff;
                margin: 20px auto;
                border-radius: 3px;
                padding: 20px;
                font-weight: 500;
            "
        >
            <div
                style="
                    text-align: center;
                    font-size: 20px;
                "
            >
                {data["title"]}
            </div>
            <p>
                <p>
                    {receipt if data["receipt"] else delivery}
                </p>
                <p>
                    {data["item"] if data["receipt"] else ""}
                </p>
                If you have any questions or concerns regarding this transaction, please
                feel free to <a href="mailto:emial@kryspatra.com">reach out to our 
                customer support team.</a> 

                <p>
                    Thank you for choosing our services.
                </p>

                <div>
                    Best regards,
                </div>
                <div>
                    Krystpatra team
                </div>
            </p>
            
        </div>
        <div
            style="
                max-width: 600px;
                margin: 20px auto;
                padding: 0 20px;
                font-size: 14px;
            "
        >
            
            <p 
                style="
                    text-align: center;
                    padding-bottom: 25px;
                "
            >
                <span>
                    <a href="mailto:kryspatra.services.com" style="color:#B19999 !important; text-decoration: none;">
                        kryspatra.services.com
                    </a>
                </span>
                <span style="color:#B19999 !important; text-decoration: none;padding: 0 2px;">|</span>
                <span>
                    <a href="https://www.kryspatra.com" style="color:#B19999 !important; text-decoration: none;" target="_blank">
                        kryspatra.com
                    </a>
                </span>
            </p>
        </div>
    </body>

    '''
    
    subject, to = f"Successful Payment Confirmation - Transaction ID: {data['id']}" if data["receipt"] else f'Order Delivery Confirmation - Order ID: {data["id"]}', user
    text_content = ''
    form_email = settings.ADMIN_EMAIL_ADDRESSS
    msg = EmailMultiAlternatives(subject, text_content,form_email, [to])
    msg.attach_alternative(html_massage, "text/html")
    msg.send(fail_silently=True)



