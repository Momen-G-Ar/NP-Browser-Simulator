start_html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body style='display:flex; flex-direction: column; justify-content:center; align-items: center; height: 90vh; gap: 10px'>
        '''
end_html = '''
            </body>
            </html>
        '''
invalid_credentials_html = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body style='display:flex; flex-direction: column; justify-content:center; align-items: center; height: 90vh; gap: 10px'>
                <h1 style='color: red'> Invalid Credentials </h1>
            </body>
            </html>
'''

our_items = '''
            <h2>Our Items</h2>
        '''
item = '''
            <div style='border: 1px solid #000; width: 200px; padding: 5px; border-radius: 3px; margin-top: 10px; display: flex; flex-direction: column; align-items: center'>
                <span>Name: {}</span>
                <span>Price: {}</span>
            </div>
        '''

item_added_successfully = '''<h1 style='color: green'> Item Added Successfully </h1>'''
