def cool_js():
    return """
console.log("=== starting custom js ===");

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

        if (window.localStorage.sfxModEnabled === "true") {
          emoteSound(jqueryChatSpan, this[0].className);
        }
      }
    }
    return oldAppend.apply(this, arguments);
  };
}


function modSoy(jqueryChatSpan, chatText, chatDiv) {
	//first, display none all soooys
	jqueryChatSpan.find("img[title='/soooy'], img[title='/gunPointLeft'], img[title='/gunPointRight'], img[title='/heart']").css("display", "none");
	chatText.css("position", "relative");

	window.setTimeout(() => {
		//second, find all the soys again, and position them on the previous emote
		var chatTextRect = chatText[0].getBoundingClientRect();
		var emotesFound = jqueryChatSpan.find("img");
		var prevNonOverlayRect = null;
		var prevEmoteTitle = "";
		var emoteCombo = 0;
		for(var i = 0; i < emotesFound.length; i++) {
			var emoteTitle = emotesFound[i].getAttribute("title");

			if(emoteTitle === "/soooy" || emoteTitle === "/gunPointLeft" || emoteTitle === "/gunPointRight" || emoteTitle === "/heart") {
				emotesFound[i].style.display = "";

				if(prevEmoteTitle === emoteTitle) {
					emoteCombo++;
				} else {
					emoteCombo = 0;
				}

				//if its the first emote, count it as the first non-overlayed emote instead
				if(i === 0) {
					prevNonOverlayRect = emotesFound[i].getBoundingClientRect();
					emoteCombo = 0;
				}
				else {
					// console.log("found soy " + i);
					emotesFound[i].classList.add("emote-overlay");
					var overlayEmoteRect = emotesFound[i].getBoundingClientRect();

					//adjust the overlay depending on the emote
					switch(emoteTitle) {
						case "/heart":
						case "/soooy":
							var leftPrevEmote = prevNonOverlayRect.left - chatTextRect.left;
							var topPrevEmote = prevNonOverlayRect.top - chatTextRect.top;
							emotesFound[i].style.left = leftPrevEmote - Math.round((overlayEmoteRect.width - prevNonOverlayRect.width) / 2) + emoteCombo + "px";
							emotesFound[i].style.top = topPrevEmote - Math.round((overlayEmoteRect.height - prevNonOverlayRect.height) / 2) + emoteCombo + "px";
							break;
						case "/gunPointLeft":
							var leftPrevEmote = prevNonOverlayRect.left - chatTextRect.left;
							emotesFound[i].style.left = leftPrevEmote - Math.round(overlayEmoteRect.width/4) + emoteCombo + "px";
							emotesFound[i].style.bottom = -Math.round(overlayEmoteRect.height/2) + emoteCombo + "px";
							break;
						case "/gunPointRight":
							var rightPrevEmote = prevNonOverlayRect.right - chatTextRect.left;
							emotesFound[i].style.left = rightPrevEmote - Math.round(overlayEmoteRect.width*3/4) + emoteCombo + "px";
							emotesFound[i].style.bottom = -Math.round(overlayEmoteRect.height/2) + emoteCombo + "px";
							break;
					}

					prevEmoteTitle = emoteTitle;
				}
			} else {
				prevNonOverlayRect = emotesFound[i].getBoundingClientRect();
				emoteCombo = 0;
			}
		}
	}, 500)

}

var controlsDiv = $("#emotelistbtn").parent()[0];

var messageSpans = $(
  "#messagebuffer > div > span:not(.text-lottery):not(.timestamp):not(.userlist_owner)"
);

function NodeListToArray(nodeList) {
  return nodeList instanceof NodeList
    ? [].slice.call(nodeList)
    : typeof nodeList === "string"
    ? NodeListToArray(document.querySelectorAll(nodeList))
    : console.log("error: NodeListToArray");
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
        var prevChat = chatDiv.prev("div[class*=chat-msg]");
		
        if (prevChat.length > 0) {
          var victimGolds = prevChat.find("span.text-lottery").length;

          if (victimGolds === 1) {
            if (window.localStorage.sfxModEnabled === "true") {
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

//////////////////////////////////////
// Client Side Preferences          //
//////////////////////////////////////

//Should only be called once when the channel js is loaded in.
if(!createdPreferencesVariables) {
	var createdPreferencesVariables = true;
	var defaultVideoZoomLevel = 5;
	var currentVideoZoomLevel = defaultVideoZoomLevel; //always starts at 5 from cytube
	var minVideoZoomLevel = 1;
	var maxVideoZoomLevel = 7;

	var hideUserlistDefault = false; //always starts false from cytube
	var currentHideUserlist = hideUserlistDefault;
}

function updateZoomLevel(modZoomLevel) {
	if(isNaN(currentVideoZoomLevel)) {
		currentVideoZoomLevel = defaultVideoZoomLevel; //not sure how this could happen, but just in case
	}

	currentVideoZoomLevel += modZoomLevel;

	if(currentVideoZoomLevel > maxVideoZoomLevel) {
		currentVideoZoomLevel = maxVideoZoomLevel
	} else if (currentVideoZoomLevel < minVideoZoomLevel) {
		currentVideoZoomLevel = minVideoZoomLevel;
	}

	window.localStorage.setItem("videoZoomLevel", currentVideoZoomLevel);
}

function applyZoomLevel() {
	var targetZoomLevel = defaultVideoZoomLevel;

	var testInt = parseInt(window.localStorage.videoZoomLevel, 10);
	if (testInt !== undefined && !isNaN(testInt)) {
		targetZoomLevel = testInt;
	}

	var counter = 0;
	var maxCounter = maxVideoZoomLevel - minVideoZoomLevel + 1;
	var videoSmaller = document.getElementById("resize-video-smaller");
	var videoLarger = document.getElementById("resize-video-larger");
	while(currentVideoZoomLevel !== targetZoomLevel && counter < maxCounter) {
		if(currentVideoZoomLevel < targetZoomLevel) {
			videoLarger.click();
			currentVideoZoomLevel++;
		}
		else if (currentVideoZoomLevel > targetZoomLevel) {
			videoSmaller.click();
			currentVideoZoomLevel--;
		}
		else {
			break;
		}
		counter++;
	}
}


function updateHideUserlist() {
	if(currentHideUserlist === undefined) {
		currentHideUserlist = hideUserlistDefault; //not sure how this could happen, but just in case
	}
	currentHideUserlist = currentHideUserlist ? false : true;

	window.localStorage.setItem("hideUserlist", currentHideUserlist);
}

function applyHideUserlist() {
	var targetHide = hideUserlistDefault;

	var testbool = window.localStorage.hideUserlist;
	if (testbool !== undefined && testbool === "true") {
		targetHide = testbool;
	}

	currentHideUserlist = targetHide;

	if(currentHideUserlist) {
		$("#usercount").click();
	}
}


//Should only be called once when the channel js is loaded in.
if(!preferencesApplied) {
	var preferencesApplied = true;

	//apply video zoom level preference
	applyZoomLevel();

	//apply functions to update/save the video zoom level prereference
	$("#resize-video-smaller").click(() => updateZoomLevel(-1));
	$("#resize-video-larger").click(() => updateZoomLevel(1));

	//apply hiding the user list preference
	applyHideUserlist();

	//apply functions to update/save the hide user list preference
	$("#usercount").click(() => updateHideUserlist());
	$("#userlisttoggle").click(() => updateHideUserlist());
}

//////////////////////////////////////
// Client Side Preferences done     //
//////////////////////////////////////


var play = true;
var playreal = false;

if (play) {
  if (myaudio) {
    myaudio.pause();
    myaudio.currentTime = 0;
  }
  if (playreal) {
    var myaudio = new Audio(
      "https://static.dontcodethis.com/sounds/clap2.mp3"
    );

    myaudio.type = "audio/wav";
    myaudio.play();
    myaudio.playbackRate = 1.0;
  }
}

/* Dumb Halloween Stuff */
var today = new Date();
var halloweenDate = new Date("10/31/2023");

// Calculate the number of days until Halloween
var daysUntilHalloween = Math.max(halloweenDate.getDate() - (today.getDate()), 0);

// Width boundaries 
var initialWidth = 4; 
var maxWidth = 150;
// Height boundaries 
var initialHeight = 6;
var maxHeight = 20;

// Interval based on 7 days from when this was written
var widthInterval = (maxWidth - initialWidth) / 7;
var heightInterval = (maxHeight - initialHeight ) / 7;

// Interval * number of days that have passed since a week ago, capping at Halloween
// This is suppose to be "counting up" to Halloween so the numbers got larger as we got closer to Halloween
var currWidth = Math.min(maxWidth, widthInterval * (7 - daysUntilHalloween) + initialWidth);
var currHeight = Math.min(maxHeight, heightInterval * (7 - daysUntilHalloween) + initialHeight);

// Update vars which are on the pseudo elements on body
document.querySelectorAll('body')[0].style.setProperty("--skel-width", currWidth + "vw");
document.querySelectorAll('body')[0].style.setProperty("--skel-height", currHeight + "vh");

/* End dumb halloween stuff */

console.log("=== ending custom js ===");
"""
