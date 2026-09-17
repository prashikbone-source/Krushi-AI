const API = "http://127.0.0.1:5000";

// LOGIN
function login(){
 fetch(API+"/login",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
    username:username.value,
    password:password.value
  })
 })
 .then(r=>r.json())
 .then(d=>{
  if(d.status==="success"){
    window.location="dashboard.html"
  } else {
    msg.innerText="Invalid login"
  }
 })
}

// MILK
function saveMilk(){
 fetch(API+"/milk",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
    animal:animal.value,
    litre:litre.value
  })
 }).then(()=>alert("Saved"))
}

// CROP
function getCrop(){
 fetch(API+"/crop",{
  method:"POST",
  headers:{"Content-Type":"application/json"},
  body:JSON.stringify({
    soil:soil.value,
    season:season.value
  })
 })
 .then(r=>r.json())
 .then(d=>{
  cropResult.innerText="🌱 "+d.crop
 })
}

// AI
function detect(){
 let file=image.files[0]
 let fd=new FormData()
 fd.append("image",file)

 fetch(API+"/detect",{method:"POST",body:fd})
 .then(r=>r.json())
 .then(d=>{
  aiResult.innerHTML=`
  <b>Disease:</b> ${d.disease}<br>
  <b>Confidence:</b> ${d.confidence}%<br>
  <b>Health:</b> ${d.health}<br>
  <b>Solution:</b> ${d.solution}
  `
 })
}