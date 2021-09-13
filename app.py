#Flask is a web framework which allows us to create web applications
#Twilio App or Twilio API allows us to send messages to the registered whatsapp no.
import requests
from flask import Flask, render_template, request
from twilio.rest import Client
#import requests_cache

account_sid = 'ACb4abb66cb74312ccb4cb7f241a952142'
auth_token ='0c807cfaa83352592b848da42f339093'

client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')
#App is an interface b/w your web server and your web pages

@app.route('/')
def registeration_form():
    return render_template('login_page.html')

@app.route('/login_page', methods=['GET','POST'])
def login_registeration_details():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['srcst']
    source_dt = request.form['srcdt']
    destination_st = request.form['destst']
    destination_dt = request.form['destdt']
    phno = request.form['phno']
    id_proof = request.form['aadharno']
    date = request.form['date']
    full_name = first_name+"."+last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    count = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((count/pop)*100)
    if travel_pass<30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="whatsapp:+917702466213", from_="whatsapp:+14155238886",
        body = "Hello "+full_name+". Your travel from "+source_dt+" to "+destination_dt+" has been "+status+
               " on "+date+".");

        return render_template('user_registeration_details.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phno, var8=date, var9=status)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to="whatsapp:+917702466213", from_="whatsapp:+14155238886",
             body = "Hello " + full_name + ". Your travel from " + source_dt + " to " + destination_dt + " has been " + status +
                    " on " + date + ". Apply later.");

        return render_template('user_registeration_details.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phno, var8=date, var9=status)

if __name__ == '__main__':
    app.run(port=9001, debug=True)