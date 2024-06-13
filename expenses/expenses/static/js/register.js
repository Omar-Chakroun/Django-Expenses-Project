const usernameField=document.querySelector("#usernameField");
const feedbackField=document.querySelector(".invalid-feedback");
const emailField=document.querySelector("#emailField");
const emailFeedbackField=document.querySelector(".emailFeedBackArea");
const showPasswordToggle=document.querySelector("#password");
const passwordField=document.querySelector("#passwordField");
const submit_button=document.querySelector("#submit-btn");
showPasswordToggle.style.cursor="pointer";

const handleToggleInput = () => {
    
    if (showPasswordToggle.textContent === "SHOW") {
      showPasswordToggle.textContent = "HIDE";
      passwordField.type = "text";
    } else {
      showPasswordToggle.textContent = "SHOW";
      passwordField.type = "password";
    }
  };

  showPasswordToggle.addEventListener("click", (e)=>{
    e.preventDefault()
    handleToggleInput(e)
  });





emailField.addEventListener("keyup",(e)=>{

    emailField.classList.remove("is-invalid");
    emailFeedbackField.style.display="none";
    const  emailVal=e.target.value;

    if (emailVal.length > 0){
        fetch("/authentication/validate-email",{
            body:JSON.stringify({ email : emailVal }),
            method:"POST"
        
        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log("data",data);

            if(data.email_error){
                submit_button.setAttribute("disabled","disabled");
                emailField.classList.add("is-invalid");
                emailFeedbackField.style.display="block";
                emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;            
            
            }else{
                submit_button.removeAttribute("disabled");
            }

        });

    }

})







usernameField.addEventListener("keyup",(e)=>{
    
    usernameField.classList.remove("is-invalid");
    feedbackField.style.display="none";
    const  usernameVal=e.target.value;

    if (usernameVal.length > 0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({ username : usernameVal }),
            method:"POST"
        
        })
        .then((res)=>res.json())
        .then((data)=>{
            console.log("data",data);

            if(data.length ===0){
                
            }

            if(data.username_error){
                usernameField.classList.add("is-invalid");
                feedbackField.style.display="block";
                feedbackField.innerHTML = `<p>${data.username_error}</p>`;            }
        });

    }

});