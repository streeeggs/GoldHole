/*
    Used to test text lottery. Needs to be updated if textLottery ever updates. 
    Or textLottery should have discrete hashing functions to let me call this easily
*/
function textLottery2(chatText, howFarAreYouWillingToGo = 10) {
  var currText = chatText;

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

  var count = 1;

  while (count < howFarAreYouWillingToGo ?? 10) {
    currText = chatText
      .split(" ")
      .map((w) => w + " ".repeat(count))
      .join("");

    lotteryText = currText + currentVideoTitle + "co" + dateModifier.toString();
    lotteryHash = hashFunc(lotteryText);
    lotteryHash %= 100;

    lotteryHash = lotteryHash < 0 ? -lotteryHash : lotteryHash;
    if (lotteryHash === 1) {
      console.log(lotteryHash, lotteryText, count);
      $("#chatline").val(currText);
      return currText;
    }
    count++;
    currText = chatText;
  }
  return "**NOTHING**";
}
