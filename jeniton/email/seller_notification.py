from decouple import config

def seller_mail_sender(data={}):
    if not data:
        return
    receipt = f'''
        <div style="display: flex;">
            <div style="
                font-family: Arial, sans-serif; line-height: 1.6; 
                max-width: 600px; width: 100%;
                border: 1px solid #f1f1f1;
                border-radius: 20px;
                margin: 0 auto;
                color: black;
                padding: 5px;
            ">
                <div 
                    style="
                        padding: 18px; 
                        text-align: center;
                        background-color: #ffffff;
                        border-radius: 20px;
                        color: white;
                    "
                >
                    <img style="max-width: 100%; width: 100px;" src="https://kidsmulticulturalworld.s3.us-east-2.amazonaws.com/media/kmw.jpg" alt="Kids Multicultural World">
                </div>

                <div
                    style="
                        padding: 10px; 
                        background-color: #f1f1f1;
                        border-radius: 18px;
                        margin-top: 5px;
                    "
                >
                    <div style="padding-bottom: 20px;">
                        <div style="border-bottom: 1px solid #fff;padding-bottom: 10px; padding-left: 20px; padding-right: 20px;">
                            <h2 style="text-align: center;">{data["title"] if data else "Sales alert!"}</h2>
                            <h3 style="text-align: center;">{data["message"] if data else "An order was received!"}</h3>
                        </div>
                        <div>
                            <div style="
                                    border-bottom: 1px solid #fff;
                                    padding: 20px; 
                                    margin-bottom: 10px;
                                "
                            >
                                <div style="margin-top: 20px; ">
                                    {f'<h4>{data["body"]}</h4>' if data else f'<h4 style="text-align: center;">Please visit your <a href="{config("FRONTEND_URL")}/user/placed-orders" style="text-decoration: none;">order dashboard</a> for more detail</h4>'}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="padding-bottom: 20px;">
                            Best regards,
                            <div style="font-weight: 700;">
                                FAITTONE
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    '''
    others.append(receipt)
    others.append(delivery)