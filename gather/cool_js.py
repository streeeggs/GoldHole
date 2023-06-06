def cool_js():
    return """
console.log("=== starting custom js ===");

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
        var prevChat = chatDiv.prev();

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

  if(currentTitle.length === 1) {
	currentVideoTitle = currentTitle.text();
  } else {
	//Check the 'active videos' in the queue, and grab the last found record
	//Its 'last' to handle the common case when a mod makes the top video a 'permanent' and hit plays on a video below.
	currentVideoTitle = $(".queue_active .qe_title").last().text();
  }

  var dateModifier = Math.floor((new Date().getUTCMonth() + 3)/3) + new Date().getUTCFullYear();
//   var dateModifier = Math.floor((new Date("12/1/2022").getUTCMonth() + 3)/3) + new Date("12/1/2022").getUTCFullYear();
  var lotteryText = chatText.toString() + currentVideoTitle + "co" + dateModifier.toString();
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

console.log("=== ending custom js ===");
"""
