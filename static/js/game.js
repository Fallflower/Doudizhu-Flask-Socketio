let ownCards = [];
// let player_names = [];
// let player_card_nums = [];

socket.on('member_joined', (data) => {
    console.log('fuck and this is member_joined');
    updatePlayers(data.player_id, data.members);
});

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

function render_player(index, player) {
    const playerBox = document.getElementById(`player${index+1}`)
    playerBox.innerHTML = ''; // 清空原有内容
    const playerInfo = document.createElement('div');
    playerInfo.classList.add('player-info');

    const playerName = document.createElement('h3');
    playerName.textContent = player.name;
    playerInfo.appendChild(playerName);

    // const playerScore = document.createElement('p');
    // playerScore.textContent = `积分: ${player.score}`;
    // playerInfo.appendChild(playerScore);

    playerBox.appendChild(playerInfo);

    const cardsContainer = document.createElement('div');
    cardsContainer.classList.add('cards');

    for (let i = 0; i < player.card_num; i++) {
        const cardBack = document.createElement('img');
        cardBack.classList.add('card-back');
        cardBack.src = '../static/image/yellow_back.png'
        cardBack.alt = 'card-back';
        cardsContainer.appendChild(cardBack);
    }
    playerBox.appendChild(cardsContainer);
}


function updatePlayers(view, members) {
    console.log(`my view: ${view}`)
    console.log(members)
    // 从view的视角看到的玩家信息
    let p2i = (view + 1) % 3
    let p1i = (view + 2) % 3
    render_player(p2i, members[p2i]);
    render_player(p1i, members[p1i]);
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
    // get_others_name()
    //     .then(None => render_player(0))
    //     .then(None => render_player(1))
}

