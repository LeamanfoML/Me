document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    
    // Проверяем сохраненную тему
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
    
    // Переключение темы
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        
        // Сохраняем выбор темы
        const currentTheme = document.body.classList.contains('dark-theme') 
            ? 'dark' 
            : 'light';
        localStorage.setItem('theme', currentTheme);
    });
    
    // Плавная прокрутка
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
