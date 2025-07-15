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

    // ========== NOVAS FUNÇÕES PARA DESPESAS ==========

    // Função para aplicar máscara monetária específica para despesas
    function applyExpenseMoneyMask(input) {
        if (!input) return;
        
        // Formatar valor inicial se existir
        if (input.value && input.value !== '' && input.value !== '0') {
            // Se o valor já está formatado (contém vírgula), não reformata
            if (input.value.includes(',')) {
                // Já está formatado, apenas aplica os eventos
            } else {
                // Valor vem do banco como decimal (ex: 150.50), precisa formatar
                let formattedValue = formatDecimalToCurrency(input.value);
                input.value = formattedValue;
            }
        }

        // Evento para aplicar máscara durante a digitação
        input.addEventListener('input', function(e) {
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
        input.addEventListener('keypress', function(e) {
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
    }

    // Função para aplicar máscaras a todos os campos monetários de despesas
    function applyExpenseMoneyMasks() {
        const valorInput = document.querySelector('input[name="valor"]');
        
        if (valorInput) {
            applyExpenseMoneyMask(valorInput);
        }
    }

    // Função para preparar formulário de despesas antes do envio
    function prepareExpenseFormSubmit() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            // Verifica se é um formulário de despesa (contém campo valor)
            const valorField = form.querySelector('input[name="valor"]');
            
            if (valorField) {
                form.addEventListener('submit', function(e) {
                    // Converte valor formatado para decimal antes do envio
                    if (valorField.value) {
                        valorField.value = convertExpenseCurrencyToDecimal(valorField.value);
                    }
                });
            }
        });
    }

    // Função para converter valor monetário de despesa para decimal
    function convertExpenseCurrencyToDecimal(formattedValue) {
        if (!formattedValue) return '';
        return formattedValue
            .replace(/\./g, '') // Remove pontos dos milhares
            .replace(',', '.'); // Substitui vírgula por ponto decimal
    }

    // ========== NOVAS FUNÇÕES PARA SERVIÇOS ==========

    // Função específica para máscara monetária dos campos de serviço
    function maskServiceMoney(input) {
        let value = input.value.replace(/\D/g, '');
        
        // Se não há valor, limpa o campo
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

    // Função para formatar valor decimal para formato monetário brasileiro
    function formatDecimalToCurrency(decimalValue) {
        if (!decimalValue || decimalValue === '' || decimalValue === '0' || decimalValue === '0.00') {
            return '';
        }
        
        // Converte para float e garante 2 casas decimais
        let floatValue = parseFloat(decimalValue);
        if (isNaN(floatValue)) {
            return '';
        }
        
        // Converte para string com 2 casas decimais fixas
        let valueString = floatValue.toFixed(2);
        
        // Separa parte inteira e decimal
        let [integerPart, decimalPart] = valueString.split('.');
        
        // Adiciona pontos como separadores de milhares
        integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        
        return integerPart + ',' + decimalPart;
    }

    // Função para aplicar máscara monetária a um campo específico de serviço
    function applyServiceMoneyMask(input) {
        if (!input) return;
        
        // Formatar valor inicial se existir
        if (input.value && input.value !== '' && input.value !== '0') {
            // Se o valor já está formatado (contém vírgula), não reformata
            if (input.value.includes(',')) {
                // Já está formatado, apenas aplica os eventos
            } else {
                // Valor vem do banco como decimal (ex: 150.50), precisa formatar
                let formattedValue = formatDecimalToCurrency(input.value);
                input.value = formattedValue;
            }
        }

        // Evento para aplicar máscara durante a digitação
        input.addEventListener('input', function(e) {
            let cursorPosition = this.selectionStart;
            let oldLength = this.value.length;
            
            maskServiceMoney(this);
            
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
        input.addEventListener('keypress', function(e) {
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
    }

    // Função para aplicar máscaras a todos os campos monetários de serviços
    function applyServiceMoneyMasks() {
        // Campos principais do serviço
        const valorServicoInput = document.getElementById('id_valor_servico');
        const valorPagoInput = document.getElementById('id_valor_pago');
        
        if (valorServicoInput) {
            applyServiceMoneyMask(valorServicoInput);
        }
        
        if (valorPagoInput) {
            applyServiceMoneyMask(valorPagoInput);
        }

        // Campos de valor unitário dos produtos existentes
        document.querySelectorAll('.valor-unitario-mask').forEach(input => {
            applyServiceMoneyMask(input);
        });
    }

    // Função para converter valor monetário de serviço para decimal
    function convertServiceCurrencyToDecimal(formattedValue) {
        if (!formattedValue) return '';
        return formattedValue
            .replace(/\./g, '') // Remove pontos dos milhares
            .replace(',', '.'); // Substitui vírgula por ponto decimal
    }

    // ========== NOVAS FUNÇÕES PARA PRODUTOS ==========

    // Função para aplicar máscara monetária a um campo específico de produto
    function applyProductMoneyMask(input) {
        if (!input) return;
        
        // FORÇA o campo a ser do tipo text para evitar validação HTML5
        input.setAttribute('type', 'text');
        
        // Remove TODOS os atributos de validação HTML5
        input.removeAttribute('step');
        input.removeAttribute('min');
        input.removeAttribute('max');
        input.removeAttribute('required');
        
        // Desabilita validação customizada do browser
        input.addEventListener('invalid', function(e) {
            e.preventDefault();
            return false;
        });
        
        // Remove evento de validação do form
        input.setCustomValidity('');
        
        // Formatar valor inicial se existir
        if (input.value && input.value !== '' && input.value !== '0') {
            // Se o valor já está formatado (contém vírgula), não reformata
            if (input.value.includes(',')) {
                // Já está formatado, apenas aplica os eventos
            } else {
                // Valor vem do banco como decimal (ex: 150.50), precisa formatar
                let formattedValue = formatDecimalToCurrency(input.value);
                input.value = formattedValue;
            }
        }

        // Evento para aplicar máscara durante a digitação
        input.addEventListener('input', function(e) {
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
        input.addEventListener('keypress', function(e) {
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
    }

    // Função para aplicar máscaras a todos os campos monetários de produtos
    function applyProductMoneyMasks() {
        const precoField = document.getElementById('id_preco');
        const precoCustoField = document.getElementById('id_preco_custo');
        
        if (precoField) {
            applyProductMoneyMask(precoField);
        }
        
        if (precoCustoField) {
            applyProductMoneyMask(precoCustoField);
        }
    }

    // Função para converter valor monetário de produto para decimal
    function convertProductCurrencyToDecimal(formattedValue) {
        if (!formattedValue) return '';
        return formattedValue
            .replace(/\./g, '') // Remove pontos dos milhares
            .replace(',', '.'); // Substitui vírgula por ponto decimal
    }

    // Função para preparar campos de produto antes do envio do formulário
    function prepareProductFormSubmit() {
        const form = document.getElementById('produtoForm');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            // Remove validação HTML5 do formulário
            this.setAttribute('novalidate', 'novalidate');
            
            // Converte valores formatados para decimal antes do envio
            const precoField = document.getElementById('id_preco');
            const precoCustoField = document.getElementById('id_preco_custo');
            
            if (precoField && precoField.value) {
                precoField.value = convertProductCurrencyToDecimal(precoField.value);
            }
            
            if (precoCustoField && precoCustoField.value) {
                precoCustoField.value = convertProductCurrencyToDecimal(precoCustoField.value);
            }
            
            // Força todos os campos monetários como texto no momento do submit
            [precoField, precoCustoField].forEach(field => {
                if (field) {
                    field.setAttribute('type', 'text');
                    field.setCustomValidity('');
                }
            });
        });
    }

    // Torna as funções disponíveis globalmente para uso no template
    window.applyServiceMoneyMasks = applyServiceMoneyMasks;
    window.applyServiceMoneyMask = applyServiceMoneyMask;
    window.convertServiceCurrencyToDecimal = convertServiceCurrencyToDecimal;
    window.formatDecimalToCurrency = formatDecimalToCurrency;
    
    // Novas funções para produtos disponíveis globalmente
    window.applyProductMoneyMasks = applyProductMoneyMasks;
    window.applyProductMoneyMask = applyProductMoneyMask;
    window.convertProductCurrencyToDecimal = convertProductCurrencyToDecimal;
    window.prepareProductFormSubmit = prepareProductFormSubmit;

    // Novas funções para despesas disponíveis globalmente
    window.applyExpenseMoneyMasks = applyExpenseMoneyMasks;
    window.applyExpenseMoneyMask = applyExpenseMoneyMask;
    window.convertExpenseCurrencyToDecimal = convertExpenseCurrencyToDecimal;
    window.prepareExpenseFormSubmit = prepareExpenseFormSubmit;

    // ========== CÓDIGO ORIGINAL MANTIDO ==========

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

    // Função para aplicar máscara monetária a um campo específico - CORRIGIDA PARA PRODUTOS
    function applyMoneyMask(input) {
        if (!input) return;
        
        // FORÇA o campo a ser do tipo text para evitar validação HTML5
        input.setAttribute('type', 'text');
        
        // Remove TODOS os atributos de validação HTML5
        input.removeAttribute('step');
        input.removeAttribute('min');
        input.removeAttribute('max');
        input.removeAttribute('required');
        
        // Desabilita validação customizada do browser
        input.addEventListener('invalid', function(e) {
            e.preventDefault();
            return false;
        });
        
        // Remove evento de validação do form
        input.setCustomValidity('');
        
        // Formatar valor inicial se existir
        if (input.value && input.value !== '' && input.value !== '0') {
            // Se o valor já está formatado (contém vírgula), não reformata
            if (input.value.includes(',')) {
                // Já está formatado, apenas aplica os eventos
            } else {
                // Valor vem do banco como decimal (ex: 150.50), precisa formatar
                let initialValue = parseFloat(input.value);
                if (!isNaN(initialValue)) {
                    // Converte para string com 2 casas decimais fixas
                    let valueString = initialValue.toFixed(2);
                    
                    // Separa parte inteira e decimal
                    let [integerPart, decimalPart] = valueString.split('.');
                    
                    // Adiciona pontos como separadores de milhares
                    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
                    
                    input.value = integerPart + ',' + decimalPart;
                }
            }
        }

        // Evento para aplicar máscara durante a digitação
        input.addEventListener('input', function(e) {
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
        input.addEventListener('keypress', function(e) {
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
    }

    // Aplicando máscara aos campos monetários de PRODUTOS
    const campos = ['id_valor', 'id_preco', 'id_preco_custo'];
    const form = document.querySelector('form');
    
    campos.forEach(campoId => {
        const input = document.getElementById(campoId);
        if (input) {
            applyMoneyMask(input);
        }
    });

    // Função ESPECÍFICA para forçar campos de produtos como texto
    function forceProductFieldsAsText() {
        const productMoneyFields = ['id_preco', 'id_preco_custo'];
        
        productMoneyFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                // FORÇA tipo texto
                field.setAttribute('type', 'text');
                
                // Remove TODOS os atributos de validação HTML5
                field.removeAttribute('step');
                field.removeAttribute('min');
                field.removeAttribute('max');
                field.removeAttribute('required');
                
                // Remove validação customizada do browser
                field.addEventListener('invalid', function(e) {
                    e.preventDefault();
                    return false;
                });
                
                // Limpa qualquer validação customizada
                field.setCustomValidity('');
            }
        });
    }

    // Chama a função para forçar campos como texto
    forceProductFieldsAsText();

    // Intercepta o submit do form para garantir que não há validação HTML5
    if (form) {
        form.addEventListener('submit', function(e) {
            // Remove validação HTML5 do formulário
            this.setAttribute('novalidate', 'novalidate');
            
            // NOVA FUNCIONALIDADE: Converte valores formatados para decimal
            const precoField = document.getElementById('id_preco');
            const precoCustoField = document.getElementById('id_preco_custo');
            
            if (precoField && precoField.value) {
                precoField.value = convertToDecimal(precoField.value);
            }
            
            if (precoCustoField && precoCustoField.value) {
                precoCustoField.value = convertToDecimal(precoCustoField.value);
            }
            
            // Força todos os campos monetários como texto no momento do submit
            const productFields = ['id_preco', 'id_preco_custo'];
            productFields.forEach(fieldId => {
                const field = document.getElementById(fieldId);
                if (field) {
                    field.setAttribute('type', 'text');
                    field.setCustomValidity('');
                }
            });
        });
    }

    // Inicializa funções para produtos se estivermos na página de produtos
    if (document.getElementById('id_preco') || document.getElementById('id_preco_custo')) {
        applyProductMoneyMasks();
        prepareProductFormSubmit();
    }

    // ========== INICIALIZAÇÃO AUTOMÁTICA PARA DESPESAS ==========
    
    // Inicializa funções para despesas se estivermos na página de despesas
    if (document.querySelector('input[name="valor"]')) {
        applyExpenseMoneyMasks();
        prepareExpenseFormSubmit();
    }
});