const image = new Image(60,60); 
image.src = "images/envelope.png";
const image2 = new Image(60,60); 
image2.src = "images/bomb.png";
const image3 = new Image(60,60); 
image3.src = "images/flag.png";

var bombs=[]
var messages=[]


var pressed=0
function showInstructions()
{
var pmes=document.getElementById("instructions")
if(pmes)
if(pressed==0)
{
pressed=1
pmes.style.display="block"
}
else
{
pressed=0
pmes.style.display="none"
}

}









async function get(){
return fetch("http://localhost:8080/messages",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
    console.log('Success:',data);
     messages=data['texts']
     
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
  
  
  
  
  
}

async function get_bombs()
{
await get()
return fetch("http://localhost:8080/bombs",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
    console.log('Success:',data);
     bombs=data["obstacol"]
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}

get_bombs()


window.addEventListener("keydown", function(e) {
    if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault();
    }
}, false);

