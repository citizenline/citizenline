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

    // Set rating while binding
    var avgRating = getAvgRating(el);
    var maxRating = getMaxRating(el);
    var parent = utils.findParent(el, "star-ratings");
    var user_rating = parent.getAttribute("data-user-rating")
    var percentage = 100 / maxRating * avgRating + "%";
    if (user_rating > 0) {
        percentage = 100 / maxRating * user_rating + "%";
    }
    parent.querySelector(".star-ratings-rating-foreground").style.width = percentage;

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
        return parent.getAttribute('data-avg-rating').replace(',', '.');
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
    parent.setAttribute("data-user-rating", rating.user_rating);

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

    // parent.querySelector(".star-ratings-rating-foreground").style.width = rating.percentage + '%';
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
        init_extra();
    }
});


module.exports = {
    bindRating: bindRatings
};


function init_extra() {
  var radios = document.querySelectorAll('.star-ratings-rating-stars-container input[type=radio]');

  var rest_rate = function(form) {
    // An AJAX request could send the data to the server
    stars = form.querySelector(':checked ~ label span').textContent
    radio = form.querySelector('.star-ratings-rating-stars-container :checked')
    rate(form.action, radio.value, radio);

    //output = form.querySelector('.star-ratings output');
    //output.textContent = stars;
  };

  // Iterate through all radio buttons and add a click
  // event listener to the labels
  Array.prototype.forEach.call(radios, function(el, i){
    el.onchange = function () {
      radio = this;
      rest_rate(radio.form);
    }
  });

  // If the form gets submitted, do a rest rate
  document.querySelector('.star-ratings').addEventListener('submit', function(event){
    event.preventDefault();
    event.stopImmediatePropagation();
    rest_rate(event.target);
  });
}
