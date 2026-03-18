// main.js - 오토플렉스 통합 웹사이트

function toggleMenu() {
    document.getElementById('mobileMenu').classList.toggle('open');
}

// 스크롤 시 카드 등장 애니메이션
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
            setTimeout(() => {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }, i * 80);
        }
    });
}, { threshold: 0.1 });

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.product-card, .strength-card, .vision-card, .shop-card, .info-card').forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    // 현재 페이지 네비 링크 강조
    document.querySelectorAll('.nav-links a').forEach(link => {
        if (link.href === window.location.href) {
            link.style.color = '#ff6b35';
        }
    });
});