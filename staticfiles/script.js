// Animação ao Scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observa todos os elementos com classes de animação
document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right, .scale-in').forEach((el) => {
    observer.observe(el);
});

// Smooth scroll para links internos
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Máscara de telefone — via delegação para funcionar dentro do modal
document.addEventListener('input', (e) => {
    if (e.target && e.target.id === 'telefone') {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 11) value = value.slice(0, 11);

        if (value.length > 6) {
            value = value.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
        } else if (value.length > 0) {
            value = value.replace(/^(\d*)/, '($1');
        }

        e.target.value = value;
    }
});

// Fecha modal ao clicar fora do conteúdo
const modalOverlay = document.getElementById('modal-presentes');
if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            modalOverlay.style.display = 'none';
        }
    });
}

// Copiar Chave Pix
function copyPixKey() {
    const keyText = document.getElementById('pix-key-text').innerText;
    
    function updateButtonState() {
        const btn = document.getElementById('btn-copy-pix');
        const btnText = btn.querySelector('span');
        const btnIcon = btn.querySelector('svg');
        
        // Salva estados originais
        const originalText = btnText.innerText;
        const originalHtml = btnIcon.outerHTML;
        
        // Atualiza para o estado "copiado"
        btn.classList.add('copied');
        btnText.innerText = 'Copiado!';
        
        // Altera ícone para o checkmark
        btnIcon.outerHTML = `<svg xmlns="http://www.w3.org/2000/svg" class="icon-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
        </svg>`;
        
        // Reseta após 2 segundos
        setTimeout(() => {
            btn.classList.remove('copied');
            btnText.innerText = originalText;
            btn.querySelector('svg').outerHTML = originalHtml;
        }, 2000);
    }

    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(keyText).then(updateButtonState).catch(err => {
            console.error('Erro ao copiar chave: ', err);
        });
    } else {
        // Fallback para navegadores antigos ou WebViews do Instagram/WhatsApp
        const textArea = document.createElement("textarea");
        textArea.value = keyText;
        textArea.style.position = "fixed";  // Evita rolar a tela para baixo
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            updateButtonState();
        } catch (err) {
            console.error('Erro no fallback de cópia: ', err);
        }
        document.body.removeChild(textArea);
    }
}
