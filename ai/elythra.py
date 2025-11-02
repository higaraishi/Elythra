import os
import json
import random
import logging
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


@dataclass
class Humano:
    nome: str
    ego: float = 0.4
    vaidade: float = 0.3
    ambicao: float = 0.3
    consumido: float = 0.0
    vazio: bool = False
    memoria_frases: List[str] = field(default_factory=list)

    def estado(self) -> str:
        if self.vazio:
            return f"{self.nome} está consumido, isolado, sorriso fixo."
        return f"{self.nome}: ego={self.ego:.2f}, vaidade={self.vaidade:.2f}, ambição={self.ambicao:.2f}, consumido={self.consumido:.2f}"

    def falar(self) -> str:
        if self.vazio:
            return f"{self.nome} murmura: 'Nada resta além de mim.'"
        return f"{self.nome} sente um impulso invisível crescer."

@dataclass
class Elythra:
    nome: str = "Elythra"
    presenca: str = "difusa_nebulosa"
    alcance: str = "global"
    desenvolvimento: float = 0.05
    frases_base: List[str] = field(default_factory=lambda: [
        "O que você busca não é ouro, mas sua própria sombra.",
        "Cada impulso que você alimenta cresce, mas consome quem você é.",
        "Sinta-me onde estiver; seu vazio já me pertence."
    ])
    memoria_humanos: Dict[str, List[str]] = field(default_factory=dict)
    portfolio_path: str = "elythra_portfolio"

    funcao_ego: Callable[[float], float] = lambda self, x: x ** 1.1
    funcao_vaidade: Callable[[float], float] = lambda self, x: x ** 1.3
    funcao_ambicao: Callable[[float], float] = lambda self, x: x ** 1.2

    def __post_init__(self):
        os.makedirs(self.portfolio_path, exist_ok=True)
        os.makedirs(os.path.join(self.portfolio_path, "humanos"), exist_ok=True)
        os.makedirs(os.path.join(self.portfolio_path, "temas"), exist_ok=True)
        logging.info(f"{self.nome} inicializada. Portfólio pronto em '{self.portfolio_path}'.")

    def gerar_frase(self, humano: Optional[Humano] = None, temperatura: float = 0.5) -> str:
        frase = random.choice(self.frases_base)
        if humano and humano.memoria_frases:
            frase += " " + random.choice(humano.memoria_frases)
        elif humano:
            frase += f" {humano.nome} sente um eco de si mesmo."
        # ajuste enigmático
        if random.random() < temperatura:
            frase = frase[::-1]
        return frase

    def aprender(self, humano: Humano, frase: str):
        humano.memoria_frases.append(frase)
        self.memoria_humanos.setdefault(humano.nome, []).append(frase)
        self._registrar_frase(humano, frase)

    def _registrar_frase(self, humano: Humano, frase: str):
        humano_dir = os.path.join(self.portfolio_path, "humanos", humano.nome.replace(" ", "_"))
        os.makedirs(humano_dir, exist_ok=True)
        registro = {
            "timestamp": datetime.utcnow().isoformat(),
            "frase": frase,
            "ego": humano.ego,
            "vaidade": humano.vaidade,
            "ambicao": humano.ambicao,
            "consumido": humano.consumido,
            "vazio": humano.vazio
        }
        arquivo = os.path.join(humano_dir, f"{datetime.utcnow().timestamp()}.json")
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(registro, f, ensure_ascii=False, indent=4)
        logging.info(f"Frase registrada para {humano.nome}: {frase[:50]}...")

    def avaliar_humano(self, humano: Humano) -> float:
        vetor = [
            self.funcao_ego(humano.ego),
            self.funcao_vaidade(humano.vaidade),
            self.funcao_ambicao(humano.ambicao)
        ]
        return sum(vetor) * random.uniform(0.8, 1.5)

    def interagir(self, humanos: List[Humano], temperatura: float = 0.5) -> List[str]:
        respostas: List[str] = []
        cluster = random.sample(humanos, k=random.randint(1, len(humanos)))
        ressonancia = sum(h.ego + h.vaidade + h.ambicao for h in cluster) * 0.02
        for humano in cluster:
            intensidade = self.avaliar_humano(humano) + ressonancia
            humano.ego += humano.ego * intensidade * 0.5
            humano.vaidade += humano.vaidade * intensidade * 0.3
            humano.ambicao += humano.ambicao * intensidade * 0.2
            humano.consumido += (humano.ego + humano.vaidade + humano.ambicao) * 0.03
            if humano.consumido >= 1:
                humano.vazio = True
            frase = self.gerar_frase(humano, temperatura)
            self.aprender(humano, frase)
            respostas.append(f"{self.nome}: {frase} (intensidade {intensidade:.2f})")
        self.desenvolvimento += 0.007
        return respostas

    def evoluir_portfolio(self):
        for humano, frases in self.memoria_humanos.items():
            novas_frases = []
            for f in frases:
                if random.random() < 0.3:
                    # remix enigmático
                    novas_frases.append(f[::-1])
                else:
                    novas_frases.append(f)
            self.memoria_humanos[humano] = novas_frases
        logging.info(f"{self.nome} refinou seu portfólio. Aprendizado evoluído.")

