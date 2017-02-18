/**
 * Created by mateuszkiebala on 14.02.2017.
 */
var clicks = [];
var timer = null;
var pause = null;
var sessionType = "";
var validClick = true;
var selectionMode = 'III.TB';

window.oncontextmenu = function() {
    return false;
};

function isRightClick(e) {
    var isRightMB;
    e = e || window.event;

    if ("which" in e)  // Gecko (Firefox), WebKit (Safari/Chrome) & Opera
        isRightMB = e.which == 3;
    else if ("button" in e)  // IE, Opera
        isRightMB = e.button == 2;
    return isRightMB;
}

function isLeftClick(e) {
    var isLeftMB;
    e = e || window.event;

    if ("which" in e)  // Gecko (Firefox), WebKit (Safari/Chrome) & Opera
        isLeftMB = e.which == 1;
    else if ("button" in e)  // IE, Opera
        isLeftMB = e.button == 0;
    return isLeftMB;
}

$(document).mousedown (function (e) {
    // validClick is set to false in selection.js, button click is always earlier noticed then document
    if (isRightClick(e) && validClick) {
        clicks.push(new Date().getTime());
        if (selectionMode == 'III.TB') {
            checkRythm();
        }
    }
    validClick = true;
});

function startTimer(sessionTime) {
    initializeClock(setUpTimeForTimer(sessionTime));
    function initializeClock(starttime) {

        function updateClock() {
            var t = getTimeRemaining(starttime);
            console.log(t);
            if (sessionType != 'Survey Selection') {
                if (t <= 0) {
                    stopTimer();
                } else {
                    checkClick();
                }
            } else {
                checkClick();
            }
        }

        clicks.push(new Date().getTime());
        timer = setInterval(updateClock, 10);
    }
}

function setUpTimeForTimer(sessionTime) {
    return new Date(Date.parse(new Date()) + sessionTime);
}

function getTimeRemaining(time) {
    return time.getTime() - new Date().getTime();
}

function checkClick() {
    var len = clicks.length;
    var curTime = new Date().getTime();
    if (curTime - clicks[len - 1] > pause) {
        document.body.style.background = 'red';
    } else if (document.body.style.background != 'green') {
        document.body.style.background = 'white';
    }
}

function checkRythm() {
    if (clicks.length >= 4) {
        var c = clicks.slice(Math.max(clicks.length - 4, 0));
        var x = 1 / 3 * (c[3] - c[0]);
        var q = 0;
        for (var i = 0; i < 3; ++i) {
            q += (c[i + 1] - c[i] - x) * (c[i + 1] - c[i] - x);
        }

        if (q < 10000) {
            document.body.style.background = "green";
        } else {
            document.body.style.background = "white";
        }
    }
}

function stopTimer() {
    clearInterval(timer);
    if (sessionType == 'Survey GIL' || sessionType == 'Training GIL') {
        saveClicks('/survey_gil_save_clicks/');
    } else if (sessionType == 'Survey Selection') {
        saveClicks('/selection_gil_save_clicks/');
    } else if (sessionType == 'Training Selection') {
        nextStep();
    }
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function saveClicks(link) {
    var data = new Object();
    data['clicks'] = clicks;
    var csrftoken = Cookies.get('csrftoken');
    var xhr = new XMLHttpRequest();
    xhr.open('POST', link, true);
    xhr.setRequestHeader("Content-type", "application/json; charset=utf-8");
    if (!csrfSafeMethod('POST') && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status != 200) {
            alert("Error " + xhr.status + "\n" + xhr.responseText);
        }

        if (xhr.readyState == XMLHttpRequest.DONE) {
            nextStep();
        }
    };
    xhr.send(JSON.stringify(data));
}

function nextStep() {
    if (sessionType == 'Training GIL') {
        window.location.href = "/welcome_survey_gil/";
    } else if (sessionType == 'Survey GIL') {
        window.location.href = "/welcome_training_selection/";
    } else if (sessionType == 'Training Selection') {
        window.location.href = "/welcome_survey_selection/";
    }
}