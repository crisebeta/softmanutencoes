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

    // Função para aplicar máscara monetária
    function maskMoney(input) {
        let value = input.value.replace(/\D/g, '');
        
        // Se não há valor, define como 0
        if (value === '') {
            input.value = '';
            return;
        }
        
        // Remove zeros à esquerda, mas mantém pelo menos um zero
        value = value.replace(/^0+/, '') || '0';
        
        // Limita a 10 dígitos para evitar valores muito grandes
        if (value.length > 10) {
            value = value.slice(0, 10);
        }
        
        // Para valores com menos de 3 dígitos, adiciona zeros à esquerda
        if (value.length === 1) {
            value = '00' + value;
        } else if (value.length === 2) {
            value = '0' + value;
        }
        
        // Separa parte inteira e decimal
        let integerPart = value.slice(0, -2);
        let decimalPart = value.slice(-2);
        
        // Remove zeros à esquerda da parte inteira, mas mantém pelo menos um
        integerPart = integerPart.replace(/^0+/, '') || '0';
        
        // Adiciona pontos como separadores de milhares
        integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        
        input.value = integerPart + ',' + decimalPart;
    }

    // Função para converter valor formatado para decimal
    function convertToDecimal(formattedValue) {
        return formattedValue
            .replace(/\./g, '') // Remove pontos dos milhares
            .replace(',', '.'); // Substitui vírgula por ponto decimal
    }

    // Aplicando máscaras aos campos de telefone
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

    // Aplicando máscara ao campo valor
    const valorInput = document.getElementById('id_valor');
    if (valorInput) {
        // Formatar valor inicial se existir
        if (valorInput.value && valorInput.value !== '') {
            let initialValue = parseFloat(valorInput.value);
            if (!isNaN(initialValue)) {
                // Converte para centavos e formata
                let centavos = Math.round(initialValue * 100).toString();
                if (centavos.length === 1) {
                    centavos = '00' + centavos;
                } else if (centavos.length === 2) {
                    centavos = '0' + centavos;
                }
                let integerPart = centavos.slice(0, -2) || '0';
                let decimalPart = centavos.slice(-2);
                integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
                valorInput.value = integerPart + ',' + decimalPart;
            }
        }

        // Evento para aplicar máscara durante a digitação
        valorInput.addEventListener('input', function(e) {
            let cursorPosition = this.selectionStart;
            let oldLength = this.value.length;
            
            maskMoney(this);
            
            // Ajusta a posição do cursor após aplicar a máscara
            let newLength = this.value.length;
            let newPosition = cursorPosition + (newLength - oldLength);
            
            // Garante que o cursor não ultrapasse o tamanho do valor
            if (newPosition > newLength) {
                newPosition = newLength;
            }
            
            this.setSelectionRange(newPosition, newPosition);
        });

        // Evento para prevenir caracteres não numéricos
        valorInput.addEventListener('keypress', function(e) {
            // Permite apenas números, backspace, delete, tab, escape, enter
            if ([8, 9, 27, 13, 46].indexOf(e.keyCode) !== -1 ||
                // Permite Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true)) {
                return;
            }
            // Impede qualquer coisa que não seja número
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });

        // Converter para decimal antes de enviar o formulário
        const form = valorInput.closest('form');
        if (form) {
            form.addEventListener('submit', function() {
                if (valorInput.value) {
                    valorInput.value = convertToDecimal(valorInput.value);
                }
            });
        }
    }
});