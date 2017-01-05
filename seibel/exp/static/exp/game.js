// TIMER //
var timeType = 'Time_limited';
var timeintervalTimer = null;
var timeGap = 0;
var startTime = 0;
var endTime = 0;

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
    startTime = time;
    if (timeType == 'Time_limited' || countdownFlag == true) {
        time = new Date(Date.parse(new Date()) + timeGap);
    }
    return time;
}

function getTimeRemaining(time, countdownFlag) {
    var t = 0;
    if (timeType == 'Time_limited' || countdownFlag == true) {
        t = time.getTime() - new Date().getTime();
    } else if (timeType == 'Timeless') {
        t = new Date().getTime() - time.getTime();
    }
    return convertTime(t);
}

function convertTime(t) {
    var miliseconds = Math.floor((t / 10));
    var seconds = Math.floor((t / 1000) % 60);
    return {
        'total': t,
        'seconds': seconds,
        'miliseconds': miliseconds
    };
}

function timeToString(time) {
    return time['seconds'] + "s " + time['miliseconds'] + "ms";
}

function stopTimer(countdownFlag) {
    if (!confsDone[confs[curConfsIndex]]) {
        confsDone[confs[curConfsIndex]] = true;
        endTime = endTime == 0 ? startTime : endTime;
        sendConfigurationResult(prepareDataToSend());
    }

    clearInterval(timeintervalTimer);
    if (timeType == 'Time_limited' || countdownFlag == true) {
        manageConfigurations();
        startTimer(false);
    }
}

// BULBS //

var bulbsOnCnt = 0;
var curConfsIndex = 0;
var confsNumber = 1023;
var confs = new Array(confsNumber);
var feedbackType = 'Feedback';
var configurationSucceeded = false;
var errorsCnt = 0;
var buttonClickTime = new Array(10);
var confsDone = {};
var confsDoneInPrevSession = [];

function checkKey() {
    document.onkeydown = function (e) {
        if (e.keyCode >= 48 && e.keyCode <= 57) {
            var keyId = e.keyCode - 48;
            var bulbId = 'bulb' + keyId.toString();
            var bulb = document.getElementById(bulbId);

            endTime = new Date();
            if (typeof buttonClickTime[keyId] === 'undefined') {
                buttonClickTime[keyId] = timeToString(convertTime(endTime.getTime() - startTime.getTime()));
            }

            if (bulb.src.split("/").slice(-1) == "bulb-on.png") {
                if (timeType == 'Timeless') {
                    bulb.src = "/static/exp/bulb-off.png";
                }
                --bulbsOnCnt;
                if (bulbsOnCnt == 0) {
                    configurationSucceeded = true;
                    if (curConfsIndex < confsNumber) {
                        if (timeType == 'Timeless') {
                            stopTimer(false);
                            startTimer(true);
                        }
                    } else {
                        showEndingModal();
                    }
                }
            } else if (bulb.src.split("/").slice(-1) == "bulb-off.png") {
                if (feedbackType == 'Feedback') {
                    document.getElementById('wa_beep').play();
                }
                ++errorsCnt;
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
    var len = confsDoneInPrevSession.length;
    for (var i = 0; i < len; ++i) {
        confsDone[confsDoneInPrevSession[i]] = true;
    }

    var index = 0;
    var temp = new Array(confsNumber - len);
    for (var i = 0; i < confsNumber; ++i) {
        if (!confsDone[i + 1]) {
            confsDone[i + 1] = false;
            temp[index] = i + 1;
            ++index;
        }
    }
    shuffle(temp);
    confs = confsDoneInPrevSession.concat(temp);
    curConfsIndex = len;
}

function manageConfigurations() {
    if (curConfsIndex < confsNumber) {
        updateProgressBar();
        clearBulbs();
        displayConfiguration(confs[curConfsIndex]);
        ++curConfsIndex;
    } else {
        showEndingModal();
    }
}

function displayConfiguration(conf) {
    for (var i = 0; i < 10; ++i) {
        var bulbId = 'bulb' + ((i + 1) % 10).toString();
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


// GAME //
var gameType = '';
var sessionNumber = 0;
var sessionLimit = 0;

function start() {
    var interval = setInterval(function() {
        createConfigurations();
        checkKey();
        manageConfigurations();
        startTimer(false);
        clearInterval(interval);
    }, 5000);
}

function prepareDataToSend() {
    var data = new Object();
    data['feedback_type'] = feedbackType;
    data['timer_type'] = timeType;
    data['session_number'] = sessionNumber;
    data['configuration'] = confs[curConfsIndex - 1];
    data['start_time'] = startTime;
    data['end_time'] = endTime;
    data['total_time'] = timeToString(convertTime(endTime.getTime() - startTime.getTime()));
    data['errors_count'] = errorsCnt;
    data['is_correct'] = configurationSucceeded ? 'Yes' : 'No';
    prepareBulbsResult(data);
    prepareButtonsResult(data);
    return JSON.stringify(data);
}

function prepareBulbsResult(data) {
    var conf = parseInt(data['configuration']);
    for (var i = 0; i < 10; ++i) {
        data["bulb_" + (i + 1).toString()] = ((conf & (1 << i)) != 0) ? 'On' : 'Off';
    }
}

function prepareButtonsResult(data) {
    for (var i = 1; i < 10; ++i) {
        if (typeof buttonClickTime[i] === 'undefined') {
            data['fin_' + i.toString()] = "-";
        } else {
            data['fin_' + i.toString()] = buttonClickTime[i];
        }
    }
    data['fin_10'] = (typeof buttonClickTime[0] === 'undefined') ? "-" : buttonClickTime[0];
}

function prepareSessionData() {
     var data = new Object();
     data['feedback_type'] = feedbackType;
     data['timer_type'] = timeType;
     data['session_number'] = sessionNumber;
     return JSON.stringify(data);
}

function clearConfigurationResults() {
    startTime = 0;
    endTime = 0;
    errorsCnt = 0;
    configurationSucceeded = false;
    for (var i = 0; i < 10; ++i) {
        buttonClickTime[i] = undefined;
    }
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendConfigurationResult(data) {
    var csrftoken = Cookies.get('csrftoken');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/exp/play/update_results/', true);
    xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
    xhr.setRequestHeader("Content-length", data.length);
    xhr.setRequestHeader("Connection", "close");
    if (!csrfSafeMethod('POST') && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status != 200) {
            alert("Error " + xhr.status + "\n" + xhr.responseText);
        }
    };
    xhr.send(data);
    clearConfigurationResults();
}

function sendSessionUpdate(data) {
    var csrftoken = Cookies.get('csrftoken');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/exp/play/update_session/', true);
    xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
    xhr.setRequestHeader("Content-length", data.length);
    xhr.setRequestHeader("Connection", "close");
    if (!csrfSafeMethod('POST') && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status != 200) {
            alert("Error " + xhr.status + "\n" + xhr.responseText);
        }
    };
    xhr.send(data);
}

// MODAL //
function showInstructionsModal() {
    var modalHeader = document.getElementById('modal-header-title');
    if (gameType == 'Normal') {
        modalHeader.innerHTML = 'Jesteś w sesji normalnej.';
    } else if (gameType == 'Training') {
        modalHeader.innerHTML = 'Jesteś w sesji treningowej.';
    }
    $('#myModal').modal('show');
}

function showContinuationModel() {
    var modalHeader = document.getElementById('modal-header-title');
    modalHeader.innerHTML = 'Musisz dokończyć poprzednią sesję eksperymentalną.';
    $('#myModal').modal('show');
}

function showEndingModal() {
    var modalHeader = (sessionLimit <= sessionNumber) ?
                        document.getElementById('session_endmodal-header-title') :
                        document.getElementById('endmodal-header-title');

    if (gameType == 'Normal') {
        modalHeader.innerHTML = 'Zakończyłeś sesję eksperymentalną.';
    } else if (gameType == 'Training') {
        modalHeader.innerHTML = 'Zakończyłeś sesję treningową.';
    }

    if (sessionLimit <= sessionNumber) {
        $('#sessionEndModal').modal('show');
    } else {
        $('#myEndModal').modal('show');
    }
}

function modalCloseBtn() {
    start();
}

function endModalCloseBtn() {
    window.location.href = "/accounts/loggedin/";
}

// When the user clicks anywhere outside of the modal, close it.
window.onclick = function(event) {
    if (event.target == document.getElementById('myModal')) {
        modalCloseBtn();
    }
};

window.onclick = function(event) {
    if (event.target == document.getElementById('myEndModal')) {
        endModalCloseBtn();
    }
};

window.onclick = function(event) {
    if (event.target == document.getElementById('sessionEndModal')) {
        endModalCloseBtn();
    }
};
