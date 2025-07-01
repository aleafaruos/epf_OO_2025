import json
import os
# from dataclasses import dataclass, asdict # Provavelmente não estava sendo usado

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Avaliacao:
    def __init__(self, id, nota, nome_usuario, comentario=None): # id pode não ter sido usado ou era manual
        self.id = id
        self.nota = nota
        self.nome_usuario = nome_usuario
        self.comentario = comentario if comentario is not None else "" # Já garantia que era string

    def __repr__(self):
        return f"Avaliacao(id={self.id}, nota={self.nota}, nome_usuario='{self.nome_usuario}', comentario='{self.comentario}')"

    def to_dict(self):
        return {
            'id': self.id,
            'nota': self.nota,
            'nome_usuario': self.nome_usuario,
            'comentario': self.comentario
        }

    @classmethod
    def from_dict(cls, data):
        # A forma de carregar 'id' e 'comentario' pode ter sido mais simples
        return cls(
            id=data['id'],
            nota=data['nota'],
            nome_usuario=data['nome_usuario'],
            comentario=data.get('comentario', '') # Pode já estar com get para evitar KeyError
        )


class avaliacaoModel:
    FILE_PATH = os.path.join(DATA_DIR, 'avaliacao.json')

    def __init__(self):
        self.avaliacao = self._load() # Note que era 'self.avaliacao' singular

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        try:
            # Pode não ter tido encoding='utf-8' explicitamente, ou tratamento de erro tão robusto
            with open(self.FILE_PATH, 'r') as f: 
                data = json.load(f)
                return [Avaliacao.from_dict(item) for item in data]
        except json.JSONDecodeError:
            return [] # Talvez um tratamento simples ou nenhum
        except FileNotFoundError:
            return []

    def _save(self):
        # Pode não ter tido encoding='utf-8' explicitamente
        with open(self.FILE_PATH, 'w') as f:
            json.dump([a.to_dict() for a in self.avaliacao], f, indent=4)


    def get_all(self):
        return self.avaliacao


    def get_by_id(self, avaliacao_id: int):
        # Este método era para buscar UMA avaliação pelo seu ID ÚNICO.
        for a in self.avaliacao:
            if a.id == avaliacao_id:
                return a
        return None


    def add_avaliacao(self, avaliacao: Avaliacao):
        # Nesta versão, o ID era provavelmente esperado vir já setado no objeto avaliacao,
        # ou a geração era manual/simples, sem garantia de unicidade robusta.
        self.avaliacao.append(avaliacao)
        self._save()


    def update_user(self, updated_avaliacao: Avaliacao): # Note que era 'update_user' aqui
        # Esta era a lógica original que você tinha, que foi apontada como problema
        # porque chamava update_user e não update_avaliacao.
        for i, avaliacao_item in enumerate(self.avaliacao):
            if avaliacao_item.id == updated_avaliacao.id:
                self.avaliacao[i] = updated_avaliacao
                self._save()
                return True
        return False

    def delete_user(self, avaliacao_id: int): # Note que era 'delete_user' aqui
        # Similarmente, aqui era delete_user.
        initial_len = len(self.avaliacao)
        self.avaliacao = [a for a in self.avaliacao if a.id != avaliacao_id]
        if len(self.avaliacao) < initial_len:
            self._save()
            return True
        return False