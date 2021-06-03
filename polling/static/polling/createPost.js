function createNewChoice(){
  var choiceDiv = document.getElementById("NewChoiceDiv");
  choiceNum = 0;
  console.log(choiceNum);
  // counts number of previous options by finding elements of tag "input" in a specific div
  allChoices = choiceDiv.getElementsByTagName("input").length;
  //loops through the length of other options to find the next option index
  for (i = 0; i <= allChoices; i++){
    choiceNum += 1;
  }
  //create a new option field using the index obtained by the for loop
  choiceDiv.innerHTML += "<input class='InputFormBox' type='text' name = 'Option" + choiceNum + "' placeholder='Option " + choiceNum + "'></input>"
}
