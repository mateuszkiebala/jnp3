/**
 * Created by mateuszkiebala on 15.02.2017.
 */

var cardClicked = [false, false, false, false];
var cardLastSelection = [0, 0, 0, 0];
var tasksCount = 0;
var cardsOrder = [];
var taskNumber = 0;
var sessionStartTime = 0;
var card0Clicks = [];
var card1Clicks = [];
var card2Clicks = [];
var card3Clicks = [];

function setClick(id) {
    var card = "card" + (id + 1).toString();
    if (cardClicked[id]) {
        document.getElementById(card).style.background = 'lightgray';
        cardClicked[id] = false;
    } else {
        document.getElementById(card).style.background = 'lightblue';
        cardClicked[id] = true;
    }
}

function setClickSettings() {
    $('#card1').mousedown (function(e) {
        validClick = false;
        if (isLeftClick(e)) {
            setClick(0);
            if (cardClicked[0]) {
                cardLastSelection[0] = new Date().getTime();
            }
            card0Clicks.push(new Date().getTime());
        }
    });

    $('#card2').mousedown (function(e) {
        validClick = false;
        if (isLeftClick(e)) {
            setClick(1);
            if (cardClicked[1]) {
                cardLastSelection[1] = new Date().getTime();
            }
            card1Clicks.push(new Date().getTime());
        }
    });

    $('#card3').mousedown (function(e) {
        validClick = false;
        if (isLeftClick(e)) {
            setClick(2);
            if (cardClicked[2]) {
                cardLastSelection[2] = new Date().getTime();
            }
            card2Clicks.push(new Date().getTime());
        }
    });

    $('#card4').mousedown (function(e) {
        validClick = false;
        if (isLeftClick(e)) {
            setClick(3);
            if (cardClicked[3]) {
                cardLastSelection[3] = new Date().getTime();
            }
            card3Clicks.push(new Date().getTime());
        }
    });
}

function prepareSelectionResults() {
    var data = new Object();
    data['task_id'] = taskNumber;
    data['session_start_time'] = sessionStartTime;
    data['session_end_time'] = new Date().getTime();
    data['card_0_clicks'] = [sessionStartTime].concat(card0Clicks);
    data['card_1_clicks'] = [sessionStartTime].concat(card1Clicks);
    data['card_2_clicks'] = [sessionStartTime].concat(card2Clicks);
    data['card_3_clicks'] = [sessionStartTime].concat(card3Clicks);
    data['card_0_final'] = cardClicked[0] ? cardLastSelection[0] - sessionStartTime : 0;
    data['card_1_final'] = cardClicked[1] ? cardLastSelection[1] - sessionStartTime : 0;
    data['card_2_final'] = cardClicked[2] ? cardLastSelection[2] - sessionStartTime : 0;
    data['card_3_final'] = cardClicked[3] ? cardLastSelection[3] - sessionStartTime : 0;
    data['cards_order'] = cardsOrder;

    var c = [];
    for (var i = 0; i < 4; ++i) {
        if (cardClicked[i]) {
            c.push([cardLastSelection[i], i]);
        }
    }
    c = c.sort();
    data['chosen_cards'] = [];
    for (var i = 0; i < c.length; ++i) {
       data['chosen_cards'].push(c[i][1]);
    }
    return JSON.stringify(data);
}

function saveSelectionResults(data) {
    saveChanges(data, '/selection_save_task/');
}

function savePilotModeResults(data) {
    saveChanges(data, '/save_pilot_mode_task/');
}

function saveChanges(data, link) {
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
            if (taskNumber >= tasksCount) {
                window.location.href = "/end_screen/";
            } else {
                if (sessionType == 'Pilot Mode') {
                    window.location.href = "/welcome_pilot_mode/";
                } else {
                    window.location.href = "/welcome_survey_selection/";
                }
            }
        }
    };
    xhr.send(data);
}
