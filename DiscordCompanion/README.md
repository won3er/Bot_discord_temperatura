# Discord Weather Bot 🤖🌡️

Um bot Discord para consultar temperatura de cidades brasileiras usando a API Open-Meteo, com interface web complementar.

## 🚀 Características

- **Bot Discord** com comandos intuitivos em português
- **Interface web** moderna e responsiva
- **Todas as capitais estaduais** e principais cidades
- **60+ cidades brasileiras** suportadas
- **Dados em tempo real** via API Open-Meteo
- **Tratamento de erros** robusto
- **Design responsivo** com Bootstrap
- **Embeds ricos** no Discord
- **Organização por regiões** na interface web

## 🏙️ Cidades Suportadas

### Capitais Estaduais (27)
**Norte:** Rio Branco, Macapá, Manaus, Belém, Porto Velho, Boa Vista, Palmas

**Nordeste:** Maceió, Salvador, Fortaleza, São Luís, João Pessoa, Recife, Teresina, Natal, Aracaju

**Centro-Oeste:** Goiânia, Cuiabá, Campo Grande, Brasília

**Sudeste:** Vitória, Belo Horizonte, Rio de Janeiro, São Paulo

**Sul:** Curitiba, Porto Alegre, Florianópolis

### Principais Cidades (30+)
**São Paulo:** Campinas, Guarulhos, São Bernardo do Campo, Santo André, Osasco, Ribeirão Preto, Sorocaba, Santos

**Rio de Janeiro:** Nova Iguaçu, Duque de Caxias, Niterói, São Gonçalo

**Minas Gerais:** Contagem, Uberlândia, Juiz de Fora

**Paraná:** Londrina, Maringá

**Santa Catarina:** Joinville, Blumenau

**Rio Grande do Sul:** Caxias do Sul, Pelotas

**Bahia:** Feira de Santana

**Pernambuco:** Olinda, Caruaru, Petrolina

**Paraíba:** Campina Grande

**Ceará:** Juazeiro do Norte, Sobral, Caucaia

**Maranhão:** Imperatriz

**Rio Grande do Norte:** Parnamirim

## 🤖 Comandos do Bot Discord

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `!t <cidade>` | Mostra temperatura atual | `!t recife` |
| `!cidades` | Lista todas as cidades | `!cidades` |
| `!help` | Mostra ajuda dos comandos | `!help` |

## 🛠️ Configuração

### Pré-requisitos

- Python 3.11 ou superior
- PostgreSQL
- Discord.py
- Flask
- SQLAlchemy

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/discord-companion.git
cd discord-companion
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env com as seguintes variáveis:
DISCORD_BOT_TOKEN=seu_token_aqui
FLASK_SECRET_KEY=chave_secreta_aqui
DATABASE_URL=postgresql://user:password@localhost/db_name
```

### Executando o Projeto

1. Inicie o banco de dados PostgreSQL

2. Inicie a interface web:
```bash
python web_interface.py
```

3. Inicie o bot do Discord:
```bash
python bot.py
```

### Variáveis de Ambiente

```bash
# Discord Bot
DISCORD_BOT_TOKEN=seu_token_aqui

# Flask
FLASK_SECRET_KEY=chave_secreta_aqui

# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/db_name
