from flask import Flask, render_template, flash, redirect, request, url_for
from ContactForm import ContactForm
import csv

app = Flask(__name__)
app.config["SECRET_KEY"] = "azakiohiehzyatariq123"

@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        with open("form_data.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([form.name.data, form.email.data, form.message.data])
        flash("Message sent successfully!")
        return redirect(url_for("home"))
    return render_template("index.html", form=form)

# رمز الأمان المخصص
SECURITY_CODE = 'ayatariq123'

@app.route('/view_csv', methods=['GET', 'POST'])
def view_csv():
    if request.method == 'POST':
        # الحصول على الرمز من النموذج
        user_code = request.form.get('code')
        if user_code == SECURITY_CODE:
            with open('form_data.csv', 'r') as file:
                reader = csv.reader(file)
                data = [row for row in reader]
            return render_template('view_csv.html', data=data)
        else:
            return "رمز غير صحيح. يرجى المحاولة مرة أخرى.", 403
    
    # عرض نموذج إدخال الرمز
    return render_template('enter_code.html')

if __name__ == "__main__":
    app.run(debug=True)
