// TIMER //
var time_type = 'time_limited';
var timeintervalCountdown = null;
var timeintervalTimer = null;

function startCountdown() {
    var deadline = new Date(Date.parse(new Date()) + 1 * 30 * 1000);
    initializeClock('clockdiv', deadline);

    function getTimeRemaining(endtime) {
        var t = Date.parse(endtime) - Date.parse(new Date());
        var seconds = Math.floor((t / 1000) % 60);
        var minutes = Math.floor((t / 1000 / 60) % 60);
        return {
            'total': t,
            'minutes': minutes,
            'seconds': seconds
        };
    }

    function initializeClock(id, endtime) {
        var clock = document.getElementById(id);
        var minutesSpan = clock.querySelector('.minutes');
        var secondsSpan = clock.querySelector('.seconds');

        function updateClock() {
            var t = getTimeRemaining(endtime);
            minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
            secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

            if (t.total <= 0) {
              clearInterval(timeintervalCountdown);
            }
        }

        updateClock();
        timeintervalCountdown = setInterval(updateClock, 1000);
    }
}

function startTimer() {
    var starttime = new Date();
    initializeClock('clockdiv', starttime);

    function getTimeRemaining(starttime) {
        var t = Date.parse(new Date()) - Date.parse(starttime);
        var seconds = Math.floor((t / 1000) % 60);
        var minutes = Math.floor((t / 1000 / 60) % 60);
        return {
            'total': t,
            'minutes': minutes,
            'seconds': seconds
        };
    }

    function initializeClock(id, starttime) {
        var clock = document.getElementById(id);
        var minutesSpan = clock.querySelector('.minutes');
        var secondsSpan = clock.querySelector('.seconds');

        function updateClock() {
            var t = getTimeRemaining(starttime);
            minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
            secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

            if (t.total <= 0) {
                clearInterval(timeintervalTimer);
            }
        }

        updateClock();
        timeintervalTimer = setInterval(updateClock, 1000);
    }
}

function manageTime() {
    if (time_type == 'time_limited') {
        clearInterval(timeintervalCountdown);
        startCountdown();
    } else if (time_type == 'timeless') {
        clearInterval(timeintervalTimer);
        startTimer();
    }
}

// BULBS //

var bulbsOnCnt = 0;
var curConfsIndex = 0;
var confsNumber = 1023;
var confs = new Array(confsNumber);
var feedback_type = 'feedback';

function checkKey() {
    document.onkeydown = function (e) {
        if (e.keyCode >= 48 && e.keyCode <= 57) {
            var bulbId = 'bulb' + (e.keyCode - 48).toString();
            var bulb = document.getElementById(bulbId);
            if (bulb.src.split("/").slice(-1) == "bulb-on.png") {
                bulb.src = "/static/exp/bulb-off.png";
                --bulbsOnCnt;
                if (bulbsOnCnt == 0) {
                    manageTime();
                    manageConfigurations();
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
    updateProgressBar();
    displayConfiguration(confs[curConfsIndex]);
    ++curConfsIndex;
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

