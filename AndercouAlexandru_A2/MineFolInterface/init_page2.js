const image = new Image(60,60); 
image.src = "images/envelope.png";
const image2 = new Image(60,60); 



dangerSrc=["images/police.png","images/dog.jpg","images/bomb.png"]




const image3 = new Image(60,60); 
image3.src = "images/flag.png";

const image5 = new Image(60,60); 
image5.src = "images/gold_key.jpg";

const image4 = new Image(60,60); 
image4.src = "images/door.jpg";


var bombs=[]
var messages=[]
var key
var door


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
return fetch("http://localhost:8085/messages",{method:"GET",mode:"cors"}).then((response) => response.json())
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
return fetch("http://localhost:8085/bombs",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
    console.log('Success:',data);
     bombs=data["obstacol"]
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}








async function get_door()
{
await get_bombs()
return fetch("http://localhost:8085/door",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
     console.log('Door of Success:',data);
     door=data
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}


async function get_key()
{
await get_door()
return fetch("http://localhost:8085/key",{method:"GET",mode:"cors"}).then((response) => response.json())
  .then((data) => {
    console.log('Success key:',data);
     key=data
     
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}









get_key()

//key={"x":7,"y":7}
//door={"x":8,"y":1}


window.addEventListener("keydown", function(e) {
    if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault();
    }
}, false);
