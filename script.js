
// Função para confirmar presente
function confirmarPresente(event) {
    event.preventDefault();
    
    const form = event.target;
    const nome = form.querySelector('#nome').value;
    const telefone = form.querySelector('#telefone').value;
    const presente = form.querySelector('#presente');
    const itemSelecionado = presente.value;
    const textoItem = presente.options[presente.selectedIndex].text;
    const confirmacao = document.getElementById('confirmacao');
    const btnSubmit = form.querySelector('.btn-confirmar');
    
    if (!itemSelecionado) {
        alert('Por favor, selecione um item da lista antes de confirmar.');
        return;
    }

    if (!nome || !telefone) {
        alert('Por favor, preencha todos os campos.');
        return;
    }
    
    // Mostra mensagem de confirmação
    confirmacao.querySelector('p').textContent = `${textoItem} confirmado com sucesso!`;
    confirmacao.classList.add('show');
    
    // Desabilita o formulário após confirmação
    form.querySelectorAll('input, select, button').forEach(el => el.disabled = true);
    btnSubmit.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        Presente Confirmado
    `;
    
    // Esconde mensagem após 5 segundos
    setTimeout(() => {
        confirmacao.classList.remove('show');
    }, 5000);
    
    // Aqui você pode adicionar código para enviar para um servidor/banco de dados
    console.log(`Presente confirmado: ${textoItem} (${itemSelecionado}) - Nome: ${nome} - Telefone: ${telefone}`);
}

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

// Smooth scroll
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

// Máscara de telefone
const telefoneInput = document.getElementById('telefone');
telefoneInput.addEventListener('input', (e) => {
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
});
