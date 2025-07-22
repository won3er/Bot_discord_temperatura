# Verificação de Roles do Discord Companion

## 1. Introdução
Este documento descreve o processo de verificação de roles para o Discord Companion.

## 2. Requisitos para Verificação

### 2.1 Permissões Mínimas
- Permissão para enviar mensagens
- Permissão para ler mensagens
- Permissão para usar comandos do bot

### 2.2 Configuração do Servidor
1. O bot deve ter permissões de administrador
2. Deve haver um canal designado para comandos
3. Deve haver um canal designado para logs

## 3. Processo de Verificação

### 3.1 Comandos de Verificação
- `!verify`: Inicia o processo de verificação
- `!roles`: Lista as roles disponíveis
- `!link`: Vincula uma conta externa

### 3.2 Verificação de Usuário
1. Usuário envia comando de verificação
2. Bot envia mensagem de confirmação
3. Usuário responde com código de verificação
4. Bot confirma e atribui roles

## 4. Roles Disponíveis

### 4.1 Roles Básicas
- `Verified`: Usuário verificado
- `Weather`: Acesso a comandos de clima
- `Admin`: Administrador do bot

### 4.2 Roles Especiais
- `Weather Expert`: Acesso a comandos avançados
- `Supporter`: Suporte ao projeto
- `Developer`: Desenvolvedores do bot

## 5. Gerenciamento de Roles

### 5.1 Adição de Roles
- Roles devem ser adicionadas pelo administrador
- Roles devem ser configuradas com permissões apropriadas
- Roles devem ser documentadas

### 5.2 Remoção de Roles
- Roles podem ser removidas por violação de termos
- Roles podem ser removidas por inatividade
- Roles podem ser removidas por solicitação do usuário

## 6. Segurança

### 6.1 Proteção de Roles
- Roles administrativas devem ter proteção apropriada
- Logs devem ser mantidos de atribuições de roles
- Verificações devem ser registradas

### 6.2 Prevenção de Abuso
- Limites de rate para comandos de verificação
- Monitoramento de atividades suspeitas
- Sistema de alerta para atividades anormais

## 7. Suporte
Para qualquer dúvida sobre o processo de verificação, entre em contato através do servidor de suporte do Discord Companion.
