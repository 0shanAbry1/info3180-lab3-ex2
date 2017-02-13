"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, flash

from .forms import ContactForm
import smtplib


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render the website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/contact/', methods=['GET','POST'])
def contact():
    """Render the website's contact page."""
    form = ContactForm() #Instance
    
    if request.method == 'POST': #POST request made
        if form.validate_on_submit(): #Form fields contain valid data
            from_name = request.form['clientName']
            from_email = request.form['clientEmail']
            subject = request.form['clientSubject']
            msg = request.form['clientMessage']
            
            send_email(from_name, from_email, subject, msg) #Handles composing and sending email
            flash(u'Your message has been sent successfully :) Thank You!', 'success') #Displays message upon success
            return redirect(url_for('home'))
        else:
            flash(u'Invalid data within form field(s)', 'danger')
    
    return render_template('contact.html', form=form)


###
# The functions below should be applicable to all Flask apps.
###

def send_email(from_name, from_email, subject, msg):
    """Compose and send email message to site owner(s)"""
    
    to_name = 'First Last' #Site Owner's Name 
    to_email = 'tositeowner@gmail.com' #Site Owner's Email Address (Must be a GMAIL account)
    
    message = """From: {} <{}>\nTo: {} <{}>\nSubject: {}\n\n{}"""
    
    message_to_send = message.format(from_name, from_email, to_name, to_email, subject, msg)
    
    #Credentials
    username = 'tositeowner@gmail.com' #Site Owner's Email Address (Must be a GMAIL account)
    password = '****************' #Generated Gmail App Password
    
    #Sending Mail
    server = smtplib.SMTP('smtp.gmail.com:587') #Gmail's Remote Mail Server & Port
    server.starttls() #Start TLS (Transport Layer Security)
    server.login(username, password) # Login using Credentials
    server.sendmail(from_email, to_email, message_to_send) #Blast Off!
    server.quit() #Close Connection


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")