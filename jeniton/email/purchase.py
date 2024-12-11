def purchase_mail_sender(data,others):
    if not data:
        return
    all_items_list = ""
    for i in data["item"]:
        all_items_list += f'''
            <div style="display: grid; grid-template-columns: 10fr 2fr;">
                <p style="font-weight: 600;">{f'[{i["counter"]}]-' if i["counter"] else ''}{i["name"]}</p>
                <p>{i["price"]}</p>
            </div>
        '''
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
                            <h2 style="text-align: center;">Your order is on it's way!</h2>
                            <h3 style="text-align: center;">Here are the details:</h3>
                        </div>
                        <div>
                            <div style="
                                    border-bottom: 1px solid #fff;
                                    padding: 20px; 
                                    margin-bottom: 10px;
                                    display: flex;
                                    flex-direction: column;
                                "
                            >
                                {all_items_list}
                                <div style="display: grid;margin-top: 20px; grid-template-columns: 10fr 2fr;">
                                    <h3>Total</h3>
                                    <p>{data["price"]}</p>
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