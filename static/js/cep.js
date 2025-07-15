document.addEventListener('DOMContentLoaded', function() {
    const cepInput = document.getElementById('id_cep');
    if (cepInput) {
        cepInput.addEventListener('blur', consultaCEP);
    }
});

function consultaCEP() {
    const cep = document.getElementById('id_cep').value;
    const cepLimpo = cep.replace(/\D/g, '');

    if (cepLimpo.length !== 8) {
        return;
    }

    // Mostra indicador de carregamento
    document.getElementById('id_cep').classList.add('loading');
    
    fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`)
        .then(response => response.json())
        .then(data => {
            if (!data.erro) {
                document.getElementById('id_endereco').value = data.logradouro;
                document.getElementById('id_bairro').value = data.bairro;
                document.getElementById('id_cidade').value = data.localidade;
                document.getElementById('id_uf').value = data.uf;
                
                // Formata o CEP
                document.getElementById('id_cep').value = cepLimpo.replace(/(\d{5})(\d{3})/, '$1-$2');
            } else {
                alert('CEP não encontrado');
            }
        })
        .catch(error => {
            console.error('Erro ao consultar CEP:', error);
            alert('Erro ao consultar CEP. Tente novamente.');
        })
        .finally(() => {
            // Remove indicador de carregamento
            document.getElementById('id_cep').classList.remove('loading');
        });
} 