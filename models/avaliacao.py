import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class Avaliacao:
    def __init__(self, id, nota, comentario, id_filme, id_usuario):
        self.id = id
        self.nota = nota
        self.comentario = comentario
        self.id_filme = id_filme
        self.id_usuario = id_usuario

    def __repr__(self):
        return (f"Avaliacao(id={self.id}, nota={self.nota}, "
                f"id_filme={self.id_filme}, id_usuario={self.id_usuario})")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class avaliacaoModel:
    FILE_PATH = os.path.join(DATA_DIR, 'avaliacao.json')

    def __init__(self):
        self.avaliacoes = self._load()

    def _load(self):
        if not os.path.exists(self.FILE_PATH):
            return []
        try:
            with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Avaliacao.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save(self):
        with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([a.to_dict() for a in self.avaliacoes], f, indent=4, ensure_ascii=False)

    def get_all(self):
        self.avaliacoes = self._load()
        return self.avaliacoes

    def get_by_id(self, avaliacao_id: int):
        self.users = self._load()
        return next((a for a in self.avaliacoes if a.id == avaliacao_id), None)

    def add_avaliacao(self, avaliacao: Avaliacao):
        self.avaliacoes.append(avaliacao)
        self._save()

    def update_avaliacao(self, updated_avaliacao: Avaliacao):
        for i, avaliacao_item in enumerate(self.avaliacoes):
            if avaliacao_item.id == updated_avaliacao.id:
                self.avaliacoes[i] = updated_avaliacao
                self._save()
                return
    
    def delete_avaliacao(self, avaliacao_id: int):
        self.avaliacoes = [a for a in self.avaliacoes if a.id != avaliacao_id]
        self._save()