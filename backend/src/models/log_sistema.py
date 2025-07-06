"""
Modelo de dados para logs do sistema
"""
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class LogSistema:
    """
    Classe que representa um log do sistema
    
    Attributes:
        id (int): ID único do log
        id_processo (str): UUID do processo relacionado
        tipo_log (str): Tipo do log (INFO, WARNING, ERROR, DEBUG)
        nivel (str): Nível do log (INFO, WARNING, ERROR, DEBUG)
        mensagem (str): Mensagem do log
        detalhes (Dict): Detalhes adicionais em JSON
        timestamp (datetime): Data/hora do log
    """
    
    def __init__(self, 
                 id_processo: str,
                 tipo_log: str,
                 mensagem: str,
                 nivel: str,
                 detalhes: Optional[Dict[str, Any]] = None,
                 timestamp: Optional[datetime] = None):
        """
        Inicializa um novo log do sistema
        
        Args:
            id_processo (str): UUID do processo relacionado
            tipo_log (str): Tipo do log (INFO, WARNING, ERROR, DEBUG)
            mensagem (str): Mensagem do log
            nivel (str): Nível do log (INFO, WARNING, ERROR, DEBUG)
            detalhes (Dict, optional): Detalhes adicionais
            timestamp (datetime, optional): Data/hora do log
        """
        self.id = None  # Será definido pelo banco
        self.id_processo = id_processo
        self.tipo_log = tipo_log
        self.nivel = nivel.upper()
        self.mensagem = mensagem
        self.detalhes = detalhes or {}
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto para dicionário
        
        Returns:
            Dict[str, Any]: Dicionário com os dados do log
        """
        return {
            'id': self.id,
            'id_processo': self.id_processo,
            'tipo_log': self.tipo_log,
            'nivel': self.nivel,
            'mensagem': self.mensagem,
            'detalhes': self.detalhes,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LogSistema':
        """
        Cria um objeto LogSistema a partir de um dicionário
        
        Args:
            data (Dict[str, Any]): Dados do log
            
        Returns:
            LogSistema: Instância do log
        """
        log = cls(
            id_processo=data.get('id_processo'),
            tipo_log=data.get('tipo_log', 'INFO'),
            mensagem=data.get('mensagem', ''),
            nivel=data.get('nivel', 'INFO'),
            detalhes=data.get('detalhes'),
            timestamp=datetime.fromisoformat(data['timestamp']) if 'timestamp' in data and isinstance(data['timestamp'], str) else None
        )
        
        if 'id' in data:
            log.id = data['id']
        
        return log
    
    def __str__(self) -> str:
        """Representação string do objeto"""
        return f"LogSistema({self.nivel}: {self.mensagem})"
    
    def __repr__(self) -> str:
        """Representação detalhada do objeto"""
        return f"LogSistema(id={self.id}, nivel='{self.nivel}', mensagem='{self.mensagem}', timestamp='{self.timestamp}')" 