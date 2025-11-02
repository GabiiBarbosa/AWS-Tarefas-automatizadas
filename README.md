# Automação de Tarefas com AWS Lambda e Amazon S3

A integração entre **Amazon S3** (para armazenamento de objetos) e **AWS Lambda** (para processamento sem servidor) é o modelo clássico para automatizar tarefas em resposta a eventos de upload de arquivos.

## O que é o Padrão S3 + Lambda?

Este padrão cria um **Fluxo de Processamento Orientado a Eventos (Event-Driven)**:

1.  **Evento:** Um arquivo é carregado (ou modificado/excluído) em um *bucket* S3.
2.  **Gatilho (Trigger):** O S3 envia uma notificação (o evento) ao AWS Lambda.
3.  **Processamento:** A função Lambda é executada automaticamente para processar o arquivo.

| Componente | Função | Exemplo de Uso |
| :--- | :--- | :--- |
| **Amazon S3** | Armazenamento de dados não estruturados. | Onde o arquivo original (`notas_fiscais.json`) é salvo. |
| **AWS Lambda** | Código de back-end sem servidor. | Lógica para ler o JSON, validá-lo e inseri-lo no DynamoDB. |

---

## Passos para Configurar a Automação

### 1. Preparação do Código da Função Lambda

O código da função deve estar pronto para:

* Receber o objeto `event` do S3.
* Extrair o **nome do *bucket*** e a **chave (caminho)** do arquivo que foi carregado.
* Usar o SDK do AWS (`boto3`) para baixar o arquivo do S3.
* Processar o conteúdo (ex: ler o JSON) e executar a tarefa desejada (ex: salvar no DynamoDB).

### 2. Criação do Pacote de Deploy (`.zip`)

Antes de criar ou atualizar a função, empacotar código Python (e quaisquer dependências) em um arquivo `.zip`.

### 3. Criação da Função Lambda (usando endpoint local)

### 4. Configuração do Gatilho S3 (O Passo de Automação)

Configurar uma notificação de evento no bucket de origem para que o S3 acione sua função Lambda sempre que um arquivo for criado.

## Como Testar o Fluxo Automatizado
Copie o arquivo para o S3: O S3 registra o evento de upload.

```bash
aws s3 cp notas_fiscais.json s3://notas-fiscais-upload/notas_fiscais.json --endpoint-url=http://localhost:4566
```
A Automação é Ativada: O S3 envia a notificação para o Lambda.

A Função Lambda Roda: Sua função ProcessarNotasFiscais é executada para processar o arquivo recém-chegado.
