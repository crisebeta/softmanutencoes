document.addEventListener('DOMContentLoaded', function() {
    // Função para aplicar máscara de telefone
    function maskPhone(input) {
        let value = input.value.replace(/\D/g, '');
        if (value.length > 11) value = value.slice(0, 11);
        
        if (value.length <= 10) {
            // Máscara para telefone fixo: (99) 9999-9999
            value = value.replace(/^(\d{2})(\d{4})(\d{4}).*/, '($1) $2-$3');
        } else {
            // Máscara para celular: (99) 99999-9999
            value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
        }
        
        input.value = value;
    }

    // Aplicando máscaras aos campos
    const celularInput = document.getElementById('id_celular');
    const telefoneInput = document.getElementById('id_telefone');

    if (celularInput) {
        celularInput.addEventListener('input', function() {
            maskPhone(this);
        });
    }

    if (telefoneInput) {
        telefoneInput.addEventListener('input', function() {
            maskPhone(this);
        });
    }
}); 