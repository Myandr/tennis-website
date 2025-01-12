        // Add smooth scrolling to navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add header background on scroll
        window.addEventListener('scroll', () => {
            const header = document.querySelector('.header');
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });

        // Animate elements on scroll
        const animateOnScroll = (entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = `fadeInUp 1s ease forwards`;
                    observer.unobserve(entry.target);
                }
            });
        };

        const observer = new IntersectionObserver(animateOnScroll, { threshold: 0.1 });

        document.querySelectorAll('.section-title, .service-item, .work-item, .team-member, .process-step, .award-logo').forEach(el => {
            el.style.opacity = '0';
            observer.observe(el);
        });

        // Testimonial slider
        const testimonialSlider = document.querySelector('.testimonial-slider');
        let isDown = false;
        let startX;
        let scrollLeft;

        testimonialSlider.addEventListener('mousedown', (e) => {
            isDown = true;
            startX = e.pageX - testimonialSlider.offsetLeft;
            scrollLeft = testimonialSlider.scrollLeft;
        });

        testimonialSlider.addEventListener('mouseleave', () => {
            isDown = false;
        });

        testimonialSlider.addEventListener('mouseup', () => {
            isDown = false;
        });

        testimonialSlider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - testimonialSlider.offsetLeft;
            const walk = (x - startX) * 3;
            testimonialSlider.scrollLeft = scrollLeft - walk;
        });


        const hamburger = document.getElementById('hamburger');
        const menu = document.getElementById('menu');
        const overlay = document.getElementById('overlay');
        
        hamburger.addEventListener('click', () => {
            menu.classList.toggle('show');
            overlay.classList.toggle('active');
            hamburger.classList.toggle('active'); // Fügt den Effekt zum Schließen-Symbol hinzu
        });
        
        document.addEventListener('click', (e) => {
            if (!hamburger.contains(e.target) && !menu.contains(e.target)) {
                menu.classList.remove('show');
                overlay.classList.remove('active');
                hamburger.classList.remove('active'); // Entfernt den Effekt, um das ursprüngliche Hamburger-Symbol wiederherzustellen
            }
        });
        
        // Schließen des Menüs bei Klick auf einen Menü-Link
const menuLinks = menu.querySelectorAll('a');
menuLinks.forEach(link => {
    link.addEventListener('click', () => {
        menu.classList.remove('show');
        overlay.classList.remove('active');
        hamburger.classList.remove('active');
    });
});


        
        window.onscroll = function() {
            const scrollToTopButton = document.getElementById("scrollToTop");
            if (window.scrollY > 300) { // Button ab 300px sichtbar machen
                scrollToTopButton.style.display = "block";
            } else {
                scrollToTopButton.style.display = "none";
            }
        };


        // script.js
document.addEventListener("DOMContentLoaded", function() {
    const loader = document.getElementById("loader");
    const mainContent = document.getElementById("main-content");

    // Warte 3 Sekunden, bevor der Loader verschwindet
    setTimeout(function() {
        loader.style.display = "none"; // Blende den Loader aus
        mainContent.style.display = "block"; // Zeige den Hauptinhalt
    }, 900); // 3000 Millisekunden = 3 Sekunden
});



// JavaScript für das Umschalten der Formularsichtbarkeit
document.getElementById('toggle-form-button').addEventListener('click', function () {
    const form = document.querySelector('.termin-form');
    form.classList.toggle('hidden'); // Versteckt oder zeigt das Formular
    if (!form.classList.contains('hidden')) {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
});

document.getElementById("toggle-about-form-button").addEventListener("click", function () {
    const form = document.querySelector(".about-form");
    form.classList.toggle("hidden");
});

document.getElementById("toggle-service-form-button").addEventListener("click", function () {
    const form = document.querySelector(".service-form");
    form.classList.toggle("hidden");
});

document.getElementById("toggle-testimonial-form-button").addEventListener("click", function () {
    const form = document.querySelector(".testimonial-form");
    form.classList.toggle("hidden");  // Form toggles between visible and hidden
});


function previewImage(event) {
    const previewContainer = document.getElementById('imagePreview');
    const file = event.target.files[0];

    // Prüfen, ob eine Datei ausgewählt wurde
    if (file) {
        const reader = new FileReader();

        // Sobald das Bild geladen ist, wird es in den Container eingefügt
        reader.onload = function(e) {
            previewContainer.innerHTML = `<img src="${e.target.result}" alt="Image Preview" class="preview-image">`;
        };

        reader.readAsDataURL(file);
    } else {
        // Wenn keine Datei ausgewählt ist, Standardtext anzeigen
        previewContainer.innerHTML = '<p>No image selected</p>';
    }
}


