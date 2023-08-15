const lanIP = `${window.location.hostname}:5000`;
const socket = io(lanIP);

const querystring = new URLSearchParams(window.location.search);

let btn_find;

let html_devs;


const showDevs = function(json) {
    console.log(json)
    html_string = ''
    for(let i = 0; i < json.length; i++) {
        html_string += `<div class="o-layout__item u-1-of-3">
                        <div class="c-takel">

                            <div class="c-takel__name">
                                <div class="">Name: Takel ${json[i][0].takel_id}</div>
                                <div class="">IP: ${json[i][0].ip}</div>
                            </div>

                            <div class="o-layout">
                                <div class="o-layout__item u-1-of-3">
                                    <div class="c-bar">
                                        <div class="c-bar-progress" data="70"></div>
                                        <div class="c-bar-bol"></div>
                                    </div>
                                </div>
                                <div class="o-layout__item u-2-of-3">
                                    <div class="c-takel__info">
                                        <li class="c-takel__item">Subnet: ${json[i][0].subnet}</li>
                                        <li class="c-takel__item">Universe: ${json[i][0].universe}</li>
                                        <li class="c-takel__item">Channel: ${json[i][0].channel}</li>
                                        <li class="c-takel__item">Position: ${json[i][0].CURR_POS}</li>
                                    </div>

                                    <button class="c-btn-setup" onclick="location.href='setup.html?id=${json[i][0].takel_id}'">setup</button>
                                </div>    
                            </div>

                        </div>`
    }
    html_devs.innerHTML = html_string;
}

const reloadDevs = function(json) {
    console.log(json)
    html_string = ''
    for(let i = 0; i < json.length; i++) {
        console.log(json[i])
        html_string += `<div class="o-layout__item u-1-of-3">
                        <div class="c-takel">

                            <div class="c-takel__name">
                                <div class="">Name: Takel ${json[i].takel_id}</div>
                                <div class="">IP: ${json[i].ip}</div>
                            </div>

                            <div class="o-layout">
                                <div class="o-layout__item u-1-of-3">
                                    <div class="c-bar">
                                        <div class="c-bar-progress" data="70"></div>
                                        <div class="c-bar-bol"></div>
                                    </div>
                                </div>
                                <div class="o-layout__item u-2-of-3">
                                    <div class="c-takel__info">
                                        <li class="c-takel__item">Subnet: ${json[i].subnet}</li>
                                        <li class="c-takel__item">Universe: ${json[i].universe}</li>
                                        <li class="c-takel__item">Channel: ${json[i].channel}</li>
                                        <li class="c-takel__item">Position: ${json[i].CURR_POS}</li>
                                    </div>

                                    <button class="c-btn-setup" onclick="location.href='setup.html?id=${json[i].takel_id}'">setup</button>
                                </div>    
                            </div>

                        </div>`
    }
    html_devs.innerHTML = html_string;
}

const listenToUI = function() {
    btn_find.addEventListener('click', function() {
        socket.emit('F2B_find_devs')
    })
}

const listenToSocket = function() {
    socket.on("B2F_devices", showDevs);

    socket.on('B2F_takel_info', reloadDevs)
}

const get_takel_info = function() {
    takel_id = querystring.get("id");
    socket.emit('F2B_give_takel_id', {
        'id': takel_id
    })
}

const init = function() {
    console.log('DOM loaded')

    btn_find = document.querySelector('.js-find')

    html_devs = document.querySelector('.js-devs')

    if(querystring.get("id")) {
        console.log('id')
        get_takel_info()
    }

    listenToUI();
    listenToSocket();
}


document.addEventListener('DOMContentLoaded', function () {
    init();
})