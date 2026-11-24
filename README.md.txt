# RentSmart — Sistema de Orçamento de Locação

Projeto acadêmico em Python para automatizar os orçamentos de locação da R.M Imóveis, aplicando Programação Orientada a Objetos.

## Requisitos
- Python 3.10 ou superior.
- Não utiliza bibliotecas externas: apenas recursos da biblioteca padrão do Python.

## Como executar
1. Baixe ou clone este repositório.
2. Abra a pasta do projeto no VS Code.
3. Abra o terminal integrado.
4. Execute:

```bash
python rentsmart.py
```

No Windows, se o comando acima não funcionar, tente:

```bash
py rentsmart.py
```

5. Responda às perguntas no terminal.
6. O sistema exibirá o orçamento e criará `projecao_12_meses.csv` na mesma pasta do programa.

## Regras implementadas
- Apartamento: base de R$ 700,00; segundo quarto acrescenta R$ 200,00; garagem acrescenta R$ 300,00.
- Casa: base de R$ 900,00; segundo quarto acrescenta R$ 250,00; garagem acrescenta R$ 300,00.
- Estúdio: base de R$ 1.200,00; pacote inicial de duas vagas custa R$ 250,00; cada vaga acima de duas acrescenta R$ 60,00.
- Apartamento sem crianças recebe desconto de 5% após os adicionais.
- Taxa contratual de R$ 2.000,00, parcelada de 1 a 5 vezes e exibida separadamente.
- CSV com aluguel, parcela contratual, total mensal e saldo da taxa nos 12 meses.

## Estrutura de classes
- `Imovel`: classe abstrata com atributos comuns e operações que cada tipo implementa.
- `Apartamento`: regras de apartamento e desconto específico.
- `Casa`: regras de casa.
- `Estudio`: regra própria de estacionamento.
- `Orcamento`: reúne o imóvel, calcula os valores e gera o CSV.

## Premissas adotadas
1. Para casas e apartamentos, o enunciado descreve uma vaga de garagem como adicional; por isso, o programa pergunta se o cliente deseja uma vaga.
2. Para estúdios, considera-se 0 vagas ou pacote inicial de 2 vagas. A opção de somente 1 vaga não foi definida no enunciado e, por isso, não é aceita. A partir da terceira vaga, cada vaga adicional custa R$ 60,00.
3. A taxa contratual é dividida em parcelas iguais, com eventual ajuste de centavos na última parcela para que a soma seja exatamente R$ 2.000,00.
4. A projeção considera o mesmo aluguel nos 12 meses, sem reajustes, multas, condomínio ou outros encargos, pois esses itens não foram especificados no enunciado.

## Testes manuais sugeridos
- Apartamento de 1 quarto, sem garagem, sem crianças: aluguel de R$ 665,00.
- Apartamento de 2 quartos, com garagem e com crianças: aluguel de R$ 1.200,00.
- Casa de 2 quartos, com garagem: aluguel de R$ 1.450,00.
- Estúdio com 4 vagas: aluguel de R$ 1.570,00.
- Conferir que a taxa contratual totaliza R$ 2.000,00 no número de parcelas escolhido.

## Entrega acadêmica
Consulte `documentacao_teorica.pdf` e `roteiro_video_pitch.md` para apoiar a apresentação. Revise os materiais e personalize os dados de identificação antes de enviar.
