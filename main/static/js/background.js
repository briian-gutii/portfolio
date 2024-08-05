const background = document.getElementById('background');
const languages = ['Python', 'JavaScript', 'HTML', 'CSS', 'Django', 'React', 'SQL'];

function addLanguage() {
    const language = languages[Math.floor(Math.random() * languages.length)];
    const element = document.createElement('div');
    element.textContent = language;
    element.style.position = 'absolute';
    element.style.left = `${Math.random() * 100}%`;
    element.style.top = `${Math.random() * 100}%`;
    element.style.opacity = '0';
    element.style.transition = 'opacity 2s';
    
    background.appendChild(element);
    
    setTimeout(() => {
        element.style.opacity = '1';
    }, 100);
    
    setTimeout(() => {
        element.style.opacity = '0';
        setTimeout(() => {
            background.removeChild(element);
        }, 2000);
    }, 5000);
}

setInterval(addLanguage, 1000);