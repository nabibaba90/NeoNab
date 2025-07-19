from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = "neonabi_super_secret_key"  # Bunu gizli tut!

# Basit kullanıcı veritabanı (demo amaçlı, gerçek projede DB kullan)
USERS = {"admin": "123456"}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            flash("Lütfen giriş yapınız!", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USERS and USERS[username] == password:
            session["username"] = username
            flash("Giriş başarılı!", "success")
            return redirect(url_for("index"))
        else:
            flash("Kullanıcı adı veya şifre yanlış!", "error")
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password1 = request.form.get("password")
        password2 = request.form.get("password2")

        if not username or not password1 or not password2:
            flash("Tüm alanları doldurun!", "error")
        elif password1 != password2:
            flash("Şifreler uyuşmuyor!", "error")
        elif username in USERS:
            flash("Bu kullanıcı zaten kayıtlı!", "error")
        else:
            USERS[username] = password1
            flash("Kayıt başarılı! Giriş yapabilirsiniz.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/logout')
@login_required
def logout():
    session.pop("username", None)
    flash("Başarıyla çıkış yapıldı.", "success")
    return redirect(url_for("login"))

@app.route('/sorgu/<sorgu_tipi>', methods=['GET', 'POST'])
@login_required
def sorgu(sorgu_tipi):
    sonuc = None
    try:
        if request.method == 'POST':
            if sorgu_tipi == "adsoyad":
                ad = request.form.get("ad")
                soyad = request.form.get("soyad")
                url = f"https://api.hexnox.pro/sowixapi/adsoyadilice.php?ad={ad}&soyad={soyad}"

            elif sorgu_tipi == "adsoyadil":
                ad = request.form.get("ad")
                soyad = request.form.get("soyad")
                il = request.form.get("il")
                url = f"https://api.hexnox.pro/sowixapi/adsoyadilce.php?ad={ad}&soyad={soyad}&il={il}"

            elif sorgu_tipi == "telegram":
                username = request.form.get("username")
                url = f"https://api.hexnox.pro/sowixapi/telegram_sorgu.php?username={username}"

            elif sorgu_tipi == "tc":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/tcpro.php?tc={tc}"

            elif sorgu_tipi == "tcgsm":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/tcgsm.php?tc={tc}"

            elif sorgu_tipi == "tapu":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/tapu.php?tc={tc}"

            elif sorgu_tipi == "sulale":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/sulale.php?tc={tc}"

            elif sorgu_tipi == "okulno":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/okulno.php?tc={tc}"

            elif sorgu_tipi == "isyeriyetkili":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/isyeriyetkili.php?tc={tc}"

            elif sorgu_tipi == "isyeri":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/isyeri.php?tc={tc}"

            elif sorgu_tipi == "hane":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/hane.php?tc={tc}"

            elif sorgu_tipi == "gsmdetay":
                gsm = request.form.get("gsm")
                url = f"https://api.hexnox.pro/sowixapi/gsmdetay.php?gsm={gsm}"

            elif sorgu_tipi == "gsm":
                gsm = request.form.get("gsm")
                url = f"https://api.hexnox.pro/sowixapi/gsm.php?gsm={gsm}"

            elif sorgu_tipi == "baba":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/baba.php?tc={tc}"

            elif sorgu_tipi == "anne":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/anne.php?tc={tc}"

            elif sorgu_tipi == "aile":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/aile.php?tc={tc}"

            elif sorgu_tipi == "tcgenel":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/tc.php?tc={tc}"

            elif sorgu_tipi == "adres":
                tc = request.form.get("tc")
                url = f"https://api.hexnox.pro/sowixapi/adres.php?tc={tc}"

            else:
                flash("Geçersiz sorgu tipi!", "error")
                return redirect(url_for("index"))

            r = requests.get(url)
            sonuc = r.text

    except Exception as e:
        flash(f"API çağrısı sırasında hata oluştu: {str(e)}", "error")

    return render_template("sorgu.html", sorgu_tipi=sorgu_tipi, sonuc=sonuc)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
