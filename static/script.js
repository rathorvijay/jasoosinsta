const text = document.querySelector("[text]");
const circle1=document.querySelector("[circle1]");
const circle2=document.querySelector("[circle2]");
const submitdetails = document.querySelector("[submitdetails]");
const username1 = document.querySelector("[username]");
const fullname1 = document.querySelector("[fullname]");
const description1 = document.querySelector("[discription]");
const allCheckBox = document.querySelectorAll("input[type=checkbox]");
const externalUrl1 = document.querySelector("[externalUrl]");
const profilepic1 = document.querySelector("[profilepic]");
const private1 = document.querySelector("[private]");
const posts1 = document.querySelector("[posts]");
const followers1 = document.querySelector("[followers]");
const follow1 = document.querySelector("[follow]");
// card img
const cardimg = document.querySelector("[cardimg]");
const cardheading = document.querySelector("[cardheading]");
const cardpara = document.querySelector("[cardpara]");
// submit button
const formcard = document.querySelector("[formcard]");
const checkcard = document.querySelector("[checkcard]");
const submitbtn = document.querySelector("[submitbtn]");
const okbtn = document.querySelector("[okbtn]");
// loading
const loading = document.querySelector("[loading]");

const container = document.querySelector("[container]");
container.classList.add("active");
formcard.classList.remove("active");
circle1.classList.remove("active");
circle2.classList.remove("active");
const myInterval = setInterval(myTimer, 2200);

function myTimer() {
    container.classList.remove("active");
    formcard.classList.add("active");
    circle1.classList.add("active");
    circle2.classList.add("active");
    myStopFunction();
}

function myStopFunction() {
    clearInterval(myInterval);
}

okbtn.addEventListener("click", () => {
    formcard.classList.add("active");
    checkcard.classList.remove("active");
    circle1.classList.add("active");
    circle2.classList.add("active");
})


submitdetails.addEventListener("submit", (e) => {
    e.preventDefault();
    let username = "";
    let fullname = "";
    let nums_length_username = 0;
    let description = 0;
    let full_name_words = 0;
    let nums_length_fullname = 0;
    let posts = 0;
    let followers = 0;
    let follow = 0;
    let externalUrl = 0;
    let profilepic = 0;
    let private = 0;
    let user_name_equle = 0;

    username = username1.value;
    // let username="vijay123";
    let digitcount = 0;
    for (let i = 0; i < username.length; i++) {
        if (username[i] >= 0 && username[i] <= 9 && username[i] != " ") {
            digitcount++;
        }
    }

    nums_length_username = username.length==0?0:(digitcount / username.length)==0?0:username.length.toFixed(1);
    console.log("nums/length_username ", nums_length_username);

    // let fullname="vijay rathor";
    fullname = fullname1.value;
    let array = fullname.split(" ");
    full_name_words = Number(array.length==1?0:array.length);  
    digitcount = 0;
    for (let i = 0; i < fullname.length; i++) {
        if (fullname[i] >= 0 && fullname[i] <= 9 && fullname[i] != " ") {
            digitcount++;
        }
    }
    nums_length_fullname = fullname.length==0?0:(digitcount / fullname.length)==0?0:fullname.length.toFixed(1); 
    user_name_equle = parseFloat((fullname === username ? 1 : 0));
    description = description1.value;
    description = Number(description.length);
    posts = Number(posts1.value);
    
    follow = Number(follow1.value);
   
    followers = Number(followers1.value);

    if (externalUrl1.checked) externalUrl = Number(1);
    if (profilepic1.checked) profilepic = Number(1);
    if (private1.checked) private = Number(1);

    // show card
    formcard.classList.remove("active");
    loading.classList.add("active");
    circle1.classList.remove("active");
    circle2.classList.remove("active");



async function ApiCall(){
  try {
    loading.classList.add("active");
    const response = await $.ajax({
      type: "POST",
      url: "/predict",
      data: JSON.stringify({
        "username":username,
        "fullname":fullname,
        "nums/length_username": nums_length_username,
        "fullname_words": full_name_words,
        "nums/full_name_length": nums_length_fullname,
        "fullname==username": user_name_equle,
        "description": description,
        "posts": posts,
        "follow": follow,
        "followers": followers,
        "externalUrl": externalUrl,
        "profilepic": profilepic,
        "private": private
      }),
      contentType: "application/json; charset=utf-8",
      dataType: "json"
    });
    
    loading.classList.remove("active");
    checkcard.classList.add("active");
    const result = response.prediction;
    if (result == 1) {
      cardimg.src = "./static/assets/giphy.gif"; 
      cardheading.innerText = "Real Account";
      cardpara.innerText = `@${username} is a Real Account`;
    } else {
      cardimg.src = "./static/assets/sad.gif";
      cardheading.innerText = "Fake Account";
      cardpara.innerText = `@${username} is a Fake Account \n\n You can report this account`;
    }
  } catch (error) {
    console.log(error);
  }
}



    
    ApiCall();

})
