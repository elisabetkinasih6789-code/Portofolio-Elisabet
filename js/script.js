// ===================================================
// MOBILE NAV TOGGLE
// ===================================================
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');

burger.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Close mobile menu after clicking a link
navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
  });
});

// ===================================================
// SCROLL SPY — highlight active nav link
// ===================================================
const sections = document.querySelectorAll('section[id]');
const navItems = document.querySelectorAll('.nav-links a');

function setActiveLink(){
  let current = '';
  const scrollPos = window.scrollY + 120;

  sections.forEach(section => {
    if (scrollPos >= section.offsetTop){
      current = section.id;
    }
  });

  navItems.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === `#${current}`){
      link.classList.add('active');
    }
  });
}

window.addEventListener('scroll', setActiveLink);
setActiveLink();

// ===================================================
// NAVBAR SHADOW ON SCROLL
// ===================================================
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 10){
    navbar.style.boxShadow = '0 6px 18px rgba(163,18,28,0.12)';
  } else {
    navbar.style.boxShadow = 'none';
  }
});

// ===================================================
// REVEAL ON SCROLL (timeline cards, skills, projects)
// ===================================================
const revealTargets = document.querySelectorAll(
  '.timeline-card, .skill-card, .project-card, .about-text, .about-photo'
);

revealTargets.forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity .6s ease, transform .6s ease';
});

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting){
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

revealTargets.forEach(el => observer.observe(el));

// ===================================================
// CONTACT FORM SUBMISSION
// ===================================================
const contactForm = document.getElementById('contactForm');
const formSuccess = document.getElementById('formSuccess');

contactForm.addEventListener('submit', (e) => {
  e.preventDefault();

  // Simple front-end only handling — replace with real API call if needed
  formSuccess.classList.add('show');
  contactForm.reset();

  setTimeout(() => {
    formSuccess.classList.remove('show');
  }, 5000);
});