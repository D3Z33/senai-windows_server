# 🔒 **Projeto - Windows Server_Senai**

--

<div align="center">

[![Status](https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge)](#)
[![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue?style=for-the-badge&logo=python)](#)
[![Licença](https://img.shields.io/badge/Licença-Educacional-orange?style=for-the-badge)](#)

</div>

---

</div>

<div align="center">
  <img src="senai-windows_server/arquivos/senai_logo.png" alt="Logo do Projeto">
</div>

---

## 📋 **Tabela de Conteúdos**

1️⃣ [Sobre o Projeto](#sobre-o-projeto)  
2️⃣ [Estrutura do Projeto](#estrutura-do-projeto)  
3️⃣ [Como Usar](#como-usar)  
4️⃣ [Aprendizados e Impacto](#aprendizados-e-impacto)  
5️⃣ [Contato e Redes](#-contato-e-redes)

---
## **Sobre o Projeto**

Bem-vindo ao **projeto mais imersivo e transformador** que você verá hoje! 🚀 Este não é apenas um projeto com milhares de linhas ded código; é uma **experiência completa** criada para ensinar, desafiar e surpreender alunos e profissionais na área de segurança da informação.

Desenvolvido ao longo de **quatro meses intensos**, este projeto nasceu de uma ideia no papel em agosto e foi executado com maestria até sua conclusão e execução em 10 de dezembro. Durante este tempo, transformamos um desafio lançado pelo professor Fontes — **escalar privilégios** — em uma solução educativa e impactante, totalmente elaborada em Python. Foram **muitas noites em claro, testes incessantes e superação de limites** para entregar um trabalho que realmente faz a diferença.

### **Objetivo Principal**
Demonstrar, de forma prática e didática, como **pequenos descuidos em configurações de sistemas ou permissões excessivas** podem comprometer a segurança de uma infraestrutura inteira.

Prepare-se para um projeto que combina:
- 🔐 **Cenários reais de escalação de privilégios**, explorando vulnerabilidades do mundo real.
- 🌟 **Gamificação interativa e criativa**, onde cada detalhe foi pensado para uma experiência prática e educativa.
- 😅 **Humor educativo e provocações hilárias**, transformando aprendizado em diversão inesquecível.

---

## **Principais Funcionalidades**

### 🖥️ **Interface Interativa**
- Desenvolvida com **Tkinter**, a interface oferece uma experiência **imersiva e dinâmica**:
  - **Pop-ups interativos**: Alguns necessitam de interação do aluno para prosseguir, enquanto outros simulam eventos automáticos do sistema.
  - **Questões aleatórias**: 15 perguntas criadas para ensinar de forma leve e divertida.
  - **Temporizador**: 60 segundos por pergunta, com reinício a cada nova questão. Na última, o tempo é congelado para encerramento da prova.
  - **Barra de progresso**: Acompanhada de mensagens motivadoras (ou provocativas) que evoluem conforme o desempenho do aluno.

### 🛡️ **Arquivos Maliciosos Educativos**
- **9 exemplos simulados de ameaças reais**: Incluem Backdoor, Keylogger, Worm, Adware, etc.
  - Arquivos maliciosos são inseridos em **pastas pouco usuais** no sistema.
  - Cada arquivo acompanha um **.txt explicativo**, detalhando o impacto e a forma de mitigação.
  - **Execução bloqueada** sem a leitura prévia do arquivo .txt, garantindo que o aluno entenda os riscos antes de prosseguir.

### 🔒 **Escalação de Privilégios**

A exploração de permissões administrativas ou configurações inadequadas do sistema foi exemplificada por 9 arquivos maliciosos cuidadosamente desenvolvidos, cada um simulando uma ameaça real. Aqui está um **spoiler** do que cada um deles faz:

- **Adware (`adware_senai.py`)**: Simula a criação de janelas pop-up persistentes, demonstrando como softwares invasivos podem bombardear o sistema com anúncios.  
- **Backdoor (`backdoor_senai.py`)**: Abre uma porta de comunicação (4444), permitindo acesso remoto e coletando informações sensíveis como IP, hardware e versão do sistema operacional.  
- **Cryptominer (`cryptominer_senai.py`)**: Mostra o impacto de um minerador de criptomoedas, utilizando recursos da máquina de forma indesejada e consumindo CPU e memória.  
- **Downloader (`downloader_senai.py`)**: Automatiza o download e a execução de arquivos adicionais, exemplificando como um malware pode expandir seu alcance.  
- **File Manager (`file_manager.py`)**: Manipula pastas e arquivos do sistema, destacando o perigo de permissões mal configuradas.  
- **Keylogger (`keylogger_senai.py`)**: Captura as entradas de teclado do usuário, simulando o roubo de credenciais e outras informações sensíveis.  
- **Spyware (`spyware_senai.py`)**: Monitora atividades no sistema, coletando dados confidenciais como histórico de navegação e uso de aplicativos.  
- **Notifier (`notifi_senai.py`)**: Envia relatórios e notificações sobre atividades da máquina para um destinatário remoto, ilustrando um comportamento típico de malwares de vigilância.  
- **Worm (`worm_senai.py`)**: Demonstra a propagação autônoma em dispositivos conectados, simulando um cenário de ataque em rede.

Cada arquivo acompanha um `.txt` explicativo, detalhando o funcionamento, o impacto e as medidas de mitigação associadas à ameaça. Esses arquivos foram projetados para proporcionar uma experiência educacional imersiva, enfatizando os riscos e desafios enfrentados no ambiente corporativo.

### 📲 **Integração com Telegram**
- Envio de **dados em tempo real** para o Telegram de informações cruciais diretamente para o Telegram, garantindo total controle e monitoramento das atividades da prova:
  - Dados coletados incluem: endereço IP, permissões de usuário, localização (quando disponível), tipo de conta, sistema operacional, e diversos detalhes adicionais.
  - Relatórios detalhados sobre a execução de cada arquivo malicioso são enviados, permitindo análise precisa e rápida das interações realizadas durante a prova.

### 🧹 **Scripts de Limpeza**
- Inclui o arquivo `remover_arquivos.py`, que permite ao aluno limpar o ambiente de teste após concluir a prova.

---

## **Estrutura do Projeto**

### **Pasta: `arquivos`**
A pasta `arquivos` contém os componentes essenciais para o funcionamento do projeto, cada um desempenhando um papel crítico na execução e interação da prova. Aqui está um detalhamento de cada arquivo:

- 🧠 **`prova.py`**: O coração do projeto. Este é o arquivo principal que executa a prova interativa, gerenciando perguntas, respostas, temporizadores e toda a interface baseada em Tkinter.

- 🧹 **`remover_arquivos.py`**: Script dedicado à limpeza do ambiente após a execução da prova. Ele remove todos os arquivos maliciosos simulados e restaura o sistema ao estado inicial.

- 🛠️ **`utilitarios.py`**: Um conjunto de funções auxiliares que oferece suporte geral ao projeto. Este arquivo gerencia operações de fundo, como validações, manipulação de arquivos e elementos gráficos.

- 📲 **`notificacao_prova.py`**: Gerencia a integração com o Telegram. Ele envia notificações em tempo real com detalhes das execuções realizadas, incluindo informações sensíveis como IP, permissões de usuário e muito mais.

- 🔌 **`desligar_maquina.py`**: Responsável pelo controle remoto de dispositivos conectados. Este script permite desligar ou reiniciar máquinas de forma programada, destacando as brechas de permissões administrativas.

- 👀 **`monitor_arquivos.py`**: Monitora as atividades durante a execução da prova, garantindo o registro de eventos relevantes e o funcionamento correto dos scripts maliciosos simulados.

- 🖼️ **`senai_logo.png`**: Arquivo de imagem utilizado na interface gráfica do projeto, reforçando a identidade visual do sistema.

Cada um desses arquivos foi desenvolvido com modularidade em mente, garantindo um código organizado e de fácil manutenção.

### **Pasta: `maliciosos`**
A pasta `maliciosos` armazena os arquivos simulados que representam diferentes tipos de ameaças cibernéticas. Cada arquivo foi projetado para educar sobre seu funcionamento e impacto. Aqui está uma visão geral:

- 🛡️ **`backdoor_senai.py`**: Simula uma backdoor, abrindo a porta 4444 para conexões externas e coletando dados sensíveis como IP e hardware.  
  - 📄 **`backdoor_senai.txt`**: Explica o funcionamento da backdoor e como mitigar os riscos associados.

- 📊 **`adware_senai.py`**: Gera pop-ups incessantes para demonstrar como softwares adware podem bombardear um sistema.  
  - 📄 **`adware_senai.txt`**: Descreve o impacto do adware e as melhores práticas para evitá-lo.

- 💻 **`keylogger_senai.py`**: Captura entradas do teclado, simulando um ataque de roubo de credenciais.  
  - 📄 **`keylogger_senai.txt`**: Explica como funciona um keylogger e as formas de prevenção.

- 🔄 **`worm_senai.py`**: Demonstra como um worm se replica e se propaga para outros dispositivos conectados.  
  - 📄 **`worm_senai.txt`**: Fornece detalhes sobre a propagação de worms e estratégias de contenção.

- 💾 **`file_manager.py`**: Manipula arquivos e pastas para mostrar o que um malware pode fazer com permissões excessivas.  
  - 📄 **`file_manager.txt`**: Detalha os riscos e as medidas de proteção.

- 🕵️ **`spyware_senai.py`**: Monitora atividades no sistema, coletando informações confidenciais como histórico de navegação.  
  - 📄 **`spyware_senai.txt`**: Explica como os spywares operam e como proteger sua privacidade.

- 🚀 **`downloader_senai.py`**: Baixa e executa arquivos adicionais automaticamente, ampliando o alcance do ataque.  
  - 📄 **`downloader_senai.txt`**: Descreve os perigos do downloader e formas de mitigação.

- 💰 **`cryptominer_senai.py`**: Simula a mineração de criptomoedas, consumindo recursos do sistema sem permissão.  
  - 📄 **`cryptominer_senai.txt`**: Explica o impacto dos mineradores e as maneiras de detectar sua presença.

- 📢 **`notifi_senai.py`**: Envia notificações com dados capturados para um ponto remoto, simulando o comportamento de spyware avançado.  
  - 📄 **`notifi_senai.txt`**: Detalha as funções do script e como rastrear seu funcionamento.

Cada arquivo malicioso acompanha um **.txt explicativo** para oferecer uma experiência educacional completa, detalhando o impacto e as medidas de mitigação. Esses exemplos foram projetados para ilustrar ameaças reais de forma segura e controlada.

---

## **Como Usar**
⚠ **Atenção**: Este projeto foi criado **exclusivamente para fins educacionais** e deve ser utilizado **apenas em ambientes controlados**. Ele não foi feito para brincadeiras irresponsáveis ou experimentos fora de contexto. Se você está pensando em executá-lo no seu sistema principal, **pare agora mesmo e repense suas escolhas**! 

Por questões de segurança (e sanidade), **o código-fonte não será fornecido a qualquer pessoa**. Apenas aqueles que **realmente entendem o que estão fazendo** terão acesso, e isso significa saber compilar, executar e **não causar caos desnecessário no sistema ou na rede**. Se você não tem certeza, consulte alguém que saiba ou… melhor ainda, estude mais antes de tentar algo assim. 🧠

Agora que deixamos isso claro, aqui vai o guia para os **responsáveis e preparados**:

1. **Execute o arquivo `prova.py`** em uma máquina virtual com as permissões devidamente configuradas. Lembre-se: ambiente isolado, sem exceções.  
2. **Responda às questões** dentro do tempo limite de cada pergunta. O temporizador está lá para pressionar, não para enfeitar.  
3. **Explore as pastas e arquivos gerados** para compreender os cenários simulados. Cada arquivo é uma lição prática de como algo aparentemente inofensivo pode se tornar um grande problema.  
4. **Limpe tudo ao terminar** utilizando o script `remover_arquivos.py`. Afinal, ninguém quer deixar rastros maliciosos no sistema (nem mesmo no ambiente controlado).  

⚡ **Aviso importante**: Qualquer tentativa de executar este projeto em ambientes inadequados, sem conhecimento ou sem a devida responsabilidade, pode resultar em **consequências desastrosas** (e provavelmente engraçadas… para os outros, não para você). Lembre-se: a melhor defesa contra ataques cibernéticos é o conhecimento, e não a imprudência. 😉

Se você chegou até aqui, parabéns! Agora, seja sensato, divirta-se com o aprendizado e leve esta experiência como um poderoso exemplo de como a segurança digital nunca deve ser subestimada.

---

## **Aprendizados e Impacto**

### 🎯 **Desafios Superados**
Este projeto foi um verdadeiro laboratório de aprendizado, onde cada obstáculo se tornou uma oportunidade para crescer e aprimorar habilidades. Entre os maiores desafios superados, podemos destacar:

- 🚀 **Desenvolver uma interface intuitiva e responsiva com Tkinter**: Criar uma interface que fosse ao mesmo tempo funcional, esteticamente agradável e educativa foi um desafio recompensador. Foi necessário combinar elementos visuais com funcionalidades práticas, garantindo uma navegação fluida e engajante para os usuários.  
- 🔧 **Implementar tratativas de erro robustas**: Não podíamos deixar margem para erros comprometedores. Cada detalhe foi trabalhado para prevenir falhas e garantir uma experiência controlada e segura. Isso incluiu mensagens dinâmicas, feedbacks imediatos para entradas inválidas e mecanismos para lidar com situações inesperadas.  
- 🔐 **Criar um bypass no Windows Defender**: Aqui a complexidade foi elevada! O desafio era demonstrar, de forma educativa, como permissões mal configuradas podem abrir portas para ataques. Desenvolvi um método criativo para desativar o Windows Defender temporariamente, com o consentimento do usuário, e demonstrar as consequências dessa ação.  
- 📄 **Documentar cada arquivo malicioso**: Um dos maiores esforços foi garantir que cada ameaça tivesse uma documentação clara e didática. Isso incluiu a criação de explicações detalhadas no formato `.txt`, que orientavam os usuários sobre o funcionamento, impacto e as formas de mitigação das ameaças representadas.

### 🎉 **Destaques do Projeto**
O projeto não apenas entregou aprendizado técnico, mas também me trouxe momentos memoráveis que marcaram a jornada de desenvolvimento. Eis os maiores destaques:

- 🌟 **Gamificação inovadora**: Transformamos um exercício técnico em uma experiência divertida e interativa. Questões hilárias, pop-ups dinâmicos, mensagens provocativas e uma barra de progresso cativante garantiram que o aprendizado fosse leve e envolvente, mantendo o aluno imerso no desafio do início ao fim.  
- 😲 **Exploração real de vulnerabilidades**: Em um dos momentos mais marcantes, descobrimos uma falha real nos sistemas da sala. Sim, ao ajustar a data e hora do sistema, conseguimos explorar o cache de senhas administrativas armazenadas localmente. Isso nos permitiu elevar privilégios e controlar todas as máquinas conectadas.  
- 🖥️ **Controle remoto total**: Utilizando comandos como `arp` e `nmap`, mapeei a rede inteira e desenvolvi scripts que me permitiu desligar ou reiniciar máquinas remotamente. Este recurso não apenas demonstrou o impacto de permissões elevadas, mas também enfatizou a importância de boas práticas na configuração de redes e sistemas.  
- 🎮 **O botão \"Tudo ou Nada\"**: Como parte do design interativo, incluí um botão que, ao ser clicado, iniciava um ciclo de execução do código completo. Esse elemento trouxe um toque de suspense e engajamento ao final da experiência.  
- 🍒 **A cereja do bolo**: O que realmente tornou o projeto único foi o desfecho épico. Não só consegui mapear toda a rede da sala, mas também explorei com sucesso a brecha de cache de senhas para elevar privilégios em massa. Cada máquina conectada ficou sob meu controle \u2014 mas sempre com o foco educacional. Este momento coroou meses de aprendizado e dedicação, mostrando como o conhecimento pode ser poderoso quando aplicado com responsabilidade.  

Este projeto não foi apenas uma demonstração técnica; foi uma experiência completa que misturou aprendizado, criatividade e momentos de descoberta. Ele mostrou como é possível transformar desafios em oportunidades e como cada linha de código pode contar uma história de inovação e impacto.

---

## 🔗 Contato e Redes

- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github)](https://github.com/D3Z33)
- [![Discord](https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/users/deze_e)

---

**Desenvolvido com paixão, criatividade e um toque de genialidade (e algumas noites sem dormir)!**  

Este projeto é mais do que apenas linhas de código; é o resultado de uma jornada cheia de aprendizado, risadas, desafios superados e momentos de "E se..." que viraram realidade. Uma prova viva de que, quando você combina determinação, conhecimento e um pouco de cafeína (ok, muita cafeína), o impossível se torna apenas mais uma etapa no caminho.

E se você chegou até aqui, parabéns! Você não só leu sobre um projeto incrível, mas também testemunhou como ideias simples podem se transformar em algo grandioso. Agora, respire fundo, reflita sobre tudo o que acabou de explorar e, quem sabe, deixe-se inspirar a criar algo tão ousado quanto isso.

**Afinal, o conhecimento é a arma mais poderosa — e quando você aprende a usá-lo com propósito, o impacto é simplesmente inigualável.** 🚀
