document.addEventListener(
"DOMContentLoaded",
() => {


    const passwordInputs =
    document.querySelectorAll(
        'input[type="password"]'
    );

    passwordInputs.forEach(input => {

        const toggle =
        document.createElement("span");

        toggle.innerHTML = "👁";

        toggle.style.cursor = "pointer";
        toggle.style.marginLeft = "10px";

        input.parentNode.insertBefore(
            toggle,
            input.nextSibling
        );

        toggle.addEventListener(
            "click",
            () => {

                if(
                    input.type === "password"
                ){
                    input.type = "text";
                }
                else{
                    input.type = "password";
                }

            }
        );

    });

    const forms =
    document.querySelectorAll("form");

    forms.forEach(form => {

        form.addEventListener(
            "submit",
            (e) => {

                const email =
                form.querySelector(
                    'input[type="email"]'
                );

                if(email){

                    const pattern =
                    /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

                    if(
                        !pattern.test(
                            email.value
                        )
                    ){

                        e.preventDefault();

                        alert(
                            "Enter Valid Email Address"
                        );

                    }

                }

            }
        );

    });

}

);
setTimeout(()=>{

document
.querySelectorAll(".toast")
.forEach(t=>{

t.style.opacity="0";

setTimeout(()=>{

t.remove();

},500);

});

},3000);