# =============================================
# app.py - 웹사이트의 핵심 파이썬 파일
# Flask: 파이썬으로 웹사이트를 만드는 도구
# =============================================

from flask import Flask, render_template, request, flash, redirect, url_for

# Flask 앱 만들기
app = Flask(__name__)
app.secret_key = "autoflex-secret-key"  # 폼 알림 메시지에 필요한 비밀 키

# =============================================
# 회사 정보 - 여기를 수정하면 전체에 반영돼요! ✏️
# =============================================
COMPANY = {
    "name": "㈜오토플렉스",
    "name_en": "AUTOFLEX",
    "slogan": "실리콘 제조 생산 전문업체",
    "description": "㈜오토플렉스는 기계 금형 기술을 바탕으로 고품질 실리콘 제품을 생산하는 전문 제조업체입니다. Key-pad 생산 노하우와 다양한 생산 경험을 통해 고객에게 최고의 제품을 제공합니다.",
    "phone": "031-959-6031",
    "mobile": "010-9080-9615",
    "email": "autoflex@autoflex.kr",
    "address": "경기도 파주시 자운서원로410-11",
    "address_detail": "경기도 파주시 법원읍 동문리 619-1",
    "ceo": "허남혁",
    "business_no": "141-81-06639",
    "hours": "평일 09:30 - 17:00",
}

# =============================================
# 제품 목록 - 제품을 추가/수정하세요! ✏️
# =============================================
PRODUCTS = [
    {
        "id": 1,
        "type": "Rubber Type",
        "description": "일반 고무 실리콘을 금형에 넣어 압축 성형하는 방식으로 제작된 제품입니다. 내열성과 내화학성이 뛰어나며 다양한 산업 분야에 적용됩니다.",
        "features": ["내열성 우수", "내화학성 강함", "다양한 경도 선택 가능", "대량 생산 적합"],
        "icon": "🔴",
        "color": "#C0392B",
    },
    {
        "id": 2,
        "type": "LSR Type",
        "description": "액상 실리콘 고무(Liquid Silicone Rubber)를 사출 성형하는 방식입니다. 정밀도가 높고 복잡한 형상 제작에 최적화되어 있습니다.",
        "features": ["고정밀 사출 성형", "복잡한 형상 구현", "의료·식품 등급 가능", "자동화 생산"],
        "icon": "🔵",
        "color": "#2980B9",
    },
    {
        "id": 3,
        "type": "FILM Type",
        "description": "실리콘 필름을 활용한 제품으로 얇고 유연한 특성을 가집니다. 전자기기의 보호 필름, 절연재 등에 활용됩니다.",
        "features": ["초박형 설계", "뛰어난 유연성", "전기 절연성", "표면 보호 기능"],
        "icon": "🟡",
        "color": "#F39C12",
    },
    {
        "id": 4,
        "type": "SUS Type",
        "description": "스테인리스(SUS)와 실리콘을 결합한 복합 제품입니다. 금속의 강도와 실리콘의 탄성을 동시에 요구하는 부품에 사용됩니다.",
        "features": ["금속+실리콘 복합", "고강도 내구성", "부식 방지", "산업용 특수 부품"],
        "icon": "⚙️",
        "color": "#7F8C8D",
    },
]

# =============================================
# 경쟁력 (회사 강점) ✏️
# =============================================
STRENGTHS = [
    {"title": "Key-pad 생산 노하우", "desc": "오랜 경험으로 쌓인 키패드 전문 생산 기술 보유", "icon": "🏆"},
    {"title": "다양한 생산 경험", "desc": "다품종 소량부터 대량 생산까지 폭넓은 경험", "icon": "🔧"},
    {"title": "금형 관리 기술", "desc": "자체 금형 제작 및 정밀 유지관리 능력 보유", "icon": "⚙️"},
    {"title": "기술 혁신", "desc": "신기술 확보와 끊임없는 연구개발로 경쟁력 강화", "icon": "💡"},
]

# =============================================
# 페이지 라우팅 - URL과 함수를 연결해요
# @app.route('/주소') 형태로 URL을 등록
# =============================================

# 메인 홈 페이지
@app.route("/")
def index():
    # render_template: HTML 파일을 불러와서 화면에 보여줌
    return render_template("index.html",
                           company=COMPANY,
                           products=PRODUCTS,
                           strengths=STRENGTHS)

# 회사소개 페이지
@app.route("/about")
def about():
    return render_template("about.html", company=COMPANY, strengths=STRENGTHS)

# 제품 목록 페이지
@app.route("/products")
def products():
    return render_template("products.html", company=COMPANY, products=PRODUCTS)

# 제품 상세 페이지 (URL에 제품 ID가 포함됨)
# 예: /product/1, /product/2
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    # 제품 ID로 해당 제품 찾기
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return "제품을 찾을 수 없습니다.", 404
    return render_template("product_detail.html", company=COMPANY, product=product, products=PRODUCTS)

# 문의하기 페이지
@app.route("/contact", methods=["GET", "POST"])
def contact():
    # POST: 폼을 제출했을 때 / GET: 페이지를 처음 열었을 때
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # 실제 이메일 발송 로직을 여기에 추가할 수 있어요
        # 지금은 성공 메시지만 출력합니다
        print(f"📩 문의 접수: {name} / {email} / {phone}")
        print(f"내용: {message}")

        flash("문의가 성공적으로 접수되었습니다. 빠른 시일 내에 연락드리겠습니다.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", company=COMPANY)


# =============================================
# 앱 실행 - 이 파일을 직접 실행할 때만 동작
# python app.py 로 실행하면 서버가 시작됩니다
# =============================================
if __name__ == "__main__":
    # debug=True: 코드 수정 시 자동 재시작, 오류 메시지 표시
    # host="0.0.0.0": 같은 네트워크의 다른 기기에서도 접속 가능
    print("🚀 오토플렉스 웹서버 시작!")
    print("👉 브라우저에서 http://localhost:5000 으로 접속하세요")
    app.run(debug=True, host="0.0.0.0", port=5000)