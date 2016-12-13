// TIMER //
var time_type = 'time_limited';
var timeintervalTimer = null;
var userTime = 0;

function startTimer(countdownFlag) {
    clearInterval(timeintervalTimer);
    var starttime = setUpTimeForTimer(countdownFlag);
    initializeClock('clockdiv', starttime);

    function initializeClock(id, starttime) {
        var clock = document.getElementById(id);
        var milisecsSpan = clock.querySelector('.miliseconds');
        var secondsSpan = clock.querySelector('.seconds');

        function updateClock() {
            var t = getTimeRemaining(starttime, countdownFlag);
            milisecsSpan.innerHTML = ('0' + t.miliseconds).slice(-2);
            secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

            if (t.total <= 0) {
                milisecsSpan.innerHTML = '00';
                secondsSpan.innerHTML = '00';
                stopTimer(countdownFlag);
            }
        }

        timeintervalTimer = setInterval(updateClock, 10);
    }
}

function setUpTimeForTimer(countdownFlag) {
    var time = new Date();
    if (time_type == 'time_limited' || countdownFlag == true) {
        time = new Date(Date.parse(new Date()) + userTime);
    }
    return time;
}

function getTimeRemaining(time, countdownFlag) {
    var t = 0;
    if (time_type == 'time_limited' || countdownFlag == true) {
        t = time.getTime() - new Date().getTime();
    } else if (time_type == 'timeless') {
        t = new Date().getTime() - time.getTime();
    }
    return getTimeDifference(t);
}

function getTimeDifference(t) {
    var miliseconds = Math.floor((t / 10));
    var seconds = Math.floor((t / 1000) % 60);
    return {
        'total': t,
        'seconds': seconds,
        'miliseconds': miliseconds
    };
}

function stopTimer(countdownFlag) {
    clearInterval(timeintervalTimer);
    if (time_type == 'time_limited' || countdownFlag == true) {
        manageConfigurations();
        startTimer(false);
    }
}

function saveTime() {
}

// BULBS //

var bulbsOnCnt = 0;
var curConfsIndex = 0;
var confsNumber = 1023;
var confs = new Array(confsNumber);
var feedback_type = 'feedback';
var configurationSucceeded = false;

function checkKey() {
    document.onkeydown = function (e) {
        if (e.keyCode >= 48 && e.keyCode <= 57) {
            var bulbId = 'bulb' + (e.keyCode - 48).toString();
            var bulb = document.getElementById(bulbId);
            if (bulb.src.split("/").slice(-1) == "bulb-on.png") {
                bulb.src = "/static/exp/bulb-off.png";
                --bulbsOnCnt;
                if (bulbsOnCnt == 0) {
                    configurationSucceeded = true;
                    if (curConfsIndex < confsNumber) {
                        saveTime();
                        if (time_type == 'timeless') {
                            startTimer(true);
                        }
                    }
                }
            } else if (bulb.src.split("/").slice(-1) == "bulb-off.png"
                        && feedback_type == 'feedback') {
                document.getElementById('wa_beep').play();
            }
        }
    }
}

function shuffle(a) {
    var x;
    for (var i = a.length; i > 0; i--) {
        var j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

function createConfigurations() {
    for (var i = 0, len = confs.length; i < len; ++i) {
        confs[i] = i + 1;
    }
    shuffle(confs);
}

function manageConfigurations() {
    if (curConfsIndex < confsNumber) {
        updateProgressBar();
        clearBulbs();
        displayConfiguration(confs[curConfsIndex]);
        ++curConfsIndex;
    }
}

function displayConfiguration(conf) {
    for (var i = 0; i < 10; ++i) {
        var bulbId = 'bulb' + i.toString();
        var bulb = document.getElementById(bulbId);
        if ((conf & (1 << i)) != 0) {
            ++bulbsOnCnt;
            bulb.src = "/static/exp/bulb-on.png";
        }
    }
}

function updateProgressBar() {
    document.getElementById('progress_bar').style.width = ((curConfsIndex / confsNumber) * 100).toString() + '%';
}

function clearBulbs() {
    for (var i = 0; i < 10; ++i) {
         document.getElementById('bulb' + i).src = "/static/exp/bulb-off.png";
    }
}

// MODAL //
function showModal() {
    var modalHeader = document.getElementById('modal-header-title');
    if (time_type == 'timeless') {
        modalHeader.innerHTML = 'Set some additional time for each configuration';
    } else if (time_type == 'time_limited') {
        modalHeader.innerHTML = 'Set time for each configuration';
    }
    $('#myModal').modal('show');
}

function modalCloseBtn() {
    userTime = parseInt(document.getElementById('user_time').value);
    var interval = setInterval(function() {
        createConfigurations();
        checkKey();
        manageConfigurations();
        startTimer(false);
        clearInterval(interval);
    }, 500);
}

// When the user clicks anywhere outside of the modal, close it.
window.onclick = function(event) {
    if (event.target == document.getElementById('myModal')) {
        modalCloseBtn();
    }
};
