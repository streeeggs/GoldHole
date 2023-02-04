def cool_js():
    return """
console.log("=== starting custom js ===");

/////////////////////////////
// sync clock
var syncClock = false;
var syncClockStartTime = new Date("2022-12-02T23:37:40");
/////////////////////////////

//sync clock stuff
var syncClockStartTimeUTC = Date.UTC(
  syncClockStartTime.getUTCFullYear(),
  syncClockStartTime.getUTCMonth(),
  syncClockStartTime.getUTCDate(),
  syncClockStartTime.getUTCHours(),
  syncClockStartTime.getUTCMinutes(),
  syncClockStartTime.getUTCSeconds()
);

if (syncClock) {
  //create sync clock
  if (!syncClockElem) {
    var parent = $("#currenttitle").closest("div");
    var syncClockElem = document.createElement("span");
    syncClockElem.id = "syncClock";
    syncClockElem.textContent = " (00:00:00)";

    parent.append(syncClockElem);
  }

  //update sync clock
  if (!syncClockInterval) {
    var syncClockInterval = window.setInterval(() => {
      var current = new Date();
      //wierd how there is no chortcut for this. Whatever.
      var currentUTC = Date.UTC(
        current.getUTCFullYear(),
        current.getUTCMonth(),
        current.getUTCDate(),
        current.getUTCHours(),
        current.getUTCMinutes(),
        current.getUTCSeconds()
      );
      var diff = currentUTC - syncClockStartTimeUTC;
      var hh = Math.floor(diff / 3600000)
        .toString()
        .padStart(2, "0");
      var mm = Math.floor((diff % 3600000) / 60000)
        .toString()
        .padStart(2, "0");
      var ss = Math.floor((diff % 60000) / 1000)
        .toString()
        .padStart(2, "0");
      // console.log(diff + " - " + hh + ":" + mm + ":" + ss);
      syncClockElem.textContent = " (" + hh + ":" + mm + ":" + ss + ")";
    }, 5000);
  }
} else {
  //destroy sync clock
  if (syncClockElem) {
    $(syncClockElem).remove();
    syncClockElem = null;
  }
  if (syncClockInterval) {
    window.clearInterval(syncClockInterval);
    syncClockInterval = null;
  }
}

///////
// img scroll fix
addChatMessage = function (data) {
  if (IGNORED.indexOf(data.username) !== -1) {
    return;
  }
  if (data.meta.shadow && !USEROPTS.show_shadowchat) {
    return;
  }
  var msgBuf = $("#messagebuffer");
  var div = formatChatMessage(data, LASTCHAT);
  // Incoming: a bunch of crap for the feature where if you hover over
  // a message, it highlights messages from that user
  var safeUsername = data.username.replace(/[^\w-]/g, "\\$");
  div.addClass("chat-msg-" + safeUsername);
  div.appendTo(msgBuf);
  div.mouseover(function () {
    $(".chat-msg-" + safeUsername).addClass("nick-hover");
  });
  div.mouseleave(function () {
    $(".nick-hover").removeClass("nick-hover");
  });
  var oldHeight = msgBuf.prop("scrollHeight");
  var numRemoved = trimChatBuffer();
  if (SCROLLCHAT) {
    scrollChat();
  } else {
    var newMessageDiv = $("#newmessages-indicator");
    if (!newMessageDiv.length) {
      newMessageDiv = $("<div/>")
        .attr("id", "newmessages-indicator")
        .insertBefore($("#chatDragHandle"));
      var bgHack = $("<span/>")
        .attr("id", "newmessages-indicator-bghack")
        .appendTo(newMessageDiv);

      $("<span/>")
        .addClass("glyphicon glyphicon-chevron-down")
        .appendTo(bgHack);
      $("<span/>").text("New Messages Below").appendTo(bgHack);
      $("<span/>")
        .addClass("glyphicon glyphicon-chevron-down")
        .appendTo(bgHack);
      newMessageDiv.click(function () {
        SCROLLCHAT = true;
        scrollChat();
      });
    }

    if (numRemoved > 0) {
      IGNORE_SCROLL_EVENT = true;
      var diff = oldHeight - msgBuf.prop("scrollHeight");
      scrollAndIgnoreEvent(msgBuf.scrollTop() - diff);
    }
  }

  window.setTimeout(() => {
    if (SCROLLCHAT) {
      scrollChat();
    } else if ($(this).position().top < 0) {
      scrollAndIgnoreEvent(msgBuf.scrollTop() + $(this).height());
    }
  }, 100);

  var isHighlight = false;
  if (CLIENT.name && data.username != CLIENT.name) {
    if (data.msg.toLowerCase().indexOf(CLIENT.name.toLowerCase()) != -1) {
      div.addClass("nick-highlight");
      isHighlight = true;
    }
  }

  pingMessage(isHighlight);
};

// img scroll fix
///////

//laser controls
var laserClasses = ["red", "purple", "green", "blue"]; //these are the classes to put on each laser
var spotlightClasses = ["spotlight-left", "spotlight-right"]; //these are the classes to put on each spotlight

if (!oldAppend) {
  var oldAppend = $.fn.appendTo;

  $.fn.appendTo = function () {
    if (
      this.length > 0 &&
      this[0].className &&
      this[0].className.indexOf("chat-msg-") >= 0
    ) {
      var allSpans = this.find("span");
      if (allSpans.length > 0) {
        var chatSpan = allSpans[allSpans.length - 1];
        var nameSpan = this.find("span:not(.timestamp):nth-last-child(2)");
        var jqueryChatSpan = $(chatSpan);
        var chatText = jqueryChatSpan.text().toLowerCase();

        textLottery(chatText, jqueryChatSpan, this);

        allSpans.attr("data-text", chatText);
        // if(chatText.indexOf("coolhole") >= 0)
        // {
        var allText = "";
        for (var i = 0; i < allSpans.length - 1; i++) {
          allText += $(allSpans[i]).text();
        }
        allText += chatText;
        this.prop("title", allText);
        // }

        checkReturnFire(jqueryChatSpan, chatText, this);

        checkMention(chatText, this);

        // modSoy(jqueryChatSpan, jqueryChatSpan, this);

        if (nameSpan.length > 0) {
          changeChatName(nameSpan, this);
        }

        if (window.localStorage.gunshotEnabled === "true") {
          emoteSound(jqueryChatSpan, this[0].className);
        }
      }
    }
    return oldAppend.apply(this, arguments);
  };
}

function modSoy(jqueryChatSpan, chatText, chatDiv) {
  //first, display none all soooys
  jqueryChatSpan
    .find(
      "img[title='/soooy'], img[title='/gunPointLeft'], img[title='/gunPointRight']"
    )
    .css("display", "none");
  chatText.css("position", "relative");

  window.setTimeout(() => {
    //second, find all the soys again, and position them on the previous emote
    var chatTextRect = chatText[0].getBoundingClientRect();
    var emotesFound = jqueryChatSpan.find("img");
    var prevNonOverlayRect = null;
    var prevEmoteTitle = "";
    var emoteCombo = 0;
    for (var i = 0; i < emotesFound.length; i++) {
      var emoteTitle = emotesFound[i].getAttribute("title");

      if (
        emoteTitle === "/soooy" ||
        emoteTitle === "/gunPointLeft" ||
        emoteTitle === "/gunPointRight"
      ) {
        emotesFound[i].style.display = "";

        if (prevEmoteTitle === emoteTitle) {
          emoteCombo++;
        } else {
          emoteCombo = 0;
        }

        //if its the first emote, count it as the first non-overlayed emote instead
        if (i === 0) {
          prevNonOverlayRect = emotesFound[i].getBoundingClientRect();
          emoteCombo = 0;
        } else {
          // console.log("found soy " + i);
          emotesFound[i].classList.add("emote-overlay");
          var overlayEmoteRect = emotesFound[i].getBoundingClientRect();

          //adjust the overlay depending on the emote
          switch (emoteTitle) {
            case "/soooy":
              var leftPrevEmote = prevNonOverlayRect.left - chatTextRect.left;
              var topPrevEmote = prevNonOverlayRect.top - chatTextRect.top;
              emotesFound[i].style.left =
                leftPrevEmote -
                Math.round(
                  (overlayEmoteRect.width - prevNonOverlayRect.width) / 2
                ) +
                emoteCombo +
                "px";
              emotesFound[i].style.top =
                topPrevEmote -
                Math.round(
                  (overlayEmoteRect.height - prevNonOverlayRect.height) / 2
                ) +
                emoteCombo +
                "px";
              break;
            case "/gunPointLeft":
              var leftPrevEmote = prevNonOverlayRect.left - chatTextRect.left;
              emotesFound[i].style.left =
                leftPrevEmote -
                Math.round(overlayEmoteRect.width / 4) +
                emoteCombo +
                "px";
              emotesFound[i].style.bottom =
                -Math.round(overlayEmoteRect.height / 2) + emoteCombo + "px";
              break;
            case "/gunPointRight":
              var rightPrevEmote = prevNonOverlayRect.right - chatTextRect.left;
              emotesFound[i].style.left =
                rightPrevEmote -
                Math.round((overlayEmoteRect.width * 3) / 4) +
                emoteCombo +
                "px";
              emotesFound[i].style.bottom =
                -Math.round(overlayEmoteRect.height / 2) + emoteCombo + "px";
              break;
          }

          prevEmoteTitle = emoteTitle;
        }
      } else {
        prevNonOverlayRect = emotesFound[i].getBoundingClientRect();
        emoteCombo = 0;
      }
    }
  }, 200);
}

function changeChatName(nameSpan, chatDiv) {
  //if(chatDiv.hasClass("chat-msg-Miles_Gloriosus")) {
  //	chatDiv.removeClass("chat-msg-Miles_Gloriosus");
  //}
  // nameSpan.find("strong").text("He_says_she_says: ");
}

createLasers(laserClasses, spotlightClasses);

//create/destroy lasers
function createLasers(laserClasses, spotlightClasses) {
  var currLasers = $(".laser-beam");

  //delete the current lazers
  currLasers.remove();

  //then for each laser class, create a laser
  var body = $("body");
  for (var i = 0; i < laserClasses.length; i++) {
    var laserdiv = document.createElement("div");
    laserdiv.classList.add("laser-beam");
    laserdiv.classList.add(laserClasses[i]);
    body.append(laserdiv);
  }

  //also add spotlights
  var currSpotlights = $(".spot-light");
  currSpotlights.remove();
  for (var i = 0; i < spotlightClasses.length; i++) {
    var spotlightDiv = document.createElement("div");
    spotlightDiv.classList.add("spot-light");
    spotlightDiv.classList.add("white");
    spotlightDiv.classList.add(spotlightClasses[i]);
    body.append(spotlightDiv);
  }
}

//get spider js
if (!spiderJsGetting) {
  var spiderJsGetting = true;
  var spiderJsLoaded = false;
  var spiderCont = undefined;
  var spiderJsSrc =
    "https://raw.githubusercontent.com/Auz/Bug/master/bug-min.js";

  $.ajax({ url: spiderJsSrc, method: "GET" }).done(
    (responseData, textStatus, xhr) => {
      eval(responseData);

      window.SpiderController = SpiderController;
      window.BugController = BugController;
      spiderJsLoaded = true;
      spiderCont = null;
      refreshSpider();
    }
  );
}

var controlsDiv = $("#emotelistbtn").parent()[0];

//gunshot sound effect control
if ($("#cb-gunshot").length == 0) {
  var checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.value = 1;
  checkbox.name = "gunshot";
  checkbox.style.marginTop = "14px";
  checkbox.id = "cb-gunshot";

  var isChecked = window.localStorage.gunshotEnabled === "true";
  if (window.localStorage.gunshotEnabled === undefined) {
    isChecked = true;
    window.localStorage.setItem("gunshotEnabled", true);
  }

  checkbox.checked = isChecked;
  controlsDiv.appendChild(checkbox);

  var gunshotText = document.createElement("span");
  gunshotText.textContent = "Enable Gunshot";
  gunshotText.style.marginTop = "12px";
  controlsDiv.appendChild(gunshotText);

  $(document).on("change", "#cb-gunshot[type=checkbox]", function () {
    var cbChecked = $("#cb-gunshot")[0].checked;
    window.localStorage.setItem("gunshotEnabled", cbChecked);
  });
}

//facebook tracking
if ($("#cb-fb-tracking").length == 0) {
  var trackCheckbox = document.createElement("input");
  trackCheckbox.type = "checkbox";
  trackCheckbox.value = 1;
  trackCheckbox.style.marginTop = "14px";
  trackCheckbox.style.marginLeft = "14px";
  trackCheckbox.id = "cb-fb-tracking";
  trackCheckbox.checked = true;

  controlsDiv.appendChild(trackCheckbox);

  var trackText = document.createElement("span");
  trackText.textContent = "Allow Facebook Tracking Algorithms";
  trackText.style.marginTop = "12px";

  controlsDiv.appendChild(trackText);

  $(document).on("change", "#cb-fb-tracking[type=checkbox]", cbTrackedChanged);
}

//spider checkbox
if ($("#cb-spider").length == 0) {
  var spiderCheckbox = document.createElement("input");
  spiderCheckbox.type = "checkbox";
  spiderCheckbox.value = 1;
  spiderCheckbox.style.marginTop = "14px";
  spiderCheckbox.style.marginLeft = "14px";
  spiderCheckbox.id = "cb-spider";
  spiderCheckbox.checked = false;

  controlsDiv.appendChild(spiderCheckbox);
  $(document).on("change", "#cb-spider[type=checkbox]", cbSpiderChanged);
}

//spider tb
if ($("#tb-spider").length == 0) {
  var stb = document.createElement("input");
  stb.type = "texbox";
  stb.style.marginTop = "10px";
  stb.style.marginLeft = "10px";
  stb.id = "tb-spider";
  stb.style.width = "63px";
  stb.placeholder = "#sharks";

  controlsDiv.appendChild(stb);
}

/*
    =============================
    Halloween Styling
    - Change message font to pumpkin color
    - Show ghosts instead of spiders/sharks
    - Make ghosts fade in and out at semi-random intervals
    - Make ghost game
    =============================
*/

function setProperty(element, duration) {
  element.style.setProperty("--flicker-delay", duration + "s");
}

function changeAnimationTime(element) {
  let max = 10;
  let min = 3;
  let animationDuration = Math.random() * (max - min) + min;
  setProperty(element, animationDuration);
}

var addGhostClass = (el) => {
  $("body").css(
    "cursor",
    "url('http://www.rw-designer.com/cursor-view/101648.png'), auto"
  );
  el.addClass("ghost");
  let ghosts = document.querySelectorAll(".ghost");
  ghosts.forEach((ghost) => changeAnimationTime(ghost));
};

var globalSeconds = -1;
var isGhostHunting = false;
var currGhostCount = 0;
var intervalId;

var updateTime = () =>
  $("#ghost-time").text(
    ` ${Math.floor(globalSeconds / 60)}:${
      globalSeconds % 60 < 10 ? "0" + (globalSeconds % 60) : globalSeconds % 60
    }`
  );

var timer = (seconds) => {
  globalSeconds = seconds;
  intervalId = setInterval(function () {
    console.log("seconds left:", globalSeconds);
    globalSeconds--;
    updateTime();
  }, 1000);
};

var updateGhostCount = (ghostsCount) =>
  $("#num-ghosts").text(`${ghostsCount} `);

var addKillsAndCountDown = () => {
  let ghostTimeText = "Oh shit ghosts! Click them before the time runs out:";
  let ghostRemainingText = " ghosts remaining!";
  let div = $(
    `<div id="ghost-bar" class="m-0 p-0"><h1 class="text-danger ghost-status">${ghostTimeText}<span id="ghost-time"></span></h1><h2 class="text-danger ghost-status"><span id="num-ghosts"></span>${ghostRemainingText}</h2></div>`
  );
  div.appendTo("#drinkbarwrap");
  $("#drinkbarwrap").addClass("justify-content-center");
};

var addGhostClickBinding = () => {
  $(document).on("click", "div.bug.ghost", function () {
    $(this).closest("div").remove();
  });
};

var messageSpans = $(
  "#messagebuffer > div > span:not(.text-lottery):not(.timestamp):not(.userlist_owner)"
);

var yaDidIt = $(
  `<h1 class="text-success ghost-status">You fucking did it. Incredible.</h1>`
);
var yaFkIt = $(`<h1 class="text-danger ghost-status">Ya died. Why?</h1>`);

var enableGhosts = () => {
  $("#tb-spider").attr("placeholder", "#ghosts");
  $("#cb-spider").off();
  $("#cb-spider").on("click", cbGhostChanged);
  // each wouldnt be needed if user names didnt have the class nested
  $.each(messageSpans, function (_index, item) {
    if ($(item).children().length === 0) {
      $(item).css("color", "#D76B00");
    }
  });
};

var disableGhosts = () => {
  $("#tb-spider").attr("placeholder", "#sharks");
  $("#cb-spider").off();
  $("#cb-spider").on("click", cbSpiderChanged);
  // each wouldnt be needed if user names didnt have the class nested
  $.each(messageSpans, function (_index, item) {
    if ($(item).children().length === 0) {
      $(item).css("color", "");
    }
  });
  $(".bug").removeClass("ghost");
};

var itsOver = (isWinner) => {
  $("#ghost-bar").children().remove();
  $(isWinner ? yaDidIt : yaFkIt).appendTo("#ghost-bar");
  setTimeout(function () {
    $("#ghost-bar").remove();
  }, 5000);

  $("#cb-spooky").prop("checked", false);
  $("#cb-spider").prop("checked", false);
  disableGhosts();
  $("body").css("cursor", "auto");

  globalSeconds = -1;
  isGhostHunting = false;
  currGhostCount = 0;

  clearInterval(intervalId);
  refreshSpider();
};

// set up a mutation observer
// would be better to do some shit with the mutations but w/e
var bugObserver = new MutationObserver(function (_mutations, observer) {
  console.log("Monitoring ghosts");
  let ghosts = $(".bug");
  let numOfExpectedGhosts = isNaN(parseInt($("#tb-spider")[0].value))
    ? 0
    : parseInt($("#tb-spider")[0].value);

  // need a state machine jesus christ

  // checkboxes checked
  let spookyEnabled = $("#cb-spooky").length > 0 && $("#cb-spooky")[0].checked;
  let bugsLeft = ghosts.length <= numOfExpectedGhosts && ghosts.length > 0;
  let allBugsLoaded = ghosts.length === numOfExpectedGhosts;

  // true if the game has started (-1 seconds is a hack to ensure we dont fall into other states) + above
  let startGame =
    globalSeconds === -1 && !isGhostHunting && spookyEnabled && allBugsLoaded;

  // true if you uncheck spooky or ghost
  let killGame = !$("#cb-spooky")[0].checked || !$("#cb-spider")[0].checked;

  /* true if...
    - the game still has time
    - it's started
    - bugsleft
    - if you still have ghosts to kill
    - if you've killed a ghost since last read (hack optimization; otherwise updates the text every mutation)
  */
  let updateGame =
    globalSeconds > 0 &&
    isGhostHunting &&
    bugsLeft &&
    currGhostCount > ghosts.length;

  // true if time left and no ghosts
  let wonGame = globalSeconds > 0 && ghosts.length === 0;

  // true if no time left and ghosts left
  let lostGame = globalSeconds === 0 && ghosts.length > 0;

  if (startGame) {
    console.log("Started game!");
    isGhostHunting = true;
    addGhostClass(ghosts);
    addGhostClickBinding();
    addKillsAndCountDown();
    updateGhostCount(numOfExpectedGhosts);
    timer(Math.floor((numOfExpectedGhosts + 1) * 1.4));
    currGhostCount = numOfExpectedGhosts;
  } else if (killGame) {
    console.log("Killed game");
    itsOver(false);
    observer.disconnect();
  } else if (updateGame) {
    console.log("Update game");
    updateGhostCount(ghosts.length);
    currGhostCount = ghosts.length;
  } else if (wonGame) {
    console.log("Won game!");
    itsOver(true);
    observer.disconnect();
  } else if (lostGame) {
    console.log("You suck!");
    itsOver(false);
    observer.disconnect();
  }
});

var ghostSpider = (spite = null, width = null, height = null) => {
  let numBugs = isNaN(parseInt($("#tb-spider")[0].value))
    ? 0
    : parseInt($("#tb-spider")[0].value);
  return {
    imageSprite: spite ?? "https://auz.github.io/Bug/spider-sprite.png",
    bugWidth: width ?? 69,
    bugHeight: height ?? 90,
    canFly: false,
    canDie: false,
    zoom: 9,
    minDelay: 1,
    maxDelay: 1,
    minSpeed: 6,
    maxSpeed: 13,
    minBugs: numBugs,
    maxBugs: numBugs,
    num_frames: 1,
  };
};

function cbGhostChanged() {
  refreshSpider(ghostSpider("https://i.gifer.com/3V1b.gif", 200, 200));

  // HACK: Need to wait for ghosts to load before we can do anything further
  bugObserver.observe(document, {
    childList: true,
    subtree: true,
  });
}

function cbSpookyChange() {
  if ($("#cb-spooky")[0].checked) {
    enableGhosts();
  } else {
    disableGhosts();
  }
}

function createSpookyCB() {
  // If it's not created
  if (!$("#cb-spooky").length) {
    let spookyCheckbox = document.createElement("input");
    spookyCheckbox.type = "checkbox";
    spookyCheckbox.value = 1;
    spookyCheckbox.style.marginTop = "14px";
    spookyCheckbox.style.marginLeft = "14px";
    spookyCheckbox.id = "cb-spooky";
    spookyCheckbox.checked = false;

    controlsDiv.appendChild(spookyCheckbox);

    var spookyText = document.createElement("span");
    spookyText.textContent = "👻";
    spookyText.style.marginTop = "12px";

    controlsDiv.appendChild(spookyText);

    $(document).on("change", "#cb-spooky[type=checkbox]", cbSpookyChange);
  }
}

createSpookyCB();

/*
    =============================
    End Halloween Styling
    =============================
*/

//stockheimer checkbox
if ($("#cb-stockheimer").length == 0) {
  var checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.value = 1;
  checkbox.name = "stockheimer";
  checkbox.style.marginTop = "14px";
  checkbox.style.marginLeft = "14px";
  checkbox.id = "cb-stockheimer";
  var isChecked = false;

  controlsDiv.appendChild(checkbox);

  var stockheimerLink = document.createElement("a");
  var linkText = document.createTextNode("Stockheimer");
  stockheimerLink.appendChild(linkText);
  stockheimerLink.href = "https://stockheimergame.com";
  stockheimerLink.target = "_blank";
  stockheimerLink.title = "https://stockheimergame.com";
  stockheimerLink.style.marginTop = "12px";
  controlsDiv.appendChild(stockheimerLink);

  $(document).on(
    "change",
    "#cb-stockheimer[type=checkbox]",
    cbStockheimerChanged
  );

  if (isChecked) {
    refreshStockheimer();
  }
}

//background checkbox
if ($("#cb-background").length == 0) {
  var checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.value = 1;
  checkbox.name = "Disable chat Background";
  checkbox.style.marginTop = "14px";
  checkbox.style.marginLeft = "14px";
  checkbox.id = "cb-background";

  var isChecked = window.localStorage.backgroundDisabled === "true";
  if (window.localStorage.backgroundDisabled === undefined) {
    isChecked = false;
    window.localStorage.setItem("backgroundDisabled", false);
  }

  checkbox.checked = isChecked;
  controlsDiv.appendChild(checkbox);

  var bgText = document.createElement("span");
  bgText.textContent = "Bliss";
  bgText.style.marginTop = "12px";

  controlsDiv.appendChild(bgText);

  $(document).on("change", "#cb-background[type=checkbox]", cbBgChanged);

  if (isChecked) {
    refreshBg();
  }
}

function emoteSound(jqueryChatSpan, className) {
  var modOrUp = false;
  var allowGlobalSounds = true;
  className = className.replace("chat-msg-", "");
  className = className.toLowerCase();

  if (
    className == "circumsoldier" ||
    className == "orbmeat" ||
    className == "finalboss" ||
    className == "momhole" ||
    className == "axyl" ||
    className == "beepzoo" ||
    className == "deltaverse" ||
    className == "keiththefirewizard" ||
    className == "mombot" ||
    className == "rox" ||
    className == "steelshark" ||
    className == "steescribbles" ||
    className == "miles_gloriosus" ||
    className == "rottencheeseca" ||
    className == "bronxwarrior2" ||
    className == "creamkitten" ||
    className == "asoapyoid" ||
    className == "sickillusion" ||
    className == "tigref" ||
    className == "not_snax"
  ) {
    modOrUp = true;
  }

  if (modOrUp) {
    //search for emote images
    var emotesFound = jqueryChatSpan.find("img");
    var playGunshot = false;
    var playBoogie = false;
    var playFbi = false;
    var playPolis = false;
    var playCaw = false;
    var playHorn = false;
    var playOh = false;
    var playAllah = false;
    var playN = false;
    var playChirp = false;
    var batteryFound = false;
    var playReload = false;

    //find specific emote to playe gunshot sound
    for (var i = 0; i < emotesFound.length; i++) {
      var emoteTitle = emotesFound[i].getAttribute("title");
      if (emoteTitle == "/maths") {
        playGunshot = true;
      } else if (emoteTitle == "bigiron") {
        playBoogie = true;
      } else if (emoteTitle == "/agent") {
        playFbi = true;
      } else if (emoteTitle == "/polis") {
        playPolis = true;
      } else if (emoteTitle == "/Kaiattack") {
        playCaw = true;
      } else if (emoteTitle == "/airhorn") {
        playHorn = true;
      } else if (emoteTitle == "/ayytone") {
        playOh = true;
      } else if (emoteTitle == "JinnWick") {
        playAllah = true;
      } else if (emoteTitle == "hong") {
        playN = true;
      } else if (emoteTitle == "/beep") {
        playChirp = true;
      } else if (emoteTitle == "/battery") {
        batteryFound = true;
      } else if (emoteTitle == "/battery") {
        batteryFound = true;
      } else if (emoteTitle == "/reload") {
        playReload = true;
      }
    }

    if (playGunshot) {
      var audio = new Audio(
        "https://dontcodethis.com/images/Shotgun_Blast.wav"
      );
      audio.type = "audio/wav";
      audio.play();

      if (
        spiderJsLoaded === true &&
        spiderCont !== null &&
        spiderCont !== undefined
      ) {
        spiderCont.killAll();
      }
    }
    if (playBoogie) {
      var audio = new Audio(
        "https://dontcodethis.com/images/Boogie warning shot.wav"
      );
      audio.type = "audio/wav";
      audio.play();

      if (
        spiderJsLoaded === true &&
        spiderCont !== null &&
        spiderCont !== undefined
      ) {
        spiderCont.killAll();
      }
    }
    if (playFbi) {
      var audio = new Audio(
        "https://www.myinstants.com/media/sounds/fbi-open-up-sfx.mp3"
      );
      audio.type = "audio/wav";
      audio.play();
    }
    if (playPolis) {
      var audio = new Audio(
        "https://www.myinstants.com/media/sounds/11900601.mp3"
      );
      audio.type = "audio/wav";
      audio.play();
    }
    if (playCaw) {
      var audio = new Audio("https://static.dontcodethis.com/sounds/caw.wav");
      audio.type = "audio/wav";
      audio.play();
      audio.volume = 0.2;
    }
    if (playHorn) {
      var audio = new Audio(
        "https://static.dontcodethis.com/sounds/short-airhorn.mp3"
      );
      audio.type = "audio/wav";
      audio.play();
    }
    if (playOh) {
      var audio = new Audio(
        "https://freesound.org/data/previews/179/179334_2888453-lq.mp3"
      );
      audio.type = "audio/wav";
      audio.playbackRate = 4.0;
      audio.play();
    }
    if (playAllah) {
      var audio = new Audio("https://media1.vocaroo.com/mp3/1nD49ViBCBfj");
      audio.type = "audio/wav";
      audio.play();
    }
    if (playChirp) {
      var actuallyPlayChirp = true;

      //check battery emote in chat line
      if (batteryFound) {
        actuallyPlayChirp = false;
      }

      //check for battery emote on screen
      if (actuallyPlayChirp) {
        var numExistingBatteries = $(
          "#messagebuffer>div:not('.shotKilled') .channel-emote[title='/battery']"
        ).length;
        if (numExistingBatteries > 0) {
          actuallyPlayChirp = false;
        }
      }

      //play the chirp if no batteries on screen
      if (actuallyPlayChirp) {
        var audio = new Audio(
          "https://static.dontcodethis.com/sounds/smoke-alarm-chirp.mp3"
        );
        audio.type = "audio/wav";
        audio.volume = 1.0;
        audio.play();
      }
    }
    if (playReload) {
      var audio = new Audio(
        "https://static.dontcodethis.com/sounds/RELOAD.mp3"
      );
      audio.type = "audio/wav";
      audio.play();
    }

    /*		if(playN)
		{
			var audio = new Audio('https://static.dontcodethis.com/sounds/the-n.mp3');
			audio.type = 'audio/wav';
			audio.play();
		}*/
  }

  ////////////////////
  //global sounds. Comment out immediately if people abuse it.
  if (allowGlobalSounds) {
    var playChirp = false;
    var batteryFound = false;

    //search for emote images
    var emotesFound = jqueryChatSpan.find("img");
    for (var i = 0; i < emotesFound.length; i++) {
      var emoteTitle = emotesFound[i].getAttribute("title");
      if (emoteTitle == "/beep") {
        playChirp = true;
      } else if (emoteTitle == "/battery") {
        batteryFound = true;
      }
    }
    if (playChirp) {
      var actuallyPlayChirp = true;

      // check battery emote in chat line
      if (batteryFound) {
        actuallyPlayChirp = false;
      }

      //check for battery emote on screen
      if (actuallyPlayChirp) {
        var numExistingBatteries = $(
          "#messagebuffer>div:not('.shotKilled') .channel-emote[title='/battery']"
        ).length;
        if (numExistingBatteries > 0) {
          actuallyPlayChirp = false;
        }
      }

      // play the chirp if no batteries on screen
      if (actuallyPlayChirp) {
        var audio = new Audio(
          "https://static.dontcodethis.com/sounds/smoke-alarm-chirp.mp3"
        );
        audio.type = "audio/wav";
        audio.volume = 1.0;
        audio.play();
      }
    }
  }
  //
  ////////////////////
}

//let Andrew = document.querySelectorAll('.chat-msg-Andrew > span > .username');

//NodeListToArray(Andrew).forEach( e => e.innerHTML = 'CreamHole: ' );

function NodeListToArray(nodeList) {
  return nodeList instanceof NodeList
    ? [].slice.call(nodeList)
    : typeof nodeList === "string"
    ? NodeListToArray(document.querySelectorAll(nodeList))
    : console.log("error: NodeListToArray");
}

//functions for "Allow Facebook Tracking Algorithms" checkbox
var delayBetweenMessages = 60000; //ms

if (window.localStorage.dtFBMessage === undefined) {
  window.localStorage.setItem(
    "dtFBMessage",
    Date.now() - delayBetweenMessages + 4000
  );
}
var trackedMessageLastPlayed = parseInt(window.localStorage.dtFBMessage);

function cbTrackedChanged() {
  var ch = $("#cb-fb-tracking")[0].checked;

  if (ch && Date.now() >= trackedMessageLastPlayed + delayBetweenMessages) {
    trackedMessage();
  }

  window.setTimeout(() => {
    if (!ch && Date.now() >= trackedMessageLastPlayed + delayBetweenMessages) {
      trackedMessage();
    }
    $("#cb-fb-tracking")[0].checked = true;
  }, 4500);
}

function cbSpiderChanged() {
  refreshSpider();
}

function refreshSpider(customSpiderObject = null) {
  var isChecked = (cbChecked = $("#cb-spider")[0].checked === true);

  if (spiderJsLoaded === true) {
    if (customSpiderObject !== null) {
      // Kill any instance of any other spiders if a custom one is provided
      if (spiderCont !== null && spiderCont !== undefined) {
        spiderCont.stop();
        spiderCont.end();
        spiderCont = null;
      }
      spiderCont = new SpiderController(customSpiderObject);
    } else if (isChecked === true && spiderCont === null) {
      var s = $("#tb-spider")[0];
      var actuals = parseInt(s.value);

      if (!isNaN(actuals)) {
        //actual spiders
        spiderCont = new SpiderController({
          imageSprite: "https://auz.github.io/Bug/spider-sprite.png",
          bugWidth: 69,
          bugHeight: 90,
          canFly: false,
          canDie: false,
          zoom: 9,
          minDelay: 100,
          maxDelay: 100,
          minSpeed: 6,
          maxSpeed: 13,
          minBugs: actuals,
          maxBugs: actuals,
          mouseOver: "multiply",
        });
        //ghosts since i lost the link sorry
        // spiderCont = new SpiderController({
        // 	imageSprite: "https://i.gifer.com/3V1b.gif",
        // 	canFly:false,
        // 	canDie:false,
        // 	zoom:0,
        // 	minDelay:100,
        // 	maxDelay:100,
        // 	minSpeed:6,
        // 	maxSpeed:13,
        // 	minBugs:actuals,
        // 	maxBugs:actuals,
        // 	mouseOver: "multiply",
        // 	num_frames: 1,
        // 	bugWidth: 200,
        // 	bugHeight: 200
        // });
      }
    } else if (
      isChecked === false &&
      spiderCont !== null &&
      spiderCont !== undefined
    ) {
      spiderCont.stop();
      spiderCont.end();
      spiderCont = null;
    }
  }
}

function trackedMessage() {
  trackedMessageLastPlayed = Date.now();
  window.localStorage.setItem("dtFBMessage", trackedMessageLastPlayed);
  socket.emit("chatMsg", {
    msg: "I have allowed facebook to track me with their algorithms.",
    meta: {},
  });

  $("#cb-fb-tracking")[0].checked = true;
}

function cbStockheimerChanged() {
  var cbChecked = $("#cb-stockheimer")[0].checked;
  window.localStorage.setItem("stockheimerEnabled", cbChecked);
  refreshStockheimer();
}

function cbBgChanged() {
  var cbChecked = $("#cb-background")[0].checked;
  window.localStorage.setItem("backgroundDisabled", cbChecked);
  refreshBg();
}

function refreshBg() {
  var isChecked = window.localStorage.backgroundDisabled === "true";

  if (isChecked) {
    $("#messagebuffer").css("background-image", "none");
  } else {
    $("#messagebuffer").css("background-image", "");
  }
}

function refreshStockheimer() {
  var isChecked = window.localStorage.stockheimerEnabled === "true";
  if (isChecked) {
    if ($("#iframe-stockheimer").length === 0) {
      console.log("Adding stockheimer iframe.");
      var iframe = document.createElement("iframe");
      iframe.id = "iframe-stockheimer";
      iframe.src = "https://stockheimergame.com";
      iframe.style = "width: 100%; height: 640px;";
      controlsDiv.appendChild(iframe);
    }
  } else {
    console.log("Removing stockheimer iframe.");
    $("#iframe-stockheimer").remove();
  }
}

function checkMention(chatText, chatDiv) {
  if (CLIENT.name) {
    var regex = /@[^ ]*/gi;
    var matches = chatText.match(regex);
    if (matches !== null) {
      var clientName = CLIENT.name.toLowerCase();
      for (var i = 0; i < matches.length; i++) {
        var m = matches[i].replace("@", "").toLowerCase();

        if (clientName === m) {
          chatDiv.addClass("chat-mention");
        }
      }
    }
  }
}

function checkReturnFire(jqueryChatSpan, chatText, chatDiv) {
  window.setTimeout(() => {
    if (!chatDiv.hasClass("chat-shadow")) {
      var emotesFound = jqueryChatSpan.find("img");
      var killPrevChatMessage = false;

      for (var i = 0; i < emotesFound.length; i++) {
        var emoteTitle = emotesFound[i].getAttribute("title");
        if (emoteTitle == "returnfire") {
          killPrevChatMessage = true;
          break;
        }
      }

      if (killPrevChatMessage) {
        var prevChat = chatDiv.prev();

        if (prevChat.length > 0) {
          var victimGolds = prevChat.find("span.text-lottery").length;

          if (victimGolds === 1) {
            if (window.localStorage.gunshotEnabled === "true") {
              var audio = new Audio(
                "https://static.dontcodethis.com/sounds/tink.mp3"
              );
              audio.type = "audio/wav";
              audio.play();
            }

            var shooterGolds = chatDiv.find("span.text-lottery").length;
            if (shooterGolds === 0) {
              chatDiv.addClass("shotKilled");
            }
          } else if (victimGolds === 0) {
            prevChat.addClass("shotKilled");
          }
        }
      }
    }
  }, 10);
}

//this just hashes the
function textLottery(chatText, jqueryChatSpan, everything) {
  //temporarily in here
  modSoy(jqueryChatSpan, jqueryChatSpan, everything);

  //Check for the "currenttitle-content" first to calculate gold. If its not there (because they hid the video to show chat only), check the last active video in the queue.
  //Also, apparently there can be more than 1 "active" video if you just hit 'play' on a video in the queue while there is a 'permanent' video still in the queue.
  //This does break golds if there are multiple permanent videos in the queue AND they have the video turned off (because a 'permanent' flag does NOT remove
  //the queue_active class from the video queue as it plays through the permanent videos)...oh well. Its good enough.
  var currentVideoTitle = "";
  var currentTitle = $("#currenttitle-content");

  if (currentTitle.length === 1) {
    currentVideoTitle = currentTitle.text();
  } else {
    //Check the 'active videos' in the queue, and grab the last found record
    //Its 'last' to handle the common case when a mod makes the top video a 'permanent' and hit plays on a video below.
    currentVideoTitle = $(".queue_active .qe_title").last().text();
  }

  var dateModifier =
    Math.floor((new Date().getUTCMonth() + 3) / 3) +
    new Date().getUTCFullYear();
  //   var dateModifier = Math.floor((new Date("12/1/2022").getUTCMonth() + 3)/3) + new Date("12/1/2022").getUTCFullYear();
  var lotteryText =
    chatText.toString() + currentVideoTitle + "co" + dateModifier.toString();
  var lotteryHash = hashFunc(lotteryText);
  lotteryHash %= 100;

  lotteryHash = lotteryHash < 0 ? -lotteryHash : lotteryHash;

  //1% chance idk
  if (lotteryHash === 1) {
    //if(true) {
    jqueryChatSpan.addClass("text-lottery");
  }

  //var rand = Math.floor((Math.random()*25) % 25);
  //var audio = null;
  //if(rand == 0) {audio = new Audio('https://static.dontcodethis.com/sounds/cough1.mp3');audio.volume=0.1;}
  //else if (rand == 1) {audio = new Audio('https://static.dontcodethis.com/sounds/cough2.wav');audio.volume=0.1;}
  //else if (rand == 2) {audio = new Audio('https://static.dontcodethis.com/sounds/cough3.wav');audio.volume=0.1;}
  //else if (rand == 3) {audio = new Audio('https://static.dontcodethis.com/sounds/popcorn.m4a');audio.volume=0.02;}
  //else if (rand == 4) {audio = new Audio('https://static.dontcodethis.com/sounds/sniffing.mp3');audio.volume=0.1;}
  //else if (rand == 5) {audio = new Audio('https://static.dontcodethis.com/sounds/sneeze.mp3');audio.volume=0.1;}

  //if(audio !== null) {
  //	audio.type = 'audio/wav';
  //	audio.play();
  //}
}

function hashFunc(str) {
  var hash = 0,
    i,
    chr;
  if (str.length === 0) return hash;
  for (i = 0; i < str.length; i++) {
    chr = str.charCodeAt(i);
    hash = (hash << 5) - hash + chr;
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
}

//create broteam links
if (!linksCreated) {
  var linksCreated = true;
  console.log("CREATING LINKS");

  addNavDivider();
  addNavItem(
    "Patreon",
    "https://www.patreon.com/broteam",
    "https://i.ibb.co/PWR3z4P/patreon-creators-patreon.png"
  );
  addNavDivider();
  addNavItem(
    "Twitter",
    "https://twitter.com/getincoolhole",
    "https://i.ibb.co/KbWjBrY/twitter-xxl.png"
  );
  addNavDivider();
  addNavItem(
    "Videos",
    "https://videos.coolhole.org",
    "https://i.ibb.co/WvRzgxV/pill.png"
  );
  addNavDivider();
  addNavItem(
    "Donate",
    "https://streamlabs.com/getincoolhole/tip",
    "https://i.ibb.co/N1Xdg02/moneypill.png"
  );
  addNavDivider();
  addNavItem(
    "Discord",
    "https://discord.gg/gh25Pe8eaK",
    "https://i.ibb.co/bNvtgSc/discord-transparent-server-icon-12.png"
  );
  addNavDivider();
  addNavItem(
    "Goldhole",
    "https://hole.gold",
    "https://i.ibb.co/qjhRkDJ/output-onlinegiftools-4.gif"
  );
}

function addNavItem(text, url, imgUrl) {
  var navItem = $(document.createElement("li"));
  navItem.addClass("nav-item");
  navItem.css("display", "inherit"); //whatever. Need this or the text won't stay on the same line as the images

  var navLink = $(document.createElement("a"));
  navLink.text(text);
  navLink.addClass("nav-link");
  navLink.attr("href", url);
  navLink.attr("target", "_blank");

  var img = null;
  if (imgUrl) {
    img = $(document.createElement("img"));
    img.attr("src", imgUrl);
    img.attr("height", 26);
    img.css("margin-top", "5px");

    //adjust the text too so its not so far away from the image
    navLink.css("padding-left", "0px");
  }

  if (imgUrl) {
    navItem.append(img);
    navItem.append(navLink);
  } else {
    navItem.append(navLink);
  }
  $("#nav-collapsible>.nav").last().append(navItem);
  return navItem;
}

function addNavDivider() {
  var navItemDivider = $(document.createElement("li"));
  navItemDivider.addClass("nav-item");
  navItemDivider.addClass("divider");
  navItemDivider.text("|");
  $("#nav-collapsible>.nav").last().append(navItemDivider);
  return navItemDivider;
}

//add title document.title changer
if (!titleMutationObs) {
  var titleNode = document.getElementById("currenttitle");
  var titleMutationObs = new MutationObserver(() => {
    var currentVideoTitle = $("#currenttitle-content").text();
    PAGETITLE = currentVideoTitle;
    document.title = currentVideoTitle;
  });

  titleMutationObs.observe(titleNode, {
    attributes: false,
    childList: true,
    subtree: true,
  });

  //add a wrapper function for the window focus function so it stops changing the title back to the channel name
  var oldFocus = window.onfocus;
}

var play = true;
var playreal = false;

if (play) {
  if (myaudio) {
    myaudio.pause();
    myaudio.currentTime = 0;
  }
  if (playreal) {
    var myaudio = new Audio(
      "https://static.dontcodethis.com/sounds/11_O_Clock.mp3"
    );

    myaudio.type = "audio/wav";
    myaudio.play();
    myaudio.playbackRate = 1.0;
  }
}

console.log("=== ending custom js ===");
"""
