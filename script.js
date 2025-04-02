document.querySelector('.burger').addEventListener('click', function() {
    this.classList.toggle('active');
    document.querySelector('.nav-links').classList.toggle('active');
});

// Close menu on scroll
window.addEventListener('scroll', () => {
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');
    if (navLinks.classList.contains('active')) {
        burger.classList.remove('active');
        navLinks.classList.remove('active');
    }
});

// Close menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelector('.burger').classList.remove('active');
        document.querySelector('.nav-links').classList.remove('active');
    });
});