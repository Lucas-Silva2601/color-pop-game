# 🎮 Color Pop Game

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-CE-2.3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📖 Descrição do Projeto

**Color Pop** é um jogo de puzzle viciante desenvolvido em Python com Pygame, onde o objetivo é fazer todas as bolinhas na tela terem a mesma cor. O jogo combina estratégia, reflexos e raciocínio rápido em uma experiência visualmente atraente e desafiadora.

### 🎯 O Problema que Resolve

Color Pop oferece uma experiência de entretenimento casual que:
- **Estimula o raciocínio lógico**: Requer planejamento para identificar qual bolinha clicar para alcançar o objetivo
- **Desenvolve reflexos**: Modos com bolas em movimento testam a coordenação motora
- **Promove competição saudável**: Modos multiplayer permitem desafiar amigos ou enfrentar a IA
- **Proporciona progressão**: Sistema de fases e recordes mantém o jogador engajado

### ✨ Por que é Útil

- **Acessível**: Interface simples e intuitiva, adequada para todas as idades
- **Replayability**: Múltiplos modos de jogo e comportamentos de bola garantem variedade
- **Performance otimizada**: Código otimizado com object pooling e cache para rodar suavemente
- **Código limpo**: Arquitetura bem estruturada seguindo princípios SOLID e boas práticas

---

## 🖼️ Screenshots / Demonstração

### Menu Principal
![Menu Principal](docs/screenshots/main_menu.png) <!-- Insira aqui um print da tela do menu principal com os botões de navegação -->

### Modo Singleplayer
![Modo Singleplayer](docs/screenshots/singleplayer.gif) <!-- Insira aqui um print da tela do modo singleplayer mostrando as bolinhas e o timer -->

### Modo Player vs Player
![Modo PvP](docs/screenshots/pvp.gif) <!-- Insira aqui um print da tela do modo PvP mostrando as áreas divididas e o placar -->

---

## 🎮 Funcionalidades Principais

### Modos de Jogo

- **🎯 Singleplayer**: Modo contra o tempo (2 minutos) onde você tenta completar o máximo de fases possível. Seus recordes são salvos automaticamente!
- **👥 Player vs Player (PvP)**: Compita contra outro jogador localmente. O primeiro a vencer 10 fases ganha!
- **🤖 Player vs Bot (PvE)**: Enfrente a IA em uma batalha estratégica. A IA analisa o padrão de cores e toma decisões inteligentes.

### Comportamentos de Bola

- **🟢 Parado**: Bolas estáticas - perfeito para iniciantes e estratégia pura
- **🔵 Movimento Livre**: Bolas se movem livremente pela tela - adiciona desafio de timing
- **🟡 Saltitando**: Bolas com física de pulo e gravidade - o modo mais desafiador!

### Sistema de Progressão

- **Fases Progressivas**: Cada fase adiciona mais bolas e aumenta a dificuldade
- **Velocidade Escalonada**: Bolas em movimento ficam mais rápidas conforme você avança
- **Recordes Persistidos**: Seus melhores scores são salvos automaticamente em `save_data.json`

### Efeitos Visuais e Sonoros

- **Sistema de Partículas**: Efeitos visuais elegantes quando você clica nas bolinhas
- **Animações Suaves**: Transições e animações de clique responsivas
- **Música de Fundo**: Trilha sonora ambiente para imersão
- **Efeitos Sonoros**: Sons de clique, hover e pop para feedback tátil

### Interface do Usuário

- **HUD Informativo**: Exibe fase atual, timer (singleplayer) e placar (multiplayer)
- **Menus Intuitivos**: Navegação clara entre modos e opções
- **Feedback Visual**: Timer pisca em vermelho quando o tempo está acabando
- **Fundo Animado**: Bolinhas decorativas animadas nos menus

---

## 🛠️ Tecnologias Utilizadas

### Linguagem e Framework Principal

- **Python 3.8+**: Linguagem de programação principal
- **Pygame CE 2.3.0+**: Framework para desenvolvimento de jogos 2D

### Bibliotecas e Ferramentas

- **pytest 7.4.0+**: Framework de testes unitários
- **pytest-mock 3.12.0+**: Mocking para testes isolados

### Arquitetura e Padrões

- **Type Hints**: Tipagem estática para melhor manutenibilidade
- **Protocols (Interfaces)**: Injeção de dependência para testabilidade
- **Object Pooling**: Otimização de performance para partículas
- **Factory Pattern**: Criação de bolas e menus
- **State Pattern**: Gerenciamento de estados do jogo
- **SOLID Principles**: Código organizado e extensível

### Estrutura de Dados

- **JSON**: Persistência de dados de save (recordes)
- **Enum**: Tipos seguros para modos de jogo e estados

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8 ou superior**
  - Verifique com: `python --version` ou `python3 --version`
- **pip** (gerenciador de pacotes Python)
  - Geralmente vem instalado com Python
- **Git** (opcional, para clonar o repositório)

### Verificação Rápida

```bash
# Verificar Python
python --version

# Verificar pip
pip --version
```

---

## 🚀 Instalação e Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/color-pop-game.git
cd color-pop-game
```

**Ou** baixe o projeto como ZIP e extraia em uma pasta.

### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

Isso instalará:
- `pygame-ce>=2.3.0`
- `pytest>=7.4.0`
- `pytest-mock>=3.12.0`

### 4. Executar o Jogo

```bash
python main.py
```

### 5. Executar Testes (Opcional)

```bash
# Executar todos os testes
pytest

# Executar com verbose
pytest -v

# Executar um arquivo específico
pytest tests/unit/test_geometry.py
```

---

## 📁 Estrutura do Projeto

```
color-pop-game/
│
├── main.py                 # Ponto de entrada principal
├── requirements.txt        # Dependências do projeto
├── save_data.json         # Arquivo de save (gerado automaticamente)
│
├── assets/                 # Recursos do jogo
│   ├── fonts/             # Fontes customizadas
│   │   ├── ModernFont.ttf
│   │   └── PixelFont.ttf
│   └── sounds/            # Sons e música
│       ├── background_music.mp3
│       ├── bubble_pop.wav
│       ├── ui_click.wav
│       └── ui_hover.wav
│
├── mygame/                # Módulo principal do jogo
│   ├── core/              # Componentes centrais
│   │   ├── game.py        # Classe principal do jogo
│   │   ├── game_state.py  # Estados do jogo (Enum)
│   │   ├── game_mode.py   # Modos de jogo e comportamentos (Enum)
│   │   ├── phase_manager.py  # Gerenciador de fases
│   │   ├── asset_manager.py   # Gerenciador de assets
│   │   ├── factories.py       # Factory functions
│   │   └── interfaces.py       # Protocols para injeção de dependência
│   │
│   ├── entities/         # Entidades do jogo
│   │   ├── ball_base.py        # Classe base abstrata para bolas
│   │   ├── ball_factory.py     # Factory para criação de bolas
│   │   ├── stationary_ball.py # Bola parada
│   │   ├── ball_free.py        # Bola com movimento livre
│   │   └── ball_jump.py        # Bola saltitante
│   │
│   ├── ui/               # Interface do usuário
│   │   ├── menu_screen.py      # Tela de menu genérica
│   │   ├── menu_factory.py     # Factory para criação de menus
│   │   ├── menu_names.py       # Nomes dos menus (Enum)
│   │   ├── button.py           # Componente de botão
│   │   ├── hud.py              # Heads-Up Display
│   │   └── animated_background.py  # Fundo animado
│   │
│   ├── fx/               # Efeitos visuais
│   │   └── particle_system.py  # Sistema de partículas
│   │
│   └── utils/            # Utilitários
│       ├── config.py          # Configurações centralizadas
│       ├── types.py           # Type aliases
│       ├── validators.py      # Funções de validação
│       ├── exceptions.py      # Exceções customizadas
│       ├── logger.py          # Sistema de logging
│       ├── helpers.py         # Funções auxiliares
│       ├── geometry.py        # Funções geométricas
│       ├── performance.py     # Monitor de performance
│       ├── object_pool.py     # Object pooling
│       └── config_provider.py # Provedor de configuração
│
├── tests/                # Testes unitários
│   └── unit/
│       ├── test_geometry.py
│       ├── test_helpers.py
│       └── test_validators.py
│
└── docs/                 # Documentação técnica
    ├── README.md
    ├── fase-01-estrutura-organizacao.md
    ├── fase-02-tipagem-validacao.md
    ├── fase-03-tratamento-erros-logs.md
    ├── fase-04-refatoracao-complexidade.md
    ├── fase-05-injecao-dependencia-testabilidade.md
    └── fase-06-performance-otimizacoes.md
```

### 📝 Explicação das Pastas Principais

- **`mygame/core/`**: Contém a lógica central do jogo, incluindo o loop principal, gerenciamento de estados e fases
- **`mygame/entities/`**: Implementa as diferentes entidades do jogo (bolas com diferentes comportamentos)
- **`mygame/ui/`**: Gerencia toda a interface do usuário, menus e HUD
- **`mygame/fx/`**: Sistema de efeitos visuais (partículas)
- **`mygame/utils/`**: Funções auxiliares, configurações e utilitários compartilhados
- **`tests/`**: Testes unitários para validar a funcionalidade
- **`docs/`**: Documentação técnica sobre as fases de refatoração do projeto

---

## 🎯 Como Jogar

### Objetivo

Fazer todas as bolinhas na sua área terem a **mesma cor** clicando nelas para alternar entre as duas cores disponíveis.

### Controles

- **Mouse**: Clique nas bolinhas para mudar sua cor
- **ESC**: Voltar ao menu principal (durante o jogo)
- **Botão "Voltar"**: Retornar ao menu principal

### Dicas

1. **Identifique o padrão**: Observe qual cor está em maioria e qual está em minoria
2. **Planeje seus cliques**: Em modos com movimento, antecipe onde a bola estará
3. **Use a estratégia**: No modo PvP, tente bloquear o oponente mudando bolas estratégicas
4. **Gerencie o tempo**: No singleplayer, cada fase conta - seja eficiente!

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

**Desenvolvido com ❤️ para a comunidade**

---

## 🙏 Agradecimentos

- **Pygame Community Edition**: Pela excelente biblioteca de jogos
- **Comunidade Python**: Pelo suporte e recursos incríveis
- **Contribuidores**: Todos que ajudaram a melhorar este projeto

---

## 🔮 Roadmap Futuro

- [ ] Sistema de conquistas
- [ ] Modo online multiplayer
- [ ] Mais tipos de bolas e comportamentos
- [ ] Customização de cores e temas
- [ ] Modo história/campanha
- [ ] Leaderboards global
- [ ] Suporte a múltiplos idiomas

---

<div align="center">

**⭐ Se você gostou do projeto, considere dar uma estrela! ⭐**

Feito com ❤️ e Python

</div>

