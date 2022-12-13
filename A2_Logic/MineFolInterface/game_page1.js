console.log('messages:',messages);
var canvas= document.getElementById("board")
var context=canvas.getContext("2d")
var w=800
var h=735
var currentx=1
var currenty=1
var prevx
var prevy
   
var box=90
var drawableObjects=Array(9).fill(null).map( () => Array(9).fill(0))

   function drawboard()
   {
   
     context.lineWidth = 10;
     context.strokeStyle = "rgb(2,7,159)";
       for(var i=0;i<h;i+=box)
       for(var j=0;j<w;j+=box)
       {
         context.strokeRect(i+10, j+10, box,box); 
              
       }
   
   }
   function drawImage(boxi,boxj)
{
   var boxh=(boxi-1)*90+10
   var boxw=(boxj-1)*90+10
   context.drawImage(image,boxh+15,boxw+10,60,60)
   
}
   function drawImage2(boxi,boxj)
{

   var boxh=(boxi-1)*90+10
   var boxw=(boxj-1)*90+10
   context.drawImage(image2,boxh+15,boxw+10,60,60)
   
}
   function drawImage3(boxi,boxj)
{
   var boxh=(boxi-1)*90+10
   var boxw=(boxj-1)*90+10
   context.drawImage(image3,boxh+15,boxw+10,60,60)
   
}
function check_message(cx,cy)
{
for( var m of messages)
{
if(m["y"]==cy && m["x"]==cx)
{

drawableObjects[cx][cy]=1
drawImage(cx,cy)

set_message(currentx,currenty,(data)=>console.log(data))
 
var pmes=document.getElementById("messages")
if(pmes)
pmes.textContent=m["text"]



}

}
}
function check_bomb(cx,cy)
{
for( var m of bombs)
{
if(m["y"]==cy && m["x"]==cx)
{
drawableObjects[cx][cy]=2
drawImage2(cx,cy)
return true


}

}
return false
}



function set_visited(cx,cy,do_stuff)
{

return fetch("http://localhost:8080/visited/i="+cy+",j="+cx,{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
   
   
    do_stuff(data)
   
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}
function set_message(cx,cy,do_stuff)
{

return fetch("http://localhost:8080/message/i="+cy+",j="+cx,{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
   
   
    do_stuff(data)
   
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}






async function check_win(cx,cy,do_stuff)
{

return fetch("http://localhost:8080/won",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
   
   
    do_stuff(data)
   
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}


async  function check_lost(cx,cy,do_stuff)
{

return fetch("http://localhost:8080/lose",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
   
   
    do_stuff(data)
   
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}




async function inform_bomb_found(cx,cy, do_stuff)
{
return fetch("http://localhost:8080/set_mine/i="+cy+",j="+cx,{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
   
   
    do_stuff(data)
     
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });


}






async function askMace4(do_stuff)
{

return fetch("http://localhost:8080/safe/i="+currenty+",j="+currentx,{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
   
   
    do_stuff(data)
     
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
   
}








function drawCurrent()
{
 context.fillStyle ="#00FF00";
 context.fillRect((currentx-1)*90+15,(currenty-1)*90+15,80,80)

}
function drawPrevious()
{
 context.fillStyle = "#808080";
 context.fillRect((prevx-1)*90+15,(prevy-1)*90+15,80,80)

}


drawboard()






canvas.addEventListener('mousedown', function(e) {

   const rect = canvas.getBoundingClientRect()
    var x = e.clientX - rect.left
    var y = e.clientY - rect.top
    x=x/box
    y=y/box
    x=Math.trunc(x+1)
    y=Math.trunc(y+1)
    drawImage3(x,y)
    





})


function reset()
{
context.clearRect(0, 0, canvas.width, canvas.height);
drawboard()
currentx=1
currenty=1
var pmes=document.getElementById("messages")
if(pmes)
pmes.textContent=""
get_bombs()
}

function reload_page()
{
location.reload()

}

function show_answer()
{

context.clearRect(0,0,canvas.width,canvas.height)
drawboard()


for(var i=1 ;i<=8;i++)
for(var j=1 ;j<=8;j++)
{
 check_bomb(i,j)
  for( var m of messages)
{
if(m["y"]==i && m["x"]==j)
{

drawableObjects[i][j]=1
drawImage(i,j)

}

}
}

 drawCurrent()

}

function reset_game()
{
return fetch("http://localhost:8080/reset",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
   
   
    reload_page()
     
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
   
}








window.addEventListener('keydown',this.check,false);






async function check(e) {
   // alert(e.keyCode);
  
    prevx=currentx
    prevy=currenty
   
   
    if(e.keyCode==38)
    currenty-=1;
    
      if(e.keyCode==40)
     currenty+=1;
 
 
      if(e.keyCode==39)
      {  
         currentx+=1;
      }
        if(e.keyCode==37)
      {
         currentx-=1;
    
      }
      
      if(currentx<1 || currentx>8)
      currentx=prevx
        if(currenty<1 || currenty>8)
      currenty=prevy
      
      
      
      
        askMace4( (data)=>
        {
        console.log("data:",data)
        if(data["safe"]=="false")
        {
         currentx=prevx
         currenty=prevy
        
        alert("Prover9 detactaed a bomb to the position you want to go, so we will block your moving")
        }
        else
        {
        
        
        
       check_bomb(currentx,currenty)
       check_message(currentx,currenty) 
        
        
        set_visited(currentx,currenty,(data)=>console.log(data))    
       
        if(check_bomb(currentx,currenty))
        {  inform_bomb_found(currentx,currenty,(data)=>console.log(data))
        
        }    
         
         
        
        check_win(currentx,currenty,(data)=>{
         
         if(data["win"]=="true")
         {
         alert("You won , please play again!")
         reload_page()
         }
         
         } )
         
         
       check_lost(currentx,currenty,(data)=>{
         
         if(data["lost"]=="true")
         {
         alert("You lost, please try again!")
         reload_page()
         }
         
         } )
              
   if(check_bomb(currentx,currenty))
        {  
         
           currentx=1
           currenty=1
        
        }  
     
 
 
       drawboard();
        
    
       
      if(drawableObjects[currentx][currenty]==0)
      {
        drawCurrent()
      }
      if(drawableObjects[prevx][prevy]==0)
      {
        drawPrevious()
      }
     
   
    
       

      
      
      
      }
      
      
    })
    
    }
    
