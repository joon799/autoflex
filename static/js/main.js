// =============================================
// main.js - 웹사이트 인터랙션 스크립트
// =============================================

// 모바일 메뉴 열기/닫기
function toggleMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('open');
}

// 스크롤 시 요소가 부드럽게 나타나는 효과
// IntersectionObserver: 요소가 화면에 보이는지 감지하는 브라우저 기능
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

// 'fade-in' 클래스를 가진 모든 요소에 애니메이션 적용
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

// 페이지 로드 시 fade-in 클래스를 카드들에 자동 추가
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll(
        '.product-card, .strength-card, .vision-card, .stat-item, .product-full-card, .info-card'
    );
    cards.forEach((card, i) => {
        card.classList.add('fade-in');
        // 순서대로 조금씩 늦게 나타나게 (stagger effect)
        card.style.transitionDelay = `${i * 0.07}s`;
        observer.observe(card);
    });
});

// 네비게이션 - 현재 페이지 링크 강조
document.querySelectorAll('.nav-links a, .mobile-menu a').forEach(link => {
    if (link.href === window.location.href) {
        link.style.color = '#ff6b35';
    }
});