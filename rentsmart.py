from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


CENTAVO = Decimal("0.01")


def dinheiro(valor: Decimal) -> Decimal:
    """Arredonda valores monetários para duas casas decimais."""
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def formatar_brl(valor: Decimal) -> str:
    """Formata Decimal como moeda brasileira."""
    texto = f"{dinheiro(valor):,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class Imovel(ABC):
    """Classe-base para os tipos de imóvel da imobiliária."""

    def __init__(self, quartos: int, vagas: int):
        self.quartos = quartos
        self.vagas = vagas

    @property
    @abstractmethod
    def valor_base(self) -> Decimal:
        pass

    @abstractmethod
    def calcular_adicionais(self) -> Decimal:
        pass

    @abstractmethod
    def descricao(self) -> str:
        pass

    def calcular_aluguel_antes_desconto(self) -> Decimal:
        return dinheiro(self.valor_base + self.calcular_adicionais())


class Apartamento(Imovel):
    def __init__(self, quartos: int, possui_criancas: bool, tem_garagem: bool):
        if quartos not in (1, 2):
            raise ValueError("Apartamento aceita 1 ou 2 quartos.")
        super().__init__(quartos, 1 if tem_garagem else 0)
        self.possui_criancas = possui_criancas
        self.tem_garagem = tem_garagem

    @property
    def valor_base(self) -> Decimal:
        return Decimal("700.00")

    def calcular_adicionais(self) -> Decimal:
        adicional_quarto = Decimal("200.00") if self.quartos == 2 else Decimal("0.00")
        adicional_garagem = Decimal("300.00") if self.tem_garagem else Decimal("0.00")
        return adicional_quarto + adicional_garagem

    def calcular_desconto(self, subtotal: Decimal) -> Decimal:
        if not self.possui_criancas:
            return dinheiro(subtotal * Decimal("0.05"))
        return Decimal("0.00")

    def descricao(self) -> str:
        return f"Apartamento - {self.quartos} quarto(s), garagem: {'sim' if self.tem_garagem else 'não'}"


class Casa(Imovel):
    def __init__(self, quartos: int, tem_garagem: bool):
        if quartos not in (1, 2):
            raise ValueError("Casa aceita 1 ou 2 quartos.")
        super().__init__(quartos, 1 if tem_garagem else 0)
        self.tem_garagem = tem_garagem

    @property
    def valor_base(self) -> Decimal:
        return Decimal("900.00")

    def calcular_adicionais(self) -> Decimal:
        adicional_quarto = Decimal("250.00") if self.quartos == 2 else Decimal("0.00")
        adicional_garagem = Decimal("300.00") if self.tem_garagem else Decimal("0.00")
        return adicional_quarto + adicional_garagem

    def descricao(self) -> str:
        return f"Casa - {self.quartos} quarto(s), garagem: {'sim' if self.tem_garagem else 'não'}"


class Estudio(Imovel):
    def __init__(self, vagas: int):
        # Regra interpretada: 0 vagas não contrata pacote; a partir de 2 vagas,
        # o pacote inicial custa R$ 250. Não há opção de apenas 1 vaga no enunciado.
        if vagas == 1 or vagas < 0:
            raise ValueError("Para estúdio, escolha 0 vagas ou pelo menos 2 vagas.")
        super().__init__(0, vagas)

    @property
    def valor_base(self) -> Decimal:
        return Decimal("1200.00")

    def calcular_adicionais(self) -> Decimal:
        if self.vagas == 0:
            return Decimal("0.00")
        adicionais = Decimal("250.00")
        if self.vagas > 2:
            adicionais += Decimal(self.vagas - 2) * Decimal("60.00")
        return adicionais

    def descricao(self) -> str:
        return f"Estúdio - vagas contratadas: {self.vagas}"


@dataclass
class Orcamento:
    imovel: Imovel
    parcelas_contrato: int
    taxa_contratual: Decimal = Decimal("2000.00")

    def __post_init__(self):
        if not 1 <= self.parcelas_contrato <= 5:
            raise ValueError("A taxa contratual pode ser parcelada de 1 a 5 vezes.")

    @property
    def valor_base(self) -> Decimal:
        return self.imovel.valor_base

    @property
    def adicionais(self) -> Decimal:
        return dinheiro(self.imovel.calcular_adicionais())

    @property
    def subtotal(self) -> Decimal:
        return dinheiro(self.valor_base + self.adicionais)

    @property
    def desconto(self) -> Decimal:
        if isinstance(self.imovel, Apartamento):
            return self.imovel.calcular_desconto(self.subtotal)
        return Decimal("0.00")

    @property
    def aluguel_mensal(self) -> Decimal:
        return dinheiro(self.subtotal - self.desconto)

    @property
    def parcela_contrato(self) -> Decimal:
        return dinheiro(self.taxa_contratual / Decimal(self.parcelas_contrato))

    def exibir_resumo(self) -> None:
        print("\n" + "=" * 48)
        print("                 RENTSMART")
        print("           ORÇAMENTO DE LOCAÇÃO")
        print("=" * 48)
        print(f"Imóvel:                    {self.imovel.descricao()}")
        print(f"Aluguel-base:              {formatar_brl(self.valor_base)}")
        print(f"Adicionais:                {formatar_brl(self.adicionais)}")
        print(f"Subtotal:                  {formatar_brl(self.subtotal)}")
        print(f"Desconto:                  {formatar_brl(self.desconto)}")
        print("-" * 48)
        print(f"ALUGUEL MENSAL:            {formatar_brl(self.aluguel_mensal)}")
        print(f"Taxa contratual:           {formatar_brl(self.taxa_contratual)}")
        print(f"Parcelamento:              {self.parcelas_contrato}x de {formatar_brl(self.parcela_contrato)}")
        print("=" * 48)
        print("A taxa contratual é separada do aluguel mensal.")

    def gerar_projecao_csv(self, caminho: Path) -> None:
        """Gera a previsão de aluguel e taxa contratual para os 12 meses."""
        valor_restante = self.taxa_contratual
        with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow([
                "Mes", "Aluguel mensal (R$)", "Parcela contratual (R$)",
                "Total previsto no mes (R$)", "Saldo da taxa contratual (R$)"
            ])
            for mes in range(1, 13):
                parcela = Decimal("0.00")
                if mes <= self.parcelas_contrato:
                    if mes < self.parcelas_contrato:
                        parcela = self.parcela_contrato
                    else:
                        # Ajuste de centavos na última parcela para fechar exatamente R$ 2.000.
                        parcela = dinheiro(valor_restante)
                    valor_restante = dinheiro(valor_restante - parcela)

                total = dinheiro(self.aluguel_mensal + parcela)
                escritor.writerow([
                    mes,
                    f"{self.aluguel_mensal:.2f}".replace(".", ","),
                    f"{parcela:.2f}".replace(".", ","),
                    f"{total:.2f}".replace(".", ","),
                    f"{valor_restante:.2f}".replace(".", ",")
                ])


def ler_inteiro(mensagem: str, minimo: int, maximo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo or (maximo is not None and valor > maximo):
                limite = f" e no máximo {maximo}" if maximo is not None else ""
                print(f"Digite um número a partir de {minimo}{limite}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Responda com S para sim ou N para não.")


def coletar_imovel() -> Imovel:
    print("\nTIPO DE IMÓVEL")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    tipo = ler_inteiro("Escolha uma opção: ", 1, 3)

    if tipo == 1:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja uma vaga de garagem? (S/N): ")
        criancas = ler_sim_nao("O cliente possui crianças? (S/N): ")
        return Apartamento(quartos, criancas, garagem)

    if tipo == 2:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja uma vaga de garagem? (S/N): ")
        return Casa(quartos, garagem)

    vagas = ler_inteiro(
        "Quantidade de vagas para estúdio (0 ou a partir de 2): ", 0
    )
    while vagas == 1:
        print("O enunciado prevê pacote inicial de 2 vagas; 1 vaga não está prevista.")
        vagas = ler_inteiro("Digite 0 ou pelo menos 2 vagas: ", 0)
    return Estudio(vagas)


def main() -> None:
    print("=" * 48)
    print("Bem-vindo(a) ao RentSmart - R.M Imóveis")
    imovel = coletar_imovel()
    parcelas = ler_inteiro("Em quantas vezes deseja pagar a taxa contratual (1 a 5)? ", 1, 5)

    orcamento = Orcamento(imovel, parcelas)
    orcamento.exibir_resumo()

    destino = Path(__file__).resolve().parent / "projecao_12_meses.csv"
    orcamento.gerar_projecao_csv(destino)
    print(f"\nArquivo CSV gerado com sucesso: {destino.name}")


if __name__ == "__main__":
    main()
