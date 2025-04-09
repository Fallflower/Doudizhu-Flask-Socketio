// let socket = io();
// socket.on('connect', function () {
//     console.log("Connected to game server");
// })
let ownCards = [];
let room_id = 1;
let player_id = 1;


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

window.onload = function () {
    get_own_cards()
        .then(None => display_cards());
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
