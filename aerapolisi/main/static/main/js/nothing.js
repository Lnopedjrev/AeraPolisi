consoleText(["There is nothing actually","Just air"],"text",["black","blue"])
function consoleText(words,id,colors){
    if(colors==undefined) colors=["fff"];
    var visible=true;
    var con=document.getElementById("console");
    var letterCount=1;
    var x=1;
    var waiting=false;
    var target=document.getElementById(id);
    var stoptimer=0;
    target.setAttribute("style","color:"+colors[0])
    const megashow=setInterval(shows,120)
    function shows(){
        if(letterCount=== 0 && waiting===false){
            waiting=true;
            target.innerHTML=words[0].substring(0,letterCount)
            window.setTimeout(function(){
                var usedColor=colors.shift();
                colors.push(usedColor);
                var usedWord=words.shift();
                words.push(usedWord);
                x=1;
                target.setAttribute("style","color:"+ colors[0])
                letterCount+=x;
                waiting=false
            },1000)
        }
        else if(letterCount===words[0].length+1 && waiting===false){
            waiting=true;
            window.setTimeout(function(){
                x= -1;
                letterCount +=x;
                waiting=false;
            },1000)
        }
        else if(waiting===false){
            target.innerHTML =words[0].substring(0,letterCount)
            letterCount+=x
        }
    }
    window.setInterval(function() {
        if (visible === true) {
          con.className = 'console-underscore hidden'
          visible = false;
    
        } else {
          con.className = 'console-underscore'
    
          visible = true;
        }
      }, 400)    
}