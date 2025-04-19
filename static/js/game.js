let view;
let myStatus;


socket.on('member_joined', () => {
    console.log("新成员加入")
    get_members()
        .then(members => updatePlayersInfo(members))
});

socket.on('member_left', () => {
    console.log("成员离开")
    get_members()
        .then(members => updatePlayersInfo(members))
});

socket.on('status_update', (data) => {
    console.log("状态更新");

    if (data.status[view]) {
        myStatus = 'ready';
    } else {
        myStatus = 'unready';
    }

    // Check if all statuses are true
    const allReady = data.status.every(status => status);
    if (allReady) {
        myStatus = 'gaming';
    }
    update_own_area();
    // update_others_area();
});

const switch_ready = () => {
    socket.emit('change_ready');
}


const leave_room = () => {
    socket.emit('leave_room');
    turn_to('menu.html');
}


function create_cards_div(ownCards, class_name) {
    // const ownCardsDiv = document.getElementById('own-cards')
    const div = document.createElement('div')
    console.log(ownCards);
    div.innerHTML = '';
    ownCards.forEach(card => {
        const img = document.createElement('img');
        img.src = `../static/image/pokers/${card}.png`;
        img.alt = card;  // 这里设置图片的替代文本为卡片名称
        img.classList.add(class_name);  // 添加类属性以便样式控制
        div.appendChild(img);
    });
    return div
}

function update_own_area() {
    const ownStatusArea = document.getElementById('own-status')
    ownStatusArea.innerHTML = '';
    const button = document.createElement('button');
    button.classList.add('start-btn');
    button.onclick = switch_ready;
    if (myStatus === 'unready') {
        button.textContent = " 准 备 ";
        ownStatusArea.appendChild(button);
    } else if (myStatus === 'ready') {
        button.textContent = "取消准备";
        ownStatusArea.appendChild(button);
    } else if (myStatus === 'gaming') {
        get_own_history_cards()
            .then(historyCards => create_cards_div(historyCards, 'own-card'))
            .then(cardsDiv => {
                cardsDiv.classList.add('own-cards')
                ownStatusArea.appendChild(cardsDiv)
            })
        get_own_cards()
            .then(ownCards => create_cards_div(ownCards, 'own-card'))
            .then(cardsDiv => {
                cardsDiv.classList.add('own-cards');
                let ownArea = document.getElementById('own-area');
                ownArea.appendChild(cardsDiv)
            })
    }
}

function render_player_info(index, player) {
    const playerBox = document.getElementById(`player${index}`)
    playerBox.innerHTML = ''; // 清空原有内容
    const playerInfo = document.createElement('div');
    playerInfo.classList.add('player-info');

    const playerName = document.createElement('h3');
    playerName.textContent = player.name;
    playerInfo.appendChild(playerName);

    const playerScore = document.createElement('p');
    playerScore.textContent = `积分: ${player.score}`;
    playerInfo.appendChild(playerScore);

    playerBox.appendChild(playerInfo);
}
function render_player_cards(index, player) {
    const playerBox = document.getElementById(`player${index}`)

    // Remove existing cards container if it exists
    const existingCardsContainer = playerBox.querySelector('#player' + index + '-cards');
    if (existingCardsContainer) {
        playerBox.removeChild(existingCardsContainer);
    }

    const cardsContainer = document.createElement('div');
    cardsContainer.classList.add('cards');
    cardsContainer.id = `player${index}-cards`;

    for (let i = 0; i < player.card_num; i++) {
        const cardBack = document.createElement('img');
        cardBack.classList.add('card-back');
        cardBack.src = '../static/image/yellow_back.png';
        cardBack.alt = 'card-back';
        cardsContainer.appendChild(cardBack);
    }
    playerBox.appendChild(cardsContainer);
}
function render_status_area(index, player) {
    const statusArea = document.getElementById(`player${index}-status`)
    statusArea.innerHTML = '';

}


function updatePlayersInfo(members) {
    console.log(`my view: ${view}`);
    // console.log(members);
    // 从view的视角看到的玩家信息
    const p2i = (view + 1) % 3;
    const p1i = (view + 2) % 3;
    // console.log(p2i, p1i)
    render_player_info(2, members[p2i]);
    render_player_info(1, members[p1i]);
    render_player_cards(2, members[p2i]);
    render_player_cards(1, members[p1i]);
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

const get_own_history_cards = async ()=> {
    try {
        const response = await fetch("/game/get_own_history_cards");
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

const get_members = async ()=> {
    try {
        const response = await fetch("/game/get_members");
        const result = await response.json();
        if (result.status) {
            console.log(result)
            return result.members;
        }
    } catch (error) {
        console.log(error);
        alert("网络连接异常");
    }
}


document.addEventListener('DOMContentLoaded', async function () {
    try {
        view = await get_own_view();

        // const cards = await get_own_cards();
        // display_cards(cards)
    } catch (error) {
        console.error("初始化失败: ", error)
    }
});
