document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    menuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
    });
    
    // Close mobile menu when clicking on a nav link
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
        });
    });
    
    // Navigation active state based on scroll position
    const sections = document.querySelectorAll('section');
    const navItems = document.querySelectorAll('.nav-links a');
    
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - sectionHeight / 3)) {
                current = section.getAttribute('id');
            }
        });
        
        navItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href').substring(1) === current) {
                item.classList.add('active');
            }
        });
        
        // Sticky header
        const header = document.querySelector('header');
        header.classList.toggle('sticky', window.scrollY > 0);
    });
    
    // Scroll reveal animation
    const revealElements = document.querySelectorAll('.project-card, .research-card, .skill-category, .contact-item');
    
    function checkReveal() {
        const triggerBottom = window.innerHeight / 5 * 4;
        
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            
            if (elementTop < triggerBottom) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    }
    
    // Apply initial styles for animation
    revealElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Check on load and scroll
    window.addEventListener('load', checkReveal);
    window.addEventListener('scroll', checkReveal);
    
    // Form submission
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Here you would normally handle the form submission
            // For now, we'll just show a success message
            const formElements = contactForm.elements;
            let isValid = true;
            
            for (let i = 0; i < formElements.length; i++) {
                if (formElements[i].required && !formElements[i].value) {
                    isValid = false;
                    formElements[i].style.borderColor = 'red';
                } else if (formElements[i].type === 'email') {
                    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
                    if (!emailPattern.test(formElements[i].value)) {
                        isValid = false;
                        formElements[i].style.borderColor = 'red';
                    } else {
                        formElements[i].style.borderColor = '#ddd';
                    }
                } else {
                    formElements[i].style.borderColor = '#ddd';
                }
            }
            
            if (isValid) {
                // Display success message
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.textContent = 'Your message has been sent successfully!';
                successMessage.style.color = '#4CAF50';
                successMessage.style.padding = '10px';
                successMessage.style.marginTop = '10px';
                successMessage.style.textAlign = 'center';
                
                // Append message and reset form
                contactForm.appendChild(successMessage);
                contactForm.reset();
                
                // Remove message after 3 seconds
                setTimeout(() => {
                    successMessage.remove();
                }, 3000);
            }
        });
    }
});