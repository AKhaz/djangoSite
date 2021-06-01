function createNewChoice(){
  var choiceDiv = document.getElementById("NewChoiceDiv");
  choiceNum = 0;
  console.log(choiceNum);
  allChoices = choiceDiv.getElementsByTagName("input").length;
  for (i = 0; i <= allChoices; i++){
    choiceNum += 1;
  }
  choiceDiv.innerHTML += "<input class='InputFormBox' type='text' name = 'Option" + choiceNum + "' placeholder='Option " + choiceNum + "'></input>"
}
