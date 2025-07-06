"""
Modelo de dados para documentos processados
"""
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class DocumentoProcessado:
    """
    Classe que representa um documento processado no sistema
    
    Attributes:
        id_processo (str): UUID único do processo
        tipo_documento (str): Tipo do documento (RG_FRENTE, RG_VERSO, COMPROVANTE_RESIDENCIA)
        nome_completo (str): Nome completo extraído
        cpf (str): CPF extraído
        rg (str): RG extraído
        data_emissao_rg (str): Data de emissão do RG
        endereco (str): Endereço completo
        cidade (str): Cidade
        estado (str): Estado (UF)
        cep (str): CEP
        status_processamento (str): Status do processamento
        data_processamento (datetime): Data/hora do processamento
        observacoes (str): Observações sobre o processamento
        email_contato (str): E-mail de contato
        arquivo_original_nome (str): Nome do arquivo original
        dados_ia_response (Dict): Resposta completa da IA em JSON
    """
    
    def __init__(self, 
                 tipo_documento: str,
                 nome_completo: Optional[str] = None,
                 cpf: Optional[str] = None,
                 rg: Optional[str] = None,
                 data_emissao_rg: Optional[str] = None,
                 endereco: Optional[str] = None,
                 cidade: Optional[str] = None,
                 estado: Optional[str] = None,
                 cep: Optional[str] = None,
                 email_contato: Optional[str] = None,
                 arquivo_original_nome: Optional[str] = None,
                 dados_ia_response: Optional[Dict[str, Any]] = None):
        """
        Inicializa um novo documento processado
        
        Args:
            tipo_documento (str): Tipo do documento
            nome_completo (str, optional): Nome completo
            cpf (str, optional): CPF
            rg (str, optional): RG
            data_emissao_rg (str, optional): Data de emissão do RG
            endereco (str, optional): Endereço completo
            cidade (str, optional): Cidade
            estado (str, optional): Estado (UF)
            cep (str, optional): CEP
            email_contato (str, optional): E-mail de contato
            arquivo_original_nome (str, optional): Nome do arquivo original
            dados_ia_response (Dict, optional): Resposta da IA
        """
        self.id_processo = str(uuid.uuid4())
        self.tipo_documento = tipo_documento
        self.nome_completo = nome_completo
        self.cpf = cpf
        self.rg = rg
        self.data_emissao_rg = data_emissao_rg
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        self.status_processamento = 'Pendente'
        self.data_processamento = datetime.now()
        self.observacoes = None
        self.email_contato = email_contato
        self.arquivo_original_nome = arquivo_original_nome
        self.dados_ia_response = dados_ia_response or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto para dicionário
        
        Returns:
            Dict[str, Any]: Dicionário com os dados do documento
        """
        return {
            'id_processo': self.id_processo,
            'tipo_documento': self.tipo_documento,
            'nome_completo': self.nome_completo,
            'cpf': self.cpf,
            'rg': self.rg,
            'data_emissao_rg': self.data_emissao_rg,
            'endereco': self.endereco,
            'cidade': self.cidade,
            'estado': self.estado,
            'cep': self.cep,
            'status_processamento': self.status_processamento,
            'data_processamento': self.data_processamento.isoformat() if self.data_processamento else None,
            'observacoes': self.observacoes,
            'email_contato': self.email_contato,
            'arquivo_original_nome': self.arquivo_original_nome,
            'dados_ia_response': self.dados_ia_response,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def update_status(self, status: str, observacoes: Optional[str] = None):
        """
        Atualiza o status do processamento
        
        Args:
            status (str): Novo status
            observacoes (str, optional): Observações sobre o processamento
        """
        self.status_processamento = status
        self.observacoes = observacoes
        self.updated_at = datetime.now()
    
    def update_ia_response(self, ia_response: Dict[str, Any]):
        """
        Atualiza a resposta da IA
        
        Args:
            ia_response (Dict[str, Any]): Resposta da IA
        """
        self.dados_ia_response = ia_response
        self.updated_at = datetime.now()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentoProcessado':
        """
        Cria um objeto DocumentoProcessado a partir de um dicionário
        
        Args:
            data (Dict[str, Any]): Dados do documento
            
        Returns:
            DocumentoProcessado: Instância do documento
        """
        doc = cls(
            tipo_documento=data.get('tipo_documento'),
            nome_completo=data.get('nome_completo'),
            cpf=data.get('cpf'),
            rg=data.get('rg'),
            data_emissao_rg=data.get('data_emissao_rg'),
            endereco=data.get('endereco'),
            cidade=data.get('cidade'),
            estado=data.get('estado'),
            cep=data.get('cep'),
            email_contato=data.get('email_contato'),
            arquivo_original_nome=data.get('arquivo_original_nome'),
            dados_ia_response=data.get('dados_ia_response')
        )
        
        # Atualiza campos específicos
        if 'id_processo' in data:
            doc.id_processo = data['id_processo']
        
        if 'status_processamento' in data:
            doc.status_processamento = data['status_processamento']
        
        if 'observacoes' in data:
            doc.observacoes = data['observacoes']
        
        return doc
    
    def __str__(self) -> str:
        """Representação string do objeto"""
        return f"DocumentoProcessado(id={self.id_processo}, tipo={self.tipo_documento}, status={self.status_processamento})"
    
    def __repr__(self) -> str:
        """Representação detalhada do objeto"""
        return f"DocumentoProcessado(id_processo='{self.id_processo}', tipo_documento='{self.tipo_documento}', nome_completo='{self.nome_completo}', status_processamento='{self.status_processamento}')" 