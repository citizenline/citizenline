(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
module.exports = require('./src/ratings');

},{"./src/ratings":2}],2:[function(require,module,exports){
var rest = require('./rest.js');
var utils = require('./utils');


/*********************
 * Initialise ratings
 *********************/
function init () {
    var ratingActions = document.querySelectorAll(".star-ratings-rate-action"),
        i;

    // Add click events to stars
    for (i = 0; i < ratingActions.length; i += 1) {
        bindRatings(ratingActions[i]);
    }
}


/*********************
 * Bind ratings
 *********************/
function bindRatings(el) {
    el.addEventListener("click", ratingClick);

    el.onmouseenter = function () {
        var maxRating = getMaxRating(this);
        var score = this.getAttribute('data-score');
        var parent = utils.findParent(this, "star-ratings");
        parent.querySelector(".star-ratings-rating-foreground").style.width = 100 / maxRating * score + "%";
    };

    el.onmouseleave = function () {
        var avgRating = getAvgRating(this);
        var maxRating = getMaxRating(this);
        var score = this.getAttribute('data-score');
        var parent = utils.findParent(this, "star-ratings");
        var user_rating = parent.getAttribute("data-user-rating")
        var percentage = 100 / maxRating * avgRating + "%";
        if (user_rating > 0) {
            percentage = 100 / maxRating * user_rating + "%";
        }
        parent.querySelector(".star-ratings-rating-foreground").style.width = percentage;
    };

}


/*********************
 * Rating click event
 *********************/
function ratingClick(ev) {
    ev.stopPropagation();
    ev.preventDefault();
    var url = this.getAttribute('href');
    var score = this.getAttribute('data-score');
    rate(url, score, this);
}


/*********************
 * Rate instance
 *********************/
function rate(url, score, sender) {
    rest.post(url, {'score': score}, function (rating) {
        updateRating(rating, sender);
    }, function (errors) {
        showError(errors, sender);
    });
}


function getMaxRating(el) {
    var parent = utils.findParent(el, "star-ratings");
    if (parent) {
        return parseInt(parent.getAttribute('data-max-rating'));
    }

    return -1;
}


function getAvgRating(el) {
    var parent = utils.findParent(el, "star-ratings");
    if (parent) {
        return parent.getAttribute('data-avg-rating');
    }

    return -1;
}


/*********************
 * Update rating
 *********************/
function updateRating(rating, sender) {
    var parent = utils.findParent(sender, "star-ratings"),
        valueElem;

    if (parent === undefined || parent === null) {
        return;
    }

    parent.setAttribute("data-avg-rating", rating.average);

    var avgElem = parent.getElementsByClassName("star-ratings-rating-average")[0];
    if(avgElem) {
        valueElem = avgElem.getElementsByClassName('star-ratings-rating-value')[0];
        if (valueElem) {
            valueElem.innerHTML = rating.average.toFixed(2);
        }
    }

    var countElem = parent.getElementsByClassName("star-ratings-rating-count")[0];
    if(countElem) {
        valueElem = countElem.getElementsByClassName('star-ratings-rating-value')[0];
        if (valueElem) {
            valueElem.innerHTML = rating.count;
        }
    }

    var userElem = parent.getElementsByClassName("star-ratings-rating-user")[0];
    if(userElem) {
        valueElem = userElem.getElementsByClassName('star-ratings-rating-value')[0];
        if (valueElem) {
            valueElem.innerHTML = rating.user_rating;
        }
    }

    parent.querySelector(".star-ratings-rating-foreground").style.width = rating.percentage + '%';
}


function showError (errors, sender) {
    var parent = utils.findParent(sender, "star-ratings");
    if (parent === undefined || parent === null) {
        return;
    }
    parent.querySelector(".star-ratings-errors").innerHTML = errors.error;
    setTimeout(function () {
        parent.querySelector(".star-ratings-errors").innerHTML = "";
    }, 2500);
}

/*********************
 * Only initialise ratings
 * if there is something to rate
 *********************/
document.addEventListener('DOMContentLoaded', function(event) {
    if (document.querySelector('.star-ratings')) {
        init();
    }
});


module.exports = {
    bindRating: bindRatings
};

},{"./rest.js":3,"./utils":4}],3:[function(require,module,exports){
/*jslint browser:true */
"use strict";


var djangoRemarkRest = {
    getCookie: function (name) {
        // From https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/
        var cookieValue = null, cookies, i, cookie;
        if (document.cookie && document.cookie !== '') {
            cookies = document.cookie.split(';');
            for (i = 0; i < cookies.length; i += 1) {
                cookie = cookies[i].trim(); // Doesn't work in all browsers
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    makeRequest: function (url, method, success, fail) {
        var req = new XMLHttpRequest();
        if (req.overrideMimeType !== undefined) {
            req.overrideMimeType("application/json");
        }
        req.open(method, url, true);
        req.setRequestHeader('Content-Type', 'application/json');
        req.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        // When done processing data
        req.onreadystatechange = function () {
            if (req.readyState !== 4) {
                return;
            }

            if (req.status >= 200 && req.status <= 299) {
                if (success) {
                    if (req.responseText) {
                        success(JSON.parse(req.responseText));
                    } else { success(); }
                }
            } else {
                if (fail) {
                    fail(JSON.parse(req.responseText));
                }
            }
        };

        return req;
    },

    get: function (url, data, success, fail) {
        var req = this.makeRequest(url, 'GET', success, fail);
        req.send(JSON.stringify(data));
    },

    post: function (url, data, success, fail) {
        var req = this.makeRequest(url, 'POST', success, fail);
        req.setRequestHeader("X-CSRFToken", this.getCookie('csrftoken'));
        req.send(JSON.stringify(data));
    },

    put: function (url, data, success, fail) {
        var req = this.makeRequest(url, 'PUT', success, fail);
        req.setRequestHeader("X-CSRFToken", this.getCookie('csrftoken'));
        req.send(JSON.stringify(data));
    },

    patch: function (url, data, success, fail) {
        var req = this.makeRequest(url, 'PATCH', success, fail);
        req.setRequestHeader("X-CSRFToken", this.getCookie('csrftoken'));
        req.send(JSON.stringify(data));
    },

    "delete": function (url, data, success, fail) {
        var req = this.makeRequest(url, 'DELETE', success, fail);
        req.setRequestHeader("X-CSRFToken", this.getCookie('csrftoken'));
        req.send(JSON.stringify(data));
    }
};


module.exports = djangoRemarkRest;

},{}],4:[function(require,module,exports){
/**************************
 * Check if an element has a class
 **************************/
function hasClass (el, name) {
    return (' ' + el.className + ' ').indexOf(' ' + name + ' ') > -1;
}


/**************************
 * Find parent element
 **************************/
function findParent(el, className) {
    var parentNode = el.parentNode;
    while (hasClass(parentNode, className) === false) {
        if (parentNode.parentNode === undefined) {
            return null;
        }
        parentNode = parentNode.parentNode;
    }
    return parentNode
}


module.exports = {
    hasClass: hasClass,
    findParent: findParent
};

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy93YXRjaGlmeS9ub2RlX21vZHVsZXMvYnJvd3Nlci1wYWNrL19wcmVsdWRlLmpzIiwic3Rhcl9yYXRpbmdzL3N0YXRpYy9zdGFyLXJhdGluZ3MvanMvaW5kZXguanMiLCJzdGFyX3JhdGluZ3Mvc3RhdGljL3N0YXItcmF0aW5ncy9qcy9zcmMvcmF0aW5ncy5qcyIsInN0YXJfcmF0aW5ncy9zdGF0aWMvc3Rhci1yYXRpbmdzL2pzL3NyYy9yZXN0LmpzIiwic3Rhcl9yYXRpbmdzL3N0YXRpYy9zdGFyLXJhdGluZ3MvanMvc3JjL3V0aWxzLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0FDQUE7QUFDQTs7QUNEQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQzdKQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ3JGQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIGUodCxuLHIpe2Z1bmN0aW9uIHMobyx1KXtpZighbltvXSl7aWYoIXRbb10pe3ZhciBhPXR5cGVvZiByZXF1aXJlPT1cImZ1bmN0aW9uXCImJnJlcXVpcmU7aWYoIXUmJmEpcmV0dXJuIGEobywhMCk7aWYoaSlyZXR1cm4gaShvLCEwKTt2YXIgZj1uZXcgRXJyb3IoXCJDYW5ub3QgZmluZCBtb2R1bGUgJ1wiK28rXCInXCIpO3Rocm93IGYuY29kZT1cIk1PRFVMRV9OT1RfRk9VTkRcIixmfXZhciBsPW5bb109e2V4cG9ydHM6e319O3Rbb11bMF0uY2FsbChsLmV4cG9ydHMsZnVuY3Rpb24oZSl7dmFyIG49dFtvXVsxXVtlXTtyZXR1cm4gcyhuP246ZSl9LGwsbC5leHBvcnRzLGUsdCxuLHIpfXJldHVybiBuW29dLmV4cG9ydHN9dmFyIGk9dHlwZW9mIHJlcXVpcmU9PVwiZnVuY3Rpb25cIiYmcmVxdWlyZTtmb3IodmFyIG89MDtvPHIubGVuZ3RoO28rKylzKHJbb10pO3JldHVybiBzfSkiLCJtb2R1bGUuZXhwb3J0cyA9IHJlcXVpcmUoJy4vc3JjL3JhdGluZ3MnKTtcbiIsInZhciByZXN0ID0gcmVxdWlyZSgnLi9yZXN0LmpzJyk7XG52YXIgdXRpbHMgPSByZXF1aXJlKCcuL3V0aWxzJyk7XG5cblxuLyoqKioqKioqKioqKioqKioqKioqKlxuICogSW5pdGlhbGlzZSByYXRpbmdzXG4gKioqKioqKioqKioqKioqKioqKioqL1xuZnVuY3Rpb24gaW5pdCAoKSB7XG4gICAgdmFyIHJhdGluZ0FjdGlvbnMgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKFwiLnN0YXItcmF0aW5ncy1yYXRlLWFjdGlvblwiKSxcbiAgICAgICAgaTtcblxuICAgIC8vIEFkZCBjbGljayBldmVudHMgdG8gc3RhcnNcbiAgICBmb3IgKGkgPSAwOyBpIDwgcmF0aW5nQWN0aW9ucy5sZW5ndGg7IGkgKz0gMSkge1xuICAgICAgICBiaW5kUmF0aW5ncyhyYXRpbmdBY3Rpb25zW2ldKTtcbiAgICB9XG59XG5cblxuLyoqKioqKioqKioqKioqKioqKioqKlxuICogQmluZCByYXRpbmdzXG4gKioqKioqKioqKioqKioqKioqKioqL1xuZnVuY3Rpb24gYmluZFJhdGluZ3MoZWwpIHtcbiAgICBlbC5hZGRFdmVudExpc3RlbmVyKFwiY2xpY2tcIiwgcmF0aW5nQ2xpY2spO1xuXG4gICAgZWwub25tb3VzZWVudGVyID0gZnVuY3Rpb24gKCkge1xuICAgICAgICB2YXIgbWF4UmF0aW5nID0gZ2V0TWF4UmF0aW5nKHRoaXMpO1xuICAgICAgICB2YXIgc2NvcmUgPSB0aGlzLmdldEF0dHJpYnV0ZSgnZGF0YS1zY29yZScpO1xuICAgICAgICB2YXIgcGFyZW50ID0gdXRpbHMuZmluZFBhcmVudCh0aGlzLCBcInN0YXItcmF0aW5nc1wiKTtcbiAgICAgICAgcGFyZW50LnF1ZXJ5U2VsZWN0b3IoXCIuc3Rhci1yYXRpbmdzLXJhdGluZy1mb3JlZ3JvdW5kXCIpLnN0eWxlLndpZHRoID0gMTAwIC8gbWF4UmF0aW5nICogc2NvcmUgKyBcIiVcIjtcbiAgICB9O1xuXG4gICAgZWwub25tb3VzZWxlYXZlID0gZnVuY3Rpb24gKCkge1xuICAgICAgICB2YXIgYXZnUmF0aW5nID0gZ2V0QXZnUmF0aW5nKHRoaXMpO1xuICAgICAgICB2YXIgbWF4UmF0aW5nID0gZ2V0TWF4UmF0aW5nKHRoaXMpO1xuICAgICAgICB2YXIgc2NvcmUgPSB0aGlzLmdldEF0dHJpYnV0ZSgnZGF0YS1zY29yZScpO1xuICAgICAgICB2YXIgcGFyZW50ID0gdXRpbHMuZmluZFBhcmVudCh0aGlzLCBcInN0YXItcmF0aW5nc1wiKTtcbiAgICAgICAgdmFyIHVzZXJfcmF0aW5nID0gcGFyZW50LmdldEF0dHJpYnV0ZShcImRhdGEtdXNlci1yYXRpbmdcIilcbiAgICAgICAgdmFyIHBlcmNlbnRhZ2UgPSAxMDAgLyBtYXhSYXRpbmcgKiBhdmdSYXRpbmcgKyBcIiVcIjtcbiAgICAgICAgaWYgKHVzZXJfcmF0aW5nID4gMCkge1xuICAgICAgICAgICAgcGVyY2VudGFnZSA9IDEwMCAvIG1heFJhdGluZyAqIHVzZXJfcmF0aW5nICsgXCIlXCI7XG4gICAgICAgIH1cbiAgICAgICAgcGFyZW50LnF1ZXJ5U2VsZWN0b3IoXCIuc3Rhci1yYXRpbmdzLXJhdGluZy1mb3JlZ3JvdW5kXCIpLnN0eWxlLndpZHRoID0gcGVyY2VudGFnZTtcbiAgICB9O1xuXG59XG5cblxuLyoqKioqKioqKioqKioqKioqKioqKlxuICogUmF0aW5nIGNsaWNrIGV2ZW50XG4gKioqKioqKioqKioqKioqKioqKioqL1xuZnVuY3Rpb24gcmF0aW5nQ2xpY2soZXYpIHtcbiAgICBldi5zdG9wUHJvcGFnYXRpb24oKTtcbiAgICBldi5wcmV2ZW50RGVmYXVsdCgpO1xuICAgIHZhciB1cmwgPSB0aGlzLmdldEF0dHJpYnV0ZSgnaHJlZicpO1xuICAgIHZhciBzY29yZSA9IHRoaXMuZ2V0QXR0cmlidXRlKCdkYXRhLXNjb3JlJyk7XG4gICAgcmF0ZSh1cmwsIHNjb3JlLCB0aGlzKTtcbn1cblxuXG4vKioqKioqKioqKioqKioqKioqKioqXG4gKiBSYXRlIGluc3RhbmNlXG4gKioqKioqKioqKioqKioqKioqKioqL1xuZnVuY3Rpb24gcmF0ZSh1cmwsIHNjb3JlLCBzZW5kZXIpIHtcbiAgICByZXN0LnBvc3QodXJsLCB7J3Njb3JlJzogc2NvcmV9LCBmdW5jdGlvbiAocmF0aW5nKSB7XG4gICAgICAgIHVwZGF0ZVJhdGluZyhyYXRpbmcsIHNlbmRlcik7XG4gICAgfSwgZnVuY3Rpb24gKGVycm9ycykge1xuICAgICAgICBzaG93RXJyb3IoZXJyb3JzLCBzZW5kZXIpO1xuICAgIH0pO1xufVxuXG5cbmZ1bmN0aW9uIGdldE1heFJhdGluZyhlbCkge1xuICAgIHZhciBwYXJlbnQgPSB1dGlscy5maW5kUGFyZW50KGVsLCBcInN0YXItcmF0aW5nc1wiKTtcbiAgICBpZiAocGFyZW50KSB7XG4gICAgICAgIHJldHVybiBwYXJzZUludChwYXJlbnQuZ2V0QXR0cmlidXRlKCdkYXRhLW1heC1yYXRpbmcnKSk7XG4gICAgfVxuXG4gICAgcmV0dXJuIC0xO1xufVxuXG5cbmZ1bmN0aW9uIGdldEF2Z1JhdGluZyhlbCkge1xuICAgIHZhciBwYXJlbnQgPSB1dGlscy5maW5kUGFyZW50KGVsLCBcInN0YXItcmF0aW5nc1wiKTtcbiAgICBpZiAocGFyZW50KSB7XG4gICAgICAgIHJldHVybiBwYXJlbnQuZ2V0QXR0cmlidXRlKCdkYXRhLWF2Zy1yYXRpbmcnKTtcbiAgICB9XG5cbiAgICByZXR1cm4gLTE7XG59XG5cblxuLyoqKioqKioqKioqKioqKioqKioqKlxuICogVXBkYXRlIHJhdGluZ1xuICoqKioqKioqKioqKioqKioqKioqKi9cbmZ1bmN0aW9uIHVwZGF0ZVJhdGluZyhyYXRpbmcsIHNlbmRlcikge1xuICAgIHZhciBwYXJlbnQgPSB1dGlscy5maW5kUGFyZW50KHNlbmRlciwgXCJzdGFyLXJhdGluZ3NcIiksXG4gICAgICAgIHZhbHVlRWxlbTtcblxuICAgIGlmIChwYXJlbnQgPT09IHVuZGVmaW5lZCB8fCBwYXJlbnQgPT09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHBhcmVudC5zZXRBdHRyaWJ1dGUoXCJkYXRhLWF2Zy1yYXRpbmdcIiwgcmF0aW5nLmF2ZXJhZ2UpO1xuXG4gICAgdmFyIGF2Z0VsZW0gPSBwYXJlbnQuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcInN0YXItcmF0aW5ncy1yYXRpbmctYXZlcmFnZVwiKVswXTtcbiAgICBpZihhdmdFbGVtKSB7XG4gICAgICAgIHZhbHVlRWxlbSA9IGF2Z0VsZW0uZ2V0RWxlbWVudHNCeUNsYXNzTmFtZSgnc3Rhci1yYXRpbmdzLXJhdGluZy12YWx1ZScpWzBdO1xuICAgICAgICBpZiAodmFsdWVFbGVtKSB7XG4gICAgICAgICAgICB2YWx1ZUVsZW0uaW5uZXJIVE1MID0gcmF0aW5nLmF2ZXJhZ2UudG9GaXhlZCgyKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHZhciBjb3VudEVsZW0gPSBwYXJlbnQuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcInN0YXItcmF0aW5ncy1yYXRpbmctY291bnRcIilbMF07XG4gICAgaWYoY291bnRFbGVtKSB7XG4gICAgICAgIHZhbHVlRWxlbSA9IGNvdW50RWxlbS5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKCdzdGFyLXJhdGluZ3MtcmF0aW5nLXZhbHVlJylbMF07XG4gICAgICAgIGlmICh2YWx1ZUVsZW0pIHtcbiAgICAgICAgICAgIHZhbHVlRWxlbS5pbm5lckhUTUwgPSByYXRpbmcuY291bnQ7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICB2YXIgdXNlckVsZW0gPSBwYXJlbnQuZ2V0RWxlbWVudHNCeUNsYXNzTmFtZShcInN0YXItcmF0aW5ncy1yYXRpbmctdXNlclwiKVswXTtcbiAgICBpZih1c2VyRWxlbSkge1xuICAgICAgICB2YWx1ZUVsZW0gPSB1c2VyRWxlbS5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKCdzdGFyLXJhdGluZ3MtcmF0aW5nLXZhbHVlJylbMF07XG4gICAgICAgIGlmICh2YWx1ZUVsZW0pIHtcbiAgICAgICAgICAgIHZhbHVlRWxlbS5pbm5lckhUTUwgPSByYXRpbmcudXNlcl9yYXRpbmc7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBwYXJlbnQucXVlcnlTZWxlY3RvcihcIi5zdGFyLXJhdGluZ3MtcmF0aW5nLWZvcmVncm91bmRcIikuc3R5bGUud2lkdGggPSByYXRpbmcucGVyY2VudGFnZSArICclJztcbn1cblxuXG5mdW5jdGlvbiBzaG93RXJyb3IgKGVycm9ycywgc2VuZGVyKSB7XG4gICAgdmFyIHBhcmVudCA9IHV0aWxzLmZpbmRQYXJlbnQoc2VuZGVyLCBcInN0YXItcmF0aW5nc1wiKTtcbiAgICBpZiAocGFyZW50ID09PSB1bmRlZmluZWQgfHwgcGFyZW50ID09PSBudWxsKSB7XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gICAgcGFyZW50LnF1ZXJ5U2VsZWN0b3IoXCIuc3Rhci1yYXRpbmdzLWVycm9yc1wiKS5pbm5lckhUTUwgPSBlcnJvcnMuZXJyb3I7XG4gICAgc2V0VGltZW91dChmdW5jdGlvbiAoKSB7XG4gICAgICAgIHBhcmVudC5xdWVyeVNlbGVjdG9yKFwiLnN0YXItcmF0aW5ncy1lcnJvcnNcIikuaW5uZXJIVE1MID0gXCJcIjtcbiAgICB9LCAyNTAwKTtcbn1cblxuLyoqKioqKioqKioqKioqKioqKioqKlxuICogT25seSBpbml0aWFsaXNlIHJhdGluZ3NcbiAqIGlmIHRoZXJlIGlzIHNvbWV0aGluZyB0byByYXRlXG4gKioqKioqKioqKioqKioqKioqKioqL1xuZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignRE9NQ29udGVudExvYWRlZCcsIGZ1bmN0aW9uKGV2ZW50KSB7XG4gICAgaWYgKGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoJy5zdGFyLXJhdGluZ3MnKSkge1xuICAgICAgICBpbml0KCk7XG4gICAgfVxufSk7XG5cblxubW9kdWxlLmV4cG9ydHMgPSB7XG4gICAgYmluZFJhdGluZzogYmluZFJhdGluZ3Ncbn07XG4iLCIvKmpzbGludCBicm93c2VyOnRydWUgKi9cblwidXNlIHN0cmljdFwiO1xuXG5cbnZhciBkamFuZ29SZW1hcmtSZXN0ID0ge1xuICAgIGdldENvb2tpZTogZnVuY3Rpb24gKG5hbWUpIHtcbiAgICAgICAgLy8gRnJvbSBodHRwczovL2RvY3MuZGphbmdvcHJvamVjdC5jb20vZW4vMS43L3JlZi9jb250cmliL2NzcmYvXG4gICAgICAgIHZhciBjb29raWVWYWx1ZSA9IG51bGwsIGNvb2tpZXMsIGksIGNvb2tpZTtcbiAgICAgICAgaWYgKGRvY3VtZW50LmNvb2tpZSAmJiBkb2N1bWVudC5jb29raWUgIT09ICcnKSB7XG4gICAgICAgICAgICBjb29raWVzID0gZG9jdW1lbnQuY29va2llLnNwbGl0KCc7Jyk7XG4gICAgICAgICAgICBmb3IgKGkgPSAwOyBpIDwgY29va2llcy5sZW5ndGg7IGkgKz0gMSkge1xuICAgICAgICAgICAgICAgIGNvb2tpZSA9IGNvb2tpZXNbaV0udHJpbSgpOyAvLyBEb2Vzbid0IHdvcmsgaW4gYWxsIGJyb3dzZXJzXG4gICAgICAgICAgICAgICAgLy8gRG9lcyB0aGlzIGNvb2tpZSBzdHJpbmcgYmVnaW4gd2l0aCB0aGUgbmFtZSB3ZSB3YW50P1xuICAgICAgICAgICAgICAgIGlmIChjb29raWUuc3Vic3RyaW5nKDAsIG5hbWUubGVuZ3RoICsgMSkgPT09IChuYW1lICsgJz0nKSkge1xuICAgICAgICAgICAgICAgICAgICBjb29raWVWYWx1ZSA9IGRlY29kZVVSSUNvbXBvbmVudChjb29raWUuc3Vic3RyaW5nKG5hbWUubGVuZ3RoICsgMSkpO1xuICAgICAgICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGNvb2tpZVZhbHVlO1xuICAgIH0sXG5cbiAgICBtYWtlUmVxdWVzdDogZnVuY3Rpb24gKHVybCwgbWV0aG9kLCBzdWNjZXNzLCBmYWlsKSB7XG4gICAgICAgIHZhciByZXEgPSBuZXcgWE1MSHR0cFJlcXVlc3QoKTtcbiAgICAgICAgaWYgKHJlcS5vdmVycmlkZU1pbWVUeXBlICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICAgIHJlcS5vdmVycmlkZU1pbWVUeXBlKFwiYXBwbGljYXRpb24vanNvblwiKTtcbiAgICAgICAgfVxuICAgICAgICByZXEub3BlbihtZXRob2QsIHVybCwgdHJ1ZSk7XG4gICAgICAgIHJlcS5zZXRSZXF1ZXN0SGVhZGVyKCdDb250ZW50LVR5cGUnLCAnYXBwbGljYXRpb24vanNvbicpO1xuICAgICAgICByZXEuc2V0UmVxdWVzdEhlYWRlcignWC1SZXF1ZXN0ZWQtV2l0aCcsICdYTUxIdHRwUmVxdWVzdCcpO1xuXG4gICAgICAgIC8vIFdoZW4gZG9uZSBwcm9jZXNzaW5nIGRhdGFcbiAgICAgICAgcmVxLm9ucmVhZHlzdGF0ZWNoYW5nZSA9IGZ1bmN0aW9uICgpIHtcbiAgICAgICAgICAgIGlmIChyZXEucmVhZHlTdGF0ZSAhPT0gNCkge1xuICAgICAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgaWYgKHJlcS5zdGF0dXMgPj0gMjAwICYmIHJlcS5zdGF0dXMgPD0gMjk5KSB7XG4gICAgICAgICAgICAgICAgaWYgKHN1Y2Nlc3MpIHtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHJlcS5yZXNwb25zZVRleHQpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHN1Y2Nlc3MoSlNPTi5wYXJzZShyZXEucmVzcG9uc2VUZXh0KSk7XG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7IHN1Y2Nlc3MoKTsgfVxuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgaWYgKGZhaWwpIHtcbiAgICAgICAgICAgICAgICAgICAgZmFpbChKU09OLnBhcnNlKHJlcS5yZXNwb25zZVRleHQpKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgIH07XG5cbiAgICAgICAgcmV0dXJuIHJlcTtcbiAgICB9LFxuXG4gICAgZ2V0OiBmdW5jdGlvbiAodXJsLCBkYXRhLCBzdWNjZXNzLCBmYWlsKSB7XG4gICAgICAgIHZhciByZXEgPSB0aGlzLm1ha2VSZXF1ZXN0KHVybCwgJ0dFVCcsIHN1Y2Nlc3MsIGZhaWwpO1xuICAgICAgICByZXEuc2VuZChKU09OLnN0cmluZ2lmeShkYXRhKSk7XG4gICAgfSxcblxuICAgIHBvc3Q6IGZ1bmN0aW9uICh1cmwsIGRhdGEsIHN1Y2Nlc3MsIGZhaWwpIHtcbiAgICAgICAgdmFyIHJlcSA9IHRoaXMubWFrZVJlcXVlc3QodXJsLCAnUE9TVCcsIHN1Y2Nlc3MsIGZhaWwpO1xuICAgICAgICByZXEuc2V0UmVxdWVzdEhlYWRlcihcIlgtQ1NSRlRva2VuXCIsIHRoaXMuZ2V0Q29va2llKCdjc3JmdG9rZW4nKSk7XG4gICAgICAgIHJlcS5zZW5kKEpTT04uc3RyaW5naWZ5KGRhdGEpKTtcbiAgICB9LFxuXG4gICAgcHV0OiBmdW5jdGlvbiAodXJsLCBkYXRhLCBzdWNjZXNzLCBmYWlsKSB7XG4gICAgICAgIHZhciByZXEgPSB0aGlzLm1ha2VSZXF1ZXN0KHVybCwgJ1BVVCcsIHN1Y2Nlc3MsIGZhaWwpO1xuICAgICAgICByZXEuc2V0UmVxdWVzdEhlYWRlcihcIlgtQ1NSRlRva2VuXCIsIHRoaXMuZ2V0Q29va2llKCdjc3JmdG9rZW4nKSk7XG4gICAgICAgIHJlcS5zZW5kKEpTT04uc3RyaW5naWZ5KGRhdGEpKTtcbiAgICB9LFxuXG4gICAgcGF0Y2g6IGZ1bmN0aW9uICh1cmwsIGRhdGEsIHN1Y2Nlc3MsIGZhaWwpIHtcbiAgICAgICAgdmFyIHJlcSA9IHRoaXMubWFrZVJlcXVlc3QodXJsLCAnUEFUQ0gnLCBzdWNjZXNzLCBmYWlsKTtcbiAgICAgICAgcmVxLnNldFJlcXVlc3RIZWFkZXIoXCJYLUNTUkZUb2tlblwiLCB0aGlzLmdldENvb2tpZSgnY3NyZnRva2VuJykpO1xuICAgICAgICByZXEuc2VuZChKU09OLnN0cmluZ2lmeShkYXRhKSk7XG4gICAgfSxcblxuICAgIFwiZGVsZXRlXCI6IGZ1bmN0aW9uICh1cmwsIGRhdGEsIHN1Y2Nlc3MsIGZhaWwpIHtcbiAgICAgICAgdmFyIHJlcSA9IHRoaXMubWFrZVJlcXVlc3QodXJsLCAnREVMRVRFJywgc3VjY2VzcywgZmFpbCk7XG4gICAgICAgIHJlcS5zZXRSZXF1ZXN0SGVhZGVyKFwiWC1DU1JGVG9rZW5cIiwgdGhpcy5nZXRDb29raWUoJ2NzcmZ0b2tlbicpKTtcbiAgICAgICAgcmVxLnNlbmQoSlNPTi5zdHJpbmdpZnkoZGF0YSkpO1xuICAgIH1cbn07XG5cblxubW9kdWxlLmV4cG9ydHMgPSBkamFuZ29SZW1hcmtSZXN0O1xuIiwiLyoqKioqKioqKioqKioqKioqKioqKioqKioqXG4gKiBDaGVjayBpZiBhbiBlbGVtZW50IGhhcyBhIGNsYXNzXG4gKioqKioqKioqKioqKioqKioqKioqKioqKiovXG5mdW5jdGlvbiBoYXNDbGFzcyAoZWwsIG5hbWUpIHtcbiAgICByZXR1cm4gKCcgJyArIGVsLmNsYXNzTmFtZSArICcgJykuaW5kZXhPZignICcgKyBuYW1lICsgJyAnKSA+IC0xO1xufVxuXG5cbi8qKioqKioqKioqKioqKioqKioqKioqKioqKlxuICogRmluZCBwYXJlbnQgZWxlbWVudFxuICoqKioqKioqKioqKioqKioqKioqKioqKioqL1xuZnVuY3Rpb24gZmluZFBhcmVudChlbCwgY2xhc3NOYW1lKSB7XG4gICAgdmFyIHBhcmVudE5vZGUgPSBlbC5wYXJlbnROb2RlO1xuICAgIHdoaWxlIChoYXNDbGFzcyhwYXJlbnROb2RlLCBjbGFzc05hbWUpID09PSBmYWxzZSkge1xuICAgICAgICBpZiAocGFyZW50Tm9kZS5wYXJlbnROb2RlID09PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICAgIHJldHVybiBudWxsO1xuICAgICAgICB9XG4gICAgICAgIHBhcmVudE5vZGUgPSBwYXJlbnROb2RlLnBhcmVudE5vZGU7XG4gICAgfVxuICAgIHJldHVybiBwYXJlbnROb2RlXG59XG5cblxubW9kdWxlLmV4cG9ydHMgPSB7XG4gICAgaGFzQ2xhc3M6IGhhc0NsYXNzLFxuICAgIGZpbmRQYXJlbnQ6IGZpbmRQYXJlbnRcbn07XG4iXX0=
