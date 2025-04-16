let view = 0

window.unload()

socket.on('member_joined', (data) => {
    updatePlayers(data.members);
});

const ownCardsDiv = document.getElementById('own-cards')

function display_cards(ownCards) {
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
    const playerBox = document.getElementById(`player${index}`)
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


function updatePlayers(members) {
    console.log(`my view: ${view}`);
    // console.log(members);
    // 从view的视角看到的玩家信息
    const p2i = (view + 1) % 3;
    const p1i = (view + 2) % 3;
    // console.log(p2i, p1i)

    // 当p2i或p1i不存在于members时，注入虚假的信息
    if (!(p2i in members)) {
        members[p2i] = {name: '虚位以待', card_num: 0}; // 默认card_num为0
    }
    if (!(p1i in members)) {
        members[p1i] = {name: '虚位以待', card_num: 0}; // 默认card_num为0
    }

    render_player(2, members[p2i]);
    render_player(1, members[p1i]);
}

const get_own_cards = async ()=> {
    try {
        const response = await fetch("/game/get_own_cards");
        const result = await response.json();
        if (result.status) {
            return result.cards;
        }
    } catch (error) {
        console.log(error);
        alert("网络连接异常");
    }
}

const get_own_view = async ()=> {
    try {
        const response = await fetch("/game/get_own_view");
        const result = await response.json();
        if (result.status) {
            console.log(result)
            return result.player_id;
        }
    } catch (error) {
        console.log(error);
        alert("网络连接异常");
    }
}
document.addEventListener('DOMContentLoaded', async function () {
    try {
        view = await get_own_view();

        const cards = await get_own_cards();
        display_cards(cards)
    } catch (error) {
        console.error("初始化失败: ", error)
    }
});
