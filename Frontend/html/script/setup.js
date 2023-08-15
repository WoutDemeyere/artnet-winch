const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

const querystring = new URLSearchParams(window.location.search);


let takel_id, takel_ip;


let slider = 0;

let html_ip, html_name;

let btn_up, btn_down, btn_top, btn_low, btn_set_vals, btn_set_zero, btn_back;

let val_sub, val_uni, val_chan, val_speed;

const listenToUI = function () {
    slider.oninput = function () {
        console.log('change in pos')
        socket.emit("F2B_change_pos", {
            'ip': takel_ip,
            'pos': this.value
        })
    }


    btn_down.addEventListener('mousedown', move_down);
    btn_down.addEventListener('touchstart', move_down);

    btn_down.addEventListener('mouseup', stop_moving);
    btn_down.addEventListener('touchcancel', stop_moving);

    btn_up.addEventListener('mousedown', move_up);
    btn_up.addEventListener('touchstart', move_up);

    btn_up.addEventListener('mouseup', stop_moving);
    btn_up.addEventListener('touchcancel', stop_moving);

    btn_top.addEventListener('mousedown', function () {
        console.log('SET: top')
        socket.emit('F2B_set_start', {
            'ip': takel_ip,
            'start': true
        })
    });
    btn_top.addEventListener('touchstart', function () {
        socket.emit('F2B_set_start', {
            'ip': takel_ip,
            'start': true
        })
    });

    btn_top.addEventListener('mouseup', function () {
        socket.emit('F2B_set_start', {
            'ip': takel_ip,
            'start': false
        })
    });
    btn_top.addEventListener('touchcancel', function () {
        socket.emit('F2B_set_start', {
            'ip': takel_ip,
            'start': false
        })
    });

    btn_low.addEventListener('mousedown', function () {
        console.log('SET: low')
        socket.emit('F2B_set_end', {
            'ip': takel_ip,
            'end': true
        })
    });
    btn_low.addEventListener('touchstart', function () {
        socket.emit('F2B_set_end', {
            'ip': takel_ip,
            'end': true
        })
    });
    btn_low.addEventListener('mouseup', function () {
        socket.emit('F2B_set_end', {
            'ip': takel_ip,
            'end': false
        })
    });
    btn_low.addEventListener('touchcancel', function () {
        socket.emit('F2B_set_end', {
            'ip': takel_ip,
            'end': false
        })
    });

    btn_set_zero.addEventListener('mousedown', function () {
        console.log('SET: zero')
        socket.emit('F2B_set_zero', {
            'ip': takel_ip,
            'set': true
        })
    });
    btn_set_zero.addEventListener('touchstart', function () {
        socket.emit('F2B_set_zero', {
            'ip': takel_ip,
            'set': true
        })
    });
    btn_set_zero.addEventListener('mouseup', function () {
        socket.emit('F2B_set_zero', {
            'ip': takel_ip,
            'set': false
        })
    });
    btn_set_zero.addEventListener('touchcancel', function () {
        socket.emit('F2B_set_zero', {
            'ip': takel_ip,
            'set': false
        })
    });

    btn_set_vals.addEventListener('click', setValues)

    btn_back.addEventListener('click', function () {
        location.href=`index.html?id=${takel_id}`
    });

};


const listenToSocket = function () {
    socket.on("connected", function () {
        console.log("Verbonden met de socekt");
    });

    socket.on("B2F_takel_info", function (json) {
        console.log(json)
        takel_ip = json[0].ip;
        takel_ip = json[0].ip;

        html_ip.innerHTML = `IP: ${takel_ip}`;
        html_name.innerHTML = `Name: Takel ${takel_id}`;
    });

};

const setValues = function() {
    val_sub = document.getElementById("sub").value;
    val_uni = document.getElementById("uni").value;
    val_chan = document.getElementById("chan").value;
    val_speed = document.getElementById("spd").value;

    socket.emit('F2B_set_art_vals', {'ip': takel_ip, 'sub': val_sub, 'uni': val_uni, 'chan': val_chan})
};
 
const setZero = function() {
    socket.emit('F2B_set_art_vals', {'ip': takel_ip, 'set': true})
};

const getInfo = function () {
    takel_id = querystring.get("id")
    socket.emit('F2B_give_takel_id', {
        'id': takel_id
    })
};

const move_up = function () {
    console.log('MOVE: up')
    socket.emit('F2B_move', {
        'ip': takel_ip,
        'mv': 'up'
    })
}

const move_down = function () {
    console.log('MOVE: down')
    socket.emit('F2B_move', {
        'ip': takel_ip,
        'mv': 'down'
    })
}

const stop_moving = function () {
    console.log('MOVE: stop')
    socket.emit('F2B_move', {
        'ip': takel_ip,
        'mv': 'none'
    })
}

document.addEventListener('DOMContentLoaded', function () {
    console.info('DOM geladen');
    console.info('AYO geladen');

    slider = document.querySelector('.js-slider');

    html_ip = document.querySelector('.js-ip');
    html_name = document.querySelector('.js-name');

    btn_up = document.querySelector('.js-mv-up');
    btn_down = document.querySelector('.js-mv-down');

    btn_top = document.querySelector('.js-top');
    btn_low = document.querySelector('.js-low');

    btn_set_vals = document.querySelector('.js-submit');
    btn_set_zero = document.querySelector('.js-set-zero');

    btn_back = document.querySelector('.js-back')

    getInfo();

    listenToUI();
    listenToSocket();
});