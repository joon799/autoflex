# =============================================
# app.py - 오토플렉스 통합 웹사이트
# 회사 홍보 + 쇼핑몰 + 관리자 페이지 통합
# =============================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = "autoflex-secret-key-2024"

# =============================================
# ✏️ 설정값 - 여기를 수정하세요!
# =============================================
CONFIG = {
    # 관리자 로그인
    "admin_id": "admin",
    "admin_pw": "autoflex1234",      # ← 꼭 변경하세요!

    # 이메일 (Gmail)
    "email_sender":   "your_email@gmail.com",   # ← 본인 Gmail
    "email_password": "your_app_password",       # ← Gmail 앱 비밀번호
    "email_receiver": "your_email@gmail.com",    # ← 알림 받을 이메일

    # 무통장 계좌
    "bank_name":    "국민은행",
    "bank_account": "123-456-789012",            # ← 실제 계좌번호
    "bank_holder":  "오토플렉스",
}

# =============================================
# ✏️ 회사 정보
# =============================================
COMPANY = {
    "name":         "㈜오토플렉스",
    "name_en":      "AUTOFLEX",
    "slogan":       "실리콘 제조 생산 전문업체",
    "description":  "㈜오토플렉스는 기계 금형 기술을 바탕으로 고품질 실리콘 제품을 생산하는 전문 제조업체입니다. Key-pad 생산 노하우와 다양한 생산 경험을 통해 고객에게 최고의 제품을 제공합니다.",
    "phone":        "031-959-6031",
    "mobile":       "010-9080-9615",
    "email":        "autoflex@autoflex.kr",
    "address":      "경기도 파주시 자운서원로410-11",
    "address_detail": "경기도 파주시 법원읍 동문리 619-1",
    "ceo":          "허남혁",
    "business_no":  "141-81-06639",
    "hours":        "평일 09:30 - 17:00",
}

# =============================================
# ✏️ 실리콘 제품 라인업 (홍보용)
# =============================================
PRODUCT_LINES = [
    {
        "id":          1,
        "type":        "Rubber Type",
        "description": "일반 고무 실리콘을 금형에 넣어 압축 성형하는 방식으로 제작된 제품입니다. 내열성과 내화학성이 뛰어나며 다양한 산업 분야에 적용됩니다.",
        "features":    ["내열성 우수", "내화학성 강함", "다양한 경도 선택 가능", "대량 생산 적합"],
        "icon":        "🔴",
        "color":       "#C0392B",
    },
    {
        "id":          2,
        "type":        "LSR Type",
        "description": "액상 실리콘 고무(Liquid Silicone Rubber)를 사출 성형하는 방식입니다. 정밀도가 높고 복잡한 형상 제작에 최적화되어 있습니다.",
        "features":    ["고정밀 사출 성형", "복잡한 형상 구현", "의료·식품 등급 가능", "자동화 생산"],
        "icon":        "🔵",
        "color":       "#2980B9",
    },
    {
        "id":          3,
        "type":        "FILM Type",
        "description": "실리콘 필름을 활용한 제품으로 얇고 유연한 특성을 가집니다. 전자기기의 보호 필름, 절연재 등에 활용됩니다.",
        "features":    ["초박형 설계", "뛰어난 유연성", "전기 절연성", "표면 보호 기능"],
        "icon":        "🟡",
        "color":       "#F39C12",
    },
    {
        "id":          4,
        "type":        "SUS Type",
        "description": "스테인리스(SUS)와 실리콘을 결합한 복합 제품입니다. 금속의 강도와 실리콘의 탄성을 동시에 요구하는 부품에 사용됩니다.",
        "features":    ["금속+실리콘 복합", "고강도 내구성", "부식 방지", "산업용 특수 부품"],
        "icon":        "⚙️",
        "color":       "#7F8C8D",
    },
]

# =============================================
# ✏️ 판매 상품 목록 (쇼핑몰용)
# =============================================
SHOP_PRODUCTS = [
    {
        "id":           1,
        "name":         "실리콘 키패드 (Rubber Type)",
        "price":        45000,
        "description":  "오토플렉스 자체 금형으로 제작한 고내열 실리콘 키패드. 산업용·가전용으로 적합합니다.",
        "detail":       "내열성 우수, 다양한 경도 선택, 대량 주문 가능, 맞춤 제작 가능",
        "icon":         "🔴",
        "stock":        100,
        "shipping_fee": 3000,
    },
    {
        "id":           2,
        "name":         "LSR 사출 실리콘 부품",
        "price":        89000,
        "description":  "고정밀 LSR 사출 공정으로 생산된 실리콘 부품. 의료·식품 등급 소재 사용 가능합니다.",
        "detail":       "고정밀 사출 성형, 복잡한 형상 구현, 의료·식품 등급, 자동화 생산",
        "icon":         "🔵",
        "stock":        50,
        "shipping_fee": 3000,
    },
    {
        "id":           3,
        "name":         "실리콘 보호 필름 (FILM Type)",
        "price":        28000,
        "description":  "초박형 실리콘 필름으로 전자기기 보호 및 절연 용도로 사용됩니다.",
        "detail":       "초박형 설계, 뛰어난 유연성, 전기 절연성, 표면 보호 기능",
        "icon":         "🟡",
        "stock":        200,
        "shipping_fee": 2500,
    },
    {
        "id":           4,
        "name":         "SUS+실리콘 복합 부품",
        "price":        135000,
        "description":  "스테인리스와 실리콘을 결합한 복합 부품. 고강도와 탄성이 동시에 필요한 산업 현장에 최적입니다.",
        "detail":       "금속+실리콘 복합, 고강도 내구성, 부식 방지, 산업용 특수 부품",
        "icon":         "⚙️",
        "stock":        30,
        "shipping_fee": 5000,
    },
]

# 회사 강점
STRENGTHS = [
    {"title": "Key-pad 생산 노하우", "desc": "오랜 경험으로 쌓인 키패드 전문 생산 기술 보유", "icon": "🏆"},
    {"title": "다양한 생산 경험",    "desc": "다품종 소량부터 대량 생산까지 폭넓은 경험",   "icon": "🔧"},
    {"title": "금형 관리 기술",      "desc": "자체 금형 제작 및 정밀 유지관리 능력 보유",   "icon": "⚙️"},
    {"title": "기술 혁신",           "desc": "신기술 확보와 끊임없는 연구개발로 경쟁력 강화","icon": "💡"},
]


# =============================================
# 데이터베이스
# =============================================
def init_db():
    conn = sqlite3.connect("orders.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no      TEXT NOT NULL,
            name          TEXT NOT NULL,
            phone         TEXT NOT NULL,
            email         TEXT,
            zipcode       TEXT,
            address1      TEXT NOT NULL,
            address2      TEXT,
            product_id    INTEGER NOT NULL,
            product_name  TEXT NOT NULL,
            quantity      INTEGER NOT NULL,
            price         INTEGER NOT NULL,
            shipping_fee  INTEGER NOT NULL,
            total_price   INTEGER NOT NULL,
            memo          TEXT,
            status        TEXT DEFAULT '입금대기',
            created_at    TEXT NOT NULL
        )
    """)
    # 문의 테이블
    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            email      TEXT NOT NULL,
            phone      TEXT,
            product    TEXT,
            message    TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_read    INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect("orders.db")
    conn.row_factory = sqlite3.Row
    return conn

def generate_order_no():
    conn = get_db()
    today = datetime.now().strftime("%Y%m%d")
    count = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE order_no LIKE ?", (f"AF-{today}-%",)
    ).fetchone()[0]
    conn.close()
    return f"AF-{today}-{count+1:04d}"

def send_order_email(order):
    try:
        subject = f"[오토플렉스] 새 주문 접수 - {order['order_no']}"
        body = f"""
새 주문이 접수되었습니다!

주문번호: {order['order_no']}
주문일시: {order['created_at']}

[주문자]
이름: {order['name']} / 연락처: {order['phone']}
이메일: {order['email']}

[배송지]
{order['address1']} {order['address2']}
메모: {order['memo'] or '없음'}

[상품]
{order['product_name']} × {order['quantity']}개
총 결제금액: {order['total_price']:,}원

[입금 안내]
{CONFIG['bank_name']} {CONFIG['bank_account']} ({CONFIG['bank_holder']})
입금자명: {order['name']}

관리자 페이지: http://localhost:5000/admin
        """
        msg = MIMEMultipart()
        msg["From"]    = CONFIG["email_sender"]
        msg["To"]      = CONFIG["email_receiver"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(CONFIG["email_sender"], CONFIG["email_password"])
            smtp.send_message(msg)
        print(f"✅ 주문 이메일 발송 완료")
    except Exception as e:
        print(f"⚠️ 이메일 발송 실패: {e}")

def send_contact_email(name, email, message):
    try:
        subject = f"[오토플렉스] 새 문의 - {name}"
        body = f"이름: {name}\n이메일: {email}\n\n{message}"
        msg = MIMEMultipart()
        msg["From"]    = CONFIG["email_sender"]
        msg["To"]      = CONFIG["email_receiver"]
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(CONFIG["email_sender"], CONFIG["email_password"])
            smtp.send_message(msg)
    except Exception as e:
        print(f"⚠️ 문의 이메일 발송 실패: {e}")


# =============================================
# 홍보 사이트 라우팅
# =============================================

@app.route("/")
def index():
    return render_template("index.html",
                           company=COMPANY,
                           product_lines=PRODUCT_LINES,
                           strengths=STRENGTHS,
                           shop_products=SHOP_PRODUCTS)

@app.route("/about")
def about():
    return render_template("about.html", company=COMPANY, strengths=STRENGTHS)

@app.route("/products")
def products():
    return render_template("products.html", company=COMPANY, product_lines=PRODUCT_LINES)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name    = request.form.get("name")
        email   = request.form.get("email")
        phone   = request.form.get("phone", "")
        product = request.form.get("product", "")
        message = request.form.get("message")
        conn = get_db()
        conn.execute("""
            INSERT INTO contacts (name, email, phone, product, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, phone, product, message,
              datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        send_contact_email(name, email, message)
        flash("문의가 접수되었습니다. 빠른 시일 내에 연락드리겠습니다.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html", company=COMPANY)


# =============================================
# 쇼핑몰 라우팅
# =============================================

@app.route("/shop")
def shop():
    return render_template("shop.html",
                           company=COMPANY,
                           shop_products=SHOP_PRODUCTS,
                           config=CONFIG)

@app.route("/shop/product/<int:product_id>")
def shop_product(product_id):
    item = next((p for p in SHOP_PRODUCTS if p["id"] == product_id), None)
    if not item:
        flash("존재하지 않는 상품입니다.", "error")
        return redirect(url_for("shop"))
    return render_template("shop_product.html",
                           company=COMPANY,
                           product=item,
                           config=CONFIG)

@app.route("/shop/order", methods=["POST"])
def shop_order():
    product_id = int(request.form.get("product_id"))
    quantity   = int(request.form.get("quantity", 1))
    item = next((p for p in SHOP_PRODUCTS if p["id"] == product_id), None)
    if not item:
        flash("상품을 찾을 수 없습니다.", "error")
        return redirect(url_for("shop"))
    if quantity > item["stock"]:
        flash(f"재고가 부족합니다. (재고: {item['stock']}개)", "error")
        return redirect(url_for("shop_product", product_id=product_id))

    total_price = item["price"] * quantity + item["shipping_fee"]
    order_data = {
        "order_no":     generate_order_no(),
        "name":         request.form.get("name"),
        "phone":        request.form.get("phone"),
        "email":        request.form.get("email", ""),
        "zipcode":      request.form.get("zipcode", ""),
        "address1":     request.form.get("address1"),
        "address2":     request.form.get("address2", ""),
        "product_id":   product_id,
        "product_name": item["name"],
        "quantity":     quantity,
        "price":        item["price"],
        "shipping_fee": item["shipping_fee"],
        "total_price":  total_price,
        "memo":         request.form.get("memo", ""),
        "status":       "입금대기",
        "created_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    conn = get_db()
    conn.execute("""
        INSERT INTO orders
        (order_no, name, phone, email, zipcode, address1, address2,
         product_id, product_name, quantity, price, shipping_fee,
         total_price, memo, status, created_at)
        VALUES
        (:order_no, :name, :phone, :email, :zipcode, :address1, :address2,
         :product_id, :product_name, :quantity, :price, :shipping_fee,
         :total_price, :memo, :status, :created_at)
    """, order_data)
    conn.commit()
    conn.close()
    send_order_email(order_data)
    session["last_order"] = order_data
    return redirect(url_for("shop_order_complete"))

@app.route("/shop/complete")
def shop_order_complete():
    order_data = session.get("last_order")
    if not order_data:
        return redirect(url_for("shop"))
    return render_template("shop_complete.html",
                           order=order_data,
                           config=CONFIG)


# =============================================
# 관리자 페이지
# =============================================

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_orders"))
    if request.method == "POST":
        if (request.form.get("admin_id") == CONFIG["admin_id"] and
                request.form.get("admin_pw") == CONFIG["admin_pw"]):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_orders"))
        flash("아이디 또는 비밀번호가 틀렸습니다.", "error")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin"))

@app.route("/admin/orders")
def admin_orders():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))
    status_filter = request.args.get("status", "전체")
    conn = get_db()
    if status_filter == "전체":
        orders = conn.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    else:
        orders = conn.execute(
            "SELECT * FROM orders WHERE status=? ORDER BY created_at DESC",
            (status_filter,)).fetchall()
    stats = conn.execute("""
        SELECT COUNT(*) as total,
               SUM(CASE WHEN status='입금대기' THEN 1 ELSE 0 END) as pending,
               SUM(CASE WHEN status='입금확인' THEN 1 ELSE 0 END) as confirmed,
               SUM(CASE WHEN status='배송중'   THEN 1 ELSE 0 END) as shipping,
               SUM(CASE WHEN status='배송완료' THEN 1 ELSE 0 END) as done,
               SUM(total_price) as revenue
        FROM orders
    """).fetchone()
    # 읽지 않은 문의 수
    unread = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE is_read=0").fetchone()[0]
    conn.close()
    return render_template("admin_orders.html",
                           orders=orders, stats=stats,
                           status_filter=status_filter, unread=unread)

@app.route("/admin/order/<int:order_id>/status", methods=["POST"])
def update_status(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))
    new_status = request.form.get("status")
    if new_status in ["입금대기", "입금확인", "배송중", "배송완료", "취소"]:
        conn = get_db()
        conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
        conn.commit()
        conn.close()
        flash(f"주문 상태가 [{new_status}]로 변경되었습니다.", "success")
    return redirect(url_for("admin_orders"))

@app.route("/admin/order/<int:order_id>")
def admin_order_detail(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))
    conn = get_db()
    order = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    conn.close()
    if not order:
        flash("주문을 찾을 수 없습니다.", "error")
        return redirect(url_for("admin_orders"))
    return render_template("admin_order_detail.html", order=order)

@app.route("/admin/contacts")
def admin_contacts():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))
    conn = get_db()
    contacts = conn.execute(
        "SELECT * FROM contacts ORDER BY created_at DESC").fetchall()
    # 전부 읽음 처리
    conn.execute("UPDATE contacts SET is_read=1")
    conn.commit()
    conn.close()
    return render_template("admin_contacts.html", contacts=contacts)


# =============================================
# 실행
# =============================================
if __name__ == "__main__":
    init_db()
    print("🚀 오토플렉스 통합 웹사이트 시작!")
    print("🏠 홈:      http://localhost:5000")
    print("🛒 쇼핑몰:  http://localhost:5000/shop")
    print("🔐 관리자:  http://localhost:5000/admin")
    app.run(debug=True, host="0.0.0.0", port=5000)