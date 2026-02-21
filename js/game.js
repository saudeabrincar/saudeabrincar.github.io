const gameContainer = document.getElementById('game-container');

// State
let currentScene = 'title';
let magicCollected = 0;

// Content Definition
const scenes = {
    title: {
        render: () => `
            <div class="title-screen">
                <h1 style="font-size: 2rem;">O LOURENÇO FOI OPERADO<br>E O MEDO É QUE FICOU ASSUSTADO…</h1>
                <p style="font-size: 1.5rem; font-weight: bold;">SABES O QUE ACONTECEU?<br>O MEDO ENCOLHEU!</p>
                <button class="next-button" onclick="startGame()">Começar Aventura</button>
            </div>
            <img src="assets/hospital_entrance.png" style="width:100%; height:100%; object-fit: cover; position: absolute; top: 0; left: 0; z-index: -1;">
        `
    },
    scene1: {
        bg: 'url("assets/hospital_entrance.png")',
        render: () => `
            <img id="lourenco" class="character" src="assets/lourenco_isolated.png" alt="Lourenço">
            <img id="ghost" class="character" src="assets/ghost_isolated.png" onclick="talkToGhost()" alt="Fantasma do Medo">
            
            <div id="dialogue" class="dialogue-box">
                <p id="dialogue-text"></p>
                <button id="dialogue-btn" class="next-button" style="display:none;" onclick="nextDialogueSequence()">Continuar</button>
            </div>
        `
    },
    scene2: {
        bg: 'url("assets/hospital_entrance.png")', // Would ideally be a room, reusing for now or we could add a white overly
        render: () => `
            <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(255,255,255,0.8); z-index:0;"></div>
            <img id="anesthesiologist" class="character" src="assets/anesthesiologist_isolated.png" alt="Anestesista">
            <img id="serum-bag" class="character" src="assets/serum_bag_isolated.png" alt="Soro Mágico">
            
            <div id="dialogue2" class="dialogue-box">
                <p id="dialogue-text2"></p>
                <button id="dialogue-btn2" class="next-button" style="display:none;" onclick="startMiniGame()">Continuar</button>
            </div>
        `
    },
    scene3: {
        bg: 'url("assets/hospital_entrance.png")',
        render: () => `
            <div style="position: absolute; top:0; left:0; width:100%; height:100%; background: rgba(255,255,255,0.9); z-index:0;"></div>
            <img id="lourenco-brave" class="character" src="assets/lourenco_isolated.png" style="left: 50%; transform: translateX(-50%); height: 400px; bottom: 20px;" alt="Lourenço Corajoso">
            <div class="title-screen" style="z-index:20; top: 25%;">
                <h1>Parabéns!</h1>
                <p>O Lourenço está cheio de coragem e o medo desapareceu!</p>
                <button class="next-button" onclick="location.reload()">Jogar Novamente</button>
            </div>
        `
    }
};

const dialogues = {
    scene1: [
        "Olá, eu sou o Lourenço. Vou ser operado hoje...",
        "Aquele ali é o meu Medo. Ele não me larga.",
        "Clica nele para vermos o que acontece!"
    ],
    scene2: [
        "Olá Lourenço! Eu sou a Anestesista.",
        "Não precisas de ter medo do bloco operatório.",
        "Tenho aqui um Soro Mágico especial para te dar coragem!",
        "Ajuda-me a capturar as faíscas de coragem para preparar o soro!"
    ]
};

let dialogueIndex = 0;

// Core Engine Functions
function loadScene(sceneName) {
    currentScene = sceneName;
    const scene = scenes[sceneName];

    if (scene.bg) {
        gameContainer.style.backgroundImage = scene.bg;
    }

    gameContainer.innerHTML = scene.render();

    if (sceneName === 'scene1') {
        setTimeout(() => showDialogue('dialogue', 'dialogue-text', dialogues.scene1[0], 'nextDialogueSequence()', 'Continuar'), 500);
    } else if (sceneName === 'scene2') {
        dialogueIndex = 0;
        setTimeout(() => showDialogue('dialogue2', 'dialogue-text2', dialogues.scene2[0], 'nextDialogueScene2()', 'Continuar'), 500);
    }
}

function startGame() {
    loadScene('scene1');
}

// Dialogue System
function showDialogue(boxId, textId, text, nextAction, btnText) {
    const box = document.getElementById(boxId);
    const textEl = document.getElementById(textId);
    const btn = box.querySelector('button');

    box.classList.add('active');
    textEl.innerText = text;

    if (nextAction) {
        btn.style.display = 'inline-block';
        btn.setAttribute('onclick', nextAction);
        if (btnText) btn.innerText = btnText;
    } else {
        btn.style.display = 'none';
    }
}

function nextDialogueSequence() {
    dialogueIndex++;
    if (dialogueIndex < 2) {
        showDialogue('dialogue', 'dialogue-text', dialogues.scene1[dialogueIndex], 'nextDialogueSequence()', 'Continuar');
    } else if (dialogueIndex === 2) {
        showDialogue('dialogue', 'dialogue-text', dialogues.scene1[dialogueIndex], null);
    }
}

function talkToGhost() {
    if (dialogueIndex >= 2) {
        const ghost = document.getElementById('ghost');
        ghost.classList.add('fade-out');
        setTimeout(() => loadScene('scene2'), 1000);
    }
}

function nextDialogueScene2() {
    dialogueIndex++;
    if (dialogueIndex < dialogues.scene2.length - 1) {
        showDialogue('dialogue2', 'dialogue-text2', dialogues.scene2[dialogueIndex], 'nextDialogueScene2()', 'Continuar');
    } else {
        showDialogue('dialogue2', 'dialogue-text2', dialogues.scene2[dialogueIndex], 'startMiniGame()', 'Preparar o Soro!');
    }
}

// Mini Game Logic
function startMiniGame() {
    document.getElementById('dialogue2').classList.remove('active');
    magicCollected = 0;

    for (let i = 0; i < 5; i++) {
        spawnSparkle();
    }
}

function spawnSparkle() {
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    sparkle.style.left = Math.random() * (gameContainer.offsetWidth - 50) + 'px';
    sparkle.style.top = Math.random() * (gameContainer.offsetHeight - 200) + 'px'; // Keep above dialogue area

    sparkle.onclick = function () {
        this.classList.add('fade-out');
        magicCollected++;
        checkMiniGameWin();
        setTimeout(() => this.remove(), 500);
    };

    gameContainer.appendChild(sparkle);
}

function checkMiniGameWin() {
    if (magicCollected >= 5) {
        loadScene('scene3');
    }
}

// Init
window.onload = () => {
    loadScene('title');
};
