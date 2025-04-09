// let socket = io();
// socket.on('connect', function () {
//     console.log("Connected to game server");
// })
let ownCards = [];
let player_names = [];
let player_card_nums = [];


const ownCardsDiv = document.getElementById('own-cards')

function display_cards() {
    console.log(ownCards);
    ownCardsDiv.innerHTML = '';
    ownCards.forEach(card => {
        const img = document.createElement('img');
        img.src = `../static/image/${card}.png`;
        img.alt = card;  // 这里设置图片的替代文本为卡片名称
        img.classList.add('own-card');  // 添加类属性以便样式控制
        ownCardsDiv.appendChild(img);
    });
}

function render_player(index) {
    const playerBox = document.getElementById(`player${index+1}`)
    playerBox.innerHTML = ''; // 清空原有内容
    const playerInfo = document.createElement('div');
    playerInfo.classList.add('player-info');

    const playerName = document.createElement('h3');
    playerName.textContent = player_names[index];
    playerInfo.appendChild(playerName);

    // const playerScore = document.createElement('p');
    // playerScore.textContent = `积分: ${player.score}`;
    // playerInfo.appendChild(playerScore);

    playerBox.appendChild(playerInfo);

    const cardsContainer = document.createElement('div');
    cardsContainer.classList.add('cards');

    for (let i = 0; i < player_card_nums[index]; i++) {
        const cardBack = document.createElement('div');
        cardBack.classList.add('card-back');
        cardsContainer.appendChild(cardBack);
    }
    playerBox.appendChild(cardsContainer);
}


const get_own_cards = async ()=> {
    try {
        const response = await fetch("/game/get_own_cards");
        const result = await response.json();
        console.log(result.code)
        if (result.status) {
            ownCards = result.cards;
        }
    } catch (error) {
        console.log(error);
        alert("网络连接异常");
    }
}

const get_others_name = async ()=> {
    try {
        const response = await fetch("/game/get_others_name");
        const result = await response.json();
        console.log(result.code)
        if (result.status) {
            player_names = result.player_names;
        }
    } catch (error) {
        console.log(error);
        alert("网络连接异常");
    }
}

window.onload = function () {
    get_own_cards()
        .then(None => display_cards());
    get_others_name()
        .then(None => render_player(0))
        .then(None => render_player(1))
}

function playCards() {
    document.getElementById('status').style.display = 'block';
    setTimeout(() => {
        document.getElementById('status').style.display = 'none';
    }, 1000);
}

function passTurn() {
    document.getElementById('status').innerText = '跳过本轮';
    document.getElementById('status').style.display = 'block';
    setTimeout(() => {
        document.getElementById('status').style.display = 'none';
    }, 1000);
}
