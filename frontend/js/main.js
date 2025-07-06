// ===== CONFIGURAÇÕES =====
const API_BASE_URL = 'http://localhost:5000';
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];

// ===== ELEMENTOS DOM =====
const uploadForm = document.getElementById('uploadForm');
const submitBtn = document.getElementById('submitBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');

// ===== ESTADO DA APLICAÇÃO =====
let uploadedFiles = {
    rg_frente: null,
    rg_verso: null,
    comprovante: null
};

// ===== INICIALIZAÇÃO =====
document.addEventListener('DOMContentLoaded', function() {
    initializeUploadAreas();
    initializeFormValidation();
    console.log('🚀 Frontend UniFECAF inicializado');
});

// ===== INICIALIZAÇÃO DAS ÁREAS DE UPLOAD =====
function initializeUploadAreas() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]');
        const previewArea = area.querySelector('.preview-area');
        const statusElement = area.parentElement.querySelector('.upload-status');
        const type = area.dataset.type;
        
        // Event listeners para drag & drop
        area.addEventListener('dragover', handleDragOver);
        area.addEventListener('dragleave', handleDragLeave);
        area.addEventListener('drop', handleDrop);
        
        // Event listener para clique (apenas na área de upload, não no input)
        area.addEventListener('click', (e) => {
            // Evita duplicação se clicar no input
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });
        
        // Event listener para mudança de arquivo
        fileInput.addEventListener('change', (e) => handleFileSelect(e, type, previewArea, statusElement));
    });
}

// ===== HANDLERS DE DRAG & DROP =====
function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    const area = e.currentTarget;
    area.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const fileInput = area.querySelector('input[type="file"]');
        const type = area.dataset.type;
        const previewArea = area.querySelector('.preview-area');
        const statusElement = area.parentElement.querySelector('.upload-status');
        
        fileInput.files = files;
        handleFileSelect({ target: fileInput }, type, previewArea, statusElement);
    }
}

// ===== HANDLER DE SELEÇÃO DE ARQUIVO =====
function handleFileSelect(event, type, previewArea, statusElement) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    // Validação do arquivo
    const validation = validateFile(file, type);
    
    if (!validation.isValid) {
        showStatus(statusElement, validation.message, 'error');
        event.target.value = '';
        return;
    }
    
    // Armazena o arquivo
    uploadedFiles[type] = file;
    
    // Mostra preview
    showFilePreview(file, previewArea, type);
    
    // Atualiza status
    showStatus(statusElement, `Arquivo carregado: ${file.name}`, 'success');
    
    // Atualiza área de upload
    const uploadArea = event.target.closest('.upload-area');
    uploadArea.classList.add('has-file');
    
    // Atualiza validação do formulário
    updateFormValidation();
}

// ===== VALIDAÇÃO DE ARQUIVO =====
function validateFile(file, type) {
    // Verifica tamanho
    if (file.size > MAX_FILE_SIZE) {
        return {
            isValid: false,
            message: 'Arquivo muito grande. Máximo 5MB.'
        };
    }
    
    // Verifica tipo (todos os documentos agora são apenas imagens)
    if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
        return {
            isValid: false,
            message: 'Tipo de arquivo não suportado. Use apenas JPG ou PNG.'
        };
    }
    
    return {
        isValid: true,
        message: 'Arquivo válido'
    };
}

// ===== PREVIEW DE ARQUIVO =====
function showFilePreview(file, previewArea, type) {
    previewArea.innerHTML = '';
    previewArea.classList.add('has-preview');
    
    // Preview de imagem (todos os arquivos agora são imagens)
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.alt = 'Preview do arquivo';
    previewArea.appendChild(img);
    
    // Adiciona detalhes do arquivo
    const fileDetails = document.createElement('div');
    fileDetails.className = 'file-details';
    fileDetails.innerHTML = `
        <strong>Nome:</strong> ${file.name}<br>
        <strong>Tamanho:</strong> ${formatFileSize(file.size)}<br>
        <strong>Tipo:</strong> ${file.type}
    `;
    previewArea.appendChild(fileDetails);
}

// ===== FORMATAÇÃO DE TAMANHO DE ARQUIVO =====
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// ===== STATUS DE UPLOAD =====
function showStatus(element, message, type = 'info') {
    element.textContent = message;
    element.className = `upload-status ${type}`;
}

// ===== VALIDAÇÃO DO FORMULÁRIO =====
function initializeFormValidation() {
    updateFormValidation();
}

function updateFormValidation() {
    const allFilesUploaded = Object.values(uploadedFiles).every(file => file !== null);
    submitBtn.disabled = !allFilesUploaded;
    
    if (allFilesUploaded) {
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i><span>Processar Documentos</span>';
    } else {
        submitBtn.innerHTML = '<i class="fas fa-lock"></i><span>Complete todos os uploads</span>';
    }
}

// ===== SUBMISSÃO DO FORMULÁRIO =====
uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!Object.values(uploadedFiles).every(file => file !== null)) {
        showNotification('Por favor, complete todos os uploads antes de processar.', 'warning');
        return;
    }
    
    await processDocuments();
});

// ===== PROCESSAMENTO DE DOCUMENTOS =====
async function processDocuments() {
    try {
        // Mostra loading
        showLoading(true);
        
        // Converte arquivos para base64
        console.log('🔄 Convertendo arquivos para base64...');
        const base64Data = {};
        
        for (const [type, file] of Object.entries(uploadedFiles)) {
            const base64 = await fileToBase64(file);
            base64Data[type] = {
                base64: base64,
                filename: file.name,
                content_type: file.type,
                size: file.size
            };
        }
        
        console.log('✅ Arquivos convertidos para base64');
        
        // Envia base64 para o backend
        console.log('🤖 Enviando para processamento...');
        const response = await fetch(`${API_BASE_URL}/api/process-documents-base64`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(base64Data)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('❌ Erro na API:', errorText);
            throw new Error(`Erro HTTP: ${response.status} - ${errorText}`);
        }
        
        const result = await response.json();
        console.log('📊 Resultado:', result);
        
        // Esconde loading
        showLoading(false);
        
        // Mostra resultados
        showResults(result);
        
    } catch (error) {
        console.error('Erro no processamento:', error);
        showLoading(false);
        showNotification(`Erro ao processar documentos: ${error.message}`, 'error');
    }
}

// ===== CONVERSÃO DE ARQUIVO PARA BASE64 =====
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            // Remove o prefixo "data:image/jpeg;base64," para enviar apenas o base64
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = () => reject(new Error('Erro ao ler arquivo'));
        reader.readAsDataURL(file);
    });
}

// ===== CONTROLE DE LOADING =====
function showLoading(show) {
    if (show) {
        loadingSection.style.display = 'block';
        uploadForm.style.display = 'none';
        resultsSection.style.display = 'none';
    } else {
        loadingSection.style.display = 'none';
        uploadForm.style.display = 'block';
    }
}

// ===== EXIBIÇÃO DE RESULTADOS =====
function showResults(result) {
    resultsSection.style.display = 'block';
    
    if (result.success) {
        resultsContent.innerHTML = createResultsHTML(result.data);
    } else {
        resultsContent.innerHTML = `
            <div class="result-item error">
                <h4><i class="fas fa-exclamation-triangle"></i> Erro no Processamento</h4>
                <p><strong>Erro:</strong> ${result.error || 'Erro desconhecido'}</p>
            </div>
        `;
    }
    
    // Scroll para os resultados
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// ===== CRIAÇÃO DO HTML DOS RESULTADOS =====
function createResultsHTML(data) {
    let html = '<div class="result-item success">';
    html += '<h4><i class="fas fa-check-circle"></i> Dados Extraídos</h4>';
    
    // Dados pessoais
    if (data.nome_completo) {
        html += `<p><strong>Nome Completo:</strong> ${data.nome_completo}</p>`;
    }
    
    if (data.cpf) {
        html += `<p><strong>CPF:</strong> ${data.cpf}</p>`;
    }
    
    if (data.rg) {
        html += `<p><strong>RG:</strong> ${data.rg}</p>`;
    }
    
    if (data.data_emissao) {
        html += `<p><strong>Data de Emissão:</strong> ${data.data_emissao}</p>`;
    }
    
    if (data.orgao_emissor) {
        html += `<p><strong>Órgão Emissor:</strong> ${data.orgao_emissor}</p>`;
    }
    
    if (data.uf_emissor) {
        html += `<p><strong>UF Emissor:</strong> ${data.uf_emissor}</p>`;
    }
    
    if (data.data_nascimento) {
        html += `<p><strong>Data de Nascimento:</strong> ${data.data_nascimento}</p>`;
    }
    
    if (data.naturalidade) {
        html += `<p><strong>Naturalidade:</strong> ${data.naturalidade}</p>`;
    }
    
    // Dados de endereço
    if (data.endereco_completo) {
        html += `<p><strong>Endereço:</strong> ${data.endereco_completo}</p>`;
    }
    
    if (data.cidade) {
        html += `<p><strong>Cidade:</strong> ${data.cidade}</p>`;
    }
    
    if (data.estado) {
        html += `<p><strong>Estado:</strong> ${data.estado}</p>`;
    }
    
    if (data.cep) {
        html += `<p><strong>CEP:</strong> ${data.cep}</p>`;
    }
    
    html += '</div>';
    
    return html;
}

// ===== NOTIFICAÇÕES =====
function showNotification(message, type = 'info') {
    // Cria elemento de notificação
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">×</button>
    `;
    
    // Adiciona estilos inline para notificação
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;
    
    // Adiciona ao body
    document.body.appendChild(notification);
    
    // Remove após 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function getNotificationColor(type) {
    const colors = {
        success: '#28A745',
        error: '#DC3545',
        warning: '#FFC107',
        info: '#17A2B8'
    };
    return colors[type] || '#17A2B8';
}

// ===== ANIMAÇÕES CSS =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification button {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        margin-left: auto;
    }
`;
document.head.appendChild(style);

// ===== UTILITÁRIOS =====
function resetForm() {
    uploadedFiles = {
        rg_frente: null,
        rg_verso: null,
        comprovante: null
    };
    
    // Limpa previews
    document.querySelectorAll('.preview-area').forEach(area => {
        area.innerHTML = '';
        area.classList.remove('has-preview');
    });
    
    // Limpa status
    document.querySelectorAll('.upload-status').forEach(status => {
        status.textContent = '';
        status.className = 'upload-status';
    });
    
    // Remove classes de arquivo
    document.querySelectorAll('.upload-area').forEach(area => {
        area.classList.remove('has-file');
    });
    
    // Limpa inputs
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.value = '';
    });
    
    // Atualiza validação
    updateFormValidation();
    
    // Esconde resultados
    resultsSection.style.display = 'none';
    uploadForm.style.display = 'block';
}

// ===== EXPOSIÇÃO DE FUNÇÕES GLOBAIS =====
window.resetForm = resetForm; 